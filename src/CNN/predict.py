import cv2 as cv
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import src.CNN.cnn_model as cnn_model
from skimage.util.shape import view_as_windows 
IMG_SIZE = (102, 102)
MODEL = 'data/models/model_76'
WEIGHTS = 'data/models/new_weights.h5'

# hacky script to see result

model = tf.keras.models.load_model(MODEL, custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
if WEIGHTS != None:
    model.load_weights(WEIGHTS)

def get_mask_img(mask):
    mask_img = np.zeros(54, 54)
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            
            if mask[y][x][1] > mask[y][x][0]:
                mask_img[y][x] = 255
            else:
                mask_img[y,x] = 0
    return mask_img

def predict_image(img):
    """
    CNN prediction takes 102x102 centre of 
    image and predicts 54x54 centre
    therefore, we crop a 102x102 window by 54 pixel a step 
    to product all inputs that need to be predicted 
    to reconstruct the image
    """
    imgs = view_as_windows(img, (102, 102), step = 54)
    img_mask = np.zeros((img.shape[0], img.shape[1]))
   
    for x in range(imgs.shape[0]):
        for y in range(imgs.shape[1]):
            mask = model.predict(imgs[x,y,0])
            mask = get_mask_img(mask[0])
            img_mask[x*54: x*54 + 54, y*54, y*54 + 54] = mask

    return img_mask



for i in range(1,18):
   
    img = cv.imread("data/validation/image{:02d}.png".format(i))
    mask = predict_image(img)
    mask= cv.cvtColor(np.float32(mask),cv.COLOR_GRAY2RGB)
    true_mask =  cv.imread("data/validation/image{:02d}_mask.png".format(i))
    vis = np.concatenate((img, true_mask, mask), axis=1)
    vis = cv.resize(vis, (vis.shape[1]*4, vis.shape[0]*4))
    cv.imwrite(f'data/results/out{i}.png', vis)
 