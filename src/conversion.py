import cv2 as cv
import numpy as np
from openslide import open_slide
from matplotlib import pyplot as plt

"""
    When flags are 'False' conversion to such type will not occur
    If png of tiff conversion is wanted for the png image
    set PNG and TIFF flags to 'True'.
"""
PNG = False
TIFF = True

"""
    when DEBUG flag is set to true image segmentation process
    can be viewed (original image to segmented image)
"""
DEBUG = False

"""
    Arguments are a numpy array and a file name. File name includes
    the .svs suffix. Remove .svs suffix and replace with .tiff, .png
    or both if needed. Once suffix changed, save image.
"""
def convert_image(np_arr, img_name):

    # split name by '.' and get image name
    name_arr = img_name.split('.')
    og_name = name_arr[0]

    # if tiff conversion wanted
    # add '.tiff' suffix and save the new image
    if TIFF: cv.imwrite(og_name + ".tiff", np_arr)

    # if png conversion wanted
    # add '.png' suffix and save the new image
    if PNG: cv.imwrite(og_name + ".png", np_arr)

if __name__ == "__main__":

    # open the svs whole slide image
    img_name = "tp.svs"
    slide = open_slide(img_name)

    # get dimensions of slide
    dims = slide.dimensions

    # read given region of the slide
    # result is a pillow object in mode RGBA
    region_slide = slide.read_region((0,0), 0, dims)

    # convert region image to RGB
    region_slide_RGB = region_slide.convert('RGB')
    if DEBUG: region_slide_RGB.show()

    # convert image to numpy array
    region_np = np.array(region_slide_RGB)
    if DEBUG: plt.imshow(region_np)

    # convert and save the image
    convert_image(region_np, img_name)
