# -*- coding: utf-8 -*-
"""ACL_MODEL Data processing

Handle MRI images 
"""



from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, Conv2DTranspose, BatchNormalization, Dropout, Lambda
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as K
from keras.layers import Activation

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np
import cv2
import pickle
import tifffile as tiff
import matplotlib.pyplot as plt
import json
import os

from pathlib import Path
from glob import glob
from PIL import Image, ImageDraw
from tqdm import tqdm

#data load
from google.colab import files
files.upload()  # Upload kaggle.json

# !mkdir -p ~/.kaggle

# !mv kaggle.json ~/.kaggle/
# !chmod 600 ~/.kaggle/kaggle.json

# !kaggle datasets download -d sohaibanwaar1203/kneemridataset -p ./data --unzip

for root, dirs, files in os.walk('./data'):
    for file in files:
        print(os.path.join(root, file))

pck_files = []

# Collect all .pck files
for root, dirs, files in os.walk('./data'):
    for file in files:
        if file.endswith('.pck'):
            pck_files.append(os.path.join(root, file))

print(f"Found {len(pck_files)} .pck files.")

# Load and inspect the first few files
for i, path in enumerate(pck_files[:5]):
    with open(path, 'rb') as f:
        data = pickle.load(f)

    print(f"\nFile: {path}")
    print(f"Type: {type(data)}")

    if isinstance(data, dict):
        print(f"Keys: {data.keys()}")
    elif hasattr(data, 'shape'):
        print(f"Shape: {data.shape}")
    else:
        print(f"Sample content: {str(data)[:500]}")  # Preview if it's something else

meta = pd.read_csv('./data/metadata.csv')  # or wherever it's stored
print(meta.head())

labels = dict(zip(meta['volumeFilename'], meta['aclDiagnosis']))

ROOT_DIR    = Path("./data")
OUTPUT_DIR  = Path("jpeg_out")
OUTPUT_DIR.mkdir(exist_ok=True)

keep = set()

def to_uint8(arr):
    """Make sure each slice is uint8 in [0,255] for Pillow."""
    if arr.dtype != np.uint8:
        arr = arr.astype(np.float32)
        arr -= arr.min()
        maxv = arr.max()
        if maxv:                   # avoid divide-by-zero
            arr /= maxv
        arr = (arr * 255).clip(0, 255).astype(np.uint8)
    return arr

def save_slice(arr2d: np.ndarray, out_path: Path):
    img = Image.fromarray(to_uint8(arr2d), mode="L")   # grayscale
    img.save(out_path, format="JPEG", quality=95)

for root, _, files in os.walk(ROOT_DIR):
    for fname in files:
        if not fname.endswith(".pck"):
            continue
        stem = Path(fname).stem         # filename without .pck
        if keep and stem not in keep:
            continue                    # skip if not in label list

        pkl_path = Path(root) / fname
        with open(pkl_path, "rb") as f:
            volume = pickle.load(f)     # (S, H, W) or (H, W)

        # 2-D pickle → single JPEG
        if volume.ndim == 2:
            out_name = f"{stem}.jpg"
            save_slice(volume, OUTPUT_DIR / out_name)

        # 3-D pickle → one JPEG per slice
        elif volume.ndim == 3:
            for idx in range(volume.shape[0]):
                out_name = f"{stem}_slice{idx:03d}.jpg"
                save_slice(volume[idx], OUTPUT_DIR / out_name)

        else:
            print(f"⚠️  {pkl_path} skipped — unsupported shape {volume.shape}")

print(f"Done — JPEGs stored in {OUTPUT_DIR.resolve()}")

CSV_PATH     = './data/metadata.csv'
JPEG_DIR     = Path("jpeg_out")        # where your *_slice###.jpg live
MASK_DIR     = Path("mask_out")        # will hold *_slice###_mask.png
MASK_DIR.mkdir(exist_ok=True)
VIA_JSON     = "via_annotations.json"  # final VIA file

df = pd.read_csv(CSV_PATH)

via_dict = {}          # master JSON object

for row in df.itertuples(index=False):
    stem   = Path(row.volumeFilename).stem   # "329637-8"
    z0     = row.roiZ
    z1     = z0 + row.roiDepth               # non-inclusive
    label  = int(row.aclDiagnosis)           # 0 or 1

    for idx in range(z0, z1):
        # ------------------------------------------------------------------
        # 1) Build filenames
        jpeg_name = f"{stem}_slice{idx:03d}.jpg"
        jpeg_path = JPEG_DIR / jpeg_name
        mask_name = f"{stem}_slice{idx:03d}_mask.png"
        mask_path = MASK_DIR / mask_name

        # ------------------------------------------------------------------
        # 2) Skip if the slice JPEG doesn't exist (safety)
        if not jpeg_path.exists():
            print(f"⚠️  missing {jpeg_path} – skipped")
            continue

        # ------------------------------------------------------------------
        # 3) Create/append VIA record
        key = f"{jpeg_name}{os.path.getsize(jpeg_path)}"   # VIA uses filename+size as key
        via_dict[key] = {
            "filename": jpeg_name,
            "size": os.path.getsize(jpeg_path),
            "regions": [{
                "shape_attributes": {
                    "name": "rect",
                    "x": int(row.roiX),
                    "y": int(row.roiY),
                    "width":  int(row.roiWidth),
                    "height": int(row.roiHeight)
                },
                "region_attributes": {
                    "class": str(label)
                }
            }],
            "file_attributes": {}
        }

        # ------------------------------------------------------------------
        #draw binary mask
        img_h, img_w = 320, 320                       # known size
        mask = Image.new("L", (img_w, img_h), 0)      # 0 = background
        draw = ImageDraw.Draw(mask)
        draw.rectangle(
            [row.roiX, row.roiY,
             row.roiX + row.roiWidth - 1,
             row.roiY + row.roiHeight - 1],
            fill=255                                  # 255 = ROI
        )
        mask.save(mask_path)

# ----------------------------------------------------------------------
# 5) Write VIA JSON
with open(VIA_JSON, "w") as f:
    json.dump(via_dict, f, indent=2)

print(f"✅  VIA JSON saved to {VIA_JSON}")
print(f"✅  Masks in {MASK_DIR.resolve()}")

# prompt: get dimensions of the jpeg images and number of channels for example 320x320x3

from PIL import Image
import os

def get_image_dimensions(image_path):
  try:
    img = Image.open(image_path)
    width, height = img.size
    mode = img.mode
    channels = len(mode) if mode in ('RGB', 'RGBA', 'CMYK') else 1
    return f"{width}x{height}x{channels}"
  except (FileNotFoundError, OSError, IOError):
    return "Error: Could not open or read image file."


jpeg_dir = "jpeg_out"  # Replace with the actual directory

for filename in os.listdir(jpeg_dir):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image_path = os.path.join(jpeg_dir, filename)
        dimensions = get_image_dimensions(image_path)
        print(f"{filename}: {dimensions}")
        break

#Load images from folders into np arrays
image_files = sorted(JPEG_DIR.glob("*.jpg"))

# ------------------------------------------------------------------
# 2)  Read images + masks into Python lists
X_list, y_list = [], []
TARGET_SIZE = (320, 320)  # (width, height)



for img_path in image_files:
    mask_path = MASK_DIR / f"{img_path.stem}_mask.png"
    if not mask_path.exists():
        continue

    # Load and resize image and mask
    img = Image.open(img_path).convert("L").resize(TARGET_SIZE, resample=Image.BILINEAR)
    mask = Image.open(mask_path).convert("L").resize(TARGET_SIZE, resample=Image.NEAREST)

    img = np.array(img, dtype=np.uint8)
    mask = np.array(mask, dtype=np.uint8)

    mask = (mask > 0).astype(np.uint8)  # binarize

    X_list.append(img)
    y_list.append(mask)


# ------------------------------------------------------------------
# 3)  Stack into NumPy arrays: shape (N, H, W, 1)
X = np.expand_dims(np.stack(X_list, axis=0), axis=-1)  # add channel dim
y = np.expand_dims(np.stack(y_list, axis=0), axis=-1)  # add channel dim


X = X.astype("float32") / 255.0

print("Images:", X.shape, X.dtype)   # e.g. (4200, 320, 320, 1) float32
print("Masks :", y.shape, y.dtype)   # same N,H,W,1

# ------------------------------------------------------------------
# 4)  Train / test split – MAKE SURE YOU PASS BOTH ARRAYS TOGETHER
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,   # 25 % test set
    random_state=42,  # reproducible split
    shuffle=True
)

print("Train :", X_train.shape, y_train.shape)
print("Test  :", X_test.shape, y_test.shape)

import matplotlib.pyplot as plt

# Show 3 random training samples
import random
n_samples = 3
indices = random.sample(range(len(X_train)), n_samples)

for idx in indices:
    image = X_train[idx, :, :, 0]  # shape: (320, 320)
    mask  = y_train[idx, :, :, 0]  # shape: (320, 320)

    plt.figure(figsize=(8, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Input Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(mask, cmap='gray')
    plt.title("Segmentation Mask")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

#dimensions

IMG_HEIGHT = X_train.shape[1]
IMG_WIDTH  = X_train.shape[2]
IMG_CHANNELS = X_train.shape[3]

input_shape = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)
print(input_shape)

"""U NET MODEL"""

#convolution bloack: S1
def conv_block(input, num_filters):
  x = Conv2D(num_filters, 3, padding="same")(input)
  x = BatchNormalization()(x)
  x = Activation("relu")(x)

  x = Conv2D(num_filters, 3, padding="same")(x)
  x = BatchNormalization()(x)
  x = Activation("relu")(x)

  return x

#encoder block: conv block (s1) followed by maxpooling
def encoder_block(input, num_filters):
  x = conv_block(input, num_filters)
  p = MaxPooling2D((2, 2))(x)
  return x, p

#Decoder block
#skip features gets input from encoder for concatenation

def decoder_block(input, skip_features, num_filters):
  x = Conv2DTranspose(num_filters, (2, 2), strides=2, padding="same")(input)
  x = concatenate([x, skip_features])
  x = conv_block(x, num_filters)
  return x

#build unet
def build_unet(input_shape):
  inputs = Input(input_shape)

  s1, p1 = encoder_block(inputs, 64)
  s2, p2 = encoder_block(p1, 128)
  s3, p3 = encoder_block(p2, 256)
  s4, p4 = encoder_block(p3, 512)

  b1 = conv_block(p4, 1024)

  d1 = decoder_block(b1, s4, 512)
  d2 = decoder_block(d1, s3, 256)
  d3 = decoder_block(d2, s2, 128)
  d4 = decoder_block(d3, s1, 64)

  outputs = Conv2D(1, 1, padding="same", activation="sigmoid")(d4)
  model = Model(inputs, outputs, name="U-Net")
  return model

#build the model
model = build_unet(input_shape)
model.compile(optimizer=Adam(learning_rate=1e-3), loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

# from keras.preprocessing.image import ImageDataGenerator

# seed = 24           # keeps image + mask transforms in sync


# img_data_gen_args = dict(
#     rotation_range=90,        # random 0‑90° rotation
#     width_shift_range=0.3,    # ±30 % horizontal translation
#     height_shift_range=0.3,   # ±30 % vertical translation
#     shear_range=0.5,          # shear up to 0.5 rad
#     zoom_range=0.3,           # random zoom‑in/out
#     horizontal_flip=True,
#     vertical_flip=True,
#     fill_mode='reflect'       # fill empty pixels by mirroring
# )


# mask_data_gen_args = dict(
#     rotation_range=90,
#     width_shift_range=0.3,
#     height_shift_range=0.3,
#     shear_range=0.5,
#     zoom_range=0.3,
#     horizontal_flip=True,
#     vertical_flip=True,
#     fill_mode='reflect',
#     preprocessing_function=lambda x: np.where(x > 0, 1, 0).astype(np.uint8)

# )
# batch_size = 8


# image_data_generator = ImageDataGenerator(**img_data_gen_args)
# mask_data_generator  = ImageDataGenerator(**mask_data_gen_args)


# image_generator      = image_data_generator.flow(X_train, seed=seed, batch_size=batch_size)
# valid_img_generator  = image_data_generator.flow(X_test,  seed=seed, batch_size=batch_size)


# mask_generator       = mask_data_generator.flow(y_train, seed=seed, batch_size=batch_size)
# valid_mask_generator = mask_data_generator.flow(y_test,  seed=seed, batch_size=batch_size)

# def my_image_mask_generator(image_generator, mask_generator):
#     for img_batch, mask_batch in zip(image_generator, mask_generator):
#         yield img_batch, mask_batch
# my_generator       = my_image_mask_generator(image_generator, mask_generator)
# validation_datagen = my_image_mask_generator(valid_img_generator, valid_mask_generator)
# x = image_generator.next()      # shape (8, 320, 320, 1)
# y = mask_generator.next()       # shape (8, 320, 320, 1)

# for i in range(1):              # just the first image in the batch
#     plt.subplot(1,2,1); plt.imshow(x[i][:,:,0], cmap='gray')
#     plt.subplot(1,2,2); plt.imshow(y[i][:,:,0])   # mask – usually 0/1
#     plt.show()
# steps_per_epoch = 3 * (len(X_train)) // batch_size

BATCH_SIZE = 8
EPOCHS     = 50

history = model.fit(
    X_train, y_train,
    batch_size      = BATCH_SIZE,
    epochs          = EPOCHS,
    shuffle         = True,
    validation_data = (X_test, y_test)
)

