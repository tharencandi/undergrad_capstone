from CNN.tile_crop.slide import *
import CNN.tile_crop.tiles as tiles
import CNN.tile_crop.filter as filter

# import tiles
# import filter
# from slide import * 
# import util

import shutil


def single_image_to_folder_of_tiles(image_path = "", cell_threshold = 1, save=True, save_dir = ""):

  ''' 
  Takes svs file, produces folder of rgb png tiles of H/1024 * W/1024 within specified destination folder
  Tiles are appended with _keep or _delete based on specified tissue coverage threshold

  Inputs: filename of svs, folder name for output

  Outputs: 
  [file_name, (rows,cols), (h, w)]

  E.g. ["cells.svs",(10,10), (10240,10240)]
  '''

  #Choose image number to turn into a scaled down PNG
  training_slide_name_to_image(image_path)

  #applies filters to scaled down image in order to determine tissue coverage of slides.
  filter.apply_filters_to_image_name(image_path)

  # produces and classifies tiles based on tissue coverage
  # produces visual summary of keep/delete in tile_summary folders for manual inspeciton
  tile_summary = tiles.save_above_threshold_name(image_path, display=False, save_summary=True, save_data=False, 
  save_top_tiles=False, threshold=cell_threshold, save=save, directory = save_dir)

  svsDir = os.path.join(".","/".join(image_path.split("/")[:-1]))

  #clean up intermediate files
  for item in os.listdir(svsDir):
    if item.endswith(".png"):
          os.remove(os.path.join(svsDir, item))

  #clean up intermediate files
  # shutil.rmtree(FILTER_DIR)
  # for item in os.listdir(DEST_TRAIN_DIR):
  #   if item.endswith(".png"):
  #         os.remove(os.path.join(DEST_TRAIN_DIR, item))
  
  
  return [tile_summary.image_name, (tile_summary.num_row_tiles, tile_summary.num_col_tiles), (tile_summary.orig_h,tile_summary.orig_w) ]



