import cv2 as cv
import numpy as np
from openslide import open_slide
from matplotlib import pyplot as plt


"""
    When DEBUG flag is set to true images are displayed to screen.
    Flag used after loading in an image and when editing an image
    from RGBA to RGB.
"""
DEBUG = False


"""
    Converts SVS image to PNG. Takes as input input file name which
    is to be converted to the output file name. Reads input file name
    writes to output file name.
"""
def svs_to_png(input_file_name, output_file_name):

    # open the svs whole slide image
    slide = open_slide(input_file_name)

    # get dimensions of slide
    dims = slide.dimensions

    # read given region of the slide
    # result is a pillow object in mode RGBA
    region_slide = slide.read_region((0,0), 0, dims)

    # convert region image to RGB
    # note: if DEBUG is set to true loaded image will be shown
    region_slide_RGB = region_slide.convert('RGB')
    if DEBUG: region_slide_RGB.show()

    # convert image to numpy array
    # note: if DEBUG is set to true loaded image will be shown
    region_np = np.array(region_slide_RGB)
    if DEBUG: plt.imshow(region_np)

    # save the image
    cv.imwrite(output_file_name, region_np)


"""
    Converts SVS image to TIFF. Takes as input input file name which
    is to be converted to the output file name. Reads input file name
    writes to output file name.
"""
def svs_to_tiff(input_file_name, output_file_name):

    # open the svs whole slide image
    slide = open_slide(input_file_name)

    # get dimensions of slide
    dims = slide.dimensions

    # read given region of the slide
    # result is a pillow object in mode RGBA
    region_slide = slide.read_region((0,0), 0, dims)

    # convert region image to RGB
    # note: if DEBUG is set to true loaded image will be shown
    region_slide_RGB = region_slide.convert('RGB')
    if DEBUG: region_slide_RGB.show()

    # convert image to numpy array
    # note: if DEBUG is set to true loaded image will be shown
    region_np = np.array(region_slide_RGB)
    if DEBUG: plt.imshow(region_np)

    # save the image
    cv.imwrite(output_file_name, region_np)


