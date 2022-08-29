import tensorflow as tf
from tensorflow import keras
from keras import layers
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import cnn_model
import dataset

IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
EPOCHS = 3
BATCH_SIZE = 1
MODEL_FILE_NAME = "test_model.model"

   
imgs,labels, v_imgs, v_lbls = dataset.load_dataset()
imgs,labels,weights = cnn_model.add_sample_weights(imgs,labels,[1,3])

model = cnn_model.DRAN()

model.compile(optimizer=keras.optimizers.Adam(),
                  loss="sparse_categorical_crossentropy",
                  metsrics=[cnn_model.UpdatedMeanIoU(num_classes=2),])

#reshaping to deal with batch size dimension - alternative use tf datasets
img_shape = (-1,) + IMG_SIZE + (3,)
lbl_shape = (-1,) + LBL_SIZE + (1,)

imgs = np.reshape(imgs, img_shape)
labels = np.reshape(labels, lbl_shape)
v_imgs = np.reshape(v_imgs, img_shape)
v_labels = np.reshape(v_lbls, lbl_shape)

#train_dataset = tf.data.Dataset.from_tensor_slices((imgs, labels, weights))
#train_dataset = train_dataset.batch(batch_size=15)

model_history = model.fit (
    imgs, labels,batch_size=BATCH_SIZE, 
    sample_weight=weights, epochs=EPOCHS, 
    validation_data = (v_imgs, v_labels)
)

model.save(MODEL_FILE_NAME)
print(model_history)  


