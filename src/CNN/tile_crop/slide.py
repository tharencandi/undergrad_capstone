# ------------------------------------------------------------------------
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ------------------------------------------------------------------------

#source: https://github.com/CODAIT/deep-histopath/blob/master/deephistopath/wsi/slide.py#L17

import glob
import math
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import openslide
from openslide import OpenSlideError
import os
import PIL
from PIL import Image
import re
import sys
import tile_crop.util as util
from tile_crop.util import Time

BASE_DIR = os.path.join(".", "data")
# BASE_DIR = os.path.join(os.sep, "Volumes", "BigData", "TUPAC")
TRAIN_PREFIX = "CELLCIRC-"
SRC_TRAIN_DIR = os.path.join(BASE_DIR, "training_slides")
SRC_TRAIN_EXT = "svs"
DEST_TRAIN_SUFFIX = ""  # Example: "train-"
DEST_TRAIN_EXT = "png"
SCALE_FACTOR = 32
DEST_TRAIN_DIR = os.path.join(BASE_DIR, "training_" + DEST_TRAIN_EXT)
THUMBNAIL_SIZE = 300
THUMBNAIL_EXT = "jpg"

DEST_TRAIN_THUMBNAIL_DIR = os.path.join(BASE_DIR, "training_thumbnail_" + THUMBNAIL_EXT)

FILTER_SUFFIX = ""  # Example: "filter-"
FILTER_RESULT_TEXT = "filtered"
FILTER_DIR = os.path.join(BASE_DIR, "filter_" + DEST_TRAIN_EXT)
FILTER_THUMBNAIL_DIR = os.path.join(BASE_DIR, "filter_thumbnail_" + THUMBNAIL_EXT)
FILTER_PAGINATION_SIZE = 50
FILTER_PAGINATE = True
FILTER_HTML_DIR = BASE_DIR

TILE_SUMMARY_DIR = os.path.join(BASE_DIR, "tile_summary_" + DEST_TRAIN_EXT)
TILE_SUMMARY_ON_ORIGINAL_DIR = os.path.join(BASE_DIR, "tile_summary_on_original_" + DEST_TRAIN_EXT)
TILE_SUMMARY_SUFFIX = "tile_summary"
TILE_SUMMARY_THUMBNAIL_DIR = os.path.join(BASE_DIR, "tile_summary_thumbnail_" + THUMBNAIL_EXT)
TILE_SUMMARY_ON_ORIGINAL_THUMBNAIL_DIR = os.path.join(BASE_DIR, "tile_summary_on_original_thumbnail_" + THUMBNAIL_EXT)
TILE_SUMMARY_PAGINATION_SIZE = 50
TILE_SUMMARY_PAGINATE = True
TILE_SUMMARY_HTML_DIR = BASE_DIR

TILE_DATA_DIR = os.path.join(BASE_DIR, "tile_data")
TILE_DATA_SUFFIX = "tile_data"

TOP_TILES_SUFFIX = "top_tile_summary"
TOP_TILES_DIR = os.path.join(BASE_DIR, TOP_TILES_SUFFIX + "_" + DEST_TRAIN_EXT)
TOP_TILES_THUMBNAIL_DIR = os.path.join(BASE_DIR, TOP_TILES_SUFFIX + "_thumbnail_" + THUMBNAIL_EXT)
TOP_TILES_ON_ORIGINAL_DIR = os.path.join(BASE_DIR, TOP_TILES_SUFFIX + "_on_original_" + DEST_TRAIN_EXT)
TOP_TILES_ON_ORIGINAL_THUMBNAIL_DIR = os.path.join(BASE_DIR,
                                                   TOP_TILES_SUFFIX + "_on_original_thumbnail_" + THUMBNAIL_EXT)

TILE_DIR = os.path.join(BASE_DIR, "tiles_" + DEST_TRAIN_EXT)
TILE_SUFFIX = "tile"

STATS_DIR = os.path.join(BASE_DIR, "svs_stats")


def open_slide(filename):
  """
  Open a whole-slide image (*.svs, etc).

  Args:
    filename: Name of the slide file.

  Returns:
    An OpenSlide object representing a whole-slide image.
  """
  try:
    slide = openslide.open_slide(filename)
  except OpenSlideError:
    slide = None
  except FileNotFoundError:
    slide = None
  return slide


def open_image(filename):
  """
  Open an image (*.jpg, *.png, etc).

  Args:
    filename: Name of the image file.

  returns:
    A PIL.Image.Image object representing an image.
  """
  image = Image.open(filename)
  return image


def open_image_np(filename):
  """
  Open an image (*.jpg, *.png, etc) as an RGB NumPy array.

  Args:
    filename: Name of the image file.

  returns:
    A NumPy representing an RGB image.
  """
  pil_img = open_image(filename)
  np_img = util.pil_to_np_rgb(pil_img)
  return np_img



def get_training_slide_path_name(image_name):
  """
  Convert slide number to a path to the corresponding WSI training slide file.

  Example:
    5 -> ../data/training_slides/TUPAC-TR-005.svs

  Args:
    slide_number: The slide number.

  Returns:
    Path to the WSI training slide file.
  """
  slide_filepath = os.path.join(".",image_name.rstrip(".svs") + "." + SRC_TRAIN_EXT)
  return slide_filepath



def get_tile_image_path_name(tile, directory):
  """
  Obtain tile image path based on tile information such as row, column, row pixel position, column pixel position,
  pixel width, and pixel height.

  Args:
    tile: Tile object.

  Returns:
    Path to image tile.
  """
  t = tile
  #updating this might cause issues with rest of codebase - to be confirmed before removing additional name info
  # tile_path = os.path.join(directory, t.image_name + "-" + TILE_SUFFIX + "-r%d-c%d-x%d-y%d-w%d-h%d" % (
  #                            t.r, t.c, t.o_c_s, t.o_r_s, t.o_c_e - t.o_c_s, t.o_r_e - t.o_r_s) + "." + DEST_TRAIN_EXT)

  # tile_path = os.path.join(directory, "r%d-c%d" % (
  #                           t.r, t.c) + "." + DEST_TRAIN_EXT)

  tile_path = os.path.join(directory, "r%d-c%d-tp%d" % (
                            t.r, t.c, t.tissue_percentage) + "." + DEST_TRAIN_EXT)
  return tile_path




def get_tile_image_path_by_slide_row_col(slide_number, row, col):
  """
  Obtain tile image path using wildcard lookup with slide number, row, and column.

  Args:
    slide_number: The slide number.
    row: The row.
    col: The column.

  Returns:
    Path to image tile.
  """
  padded_sl_num = str(slide_number).zfill(3)
  wilcard_path = os.path.join(TILE_DIR, padded_sl_num,
                              TRAIN_PREFIX + padded_sl_num + "-" + TILE_SUFFIX + "-r%d-c%d-*." % (
                                row, col) + DEST_TRAIN_EXT)
  img_path = glob.glob(wilcard_path)[0]
  return img_path

def get_training_image_path_name(image_name, large_w=None, large_h=None, small_w=None, small_h=None):
  """
  Convert slide number and optional dimensions to a training image path. If no dimensions are supplied,
  the corresponding file based on the slide number will be looked up in the file system using a wildcard.

  Example:
    5 -> ../data/training_png/TUPAC-TR-005-32x-49920x108288-1560x3384.png

  Args:
    slide_number: The slide number.
    large_w: Large image width.
    large_h: Large image height.
    small_w: Small image width.
    small_h: Small image height.

  Returns:
     Path to the image file.
  """
  
  if large_w is None and large_h is None and small_w is None and small_h is None:
    wildcard_path = os.path.join(".", image_name.rstrip(".svs") + "*." + DEST_TRAIN_EXT)
    img_path = glob.glob(wildcard_path)[0]
  else:
    img_path = os.path.join(".", image_name.rstrip(".svs") + "-" + str(
      SCALE_FACTOR) + "x-" + DEST_TRAIN_SUFFIX + str(
      large_w) + "x" + str(large_h) + "-" + str(small_w) + "x" + str(small_h) + "." + DEST_TRAIN_EXT)
  return img_path






def get_filter_image_path_name(image_name, filter_number, filter_name_info):
  """
  Convert slide number, filter number, and text to a path to a filter image file.

  Example:
    5, 1, "rgb" -> ../data/filter_png/TUPAC-TR-005-001-rgb.png

  Args:
    slide_number: The slide number.
    filter_number: The filter number.
    filter_name_info: Descriptive text describing filter.

  Returns:
    Path to the filter image file.
  """
  dir = FILTER_DIR
  if not os.path.exists(dir):
    os.makedirs(dir)
  img_path = os.path.join(dir, get_filter_image_filename_name(image_name, filter_number, filter_name_info))
  return img_path


def get_filter_image_filename_name(image_name, filter_number, filter_name_info, thumbnail=False):
  """
  Convert slide number, filter number, and text to a filter file name.

  Example:
    5, 1, "rgb", False -> TUPAC-TR-005-001-rgb.png
    5, 1, "rgb", True -> TUPAC-TR-005-001-rgb.jpg

  Args:
    slide_number: The slide number.
    filter_number: The filter number.
    filter_name_info: Descriptive text describing filter.
    thumbnail: If True, produce thumbnail filename.

  Returns:
    The filter image or thumbnail file name.
  """
  if thumbnail:
    ext = THUMBNAIL_EXT
  else:
    ext = DEST_TRAIN_EXT
  padded_fi_num = str(filter_number).zfill(3)
  img_filename = image_name.split("/")[-1] + "-" + padded_fi_num + "-" + FILTER_SUFFIX + filter_name_info + "." + ext
  return img_filename




def get_tile_summary_image_path_name(image_name):
  """
  Convert slide number to a path to a tile summary image file.

  Example:
    5 -> ../data/tile_summary_png/TUPAC-TR-005-tile_summary.png

  Args:
    slide_number: The slide number.

  Returns:
    Path to the tile summary image file.
  """
  if not os.path.exists(TILE_SUMMARY_DIR):
    os.makedirs(TILE_SUMMARY_DIR)
  img_path = os.path.join(TILE_SUMMARY_DIR, get_tile_summary_image_filename_name(image_name))
  return img_path


def get_tile_summary_on_original_image_path_name(image_name):
  """
  Convert slide number to a path to a tile summary on original image file.

  Example:
    5 -> ../data/tile_summary_on_original_png/TUPAC-TR-005-tile_summary.png

  Args:
    slide_number: The slide number.

  Returns:
    Path to the tile summary on original image file.
  """
  if not os.path.exists(TILE_SUMMARY_ON_ORIGINAL_DIR):
    os.makedirs(TILE_SUMMARY_ON_ORIGINAL_DIR)
  img_path = os.path.join(TILE_SUMMARY_ON_ORIGINAL_DIR, get_tile_summary_image_filename_name(image_name))
  return img_path


def get_tile_summary_on_original_thumbnail_path(slide_number):
  """
  Convert slide number to a path to a tile summary on original thumbnail file.

  Example:
    5 -> ../data/tile_summary_on_original_thumbnail_jpg/TUPAC-TR-005-tile_summary.jpg

  Args:
    slide_number: The slide number.

  Returns:
    Path to the tile summary on original thumbnail file.
  """
  if not os.path.exists(TILE_SUMMARY_ON_ORIGINAL_THUMBNAIL_DIR):
    os.makedirs(TILE_SUMMARY_ON_ORIGINAL_THUMBNAIL_DIR)
  img_path = os.path.join(TILE_SUMMARY_ON_ORIGINAL_THUMBNAIL_DIR,
                          get_tile_summary_image_filename(slide_number, thumbnail=True))
  return img_path


def get_top_tiles_on_original_image_path(slide_number):
  """
  Convert slide number to a path to a top tiles on original image file.

  Example:
    5 -> ../data/top_tiles_on_original_png/TUPAC-TR-005-32x-49920x108288-1560x3384-top_tiles.png

  Args:
    slide_number: The slide number.

  Returns:
    Path to the top tiles on original image file.
  """
  if not os.path.exists(TOP_TILES_ON_ORIGINAL_DIR):
    os.makedirs(TOP_TILES_ON_ORIGINAL_DIR)
  img_path = os.path.join(TOP_TILES_ON_ORIGINAL_DIR, get_top_tiles_image_filename(slide_number))
  return img_path


def get_top_tiles_on_original_thumbnail_path(slide_number):
  """
  Convert slide number to a path to a top tiles on original thumbnail file.

  Example:
    5 -> ../data/top_tiles_on_original_thumbnail_jpg/TUPAC-TR-005-32x-49920x108288-1560x3384-top_tiles.jpg

  Args:
    slide_number: The slide number.

  Returns:
    Path to the top tiles on original thumbnail file.
  """
  if not os.path.exists(TOP_TILES_ON_ORIGINAL_THUMBNAIL_DIR):
    os.makedirs(TOP_TILES_ON_ORIGINAL_THUMBNAIL_DIR)
  img_path = os.path.join(TOP_TILES_ON_ORIGINAL_THUMBNAIL_DIR,
                          get_top_tiles_image_filename(slide_number, thumbnail=True))
  return img_path



def get_tile_summary_image_filename_name(image_name, thumbnail=False):
  """
  Convert slide number to a tile summary image file name.

  Example:
    5, False -> TUPAC-TR-005-tile_summary.png
    5, True -> TUPAC-TR-005-tile_summary.jpg

  Args:
    slide_number: The slide number.
    thumbnail: If True, produce thumbnail filename.

  Returns:
    The tile summary image file name.
  """
  if thumbnail:
    ext = THUMBNAIL_EXT
  else:
    ext = DEST_TRAIN_EXT

  training_img_path = get_training_image_path_name(image_name)
  large_w, large_h, small_w, small_h = parse_dimensions_from_image_filename(training_img_path)
  img_filename = image_name.split("/")[-1] + "-" + str(SCALE_FACTOR) + "x-" + str(large_w) + "x" + str(
    large_h) + "-" + str(small_w) + "x" + str(small_h) + "-" + TILE_SUMMARY_SUFFIX + "." + ext

  return img_filename



def get_filter_image_result_name(image_name):
  """
  Convert slide number to the path to the file that is the final result of filtering.

  Example:
    5 -> ../data/filter_png/TUPAC-TR-005-32x-49920x108288-1560x3384-filtered.png

  Args:
    slide_number: The slide number.

  Returns:
    Path to the filter image file.
  """

  training_img_path = get_training_image_path_name(image_name)
  large_w, large_h, small_w, small_h = parse_dimensions_from_image_filename(training_img_path)
  img_path = os.path.join(FILTER_DIR, image_name.split("/")[-1] + "-" + str(
    SCALE_FACTOR) + "x-" + FILTER_SUFFIX + str(large_w) + "x" + str(large_h) + "-" + str(small_w) + "x" + str(
    small_h) + "-" + FILTER_RESULT_TEXT + "." + DEST_TRAIN_EXT)
  return img_path





def parse_dimensions_from_image_filename(filename):
  """
  Parse an image filename to extract the original width and height and the converted width and height.

  Example:
    "TUPAC-TR-011-32x-97103x79079-3034x2471-tile_summary.png" -> (97103, 79079, 3034, 2471)

  Args:
    filename: The image filename.

  Returns:
    Tuple consisting of the original width, original height, the converted width, and the converted height.
  """
  m = re.match(".*-([\d]*)x([\d]*)-([\d]*)x([\d]*).*\..*", filename)
  large_w = int(m.group(1))
  large_h = int(m.group(2))
  small_w = int(m.group(3))
  small_h = int(m.group(4))
  return large_w, large_h, small_w, small_h


def small_to_large_mapping(small_pixel, large_dimensions):
  """
  Map a scaled-down pixel width and height to the corresponding pixel of the original whole-slide image.

  Args:
    small_pixel: The scaled-down width and height.
    large_dimensions: The width and height of the original whole-slide image.

  Returns:
    Tuple consisting of the scaled-up width and height.
  """
  small_x, small_y = small_pixel
  large_w, large_h = large_dimensions
  large_x = round((large_w / SCALE_FACTOR) / math.floor(large_w / SCALE_FACTOR) * (SCALE_FACTOR * small_x))
  large_y = round((large_h / SCALE_FACTOR) / math.floor(large_h / SCALE_FACTOR) * (SCALE_FACTOR * small_y))
  return large_x, large_y


def training_slide_name_to_image(slide_name):
  """
  Convert a WSI training slide to a saved scaled-down image in a format such as jpg or png.

  Args:
    slide_number: The slide number.
  """

  img, large_w, large_h, new_w, new_h = slide_name_to_scaled_pil_image(slide_name)

  img_path = get_training_image_path_name(slide_name, large_w, large_h, new_w, new_h)
  print("Saving image to: " + img_path)
  if not os.path.exists(DEST_TRAIN_DIR):
    os.makedirs(DEST_TRAIN_DIR)
  img.save(img_path)

  # thumbnail_path = get_training_thumbnail_path(slide_number, large_w, large_h, new_w, new_h)
  # save_thumbnail(img, THUMBNAIL_SIZE, thumbnail_path)



def slide_name_to_scaled_pil_image(slide_name):
  """
  Convert a WSI training slide to a scaled-down PIL image.

  Args:
    slide_number: The slide number.

  Returns:
    Tuple consisting of scaled-down PIL image, original width, original height, new width, and new height.
  """
  dir = os.path.join(".",slide_name)
  print("Opening Slide : %s" % (slide_name))
  slide = open_slide(dir)

  large_w, large_h = slide.dimensions
  new_w = math.floor(large_w / SCALE_FACTOR)
  new_h = math.floor(large_h / SCALE_FACTOR)
  level = slide.get_best_level_for_downsample(SCALE_FACTOR)
  whole_slide_image = slide.read_region((0, 0), level, slide.level_dimensions[level])
  whole_slide_image = whole_slide_image.convert("RGB")
  img = whole_slide_image.resize((new_w, new_h), PIL.Image.BILINEAR)
  return img, large_w, large_h, new_w, new_h


def slide_to_scaled_np_image(slide_number):
  """
  Convert a WSI training slide to a scaled-down NumPy image.

  Args:
    slide_number: The slide number.

  Returns:
    Tuple consisting of scaled-down NumPy image, original width, original height, new width, and new height.
  """
  pil_img, large_w, large_h, new_w, new_h = slide_to_scaled_pil_image(slide_number)
  np_img = util.pil_to_np_rgb(pil_img)
  return np_img, large_w, large_h, new_w, new_h



def save_thumbnail(pil_img, size, path, display_path=False):
  """
  Save a thumbnail of a PIL image, specifying the maximum width or height of the thumbnail.

  Args:
    pil_img: The PIL image to save as a thumbnail.
    size:  The maximum width or height of the thumbnail.
    path: The path to the thumbnail.
    display_path: If True, display thumbnail path in console.
  """
  max_size = tuple(round(size * d / max(pil_img.size)) for d in pil_img.size)
  img = pil_img.resize(max_size, PIL.Image.BILINEAR)
  if display_path:
    print("Saving thumbnail to: " + path)
  dir = os.path.dirname(path)
  if dir != '' and not os.path.exists(dir):
    os.makedirs(dir)
  img.save(path)


def get_num_training_slides():
  """
  Obtain the total number of WSI training slide images.

  Returns:
    The total number of WSI training slide images.
  """
  num_training_slides = len(glob.glob1(SRC_TRAIN_DIR, "*." + SRC_TRAIN_EXT))
  return num_training_slides
