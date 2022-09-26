import cv2 as cv
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from skimage import measure, color, io
from skimage.segmentation import clear_border

"""
    when DEBUG flag is set to true image segmentation process
    can be viewed (original image to segmented image)
"""
DEBUG = True

"""
    Functions takes the path to an image as an argument,
    loads the image and returns it
"""
def load_image(img_to_load):

    # load in image, DEBUG if needed
    img = cv.imread(img_to_load)
    if(DEBUG): cv.imshow("og img", img)

    # return loaded image
    return img

"""
    Functions takes an image as an argument, blurs it, 
    and then makes it gray
"""
def gray_blur_image(img):

    # blur image before grey
    img_blur = cv.medianBlur(img,7)

    # create gray image and find threshold value
    # note: threshold pixels will be set to 255
    img_gray_blur = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

    # what gray blur look like
    if(DEBUG): cv.imshow("image01_gray_blur", img_gray_blur)

    # return img
    return img_gray_blur

"""
    Takes edited image saves and loads it
"""
def save_and_load(img):

    # Save grey blur img
    plt.imsave("image01_gray_blur.png", img)

    # filter blue channel?
    new_img = cv.imread("image01_gray_blur.png")

    # return new image
    return new_img

"""
    Find threshold of image, use threshold to open, erode, 
    and close edges within the image. Takes as an argument
    an image and returns the image with noise removed and 
    kernel as an array
"""
def remove_noise(img):

    # find threshold value (clearer gray image)
    # note: threshold pixels will be set to 255
    r1, threshold = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

    # remove small initial noise from image
    kernel = np.ones((3,3), np.uint8)
    opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel, iterations = 2)

    # remove edge touching grains (clears larger areas)
    opening = clear_border(opening)

    # continue removal of noise from image
    ero = cv.morphologyEx(opening, cv.MORPH_ERODE, kernel, iterations = 4)
    close = cv.morphologyEx(ero, cv.MORPH_CLOSE, kernel, iterations = 3)

    # make final image after removal of noise equal the initial image
    opening = close
    if(DEBUG): cv.imshow("opening after cleaning", opening)

    # create array to return
    ker_open_arr = [opening, kernel]

    # return kernel and opening
    return ker_open_arr

"""
    Takes an array and calculates sure foreground, sure
    background, and ambiguous region of the image. 
    Returns array of unknown and sure foreground
"""
def ambiguous_region(arr):

    # watershed for area that is sure background
    sure_bg = cv.dilate(arr[0], arr[1], iterations = 3)
    if(DEBUG): cv.imshow("sure bg", sure_bg)

    # watershed for area that is sure foreground
    dist_transform = cv.distanceTransform(arr[0], cv.DIST_L2, 5)
    max_dist_transform = dist_transform.max()
    r2, sure_fg = cv.threshold(dist_transform, 0.2*max_dist_transform, 255, 0)

    # getting unknown ambiguous region (background - foreground)
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)
    
    # create unknown and sure_fg array to return
    ukwn_sfg_arr = [unknown, sure_fg]

    # return temp array
    return ukwn_sfg_arr

"""
    Creates markers and labels the regions
"""
def mark_label_region(arr):

    # Create marker and label the regions
    r3, markers = cv.connectedComponents(arr[1])

    # increment and update markers
    markers = markers + 1
    markers[arr[0] == 255] = 0

    # return markers
    return markers

if __name__ == "__main__":

    # load in image to segment
    img = load_image("image01_without_mask.png")

    # blur and gray image
    img_gray_blur = gray_blur_image(img)

    # save newly created image and load it
    upd_img = save_and_load(img_gray_blur)

    # creates gray image (fuzzy not as good as below gray image)
    # cells = img[:,:,0]
    # cv.imshow("cells", cells)

    # create gray image
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if(DEBUG): cv.imshow("gray img", gray_img)

    # remove noise from image
    noise_rmv_arr = remove_noise(gray_img)

    # find sure background and sure foreground and calculate
    # ambiguous region (background - foreground)
    unkwn_sgf_arr = ambiguous_region(noise_rmv_arr)

    # create marker and label the region
    markers = mark_label_region(unkwn_sgf_arr)

    # perform watershed algorithm and reassign boundaries
    markers = cv.watershed(img, markers)
    img[markers == -1] = [0, 255, 0]

    # return an RBG image where color-coded labels are painted over
    img2 = color.label2rgb(markers, bg_label = 0)

    # display images and wait for key to close image window
    cv.imshow("Image", img)
    cv.waitKey(0)
