import tensorflow as tf
from tensorflow import keras
from keras import layers
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import cnn_model
import pydot


NUM = 498
IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
EPOCHS = 1
BATCH_SIZE = 32
MODEL_SAVE_LOCATION = "data/models/"
MODEL_FILE_NAME = "test_model.model"

imgs = []
masks = []

print("loading dataset...")
for i in range(NUM):
    img = cv.imread("data/NBL/image{:04d}.png".format(i))
    mask = cv.imread("data/NBL/image{:04d}_mask.png".format(i), cv.IMREAD_GRAYSCALE)
    img = cv.resize(img, IMG_SIZE)

    #extract centre region of mask
    T = np.float32([[1, 0, -((mask.shape[0]//2)-(LBL_SIZE[0]//2))], [0, 1, -((mask.shape[0]//2)-(LBL_SIZE[1]//2))]])
    mask = cv.warpAffine(mask, T, LBL_SIZE)
   
    n_mask = np.array(mask/mask.max(),dtype=np.uint8)

    imgs.append(np.array(img))  
    masks.append(n_mask)


print("converting to tf dataset...")

imgs = np.array(imgs)
masks = np.array(masks)

#imgs,masks,weights = cnn_model.add_sample_weights(imgs,masks,[1,3])
#print(masks.shape)
SHUFFLE_BUFFER_SIZE = 100
train_dataset = tf.data.Dataset.from_tensor_slices((imgs, masks))
train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)


print("contructing and compiling model...")

model = cnn_model.DRAN()

model.compile(optimizer=keras.optimizers.Adam(),
                  loss="sparse_categorical_crossentropy",
                  metrics=[cnn_model.UpdatedMeanIoU(num_classes=2),])

#dot_img_file = 'model_1.png'
#tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)


model = tf.keras.models.load_model('model_76', custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
print("commencing training...")

model_history = model.fit (
    train_dataset, epochs=EPOCHS
)

model.save_weights(MODEL_SAVE_LOCATION + MODEL_FILE_NAME)

#model.save(MODEL_FILE_NAME)
#print(model_history)  


