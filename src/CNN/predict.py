from genericpath import isfile
import os
import subprocess as sb
import sys
import cv2 as cv
import numpy as np
import tensorflow as tf
import cnn_model as cnn_model
import file_management as file_management
import dataset as dataset
import math
import json
from yaml import safe_load
#import src.tile_crop.tile_crop_main
from tile_crop.tile_crop_main import single_image_to_folder_of_tiles as tile_image

IMG_SIZE = (102, 102)
MODEL = 'data/models/model_76'
WEIGHTS = 'data/models/best_b8e40.h5'
TILE_MASK_NAME_F = "{}_{}.mask"

model = tf.keras.models.load_model(MODEL, custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
if WEIGHTS != None:
    model.load_weights(WEIGHTS)


def get_mask_img(mask):
    """
    input is prediction of CNN
    output is a 2d binary image.
    """
    mask_img = np.zeros((54, 54))
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            
            if mask[y][x][1] > mask[y][x][0]:
                mask_img[y][x] = 255
            else:
                mask_img[y,x] = 0
    return mask_img


def val_mask_to_bin(true_mask):
    """
    convert mask with many values to binary values:
    bg = 0
    fg = 255
    """
    for i in range(true_mask.shape[0]):
            for j in range(true_mask.shape[1]):
                if true_mask[i,j,2] != 0:
                    true_mask[i,j] = [255,255,255]
    return true_mask



def create_windows(img):
    """
    Produce list of 102x102 images such that the centre 54x54
    of all images exactly cover the image image

    returns:
        - windows (list)
        - tile_dim (tuple that defines how many tiles span width and height of image)
    """
    og_img = np.copy(img)
    og_shape = og_img.shape
    windows = []
    right_buff = (img.shape[1] % 54) + 102
    bottom_buff = (img.shape[0] % 54) + 102
    img = cv.copyMakeBorder(img, 24, bottom_buff , 24, right_buff, cv.BORDER_CONSTANT)
    img = np.array(img)

    tile_dim= (
        math.ceil(og_shape[0]/54),
        math.ceil(og_shape[1]/54)
    )

    for i in range(tile_dim[0]):
        for j in range(tile_dim[1]):
            window = np.zeros((102,102,3), dtype=np.uint8)
            x = (i * 54) + 24
            y = (j * 54) + 24
            window = img[x-24:x+78, y-24:y+78]
            windows.append(window)
            #img_center = og_img[x-24:(x-24) + 54, y-24:(y-24) + 54]    
            #windows.append(np.array([window]))
        
    return np.float32(windows), tile_dim


 
def predict_image(img):
    """
    CNN prediction takes 102x102 centre of 
    image and predicts 54x54 centre
    therefore, we crop a 102x102 window by 54 pixel a step 
    to product all inputs that need to be predicted 
    to reconstruct the image
    """
   
    bot_cen_pad = img.shape[0] % 54
    right_cen_pad = img.shape[1] % 54
    
    img_mask = np.zeros((img.shape[0], img.shape[1]))
    imgs, tiles = create_windows(img)
    masks = model.predict(imgs)
    i = 0
    for x in range(tiles[0]):
        for y in range(tiles[1]):
            
            #mask = model.predict(imgs[i])
            mask = get_mask_img(masks[i])
            x_off = 54
            y_off = 54

            if x == tiles[0] - 1 and bot_cen_pad != 0:
                x_off = bot_cen_pad
            if y == tiles[1] - 1 and right_cen_pad != 0:
                y_off = right_cen_pad
            img_mask[x*54: x*54 + x_off, y*54: y*54 + y_off] = mask[0:x_off, 0:y_off]
            i += 1
    return img_mask


def construct_whole_mask(num_tiles, in_loc, out_loc, out_name):
    """
    constructs an entire image mask (.mask format) from tile masks (.mask formats)
    used for WSI mask creation.
    """
    
    masks = []
    img_size = [0,0]
    tile_dim = None
    #read masks and get whole mask size
    for i in range(1, num_tiles[0]+1):
        for j in range(1, num_tiles[1] + 1):
            f_name = TILE_MASK_NAME_F.format(i,j)
            print("decoding mask for tile",(i,j))
            tile_mask = dataset.decode_label(f"{in_loc}/{f_name}")[0]
            if i == 1:
                img_size[1] += tile_mask.shape[1]
            if j == 1:
                img_size[0] += tile_mask.shape[0]
            if i == 1 and j == 1:
                tile_dim = tile_mask.shape
            masks.append(tile_mask)
 
    print(img_size)
    whole_mask = np.zeros((img_size[0], img_size[1]))
    count = 0
    for i in range(1, num_tiles[0]+1):
        for j in range(1, num_tiles[1]+1):
            tile_mask = masks[count]
            end_0 = (i-1)*tile_dim[0] + tile_dim[0]
            end_1 = (j-1)*tile_dim[1] + tile_dim[1]
            print("stitching whole mask with tile", (i,j))
            if whole_mask.shape[0] - (i-1)*tile_dim[0] < end_0:
                end_0 = whole_mask.shape[0] - (i-1)*tile_dim[0] 
            if whole_mask.shape[1] - (j-1)*tile_dim[1] < end_1:
                end_1 = whole_mask.shape[1] - (j-1)*tile_dim[1]
            whole_mask [
                (i-1)*tile_dim[0]:end_0, 
                (j-1)*tile_dim[1]:end_1
            ] = tile_mask
            count += 1
    if dataset.encode_label(whole_mask, out_loc, out_name) != 0:
        return None
    
    return f"{out_loc}/{out_name}"


def predict_slide(svs_id, svs_file, tmp_dir, masks_dir):
    """
    produces svs_id.mask in masks_dir.
    used to predict WSI masks.
    saves current progress in tmp_dir in a .json 
    so progress can be resumed.

    tiles svs. Uses hueristics to determine if a tile has any tissue.
    if not, the mask for that tile will be all bg.

    progress is resumed by to first unpredicted tile.
    
    """
    ZOOM = 40
    TILE_NAME_PREDICT = "r{}-c{}_keep.png"
    TILE_NAME_IGNORE = "r{}-c{}_delete.png"
    TILE_JSON = "meta.json"
    json_file_path = f"{tmp_dir}/{TILE_JSON}"

    svs_file_name = svs_file[len(p_conf[file_management.SVS_DIR])+1:]
    

    #init
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_fd:
            j_dict = json.load(json_fd)
        num_tiles = j_dict["num_tiles"]
        
        #integrity check
        tile_ls = [file for file in os.listdir(tmp_dir) if (".png" in file)]
        if (num_tiles[0] * num_tiles[1]) != len(tile_ls) or j_dict["svs_image"] != svs_id:
            print("json exists but tiles not found, retiling.")
            #num_tiles = tile_slide(svs_file, ZOOM, tmp_dir)
            num_tiles =  tile_image(image_path = svs_file, save_dir=tmp_dir)[1]
            j_dict = {"svs_image": svs_id, "num_tiles": num_tiles, "current_tile": (1,1)}
            #num_tiles = dataset.create_grid(svs_file, tmp_dir, ZOOM)
         
    else:
        print("tiling current svs.")
        #num_tiles  = tile_slide(svs_file, ZOOM, tmp_dir)
        num_tiles =  tile_image(image_path = svs_file, save_dir=tmp_dir)[1]
        j_dict = {"svs_image": svs_id, "num_tiles": num_tiles, "current_tile": (1,1)}
       
    current_tile = j_dict["current_tile"]

    #start at current tile. 
    for i in range(current_tile[0], num_tiles[0]+1):
        for j in range(current_tile[1], num_tiles[1]+1):

            #update json.
            j_dict["current_tile"] = (i,j)
            
            with open(json_file_path, "w") as json_fd:
                json.dump(j_dict, json_fd)
            
            print(f"\npredicting {(i,j)}\n")

            #if tile labelled "delete". mask is all bg.
            if os.path.isfile(tmp_dir + "/" + TILE_NAME_IGNORE.format(i,j)):
                tile = cv.imread(tmp_dir + "/" + TILE_NAME_IGNORE.format(i,j))
                mask = np.zeros((tile.shape[0], tile.shape[1]))
            else:
                name = TILE_NAME_PREDICT.format(i,j)
                tile = cv.imread(f"{tmp_dir}/{name}")
                mask = predict_image(tile)

            #save mask of tile.
            dataset.encode_label (
                mask = mask, 
                file_location = f"{tmp_dir}/masks", 
                filename = TILE_MASK_NAME_F.format(i,j)
            )

    mask_loc = construct_whole_mask (
        num_tiles = num_tiles, 
        in_loc = f"{tmp_dir}/masks", 
        out_loc = masks_dir, 
        out_name = f"{svs_id}.mask"
    )
    
    # clean up
    file_management.clear_dir(tmp_dir)

    return mask_loc
    
def predict_manifest():
    """
        attempts to predict all svs files from manifest_in in yaml config. 
        searches for the first svs in manifest that has not been predicted
        (is not recorded in manifest_out). 

        assumes that download script is running, will wait for svs to be downloaded.
        Note. The function will not search first svs that is downloaded and is not predicted.

        Download script assumed to be using the same manifest_in, and therefore has the same 
        download/processing order. 
    """
    current_svs = svs_manager.get_new_svs()
    print(f"checking if svs with id {current_svs} is downloaded.")
    while current_svs != None:
        if not svs_manager.is_downloaded(current_svs):
            continue
        
        print(f"processing svs with id {current_svs}.")

        svs_file = svs_manager.find_file_from_id(current_svs)
        
        mask_file = predict_slide(
            current_svs,
            f"{p_conf[file_management.SVS_DIR]}/{svs_file}", 
            p_conf[file_management.TMP_DIR], 
            p_conf[file_management.MASK_DIR]
        )
        
        if mask_file == None:
            print("error predicting mask. Re-processing image.")
            continue

        svs_manager.append_manifest_out(current_svs, svs_file, f"{current_svs}.mask")

        print(f"Processing complete. Deleting svs with id {current_svs}")

        svs_manager.delete_svs(current_svs)

        current_svs = svs_manager.get_new_svs()



ARGS_LEN = 1
if __name__ == "__main__":
    #get config
    if len(sys.argv) < ARGS_LEN + 1:
        err_msg = """
        run program with the following format:
        python3 predict.py predict_config_.yaml
        """
        print(err_msg)
        exit(os.EX_USAGE)

    p_config_file = sys.argv[1].strip()
  
    if not os.path.exists(p_config_file or not os.path.isfile(p_config_file)):
        raise FileNotFoundError("predict config file does not exists.")

    p_conf = {}
    with open(p_config_file, "r") as conf:
        p_conf =  safe_load(conf)
    try:
        file_management.conf_init(p_conf)
    except Exception as err:
        print(str(err))
        exit(os.EX_CONFIG)

    svs_manager = file_management.svs_management(p_conf)

    try:
        file_management.check_manifest(p_conf[file_management.MANIFEST_IN])
    except Exception as err:
        print(str(err))
        exit(os.EX_CONFIG)

    predict_manifest()






    
