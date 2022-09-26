import os
import subprocess as sb
import sys

print(sys.path)
import cv2 as cv
import numpy as np
import tensorflow as tf
import cnn_model, file_management, dataset
from iou import get_iou
import math
import json


#from src.download_tool.config import field_validator, load_config
from yaml import safe_load



IMG_SIZE = (102, 102)
MODEL = 'data/models/model_76'
WEIGHTS = 'data/models/sep_15_aug_val.h5'


model = tf.keras.models.load_model(MODEL, custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
if WEIGHTS != None:
    model.load_weights(WEIGHTS)

"""
    input is prediction of CNN
    output is a 2d binary image.
"""
def get_mask_img(mask):
    mask_img = np.zeros((54, 54))
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            
            if mask[y][x][1] > mask[y][x][0]:
                mask_img[y][x] = 255
            else:
                mask_img[y,x] = 0
    return mask_img


def val_mask_to_bin(true_mask):
    for i in range(true_mask.shape[0]):
            for j in range(true_mask.shape[1]):
                if true_mask[i,j,2] != 0:
                    true_mask[i,j] = [255,255,255]
    return true_mask


"""
    Produce list of 102x102 images such that the centre 54x54
    of all images exactly cover the image image

    returns:
        - windows (list)
        - tile_dim (tuple that defines how many tiles span width and height of image)
"""
def create_windows(img):
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

            #img_center = og_img[x-24:(x-24) + 54, y-24:(y-24) + 54]    
            windows.append(np.array([window]))
        
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

    i = 0
    for x in range(tiles[0]):
        for y in range(tiles[1]):
            
            mask = model.predict(imgs[i])
            mask = get_mask_img(mask[0])
            x_off = 54
            y_off = 54

            if x == tiles[0] - 1 and bot_cen_pad != 0:
                x_off = bot_cen_pad
            if y == tiles[1] - 1 and right_cen_pad != 0:
                y_off = right_cen_pad
            img_mask[x*54: x*54 + x_off, y*54: y*54 + y_off] = mask[0:x_off, 0:y_off]
            i += 1
    return img_mask


def tile_slide(file,zoom, save_loc):
    return


def predict_slide(svs_id, svs_file, tmp_dir, masks_dir):
    ZOOM = 30
    TILE_NAME_PREDICT = "tile_{}_{}.png"
    TILE_NAME_IGNORE = "tile_{}_{}_delete.png"
    TILE_JSON = "meta.json"
    json_file_path = f"{tmp_dir}/{TILE_JSON}"
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_fd:
            j_dict = json.load(json_fd)
        num_tiles = j_dict["num_tiles"]
        
        tile_ls = [file for file in os.listdir(tmp_dir) if ("tile" in file)]
        if (num_tiles[0] * num_tiles[1]) != len(tile_ls):
            print("tiles not found, retiling.")
            num_tiles = tile_slide(svs_file, ZOOM, tmp_dir)
    else:
        num_tiles  = tile_slide(svs_file, ZOOM, tmp_dir)
        j_dict = {"svs_image": svs_id, "num_tiles": num_tiles, "current_tile": (0,0)}
       

    current_tile = j_dict["current_tile"]
    for i in range(current_tile[0], num_tiles[0]):
        for j in range(current_tile[1], num_tiles[1]):
            j_dict["current_tile"] = (i,j)
            with open(json_file_path, "w") as json_fd:
                json.dump(j_dict, json_fd)

            #scuffed solution
            if os.path.exists(TILE_NAME_IGNORE.format(i,j)):
                tile = cv.imread(TILE_NAME_IGNORE.format(i,j))
                mask = np.zeros((tile.shape[0], tile.shape[1]))
            else:
                tile = cv.imread(TILE_NAME_PREDICT.format(i,j))
                mask = predict_image(tile)
            #save mask
            dataset.encode_label(mask, f"{masks_dir}/{i}_{j}.mask")
    
    return 
    
def predict_manifest():
   
    current_svs = svs_manager.get_new_svs()
    print(f"checking if svs with id {current_svs} is downloaded.")
    while current_svs != None:
        if not svs_manager.is_downloaded(current_svs):
            continue
        
        print(f"processing svs with id {current_svs}.")

        svs_file = svs_manager.find_file_from_id(current_svs)
        #mask_file = predict_slide(f"{p_conf[metadata.SVS_DIR]}/{svs_file}", p_conf[metadata.TMP_DIR])
        
        
        svs_img = cv.imread(f"{p_conf[file_management.SVS_DIR]}/{svs_file}")
        mask = predict_image(svs_img)
        if dataset.encode_label(mask, p_conf[file_management.MASK_DIR], f"{current_svs}.mask") != 0:
            print("error encoding mask.")
        else:
            svs_manager.append_manifest_out(current_svs, svs_file, f"{current_svs}.mask")
        

        print(f"Processing complete. Deleting svs with id {current_svs}")

        current_svs = svs_manager.get_new_svs()



#predict_manifest()
#predict_slide("data/example_WSI.svs", "s")
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

    svs_manager = file_management.metadata(p_conf)

    try:
        file_management.check_manifest(p_conf[file_management.MANIFEST_IN])
    except Exception as err:
        print(str(err))
        exit(os.EX_CONFIG)

    predict_manifest()






    
