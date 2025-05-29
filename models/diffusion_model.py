from typing import Tuple, Optional
import torch
import torch.nn.functional as F
import torch.utils.data
from torch import nn
from labml_nn.diffusion.ddpm.utils import gather 


class DenoiseDiffusion:
    def __inti__