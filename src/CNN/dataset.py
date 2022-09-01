
from re import I
import cv2 as cv
import numpy as np
import openslide as osl
import tensorflow as tf
import random
from skimage.util.shape import view_as_windows 
TRAIN_LOCATION = "data/training/images-and-masks/"
VAL_LOCATION = "data/validation/"
IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
NUM = 15


"""
    takes labels.txt and produces binary image / numpy array
    dimensions are first line of txt fime
"""
def decode_label(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    size = lines[0].split()
    size = (int(size[1]), int(size[0]))
    label_array = np.zeros(size)
    l = []
    x = 0
    y = 0
    for num in lines[1:]:
        num = int(num)
        if num != 0:
            label_array[x][y] = 255
        else:
            label_array[x][y] = 0
        if y == size[1]-1 :
            x += 1
            y = 0
        else:
            y += 1
    return label_array


"""
    load dataset as np arrays
    normalisation and resizing applied
    image flip augmentation applied to double dataset
"""
def load_dataset():
    train_images = []
    train_labels = []

    val_images = []
    val_labels = []
    for i in range(1, NUM+1):
        #train
        img = cv.imread(TRAIN_LOCATION + "image{:02d}.png".format(i))
        label = decode_label(TRAIN_LOCATION + "image{:02d}_mask.txt".format(i))
        
        """
        s_label = cv.resize(label,LBL_SIZE , interpolation=cv.INTER_NEAREST)
        s_img = cv.resize(img, IMG_SIZE, interpolation=cv.INTER_NEAREST)
        n_img = np.zeros(IMG_SIZE+(3,))
        cv.normalize(s_img, n_img,0,1)  
        """
        train_labels.append(label)
        train_images.append(np.array(img))
        
        
        #train_labels.append(cv.flip(s_label,0))
        #train_images.append(cv.flip(n_img,0))

        #validation
        """
        v_img = cv.imread(VAL_LOCATION + "image{:02d}.png".format(i))
        v_lbl = decode_label(VAL_LOCATION + "image{:02d}_mask.txt".format(i))
        sv_lbl = cv.resize(v_lbl,LBL_SIZE , interpolation=cv.INTER_NEAREST)
        sv_img = cv.resize(v_img,IMG_SIZE, interpolation=cv.INTER_NEAREST)
        nv_img = np.zeros(LBL_SIZE+(3,))
        cv.normalize(sv_img, nv_img)

        val_labels.append(sv_lbl)
        val_images.append(nv_img)
        val_labels.append(cv.flip(sv_lbl,0))
        val_images.append(cv.flip(nv_img,0))
        """

    return train_images, train_labels, val_images, val_labels

LOW =  -2147483648 
HIGH = 2147483647

"slide window with a step of 54 pixels and random cropping to produce patches"
def gen_NBL(data, location):
    imgs, lbls = data
    count = 0
    for i in range(len(imgs)):
        
        #window slide
    
        c_img = view_as_windows(imgs[i], window_shape=(200,200,3), step=54)
        c_lbl = view_as_windows(lbls[i], window_shape=(200,200), step=54)
        for x in range(c_img.shape[0]):
            for y in range(c_img.shape[1]):
                cv.imwrite(location+"image{:04d}.png".format(count), c_img[x,y,0])
                cv.imwrite(location+"image{:04d}_mask.png".format(count), c_lbl[x,y])
                count += 1
        
        #random cropping
        for j in range(30):
            seed = random.randint(LOW, HIGH)
            c_img = tf.image.stateless_random_crop(imgs[i], size=(200, 200, 3), seed=(seed,seed))  
            c_lbl = tf.image.stateless_random_crop(lbls[i], size = (200,200), seed=(seed,seed))

            cv.imwrite(location+"image{:04d}.png".format(count), np.array(c_img))
            cv.imwrite(location+"image{:04d}_mask.png".format(count), np.array(c_lbl))
            
            count += 1
          
       


"""s
    preserves image aspect ratio
"""
def create_grid(svs_file,location, zoom):
    slide = osl.OpenSlide(svs_file)
    size = (int(slide.properties["aperio.OriginalHeight"]), int(slide.properties["aperio.OriginalWidth"]))
    region_size = (size[0]//zoom, size[1]//zoom)

    for i in range(zoom):
        for j in range(zoom):

            img = slide.read_region((i*region_size[1], j*region_size[0] ), 0, region_size )
            cv_image = np.array(img) 
            cv.imwrite(f"{location}/{i}_ {j}.jpg", cv_image)

    slide.close()


imgs, lbls, v_imgs, v_lbls = load_dataset()

gen_NBL((imgs, lbls), "data/NBL/")