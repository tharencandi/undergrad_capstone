import cv2 as cv
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from skimage import measure, color, io
from skimage.segmentation import clear_border

# load in image
img = cv.imread("image01.png")

# cells = img[:,:,0]
# plt.imshow(cells, cmap = "gray")

# create gray image and find threshold value
# note: threshold pixels will be set to 255
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
r1, threshold = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

# remove small initial noise from image
kernel = np.ones((3,3), np.unit8)
opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel, iterations = 2)

# remove edge touching grains
# opening = clear_border(opening)
# plt.imshow(opening, cmap = "gray")

# watershed for area that is sure background
sure_bg = cv.dilate(opening, kernel, iteration = 10)
# plt.imshow(sure_bg, cmap = "gray")

# watershed for area that is sure foreground
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
# plt.imshow(dist_transform, cmap = "gray")
max_dist_transform = dist_transform.max()
r2, sure_fg = cv.threshold(dist_transform, 0.5*max_dist_transform, 255, 0)
# plt.imshow(sure_fg, cmap = "gray")

# getting unknown ambiguous region (background - foreground)
sure_fg = np.unit8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)
# plt.imshow(unknown, cmap = "gray")



