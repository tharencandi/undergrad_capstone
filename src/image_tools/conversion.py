import cv2 as cv
import numpy as np
from openslide import open_slide, OpenSlideError
import os
from gc import collect
from psutil import disk_usage
import tifffile as tif

GOOD = 0
EXTENSION_FORMAT_ERR = 1
DISK_MEMORY_ERR = 2
EXCEPTION_RAISED = 3
FILE_INPUT_ERROR = 4 

TILE = 1024
TMP_DIR =  f"{os.getcwd()}/" #if path end with slash. This is the programmers responsibility. 
TMP_FILE = "temp_arr.np"

def _read_slide_to_array(slide_file_path, tile):
    """
        Read slide to a memory mapped array in chunks (tile, tile) pixels large.
        return memory mapped array.

        @warning
        IT IS THE CALLERS FUNCTION JOB TO APPROPRIATLEY DELETE THIS MEMORY MAPPED
        ARRAY AND CALL PYTHON GARBAGE COLLECTION FOR CLEANUP FOR GOOD CODE PERFORMANCE.

        @exceptions
        raises memory error if not enough storage for memmap.
        
    """
    
    svs = open_slide(slide_file_path)

    width, height = svs.dimensions
    free_space = disk_usage(TMP_DIR).free
    
    svs_file_size = os.path.getsize(slide_file_path)

    if (width*height) + 2*svs_file_size > free_space:
        raise MemoryError
    
    arr = np.memmap(TMP_DIR + TMP_FILE ,shape=(height, width, 3),dtype = np.uint8, mode="w+")
    
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            tile_height = min(tile, height-y)
            tile_width = min(tile, width-x)
            
            arr[y:y+tile_height,x:x + tile_width] = svs.read_region (
                location=(x,y),
                level=0, 
                size=(tile_width, tile_height)
            ).convert('RGB')
    arr.flush()
    svs.close()
    return arr


"""
    Converts SVS image to PNG. Takes as input input file name which
    is to be converted to the output file name. Reads input file name
    writes to output file name.
"""
def svs_to_png(input_file_name, output_file_name):
    if input_file_name == None or output_file_name == None:
        return EXTENSION_FORMAT_ERR

    if ".svs" not in input_file_name and ".png" not in output_file_name:
        return EXTENSION_FORMAT_ERR
    
    try: 
        image_array = _read_slide_to_array(input_file_name, TILE)
        #swap RGB to BGR - this is a bad solution (slower than has to be).
        #can be improved by dealing with this in _read_slide_to_array. note that tiff func req rgb.
        cv.imwrite(output_file_name, image_array[:, :, ::-1])
        os.remove(TMP_DIR + TMP_FILE)
        del image_array
        collect() #run garbage collection
    except OpenSlideError:
        return FILE_INPUT_ERROR
    except cv.error:
        os.remove(TMP_DIR + TMP_FILE)
        return EXCEPTION_RAISED
    except MemoryError:
        return DISK_MEMORY_ERR
    except Exception as e:
        if os.path.isfile(TMP_DIR + TMP_FILE):
            os.remove(TMP_DIR + TMP_FILE)
        print(e)
        return EXCEPTION_RAISED

    return GOOD

"""
    Converts SVS image to TIFF. Takes as input input file name which
    is to be converted to the output file name. Reads input file name
    writes to output file name.
"""
def svs_to_tiff(input_file_name, output_file_name):
    if input_file_name == None or output_file_name == None:
        return EXTENSION_FORMAT_ERR
        
    if ".svs" not in input_file_name and (".tif" not in output_file_name and ".tiff" not in output_file_name):
        print(input_file_name)
        print(output_file_name)
        return EXTENSION_FORMAT_ERR
    
    try: 
        image_array = _read_slide_to_array(input_file_name, TILE)
     
        tif.imwrite(
            output_file_name,
            image_array,
            bigtiff=True,
            tile=(1024, 1024),
            compression='zlib',
            compressionargs={'level': 8},
        )
        
        
        del image_array
        os.remove(TMP_DIR + TMP_FILE)
        collect() #run garbage collection
        
    except OpenSlideError:
        return FILE_INPUT_ERROR
    except cv.error:
        os.remove(TMP_DIR + TMP_FILE)
        return EXCEPTION_RAISED
    except MemoryError:
        return DISK_MEMORY_ERR
    except Exception as e :
        if os.path.isfile(TMP_DIR + TMP_FILE):
            os.remove(TMP_DIR + TMP_FILE)
        print(e)
        return EXCEPTION_RAISED
    return GOOD
    