"""
    Script uses provided binary masks to create border pixels.
"""


import cv2 as cv 
import numpy as np
from matplotlib import pyplot as plt


"""
    Function defines borders and erodes a certain amount of pixels 
    into objects. Then it dilates this object using the border
    side provided. Final region is the border.
"""
def generate_border(img, erosion_size, border_size):

    # erode edge pixels
    init_erosion = np.ones((3,3), np.uint8)
    img_eroded = cv.erode(img, init_erosion,  iterations=erosion_size)

    # create dilation size
    # create kernel to be used for dilation then dilate
    kernel_size = (border_size*2) + 1
    dilation_kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilate_img = cv.dilate(img_eroded, dilation_kernel, iterations=1)

    # where 255 image values are, replace with 127.
    dilate_replace = np.where(dilate_img == 255, 127, dilate_img)

    # convert eroded object region to 255 pixel value
    border = np.where(img_eroded > 127, 255, dilate_replace)

    # return original image with borders produced
    return border


