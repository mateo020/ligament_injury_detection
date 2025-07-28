
import torch 
import torch.nn as nn 
from monai.networks.blocks import UnetOutBlock
from functools import partial

from models.base import (
    BasicBlock, UpBlock, DownBlock, UnetBasicBlock, 
    UnetResBlock, save_add, BasicDown, BasicUp, SequentialEmb
)
from models.attention import Attention, zero_module
from models.autoencoders import TimeEmbbeding
from einops import rearrange
from rotary_embedding_torch import RotaryEmbedding

def exists(x):
    return x is not None

def default(val, d):
    if exists(val):
        return val
    return d() if callable(d) else d

def is_odd(n):
    return (n % 2) == 1
class SinusoidalPosEmb(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
class SpatialLinearAttention(nn.Module):
    def __init__(self, dim, heads=4, dim_head=32):
        super().__init__()
        self.scale = dim_head ** -0.5
        self.heads = heads
        hidden_dim = dim_head * heads
        self.to_qkv = nn.Conv2d(dim, hidden_dim * 3, 1, bias=False)
        self.to_out = nn.Conv2d(hidden_dim, dim, 1)

class Residual(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def forward(self, x, *args, **kwargs):
        return self.fn(x, *args, **kwargs) + x
class UNet(nn.Module):
    def __init__(self, 
        in_ch = 1, 
        out_ch = 1, 
        spatial_dims = 3,
        hid_chs = [256, 256, 512, 1024],
        kernel_sizes = [3, 3, 3, 3],
        strides =  [1, 2, 2, 2],
        act_name = ("SWISH", {}),
        norm_name = ("GROUP", {'num_groups':32, "affine": True}),
        time_embedder = TimeEmbbeding,
        time_embedder_kwargs = {},
        cond_embedder = None,
        cond_embedder_kwargs = {},
        deep_supervision = False,
        use_res_block = True,
        estimate_variance = False ,
        use_self_conditioning = False, 
        dropout = 0.0, 
        learnable_interpolation = True,
        use_attention = 'none',
        num_res_blocks = 2
    ):
        super().__init__()
        use_attention = use_attention if isinstance(use_attention, list) else [use_attention]*len(strides) 
        self.use_self_conditioning = use_self_conditioning
        self.use_res_block = use_res_block
        self.depth = len(strides)
        self.num_res_blocks = num_res_blocks

        # ------------- Time-Embedder-----------
        if time_embedder is not None:
            self.time_embedder = time_embedder(**time_embedder_kwargs)
            time_emb_dim = self.time_embedder.emb_dim
        else:
            self.time_embedder = None 
            time_emb_dim = None 

        # ------------- Condition-Embedder-----------
        if cond_embedder is not None:
            self.cond_embedder = cond_embedder(**cond_embedder_kwargs)
        else:
            self.cond_embedder = None 


        ConvBlock = UnetResBlock if use_res_block else UnetBasicBlock

        # ----------- In-Convolution ------------
        in_ch = in_ch * 2 if self.use_self_conditioning else in_ch 
        self.in_conv = BasicBlock(spatial_dims, in_ch, hid_chs[0], kernel_size=kernel_sizes[0], stride=strides[0])
        
        
        # ----------- Encoder ------------
        #Each element in self.in_blocks is either  a convBLock + attention  or a basic Down layer that halfs the spatial size
        in_blocks = [] 
        for i in range(1, self.depth):
            for k in range(num_res_blocks):
                seq_list = [] 
                seq_list.append(
                    ConvBlock(
                        spatial_dims=spatial_dims,
                        in_channels=hid_chs[i-1 if k==0 else i],
                        out_channels=hid_chs[i],
                        kernel_size=kernel_sizes[i],
                        stride=1,
                        norm_name=norm_name,
                        act_name=act_name,
                        dropout=dropout,
                        emb_channels=time_emb_dim
                    )
                )

                seq_list.append(
                    Attention(
                        spatial_dims=spatial_dims,
                        in_channels=hid_chs[i],
                        out_channels=hid_chs[i],
                        num_heads=8,
                        ch_per_head=hid_chs[i]//8,
                        depth=1,
                        norm_name=norm_name,
                        dropout=dropout,
                        emb_dim=time_emb_dim,
                        attention_type=use_attention[i]
                    )
                )
                in_blocks.append(SequentialEmb(*seq_list))

            if i < self.depth-1:
                in_blocks.append(
                    BasicDown(
                        spatial_dims=spatial_dims,
                        in_channels=hid_chs[i],
                        out_channels=hid_chs[i],
                        kernel_size=kernel_sizes[i],
                        stride=strides[i],
                        learnable_interpolation=learnable_interpolation 
                    )
                )
 

        self.in_blocks = nn.ModuleList(in_blocks)
        
        # ----------- Middle ------------
        #compressed representation with another round of convolutionstion -> attention -> conv
        self.middle_block = SequentialEmb(
            #first conv refines the bottom level features 
            ConvBlock(
                spatial_dims=spatial_dims,
                in_channels=hid_chs[-1],
                out_channels=hid_chs[-1],
                kernel_size=kernel_sizes[-1],
                stride=1,
                norm_name=norm_name,
                act_name=act_name,
                dropout=dropout,
                emb_channels=time_emb_dim
            ),
            #allows the network mix information across entire feature map at that scale
            Attention(
                spatial_dims=spatial_dims,
                in_channels=hid_chs[-1],
                out_channels=hid_chs[-1],
                num_heads=8,
                ch_per_head=hid_chs[-1]//8,
                depth=1,
                norm_name=norm_name,
                dropout=dropout,
                emb_dim=time_emb_dim,
                attention_type=use_attention[-1]
            ),
            #more processing before upsampling
            ConvBlock(
                spatial_dims=spatial_dims,
                in_channels=hid_chs[-1],
                out_channels=hid_chs[-1],
                kernel_size=kernel_sizes[-1],
                stride=1,
                norm_name=norm_name,
                act_name=act_name,
                dropout=dropout,
                emb_channels=time_emb_dim
            )
        )

 
     
        # ------------ Decoder ----------
        #gradually upsample back to original resolution merging coarse and fine features via skip connections
        out_blocks = [] 
        for i in range(1, self.depth):
            for k in range(num_res_blocks+1):
                seq_list = [] 
                out_channels=hid_chs[i-1 if k==0 else i]
                seq_list.append(
                    ConvBlock(
                        spatial_dims=spatial_dims,
                        in_channels=hid_chs[i]+hid_chs[i-1 if k==0 else i],
                        out_channels=out_channels,
                        kernel_size=kernel_sizes[i],
                        stride=1,
                        norm_name=norm_name,
                        act_name=act_name,
                        dropout=dropout,
                        emb_channels=time_emb_dim
                    )
                )
            
                seq_list.append(
                    Attention(
                        spatial_dims=spatial_dims,
                        in_channels=out_channels,
                        out_channels=out_channels,
                        num_heads=8,
                        ch_per_head=out_channels//8,
                        depth=1,
                        norm_name=norm_name,
                        dropout=dropout,
                        emb_dim=time_emb_dim,
                        attention_type=use_attention[i]
                    )
                )

                if (i > 1) and k==0:
                    seq_list.append(
                        BasicUp(
                            spatial_dims=spatial_dims,
                            in_channels=out_channels,
                            out_channels=out_channels,
                            kernel_size=strides[i],
                            stride=strides[i],
                            learnable_interpolation=learnable_interpolation 
                        )
                    )
        
                out_blocks.append(SequentialEmb(*seq_list))
        self.out_blocks = nn.ModuleList(out_blocks)
        
        
        # --------------- Out-Convolution ----------------
        out_ch_hor = out_ch * 2 if estimate_variance else out_ch
        self.outc = zero_module(UnetOutBlock(spatial_dims, hid_chs[0], out_ch_hor, dropout=None))
        if isinstance(deep_supervision, bool):
            deep_supervision = self.depth-2 if deep_supervision else 0 
        self.outc_ver = nn.ModuleList([
            zero_module(UnetOutBlock(spatial_dims, hid_chs[i]+hid_chs[i-1], out_ch, dropout=None) )
            for i in range(2, deep_supervision+2)
        ])
 

    def forward(self, x_t, t=None, condition=None, self_cond=None):
        # x_t [B, C, *]
        # t [B,]
        # condition [B,]
        # self_cond [B, C, *]
        

        # -------- Time Embedding (Gloabl) -----------
        if t is None:
            time_emb = None 
        else:
            time_emb = self.time_embedder(t) # [B, C]

        # -------- Condition Embedding (Gloabl) -----------
        if (condition is None) or (self.cond_embedder is None):
            cond_emb = None  
        else:
            cond_emb = self.cond_embedder(condition) # [B, C] 
        
        emb = save_add(time_emb, cond_emb) # treating the condition as a global condition
       
        # ---------- Self-conditioning-----------
        if self.use_self_conditioning:
            self_cond =  torch.zeros_like(x_t) if self_cond is None else x_t 
            x_t = torch.cat([x_t, self_cond], dim=1)  
    
        # --------- Encoder --------------
        # Skip Connections: Every blocks output is stored in a python list x.append() and latter popped off to feed into decodeder
        x = [self.in_conv(x_t)]
        for i in range(len(self.in_blocks)):
            x.append(self.in_blocks[i](x[i], emb))

        # ---------- Middle --------------
        h = self.middle_block(x[-1], emb)
        
        # -------- Decoder -----------
        y_ver = []
        for i in range(len(self.out_blocks), 0, -1):
            h = torch.cat([h, x.pop()], dim=1)

            depth, j = i//(self.num_res_blocks+1), i%(self.num_res_blocks+1)-1
            y_ver.append(self.outc_ver[depth-1](h)) if (len(self.outc_ver)>=depth>0) and (j==0) else None 

            h = self.out_blocks[i-1](h, emb)

        # ---------Out-Convolution ------------
        y = self.outc(h)

        return y, y_ver[::-1]
def Upsample(dim):
    return nn.ConvTranspose3d(dim, dim, (1, 4, 4), (1, 2, 2), (0, 1, 1))


def Downsample(dim):
    return nn.Conv3d(dim, dim, (1, 4, 4), (1, 2, 2), (0, 1, 1))

def prob_mask_like(shape, prob, device):
    if prob == 1:
        return torch.ones(shape, device=device, dtype=torch.bool)
    elif prob == 0:
        return torch.zeros(shape, device=device, dtype=torch.bool)
    else:
        return torch.zeros(shape, device=device).float().uniform_(0, 1) < prob
class EinopsToAndFrom(nn.Module):
    def __init__(self, from_einops, to_einops, fn):
        super().__init__()
        self.from_einops = from_einops
        self.to_einops = to_einops
        self.fn = fn
    def forward(self, x, **kwargs):
        shape = x.shape
        reconstitute_kwargs = dict(
            tuple(zip(self.from_einops.split(' '), shape)))
        x = rearrange(x, f'{self.from_einops} -> {self.to_einops}')
        x = self.fn(x, **kwargs)
        x = rearrange(
            x, f'{self.to_einops} -> {self.from_einops}', **reconstitute_kwargs)
        return x
class RelativePositionBias(nn.Module):
    def __init__(
        self,
        heads=8,
        num_buckets=32,
        max_distance=128
    ):
        super().__init__()
        self.num_buckets = num_buckets
        self.max_distance = max_distance
        self.relative_attention_bias = nn.Embedding(num_buckets, heads)

class LayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(1, dim, 1, 1, 1))

    def forward(self, x):
        var = torch.var(x, dim=1, unbiased=False, keepdim=True)
        mean = torch.mean(x, dim=1, keepdim=True)
        return (x - mean) / (var + self.eps).sqrt() * self.gamma


class Block(nn.module):
    def __init__(self, dim, dim_out, groups=8):
        super().__init__()
        spatial_dims = 3
        Convolution = Conv[Conv.CONV, spatial_dims]
        self.proj = Convolution(
            in_channels=dim, 
            out_channels=dim_out, 
            kernel_size=(1, 3, 3), 
            stride=1, 
            padding=(0, 1, 1)
        )
        self.norm = nn.GroupNorm(groups, dim_out)
        self.act = nn.SiLU()

    def forward(self, x):
        x = self.proj(x)
        x = self.norm(x)
        x = self.act(x)
        return x


class ResnetBlock(nn.Module):
    def __init__(self, dim, dim_out, *, time_emb_dim=None, groups=8):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_emb_dim, dim_out * 2)
        ) if exists(time_emb_dim) else None

        self.block1 = Block(dim, dim_out, groups=groups)
        self.block2 = Block(dim_out, dim_out, groups=groups)
        self.res_conv = nn.Conv3d(
            dim, dim_out, 1) if dim != dim_out else nn.Identity()

    def forward(self, x, time_emb=None):

        scale_shift = None
        if exists(self.mlp):
            assert exists(time_emb), 'time emb must be passed in'
            time_emb = self.mlp(time_emb)
            time_emb = rearrange(time_emb, 'b c -> b c 1 1 1')
            scale_shift = time_emb.chunk(2, dim=1)

        h = self.block1(x, scale_shift=scale_shift)

        h = self.block2(h)
        return h + self.res_conv(x)


class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.fn = fn
        self.norm = LayerNorm(dim)

    def forward(self, x, **kwargs):
        x = self.norm(x)
        return self.fn(x, **kwargs)

class Unet3D(nn.Module):
    def __init__(
        self,
        dim,
        cond_dim=None,
        out_dim=None,
        dim_mults=(1, 2, 4, 8),
        channels=3,
        attn_heads=8,
        attn_dim_head=32,
        use_bert_text_cond=False,
        init_dim=None,
        init_kernel_size=7,
        use_sparse_linear_attn=True,
        block_type='resnet',
        resnet_groups=8
    ):
        super().__init__()
        self.channels = channels

        # temporal attention and its relative positional encoding

        rotary_emb = RotaryEmbedding(min(32, attn_dim_head))

        def temporal_attn(dim): return EinopsToAndFrom('b c f h w', 'b (h w) f c', Attention(
            dim, heads=attn_heads, dim_head=attn_dim_head, rotary_emb=rotary_emb))

        # realistically will not be able to generate that many frames of video... yet
        self.time_rel_pos_bias = RelativePositionBias(
            heads=attn_heads, max_distance=32)

        # initial conv

        init_dim = default(init_dim, dim)
        assert is_odd(init_kernel_size)

        init_padding = init_kernel_size // 2
        self.init_conv = nn.Conv3d(channels, init_dim, (1, init_kernel_size,
                                   init_kernel_size), padding=(0, init_padding, init_padding))

        self.init_temporal_attn = Residual(
            PreNorm(init_dim, temporal_attn(init_dim)))

        # dimensions

        dims = [init_dim, *map(lambda m: dim * m, dim_mults)]
        in_out = list(zip(dims[:-1], dims[1:]))

        # time conditioning

        time_dim = dim * 4
        self.time_mlp = nn.Sequential(
            SinusoidalPosEmb(dim),
            nn.Linear(dim, time_dim),
            nn.GELU(),
            nn.Linear(time_dim, time_dim)
        )

        # text conditioning

        self.has_cond = exists(cond_dim)

        self.null_cond_emb = nn.Parameter(
            torch.randn(1, cond_dim)) if self.has_cond else None

        cond_dim = time_dim + int(cond_dim or 0)

        # layers

        self.downs = nn.ModuleList([])
        self.ups = nn.ModuleList([])

        num_resolutions = len(in_out)

        # block type

        block_klass = partial(ResnetBlock, groups=resnet_groups)
        block_klass_cond = partial(block_klass, time_emb_dim=cond_dim)

        # modules for all layers

        for ind, (dim_in, dim_out) in enumerate(in_out):
            is_last = ind >= (num_resolutions - 1)

            self.downs.append(nn.ModuleList([
                block_klass_cond(dim_in, dim_out),
                block_klass_cond(dim_out, dim_out),
                Residual(PreNorm(dim_out, SpatialLinearAttention(
                    dim_out, heads=attn_heads))) if use_sparse_linear_attn else nn.Identity(),
                Residual(PreNorm(dim_out, temporal_attn(dim_out))),
                Downsample(dim_out) if not is_last else nn.Identity()
            ]))

        mid_dim = dims[-1]
        self.mid_block1 = block_klass_cond(mid_dim, mid_dim)

        spatial_attn = EinopsToAndFrom(
            'b c f h w', 'b f (h w) c', Attention(mid_dim, heads=attn_heads))

        self.mid_spatial_attn = Residual(PreNorm(mid_dim, spatial_attn))
        self.mid_temporal_attn = Residual(
            PreNorm(mid_dim, temporal_attn(mid_dim)))

        self.mid_block2 = block_klass_cond(mid_dim, mid_dim)

        for ind, (dim_in, dim_out) in enumerate(reversed(in_out)):
            is_last = ind >= (num_resolutions - 1)

            self.ups.append(nn.ModuleList([
                block_klass_cond(dim_out * 2, dim_in),
                block_klass_cond(dim_in, dim_in),
                Residual(PreNorm(dim_in, SpatialLinearAttention(
                    dim_in, heads=attn_heads))) if use_sparse_linear_attn else nn.Identity(),
                Residual(PreNorm(dim_in, temporal_attn(dim_in))),
                Upsample(dim_in) if not is_last else nn.Identity()
            ]))

        out_dim = default(out_dim, channels)
        self.final_conv = nn.Sequential(
            block_klass(dim * 2, dim),
            nn.Conv3d(dim, out_dim, 1)
        )

    def forward_with_cond_scale(
        self,
        *args,
        cond_scale=2.,
        **kwargs
    ):
        logits = self.forward(*args, null_cond_prob=0., **kwargs)
        if cond_scale == 1 or not self.has_cond:
            return logits

        null_logits = self.forward(*args, null_cond_prob=1., **kwargs)
        return null_logits + (logits - null_logits) * cond_scale

    def forward(
        self,
        x,
        time,
        cond=None,
        null_cond_prob=0.,
        focus_present_mask=None,
        # probability at which a given batch sample will focus on the present (0. is all off, 1. is completely arrested attention across time)
        prob_focus_present=0.
    ):
        assert not (self.has_cond and not exists(cond)
                    ), 'cond must be passed in if cond_dim specified'
        batch, device = x.shape[0], x.device

        focus_present_mask = default(focus_present_mask, lambda: prob_mask_like(
            (batch,), prob_focus_present, device=device))

        time_rel_pos_bias = self.time_rel_pos_bias(x.shape[2], device=x.device)

        x = self.init_conv(x)
        r = x.clone()

        x = self.init_temporal_attn(x, pos_bias=time_rel_pos_bias)

        t = self.time_mlp(time) if exists(self.time_mlp) else None

        # classifier free guidance

        if self.has_cond:
            batch, device = x.shape[0], x.device
            mask = prob_mask_like((batch,), null_cond_prob, device=device)
            cond = torch.where(rearrange(mask, 'b -> b 1'),
                               self.null_cond_emb, cond)
            t = torch.cat((t, cond), dim=-1)

        h = []

        for block1, block2, spatial_attn, temporal_attn, downsample in self.downs:
            x = block1(x, t)
            x = block2(x, t)
            x = spatial_attn(x)
            x = temporal_attn(x, pos_bias=time_rel_pos_bias,
                              focus_present_mask=focus_present_mask)
            h.append(x)
            x = downsample(x)

        x = self.mid_block1(x, t)
        x = self.mid_spatial_attn(x)
        x = self.mid_temporal_attn(
            x, pos_bias=time_rel_pos_bias, focus_present_mask=focus_present_mask)
        x = self.mid_block2(x, t)

        for block1, block2, spatial_attn, temporal_attn, upsample in self.ups:
            x = torch.cat((x, h.pop()), dim=1)
            x = block1(x, t)
            x = block2(x, t)
            x = spatial_attn(x)
            x = temporal_attn(x, pos_bias=time_rel_pos_bias,
                              focus_present_mask=focus_present_mask)
            x = upsample(x)

        x = torch.cat((x, r), dim=1)
        return self.final_conv(x)

# gaussian diffusion trainer class

