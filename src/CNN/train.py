import tensorflow as tf
from tensorflow import keras
from keras import layers
#import tensorflow_datasets as tfds
#import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import cnn_model
#import pydot
import os
from augmentation import augment

NUM = 1609
IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
EPOCHS = 64
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000
MODEL_SAVE_LOCATION = "data/models/"
MODEL_FILE_NAME = "test_model.model"
TRAIN_LOCATION = "data/NBL"
TEST_LOCATION = "data/NBL_TEST"
CELL_CLASS_WEIGHT = 1
BG_CLASS_WEIGHT = 1

if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(MODEL_SAVE_LOCATION):
	print(f"creating {MODEL_SAVE_LOCATION}")
	os.mkdir(MODEL_SAVE_LOCATION)


print("loading dataset...")
imgs = []
masks = []
num_train = sum('mask' in s for s in os.listdir(TRAIN_LOCATION)) 
num_test = sum('mask' in s for s in os.listdir(TEST_LOCATION)) 
imgs, masks = augment(TRAIN_LOCATION, TRAIN_LOCATION, num_train)
v_imgs, v_masks = augment(TEST_LOCATION, TEST_LOCATION, num_test)

print("converting to tf dataset...")
imgs = np.array(imgs)
masks = np.array(masks)
v_imgs = np.array(v_imgs)
v_masks = np.array(v_masks)

print(len(imgs), imgs.shape)
print(len(masks), masks.shape)
print(len(v_imgs), v_imgs.shape)
print(len(v_masks), v_masks.shape)

imgs,masks,weights = cnn_model.add_sample_weights(imgs,masks,[BG_CLASS_WEIGHT,CELL_CLASS_WEIGHT])

train_dataset = tf.data.Dataset.from_tensor_slices((imgs, masks, weights))
train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)

test_dataset = tf.data.Dataset.from_tensor_slices((v_imgs, v_masks))
test_dataset = test_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
<<<<<<< HEAD
=======

>>>>>>> 236bd7967dca3517b4225524750f078c6c20f053
print("contructing and compiling model...")

model = cnn_model.DRAN()

model.compile(optimizer=keras.optimizers.Adam(),
                  loss="sparse_categorical_crossentropy",
                  metrics=[cnn_model.UpdatedMeanIoU(num_classes=2),])

#dot_img_file = 'model_1.png'
#tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)

print("commencing training...")
model_history = model.fit (
    train_dataset, epochs=EPOCHS, validation_data=test_dataset
)


model.save_weights(MODEL_SAVE_LOCATION + MODEL_FILE_NAME)

#model.save(MODEL_FILE_NAME)



