import cv2 as cv
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cnn_model
import dataset
IMG_SIZE = (102, 102)


# hacky script to see result


img = cv.imread("data/training/images-and-masks/image02.png")
s_img = cv.resize(img, IMG_SIZE, interpolation=cv.INTER_NEAREST)
n_img = np.zeros(IMG_SIZE + (3,))
n_img = cv.normalize(s_img, n_img)

model = tf.keras.models.load_model('test_model.model', custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})

n_img = np.reshape(n_img, (-1, 102, 102, 3)) 
mask = model.predict(n_img)
mask = mask[0]

mask_img = np.zeros((54, 54))

for y in range(mask.shape[0]):
    for x in range(mask.shape[1]):
        if mask[y][x][1] > mask[y][x][0]:
            mask_img[y][x] = 255
        else:
            mask_img[y,x] = 0
        

mask_large = cv.resize(mask_img,(img.shape[1], img.shape[0]), interpolation=cv.INTER_NEAREST)
cv.imshow("img", dataset.decode_label("data/training/images-and-masks/image02_mask.txt"))
cv.imshow("label", mask_large)

cv.waitKey()