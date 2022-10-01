from slide import *
import tiles
import filter


def single_image_to_folder_of_tiles(image_name = "", cell_threshold = 0, save=False, save_dir = ""):

  ''' 
  Takes svs file, produces folder of rgb png tiles of H/1024 * W/1024 within specified destination folder
  Tiles are appended with _keep or _delete based on specified tissue coverage threshold

  Inputs: filename of svs, folder name for output

  Outputs: filename, number of row and columns of tile (TUPLE)

  E.g. ["cells.svs",(10,10) ]
  '''

  #Choose image number to turn into a scaled down PNG
  training_slide_name_to_image(image_name)

  #applies filters to scaled down image in order to determine tissue coverage of slides.
  filter.apply_filters_to_image_name(image_name)

  # produces and classifies tiles based on tissue coverage
  # produces visual summary of keep/delete in tile_summary folders for manual inspeciton
  tile_summary = tiles.save_above_threshold_name(image_name, display=False, save_summary=True, save_data=False, 
  save_top_tiles=False, threshold=cell_threshold, save=save, directory = save_dir)

  return [tile_summary.image_name, (tile_summary.num_row_tiles, tile_summary.num_col_tiles) ]



