from textwrap import fill
from CNN.predict import construct_whole_mask
import numpy as np
import cv2 as cv
from os import path, mkdir
import shutil

TMP = "src/tests/CNN_tests/tmp"
if not path.exists(TMP):
    mkdir(TMP)
TILE_MASK_NAME_F = "{}_{}.png"

"""
checker board pattern to emulate masks
"""
def _gen_temp_files(rows, columns, tile_shape):
    isBlack = True
    for col in range(columns):
        for row in range(rows):
            if isBlack:
                tile = np.zeros(tile_shape, dtype = np.uint8)
            else:
                tile = np.full(tile_shape, dtype = np.uint8, fill_value=255)
            isBlack = not isBlack
            name = TILE_MASK_NAME_F.format(col+1, row+1)
            cv.imwrite(f"{TMP}/{name}", tile)

def _clean_up():
    shutil.rmtree(TMP)
    mkdir(TMP)


def test_good():
    out_name = "good_test.tiff"
    img_shape = (5*1024, 5*1024)
    _gen_temp_files(5,5,(1024, 1024))
    ret = construct_whole_mask((5,5), TMP,TMP, out_name, img_shape )
    assert ret == f"{TMP}/{out_name}"
    img = cv.imread(ret, cv.IMREAD_GRAYSCALE)
    assert img.shape == img_shape
    isBlack = True
    white = np.full((1024,1024), dtype=np.uint8, fill_value=255)
    black = np.zeros((1024,1024), dtype=np.uint8)
    for i in range(img.shape[0]-1024, 1024):
        for j in range(img.shape[1]-1024, 1024):
            if isBlack:
                np.testing.assert_array_equal(img[i:i+1024, j:j+1024],black)
            else:
                np.testing.assert_array_equal(img[i:i+1024, j:j+1024],white)
            isBlack = not isBlack
    _clean_up()

def test_inconsistent_size():
    out_name = "bad_test.tiff"
    img_shape = ((5*1024)-5, (5*1024)-5)
    _gen_temp_files(5,5,(1024, 1024))
    ret = construct_whole_mask((5,5), TMP,TMP, out_name, img_shape )
    
    assert ret == None

    _clean_up()

