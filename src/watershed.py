import cv2 as cv
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from skimage import measure, color, io
from skimage.segmentation import clear_border

DEBUG = False

#To be confirmed with scale of original image
#pixels_to_um = 0.454

# load in image
img = cv.imread("image01_without_mask.png")

# cells = img[:,:,0]
# plt.imshow(cells, cmap = "gray")

#Try blur image before grey?
img_blur = cv.medianBlur(img,7)

# create gray image and find threshold value
# note: threshold pixels will be set to 255
image01GrayBlur = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

#Whats gray blur look like
if(DEBUG):cv.imshow("image01_gray_blur",image01GrayBlur)

#Save grey blur img
plt.imsave("image01_gray_blur.png",image01GrayBlur)

#filter blue channel?
image01GrayBlur = cv.imread("image01_gray_blur.png")
cells = image01GrayBlur[:,:,0]

#What does filtered look like?
if(DEBUG): cv.imshow("gray_filtered_img",cells)

r1, threshold = cv.threshold(cells, 0, 255, 
cv.THRESH_BINARY +cv.THRESH_OTSU)

# remove small initial noise from image
kernel = np.ones((3,3), np.uint8)
opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, 
kernel, iterations = 2)

#What does opening look like?
if(DEBUG): cv.imshow("opening_pre_clear",opening)

# remove edge touching grains (This removed everything? - removed)
# opening = clear_border(opening)
# cv.imshow("opening_post_clear",opening)

# Define sure background
sure_bg = cv.dilate(opening, kernel, iterations = 3)

# What does sure background look like?
if(DEBUG): cv.imshow("sure_bg",sure_bg)

# transform for area that is sure foreground
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
max_dist_transform = dist_transform.max()
r2, sure_fg = cv.threshold(dist_transform, 
0.05*max_dist_transform, 255, 0)

# What does sure foreground look like?
if(DEBUG): cv.imshow("sure_fg",sure_fg)

# getting unknown ambiguous region (background - foreground)
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)

# Create marker and label the regions
r3, markers = cv.connectedComponents(sure_fg)

# What does markers look like?
# if(DEBUG): cv.imshow("markers",markers)

#Set marker vectors fg != 0
markers = markers + 10
#Set bg = 0
markers[unknown == 255] = 0

#perform watershed
markers = cv.watershed(img, markers)

#reassign boundaries
img[markers == -1] = [0,255,0]

# return an RBG image where color-coded labels are painted over
Coloured_watershed_run_on_greyblur = color.label2rgb(markers, bg_label = 0)

# save images
plt.imsave("image01_attempt.png",img)


# plt.imshow("Overlay", img2)
# plt.imshow("Color Grains", img2)
cv.waitKey(0)
