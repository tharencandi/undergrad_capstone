from curses.panel import top_panel
import os
from pickletools import uint8
import cv2 as cv
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cnn_model as cnn_model
import openslide as osl
import openslide.deepzoom
from skimage.util.shape import view_as_windows 
import time
from iou import get_iou
import math
import json 

IMG_SIZE = (102, 102)
MODEL = 'data/models/model_76'
WEIGHTS = 'data/models/sep_15_aug_val.h5'


model = tf.keras.models.load_model(MODEL, custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
if WEIGHTS != None:
    model.load_weights(WEIGHTS)

"""
    input is prediction of CNN
    output is a 2d binary image.
"""
def get_mask_img(mask):
    mask_img = np.zeros((54, 54))
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            
            if mask[y][x][1] > mask[y][x][0]:
                mask_img[y][x] = 255
            else:
                mask_img[y,x] = 0
    return mask_img


def val_mask_to_bin(true_mask):
    for i in range(true_mask.shape[0]):
            for j in range(true_mask.shape[1]):
                if true_mask[i,j,2] != 0:
                    true_mask[i,j] = [255,255,255]
    return true_mask


"""
    Produce list of 102x102 images such that the centre 54x54
    of all images exactly cover the image image

    returns:
        - windows (list)
        - tile_dim (tuple that defines how many tiles span width and height of image)
"""
def create_windows(img):
    og_img = np.copy(img)
    og_shape = og_img.shape
    windows = []
    right_buff = (img.shape[1] % 54) + 102
    bottom_buff = (img.shape[0] % 54) + 102
    img = cv.copyMakeBorder(img, 24, bottom_buff , 24, right_buff, cv.BORDER_CONSTANT)
    img = np.array(img)

    tile_dim= (
        math.ceil(og_shape[0]/54),
        math.ceil(og_shape[1]/54)
    )

    for i in range(tile_dim[0]):
        for j in range(tile_dim[1]):
            window = np.zeros((102,102,3), dtype=np.uint8)
            x = (i * 54) + 24
            y = (j * 54) + 24
            window = img[x-24:x+78, y-24:y+78]

            #img_center = og_img[x-24:(x-24) + 54, y-24:(y-24) + 54]    
            windows.append(np.array([window]))
        
    return np.float32(windows), tile_dim


def predict_image(img):
    """
    CNN prediction takes 102x102 centre of 
    image and predicts 54x54 centre
    therefore, we crop a 102x102 window by 54 pixel a step 
    to product all inputs that need to be predicted 
    to reconstruct the image
    """

    bot_cen_pad = img.shape[0] % 54
    right_cen_pad = img.shape[1] % 54
    
    img_mask = np.zeros((img.shape[0], img.shape[1]))
    imgs, tiles = create_windows(img)

    i = 0
    for x in range(tiles[0]):
        for y in range(tiles[1]):
            
            mask = model.predict(imgs[i])
            mask = get_mask_img(mask[0])
            x_off = 54
            y_off = 54

            if x == tiles[0] - 1 and bot_cen_pad != 0:
                x_off = bot_cen_pad
            if y == tiles[1] - 1 and right_cen_pad != 0:
                y_off = right_cen_pad
            img_mask[x*54: x*54 + x_off, y*54: y*54 + y_off] = mask[0:x_off, 0:y_off]
            i += 1
    return img_mask


def predict_validation_set(n, save_location):
    iou_sum = 0
    out_str = "iou,\n"
    count = 0
    for i in range(1,n+1):
        img = cv.imread("data/validation/image{:02d}.png".format(i))
    
        mask = predict_image(img)
        mask= cv.cvtColor(np.float32(mask),cv.COLOR_GRAY2RGB)
        true_mask =  cv.imread("data/validation/image{:02d}_mask.png".format(i))
        true_mask = val_mask_to_bin(true_mask)

        vis = np.concatenate((img, true_mask, mask), axis=1)
        cv.imwrite(f'{save_location}/out_combined_{i}.png', vis)
        print(f"\nResult saved as out_combined_{i}.png in {save_location}!\n")
        
        accuracy = get_iou(mask, true_mask)
        iou_sum += accuracy*100
        out_str += str(accuracy) + ",\n"
        count += 1

    f = open(f"{save_location}/results.csv", "w")
    f.write(out_str)
    f.close()
    print("mean iou: " + str(iou_sum / count))
    


    

predict_validation_set(18, "data/results")
#predict_slide("data/example_WSI.svs", "s")
