import os
from random import random
import cv2
import numpy as np
import imutils
import random
import tensorflow
# from skimage import data
# from skimage import transform

# def rotate_image(image, angle):
#   image_center = tuple(np.array(image.shape[1::-1]) / 2)
#   rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#   result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
#   return result

dir = os.getcwd()
result_img_dir_path = dir + "/result_img"
src_img_dir_path = dir + "/src_img"
result_mask_dir_path = dir + "/result_mask"
src_mask_dir_path = dir + "/src_mask"

LOW =  -2147483648 
HIGH = 2147483647
tensorflow.random.set_seed(random.randint(LOW, HIGH))

def ran_vh_shift(img, mask):

    """
    a random vertical and horizontal shift in a range of [−0.05, 0.05] 
    with respected to the patch’s width and height
    Then save to the result folder

    input: image (read by cv2)
            correspanding mask (read by cv2)

    output: img_shifted, 
            mask_shifted
    """
    
    width = img.shape[1]
    height = img.shape[0]
    vs_factor = random.uniform(-0.05, 0.05)*height
    hs_factor = random.uniform(-0.05, 0.05)*width
    
    #vertical and horizontal shift matrix
    vhsM = np.float32([[1, 0, hs_factor], [0, 1, vs_factor]])
    img_shifted = cv2.warpAffine(img, vhsM, (width, height))
    mask_shifted = cv2.warpAffine(mask, vhsM, (width, height))

    return img_shifted, mask_shifted
    
    # cv2.imwrite(img_dest_path, img_shifted)
    # cv2.imwrite(mask_dest_path, mask_shifted)

def ran_rotation(img, mask):
    """
    a random rotation in a range of [−45◦, 45◦] degree
    Then save to the result folder

    input: image (read by cv2)
            correspanding mask (read by cv2)

    output: img_rotated, 
            mask_rotated

    """
    
    rotate_factor = random.randint(-45, 45)
    img_rotated = imutils.rotate(img, rotate_factor)
    mask_rotated = imutils.rotate(mask, rotate_factor)

    # cv2.imwrite(img_dest_path, img_rotated)
    # cv2.imwrite(mask_dest_path, mask_rotated)
    return img_rotated, mask_rotated

def ran_flip(img, mask):
    """
    a random vertical and horizontal flipping with probability 0.5

    input: image (read by cv2)
            correspanding mask (read by cv2)
            
    output: img_flipped, 
            mask_flipped
    """

    hf = bool(random.getrandbits(1))
    vf = bool(random.getrandbits(1))

    if hf and not vf:
        flip_factor = 1
    elif vf and not hf:
        flip_factor = 0
    elif hf and vf:
        flip_factor = -1
    else:
        flip_factor = random.choice([-1, 0, 1])

    img_flipped = cv2.flip(img, flip_factor)
    mask_flipped = cv2.flip(mask, flip_factor)

    # cv2.imwrite(img_dest_path, img_flipped)
    # cv2.imwrite(mask_dest_path, mask_flipped)
    return img_flipped, mask_flipped


def ran_resize(img, mask):
    """
    a random resizing with a ratio in a range of [0.7, 2.0]

    input: image (read by cv2)
            correspanding mask (read by cv2)
            
    output: img_resized, 
            mask_resized
    """

    resize_factor = random.uniform(0.7, 2.0)
    width = int(img.shape[1]*resize_factor)
    height = int(img.shape[0]*resize_factor)
    dsize = (width, height)

    img_resized = cv2.resize(img, dsize)
    mask_resized = cv2.resize(mask, dsize)

    # cv2.imwrite(img_dest_path, img_resized)
    # cv2.imwrite(mask_dest_path, mask_resized)
    return img_resized, mask_resized



def ran_shear(img, mask):
    """
    a random shear with intensity in a range of [−0.4π, 0.4π]

    input: image (read by cv2)
            correspanding mask (read by cv2)
            
    output: img_sheared, 
            mask_sheared
    """
    # LOW =  -2147483648 
    # HIGH = 2147483647
    # tensorflow.random.set_seed(random.randint(LOW, HIGH))

    # seed = random.randint(LOW, HIGH)

    # scikit_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # scikit_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    # do something in scikit
    # opencv_img = cv2.cvtColor(scikit_img, cv2.COLOR_RGB2BGR)
    # # do something in opencv
        
    shear_factor = random.uniform(-0.4, 0.4)*180

    # afine_tf = transform.AffineTransform(shear=shear_factor)

    # # Apply transform to image data
    # img_sheared = transform.warp(scikit_img, inverse_map=afine_tf)
    # mask_sheared = transform.warp(scikit_mask, inverse_map=afine_tf)
    # tensorflow.random.set_seed(random.randint(LOW, HIGH))
    # img_sheared = tensorflow.keras.preprocessing.image.random_shear(img, shear_factor, row_axis=1, col_axis=0, channel_axis=2)
    img_sheared = tensorflow.keras.preprocessing.image.apply_affine_transform(img, shear=shear_factor, row_axis=1, col_axis=0, channel_axis=2)
    mask_sheared = tensorflow.keras.preprocessing.image.apply_affine_transform(mask, shear=shear_factor, row_axis=1, col_axis=0, channel_axis=2)
    # tensorflow.random.set_seed(random.randint(LOW, HIGH))
    # mask_sheared = tensorflow.keras.preprocessing.image.random_shear(mask, shear_factor, row_axis=1, col_axis=0, channel_axis=2)

    # cv2.imwrite(img_dest_path, img_sheared)
    # cv2.imwrite(mask_dest_path, mask_sheared)
    return img_sheared, mask_sheared

def center_crop(img, mask, dim):
    """
    crop the senter of the imgs with dim x dim

    input: image (read by cv2)
            correspanding mask (read by cv2)
            
    output: img_cropped, 
            mask_cropped
    """

    width = img.shape[1]
    height = img.shape[0]
    crop_width = dim
    crop_height = dim
    mid_x, mid_y = int(width/2), int(height/2)
    cw2, ch2 = int(crop_width/2), int(crop_height/2) 
    img_cropped = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
    mask_cropped = mask[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]

    return img_cropped, mask_cropped

def black_border(img, mask, dim):
    """
    keep dim x dim content in the center of the images 
    and fill in other parts as black 
    

    input: image (read by cv2) expects 102x102
            correspanding mask (read by cv2) expects 102x102
            
    output: img_bordered, 
            mask_bordered

    """

    width = img.shape[1]
    height = img.shape[0]
    img_cropped, mask_cropped = center_crop(img, mask, dim)



    fill_width = int((width-dim)/2)
    fill_height = int((height-dim)/2)
    img_bordered = cv2.copyMakeBorder(img_cropped, fill_height, fill_height, 
                                        fill_width, fill_width, cv2.BORDER_CONSTANT, 
                                        None, value = 0)
    mask_bordered = cv2.copyMakeBorder(mask_cropped, fill_height, fill_height, 
                                        fill_width, fill_width, cv2.BORDER_CONSTANT, 
                                        None, value = 0)

    return img_bordered, mask_bordered


# disable due to unknow hidden files in dir
# n = len(os.listdir(src_img_dir_path))

# CHANGE THE VALUE OF n TO NUMBER OF IMAGES IN SRC_IMG OR SRC_MASK
n = 1
counter = 0

for i in range(n):
    img_path = src_img_dir_path+"/"+"image"+ "{:04d}".format(i) + ".png"
    mask_path = src_mask_dir_path+"/"+"image"+ "{:04d}".format(i) + "_mask.png"
    
    img = cv2.imread(img_path)
    img = np.array(img)
    mask = cv2.imread(mask_path)
    mask = np.array(mask)

    ori_img_cropped, ori_mask_cropped = center_crop(img, mask, 102)

    cv2.imwrite(result_img_dir_path+"/"+"image"+ "{:04d}".format(counter) + ".png", ori_img_cropped)
    cv2.imwrite(result_mask_dir_path+"/"+"image"+ "{:04d}".format(counter) + "_mask.png", ori_mask_cropped)
    counter += 1

    ori_img_bordered, ori_mask_bordered = black_border(ori_img_cropped, ori_mask_cropped, 54)
    cv2.imwrite(result_img_dir_path+"/"+"image"+ "{:04d}".format(counter) + ".png", ori_img_bordered)
    cv2.imwrite(result_mask_dir_path+"/"+"image"+ "{:04d}".format(counter) + "_mask.png", ori_mask_bordered)
    counter += 1

    for j in range(3):
        img_shifted, mask_shifted = ran_vh_shift(img, mask)
        img_rotated, mask_rotated = ran_rotation(img_shifted, mask_shifted)
        img_flipped, mask_flipped = ran_flip(img_rotated, mask_rotated)
        img_sheared, mask_sheared = ran_shear(img_flipped, mask_flipped)
        img_resized, mask_resized = ran_resize(img_sheared, mask_sheared)
        img_f, mask_f = center_crop(img_resized, mask_resized, 102) 
        img_path_f = result_img_dir_path+"/"+"image"+ "{:04d}".format(counter) + ".png"
        mask_path_f = result_mask_dir_path+"/"+"image"+ "{:04d}".format(counter) + "_mask.png"
        counter += 1
        cv2.imwrite(img_path_f, img_f)
        cv2.imwrite(mask_path_f, mask_f)
        print("{:04d}".format(counter), str(img_f.shape[1]), str(img_f.shape[0]), str(mask_f.shape[1]), str(mask_f.shape[0]))
        
        # img_sheared, mask_sheared = ran_shear(img, mask)
        # cv2.imwrite(img_path_f, img_resized)
        # cv2.imwrite(mask_path_f, mask_resized)


    # # a random vertical and horizontal shift in a range of [−0.05, 0.05] 
    # # with respected to the patch’s width and height
    # vhs_img_dest_path = result_img_dir_path+"/"+"image"+ "{:04d}".format(i+n) + ".png"
    # vhs_mask_dest_path = result_mask_dir_path+"/"+"image"+ "{:04d}".format(i+n) + "_mask.png"
    # vh_shift(img, mask, vhs_img_dest_path, vhs_mask_dest_path)


    # # a random rotation in a range of [−45◦, 45◦] degree
    # rot_img_dest_path = result_img_dir_path+"/"+"image"+ "{:04d}".format(i+2*n) + ".png"
    # rot_mask_dest_path = result_mask_dir_path+"/"+"image"+ "{:04d}".format(i+2*n) + "_mask.png"
    # rotation(img, mask, rot_img_dest_path, rot_mask_dest_path)

    # # a random vertical and horizontal flipping with probability 0.5
    # flip_img_dest_path = result_img_dir_path+"/"+"image"+ "{:04d}".format(i+3*n) + ".png"
    # flip_mask_dest_path = result_mask_dir_path+"/"+"image"+ "{:04d}".format(i+3*n) + "_mask.png"
    # ran_flip(img, mask, flip_img_dest_path, flip_mask_dest_path)

    # # a random resizing with a ratio in a range of [0.7, 2.0]
    # resize_img_dest_path = result_img_dir_path+"/"+"image"+ "{:04d}".format(i+4*n) + ".png"
    # resize_mask_dest_path = result_mask_dir_path+"/"+"image"+ "{:04d}".format(i+4*n) + "_mask.png"
    # resize(img, mask, resize_img_dest_path, resize_mask_dest_path)

    # # a random shear with intensity in a range of [−0.4π, 0.4π]
    # shear_img_dest_path = result_img_dir_path+"/"+"image"+ "{:04d}".format(i+5*n) + ".png"
    # shear_mask_dest_path = result_mask_dir_path+"/"+"image"+ "{:04d}".format(i+5*n) + "_mask.png"
    # ran_shear(img, mask, shear_img_dest_path, shear_mask_dest_path)


    # window_name='Rotate Image by Angle in Python'
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # cv2.imshow(window_name,img_rotated)
    # cv2.imshow(window_name,mask_rotated)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
