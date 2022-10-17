"""
    Script performs instance segmentation
"""


import tensorflow as tf
import segmentation_models as sm
import glob
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

from tensorflow.keras.utils import normalize
from tensorflow.keras.metrics import MeanIoU

import tensorflow.keras as keras
print(tf.__version__)
print(keras.__version__)


#Resizing images, if needed
SIZE_X = 256
SIZE_Y = 256
n_classes=3 #Number of classes for segmentation

total_images_to_load = 500

#Capture training image info as a list
train_images = []

for directory_path in glob.glob("data/generated_patches/images/"):
    count = 0
    for img_path in glob.glob(os.path.join(directory_path, "*.tif")):
        if count < total_images_to_load:
          my_img_path=directory_path+"img"+str(count)+".tif"
          
          #print("Reading image :", my_img_path)
          img = cv2.imread(my_img_path, 1)       
          #img = cv2.resize(img, (SIZE_Y, SIZE_X))
          train_images.append(img)
        else:
          break
        count+=1
        
#Convert list to array for machine learning processing        
train_images = np.array(train_images)
print(train_images.shape)


#Capture training image info as a list
train_masks = [] 

for directory_path in glob.glob("data/generated_patches/masks_with_border/"):
    count = 0
    for mask_path in glob.glob(os.path.join(directory_path, "*.tif")):
        if count < total_images_to_load:
          my_mask_path=directory_path+"mask"+str(count)+".tif"
          #print("Reading mask :", my_mask_path)
          mask = cv2.imread(my_mask_path, 0)       
          #mask = cv2.resize(mask, (SIZE_Y, SIZE_X), interpolation = cv2.INTER_NEAREST)  #Otherwise ground truth changes due to interpolation
          train_masks.append(mask)
        else:
          break
        count+=1
#Convert list to array for machine learning processing        
train_masks = np.array(train_masks)
print(train_masks.shape)

#Encode labels... but multi dim array so need to flatten, encode and reshape
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
n, h, w = train_masks.shape
train_masks_reshaped = train_masks.reshape(-1,1)
train_masks_reshaped_encoded = labelencoder.fit_transform(train_masks_reshaped)
train_masks_encoded_original_shape = train_masks_reshaped_encoded.reshape(n, h, w)

np.unique(train_masks_encoded_original_shape)

train_masks_input = np.expand_dims(train_masks_encoded_original_shape, axis=3)

#Create a subset of data for quick testing
#Picking 20% for testing and remaining for training
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_images, train_masks_input, test_size = 0.2, random_state = 0)

print("Class values in the dataset are ... ", np.unique(y_train))  # 0 is the background/few unlabeled 

from tensorflow.keras.utils import to_categorical
train_masks_cat = to_categorical(y_train, num_classes=n_classes)
y_train_cat = train_masks_cat.reshape((y_train.shape[0], y_train.shape[1], y_train.shape[2], n_classes))

test_masks_cat = to_categorical(y_test, num_classes=n_classes)
y_test_cat = test_masks_cat.reshape((y_test.shape[0], y_test.shape[1], y_test.shape[2], n_classes))

print(y_train_cat.shape)
print(y_test_cat.shape)


