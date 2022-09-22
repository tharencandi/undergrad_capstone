from slide import *
import tiles
import filter


#Please note the below formatting and input assumptions

# .svs images must be placed in /data/training_slides 
# .svs images must follow naming convention e.g. CELLCIRC-001.svs
# To change this, update PREFIX macro in slide.py
# output of .png tiles are located in data/tiles_png/"imageNumber"/
# if tissue proportion of slide threshold above x, _keep added to filename, else _delete


def single_image_to_folder_of_labelled_png(image_numbers = [1], cell_threshold = 0, save=False):

  ''' 
  Takes list of svs image numbers, produces corresponding folders containing tiles of H/SCALE_FACTOR * W/SCALE_FACTOR
  Tiles are appended with _keep or _delete based on specified tissue coverage threshold

  Inputs: list of image numbers corresponding to svs naming convention 
  e.g. [1,2] == [CELLCIRC-001.svs,CELLCIRC-002.svs] 

  Outputs: tile_directory (STR), number of row and columns of tiles (TUPLE)

  E.g. ["./data/tiles_png/001/CELLCIRC-001-tile-r10-c2-x1025-y9228-w1024-h1024_delete.png",(10,10) ]
  to change SCALE_FACTOR: update this macro in slide.py

  '''

  #Choose image number to turn into a scaled down PNG
  for image_number in image_numbers:
    training_slide_to_image(image_number)

  #converts all svs in training folder to png
  multiprocess_training_slides_to_images()

  #applies filters to scaled down image in order to more accurately determine tissue coverage of slides.
  filter.multiprocess_apply_filters_to_images(image_num_list = image_numbers)

  # produces and classifies tiles based on tissue coverage
  slide_dict_results = tiles.multiprocess_filtered_images_to_tiles_threshold(image_num_list = image_numbers,threshold = cell_threshold, save=save)

  #summary is a dict
  result_list = list()
 
  for slide_number,slide_summary in slide_dict_results.items():
    result_list.append([slide_number,(slide_summary.num_row_tiles,slide_summary.num_col_tiles)] )
  
  return result_list



