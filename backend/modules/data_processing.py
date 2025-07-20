import numpy as np
import torch 
from torch import nn
from torchvision import transforms as T
from pytorch_lightning import LightningDataModule
from sklearn.model_selection import train_test_split

class IdentityDataset(torch.utils.data.Dataset):
    """
        Simple dataset that returns the same data (d0, d1, ..., dn)
    """
    def __init__(self, *data):
        self.data = data

    def __len__(self):
        return self.data[-1].__len__()

    def __getitem__(self, index):
        return [d[index] for d in self.data]
    

def normalize(input_data, norm='centered-norm'):
    assert norm in ['centered-norm', 'z-score', 'min-max'], "Invalid normalization method"

    if norm == 'centered-norm':
        norm = lambda x: (2 * x - x.min() - x.max()) / (x.max() - x.min())
    elif norm == 'z-score':
        norm = lambda x: (x - x.mean()) / x.std()
    elif norm == 'min-max':
        norm = lambda x: (x - x.min()) / (x.max() - x.min())
    return norm(input_data)


class   SKMTeaDataset(torch.utils.data.Dataset):
    """
        Images always as first argument, labels and other variables as last
        Transforms are applied on first argument only
    """
    def __init__(
        self,
        *data,
        transform       = None,
        resize          = None,
        horizontal_flip = None,
        vertical_flip   = None, 
        random_crop_size = None,
        rotation        = None,
        dtype           = torch.float32
    ):
        super().__init__()
        self.data = data

        if transform is None: 
            self.transform = T.Compose([
            T.ToTensor(),  
            nn.Identity(),                             # <-- no-op passthrough
            T.Resize(resize)     if resize     else T.Lambda(lambda x: x),
            T.RandomHorizontalFlip(p=horizontal_flip) if horizontal_flip else T.Lambda(lambda x: x),
            T.RandomVerticalFlip(p=vertical_flip)     if vertical_flip   else T.Lambda(lambda x: x),
            T.RandomCrop(random_crop_size)             if random_crop_size else T.Lambda(lambda x: x),
            T.RandomRotation(rotation, fill=-1)        if rotation        else T.Lambda(lambda x: x),
            T.ConvertImageDtype(dtype),
        ])
        else:
            self.transform = transform

    def __len__(self):
        return self.data[-1].__len__()

    def __getitem__(self, index):
        return [self.transform(d[index]) if i == 0 else d[index] for i, d in enumerate(self.data)]
    
    def sample(self, n, transform=None):
        """ sampling randomly n samples from the dataset, apply or not the transform"""
        transform = self.transform if transform is not None else lambda x: x
        idx = np.random.choice(len(self), n)
        return [transform(d[idx]) if i == 0 else d[idx] for i, d in enumerate(self.data)]
    

class SKMTeaDataModule(LightningDataModule):
    def __init__(
        self,
        train_dir: str, # should target the a npy file generated via create_*.py scripts
        train_ratio: float = 0.8,
        stage: str = "first",
        norm = 'min-max',
        batch_size: int = 32,
        num_workers: int = 4,
        shuffle: bool = True,
        horizontal_flip = None,
        vertical_flip = None, 
        rotation = None,
        random_crop_size = None,
        dtype = torch.float32,
        verbose = True,
        include_radiomics = True,
        **kwargs
    ):
        super().__init__()
        self.dataset_kwargs = {
            "horizontal_flip": horizontal_flip,
            "vertical_flip": vertical_flip, 
            "random_crop_size": random_crop_size,
            "rotation": rotation,
            "dtype": dtype
        }

        self.train_dir = train_dir
        self.norm = norm
        self.stage = stage
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        self.train_ratio = train_ratio
        self.include_radiomics = include_radiomics
        self.verbose = verbose

    def prepare_data(self) -> None:
        pass
        
    def setup(self, stage=None):      
        if self.stage == "first":
            self.data = np.load(self.train_dir, allow_pickle=True).item()
            img_data = self.data['images']
            self.data = torch.from_numpy(img_data)
        elif self.stage == "second":
            self.data = np.load(self.train_dir)
        else:
            raise ValueError(f"setup() received unknown stage: {self.stage!r}. "
                            "Expected 'first' or 'second'.")
            
        


        ##############################
        if self.include_radiomics:
            self.radiomics = np.load('radiomics/radiomics.npy', allow_pickle=True).tolist()
            self.radiomics = torch.tensor(
                [
                    tuple(self.radiomics[key][i] for key in self.radiomics) 
                    for i in range(len(self.radiomics['w']))
                ],
                dtype=self.dataset_kwargs['dtype']
            )

        # if self.include_radiomics:
            train_images, train_y, val_images, val_y = train_test_split(
                self.data, self.radiomics, train_size=self.train_ratio, random_state=42, shuffle=False
            ) if self.train_ratio < 1 else (self.data, self.radiomics, [], [])

            self.train_dataset = SKMTeaDataset(train_images, train_y, **self.dataset_kwargs)
            self.val_dataset = SKMTeaDataset(val_images, val_y)
        
        else:
            train_images, val_images = train_test_split(
                self.data, train_size=self.train_ratio, random_state=42, shuffle=False
            ) if self.train_ratio < 1 else (self.data, [])

            self.train_dataset = SKMTeaDataset(train_images, **self.dataset_kwargs)
            self.val_dataset = SKMTeaDataset(val_images)

        log = """
        DataModule setup complete.
        Number of training samples: {}
        Number of validation samples: {}
        Data shape: {}
        Maximum: {}, Minimum: {}
        """.format(
            len(self.train_dataset),
            len(self.val_dataset),
            self.data.shape,
            self.data.max(),
            self.data.min()
        )

        if self.verbose: print(log)
        
    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size = self.batch_size,
            num_workers = self.num_workers,
            shuffle = self.shuffle,
            pin_memory = True
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size = self.batch_size,
            num_workers = self.num_workers,
            shuffle = False,
            pin_memory = True
        )
    
    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size = self.batch_size,
            num_workers = self.num_workers,
            shuffle = False,
            pin_memory = True
        )
    