# TensorFlow and tf.keras
import tensorflow as tf

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import cnn_model
fashion_mnist = tf.keras.datasets.fashion_mnist


#test UNET as classifer


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
SIZE = (train_images.shape[1], train_images.shape[2])

train_imgs = np.zeros(train_images.shape + (3,))
train_lbls = np.array(train_labels)
test_imgs = np.zeros(test_images.shape + (3,))
test_lbls = np.array(test_labels)
for i in range(len(train_images)):
    img = train_images[i]
    img = cv.cvtColor(img,cv.COLOR_GRAY2RGB)
    n_img = np.zeros(SIZE + (3,))
    cv.normalize(img, n_img, 0, 1)
    train_imgs[i] = n_img
  
for i in range(len(test_images)):
    img = test_images[i]
    img = cv.cvtColor(img,cv.COLOR_GRAY2RGB)
    n_img = np.zeros(SIZE + (3, ))
    cv.normalize(img, n_img, 0, 1)
    test_imgs[i] = n_img

NUM_CLASSES = len(class_names)

unet = cnn_model.unet(SIZE, NUM_CLASSES, classify=True)

unet.compile(   
        optimizer=tf.keras.optimizers.Adam(),
        loss="sparse_categorical_crossentropy",
        metrics=[cnn_model.UpdatedMeanIoU(num_classes=NUM_CLASSES),])

unet.fit(train_imgs, train_lbls, batch_size = 64, epochs= 10)


test_loss, test_acc = unet.evaluate(test_imgs,  test_lbls, verbose=2)
unet.save("fasion.model")
print(f"test_loss: {test_loss}, test_acc: {test_acc}")
