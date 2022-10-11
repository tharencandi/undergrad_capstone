import tensorflow as tf
from tensorflow import keras
from keras import layers
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import cnn_model
import os
from augmentation import augment
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt

NUM = 1609
IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
EPOCHS = 64
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000
MODEL_SAVE_LOCATION = "data/models/"
MODEL_FILE_NAME = "test_model.model"
TRAIN_LOCATION = "data/nbl"
TEST_LOCATION = "data/nbl_test"
CELL_CLASS_WEIGHT = 1
BG_CLASS_WEIGHT = 1

def grid_search(epochs, batch_size, imgs, mask, v_imgs, v_masks, t_imgs, t_masks):
    best_perfomance = 0
    best_para = (None, None)
    log = []
    for b in batch_size:
        for e in epochs:
            print("log: ", log)
            print("best_perfomance so far: ", best_perfomance)
            print("best_para so far: ", best_para)
            print("batch size: {}, epochs: {}".format(b, e))
            model = cnn_model.DRAN()

            model.compile(optimizer=keras.optimizers.Adam(),
                                loss="sparse_categorical_crossentropy",
                                metrics=[cnn_model.UpdatedMeanIoU(num_classes=2),])
            model_history = model.fit (imgs, masks, batch_size=b, epochs=e, validation_data=(v_imgs, v_masks), shuffle=True)
            result = model.evaluate(t_imgs, t_masks)
            mean_iou = result[1]
            print("batch size: {}, epochs: {}, mean iou: {}".format(b, e, mean_iou))
            log.append((b,e,result))
            if mean_iou >= best_perfomance:
                best_perfomance = mean_iou
                best_para = (b, e)
    return best_para, log

def make_graph(log):
    x = [val[0] for val in log]
    y = [val[1] for val in log]
    z = [val[2][1]  for val in log]
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.invert_yaxis()
    surf = ax.plot_trisurf(x, y, z, linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)



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



