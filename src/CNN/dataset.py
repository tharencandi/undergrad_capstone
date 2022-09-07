
from logging import raiseExceptions
from re import I
import cv2 as cv
import numpy as np
#import openslide as osl
import tensorflow as tf
import random
from skimage.util.shape import view_as_windows 



TRAIN_LOCATION = "data/training/"
VAL_LOCATION = "data/validation/"


IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
NUM = 15


"""
    takes labels.txt and produces:
    - img_mask: binary image mask
    - cell_masks: list of binary images that isolate each cell

    see data/training/README_training.txt for input file format
"""
def decode_label(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    size = lines[0].split()
    size = (int(size[1]), int(size[0]))
    img_mask = np.zeros(size)
    
    l = []
    x = 0
    y = 0
    lines = lines[1:]
    lines = list(map(int, lines))
    num_cells = max(lines)
    cell_masks = np.zeros((num_cells, size[0], size[1]))
    for num in lines:
        num = int(num)
        if num != 0:
            img_mask[x][y] = 255
            cell_masks[num-1,x,y] = 255
        else:
            img_mask[x][y] = 0
        if y == size[1]-1 :
            x += 1
            y = 0
        else:
            y += 1
    return img_mask, cell_masks

"""
    load training and validation images as np arrays
"""
def load_dataset():
    
    train_imgs = []
    train_img_mask_ls = []
    train_cell_masks_ls = []

    val_imgs = []
    val_img_mask_ls = []
    val_cell_masks_ls = []

    for i in range(1, NUM+1):
        #train
        img = cv.imread(TRAIN_LOCATION + "image{:02d}.png".format(i))
        mask, cell_masks = decode_label(TRAIN_LOCATION + "image{:02d}_mask.txt".format(i))
     
        train_imgs.append(np.array(img))
        train_img_mask_ls.append(mask)
        train_cell_masks_ls.append(cell_masks)
        
        #validation
        v_img = cv.imread(VAL_LOCATION + "image{:02d}.png".format(i))
        v_mask, v_cell_masks = decode_label(VAL_LOCATION + "image{:02d}_mask.txt".format(i))

        val_imgs.append(v_img)
        val_img_mask_ls.append(v_mask)
        val_cell_masks_ls.append(v_cell_masks)
        
    
    return train_imgs, train_img_mask_ls, train_cell_masks_ls, val_imgs, val_img_mask_ls, val_cell_masks_ls

LOW =  -2147483648 
HIGH = 2147483647

"""
    slide window with a step of 54 pixels and random cropping to produce patches

    data is a tuple containing (img_list, label_list)
    
    images and labels are expected to be larger than 200x200. 
    The corresponding image and label is expected to be the same size.
    labels are expected to be binary images.
"""
def gen_NBL(data, location):
    imgs, lbls = data
    count = 0
    for i in range(len(imgs)):
        
        if imgs[i].shape[0] != lbls[i].shape[0] or imgs[i].shape[1] != lbls[i].shape[1]:
            raise NameError("inconsistent sized arrays")

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


"""
    Get average position of foreground in binary image.
"""
def get_component_position(single_component_frame):
    
    count = 0
    x_sum = 0
    y_sum = 0

    for y in range(single_component_frame.shape[1]):
        for x in range(single_component_frame.shape[0]):
            if (single_component_frame[x][y] != 0):
                count += 1
                x_sum += x
                y_sum += y
    
    return int(x_sum/count), int(y_sum/count)

"""
Nuclei Boundary (NBD) dataset is generated by centering each
nucleus at the center of each patch. This dataset is used for 
nuclei boundary detection.   

data is a tuple containing (img_list, label_list)
    
images and labels are expected to be larger than 200x200. 
The corresponding image and label is expected to be the same size.
labels are expected to be binary images.
"""    
def gen_NBD_and_SN(data, location_NBD, location_SN):
     #isolate blobs in image
    imgs, lbls, c_lbls = data
    
    count_NBD = 0
    count_SN = 0 
    for i in range(len(imgs)):

        if imgs[i].shape[0] != lbls[i].shape[0] or imgs[i].shape[1] != lbls[i].shape[1]:
            raise NameError("inconsistent sized arrays")

        img = imgs[i]
        shape = img.shape
        comp_lbls = c_lbls[i]
        
        for j in range(comp_lbls.shape[0]):
            
            comp = comp_lbls[j]
            
            (x,y) = get_component_position(comp)
            
            #ignore cell near edge ( one that cannot be centered in a (200,200) square without black borders)
            if (x < 100 or shape[0] - 100 < x or y < 100 or shape[1] - 100 < y):
                continue
            center = (shape[0]//2, shape[1]//2)

            T = np.float32([[1, 0, -(y-100)], [0, 1, -(x-100)]])
            # We use warpAffine to transform
            # the image using the matrix, T
            mask_centered = cv.warpAffine(lbls[i], T, (200,200))
            img_centered = cv.warpAffine(img, T, (200,200))

            cv.imwrite(location_NBD+"image{:04d}.png".format(count_NBD), np.array(img_centered))
            cv.imwrite(location_NBD+"image{:04d}_mask.png".format(count_NBD), np.array(mask_centered))
            count_NBD += 1

            #check if SN compatible
            T = np.float32([[1, 0, -(100-27)], [0, 1, -(100-27)]])
            mask_centered_54 = cv.warpAffine(mask_centered, T, (54,54))
            cell_pixel_count = 0
            for c in range(mask_centered_54.shape[0]):
                for r in range(mask_centered_54.shape[1]):
                    if mask_centered_54[c,r] != 0:
                        cell_pixel_count += 1
            print(cell_pixel_count / mask_centered_54.size)
            if cell_pixel_count / mask_centered_54.size <= 0.5:
                for c in range(3):
                    cv.imwrite(location_SN+"image{:04d}.png".format(count_SN), np.array(img_centered))
                    cv.imwrite(location_SN+"image{:04d}_mask.png".format(count_SN), np.array(mask_centered))
                    count_SN += 1
        
        print(f"img {i+1}/{len(imgs)}")


"""
    preserves image aspect ratio

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
"""



#

#gen_NBL((imgs, lbls), "data/NBL/")
#gen_NBD_and_SN((imgs, lbls, comp_labels), "data/NBD/", "data/SN/")