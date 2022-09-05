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
DEBUG = False

# load in image
img = cv.imread("image01_without_mask.png")
if(DEBUG): cv.imshow("og img", img)

# blur image before grey
img_blur = cv.medianBlur(img,7)

# create gray image and find threshold value
# note: threshold pixels will be set to 255
image01GrayBlur = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

#Whats gray blur look like
if(DEBUG): cv.imshow("image01_gray_blur",image01GrayBlur)

#Save grey blur img
plt.imsave("image01_gray_blur.png",image01GrayBlur)

#filter blue channel?
image01GrayBlur = cv.imread("image01_gray_blur.png")

# creates gray image (fuzzy not as good as below gray image)
# cells = img[:,:,0]
# cv.imshow("cells", cells)

# create gray image
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
if(DEBUG): cv.imshow("gray img", gray_img)

# find threshold value (clearer gray image)
# note: threshold pixels will be set to 255
r1, threshold = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

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

# watershed for area that is sure background
sure_bg = cv.dilate(opening, kernel, iterations = 3)
if(DEBUG): cv.imshow("sure bg", sure_bg)

# watershed for area that is sure foreground
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
max_dist_transform = dist_transform.max()
r2, sure_fg = cv.threshold(dist_transform, 0.7*max_dist_transform, 255, 0)

# getting unknown ambiguous region (background - foreground)
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)

# Create marker and label the regions
r3, markers = cv.connectedComponents(sure_fg)

# increment and update markers
markers = markers + 1
markers[unknown == 255] = 0

# perform watershed algorithm
markers = cv.watershed(img, markers)

# reassign boundaries
img[markers == -1] = [0, 255, 0]

# return an RBG image where color-coded labels are painted over
img2 = color.label2rgb(markers, bg_label = 0)

# display images and wait for key to close image window
cv.imshow("Image", img)
cv.waitKey(0)
