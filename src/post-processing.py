"""
    Script performs post processing on whole slide images with binary 
    masks already produced in order to increase accuracy of predictions.
"""


import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


"""
    Function removes noising which has occured during the binary mask
    process. Takes in image with binary masks produced and returns
    the version with noise removed.
"""
def remove_noise(img_path):

    # read in image using image path provided
    img = cv.imread(img_path)

    cv.imshow("Original image", img)
    cv.waitKey(0)

if __name__ == "__main__":

    remove_noise()