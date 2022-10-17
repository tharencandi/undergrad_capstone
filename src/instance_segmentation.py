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


