import pytest


from conversion import *
from openslide import open_slide


GOOD = 0
EXTENSION_FORMAT_ERR = 1
DISK_MEMORY_ERR = 2
EXCEPTION_RAISED = 3
FILE_INPUT_ERROR = 4


TILE = 1024


"""
    Test incorrect input file name for svs_to_tiff error handling
"""
def test_incorrect_input_file_name_svs_to_tiff():
    ret = svs_to_tiff("test_img.png", "test_img.tiff")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test incorrect output file name for svs_to_tiff error handling
"""
def test_incorrect_output_file_name_svs_to_tiff():
    ret = svs_to_tiff("test_img.svs", "test_img.png")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test incorrect input file name for svs_to_png error handling
"""
def test_incorrect_input_file_name_svs_to_png():
    ret = svs_to_png("test_img.tiff", "test_img.png")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test incorrect output file name for svs_to_png error handling
"""
def test_incorrect_output_file_name_svs_to_png():
    ret = svs_to_png("test_img.svs", "test_img.tiff")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test None input file name for svs_to_tiff error handling
"""
def test_none_input_file_name_svs_to_tiff():
    ret = svs_to_tiff(None, "test_img.tiff")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test None output file name for svs_to_tiff error handling
"""
def test_none_output_file_name_svs_to_tiff():
    ret = svs_to_tiff("test_img.svs", None)
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test None input file name for svs_to_png error handling
"""
def test_none_input_file_name_svs_to_png():
    ret = svs_to_png(None, "test_img.png")
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test None output file name for svs_to_png error handling
"""
def test_none_output_file_name_svs_to_png():
    ret = svs_to_png("test_img.svs", None)
    assert ret == EXTENSION_FORMAT_ERR

"""
    Test ability to correctly convert a svs to tiff
"""
def test_svs_to_tiff():
    ret = svs_to_tiff("tp.svs", "tp.tiff")
    assert ret == GOOD

"""
    Test ability to correctly convert a svs to png
"""
def test_svs_to_png():
    ret = svs_to_png("tp.svs", "tp.png")
    assert ret == GOOD

# """
#     Test ability to correctly read slide for svs image
# """
# def test_read_svs_image():
#     input_file_name = "tp.svs"

#     slide = open_slide(input_file_name)
#     dims = slide.dimensions
#     region_slide = slide.read_region((0,0), 0, dims)

#     arr = _read_slide_to_array(input_file_name, TILE)

#     assert arr == region_slide
