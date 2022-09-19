from slide import *
import util
import sys
import tiles
import filter

#.svs images must follow naming convention seen in /data/training_slides
#output of .png tiles are located in data/tiles_png/"imageNumber"
#if threshold above x, _keep added to filename, else _delete

if __name__ == "__main__":
  # show_slide(1)
  # slide_info(display_all_properties=True)
  # slide_stats()

  training_slide_to_image(1)
  img_path = get_training_image_path(1)
  img = open_image(img_path)
  img.show()

  slide_to_scaled_pil_image(1)[0].show()
  singleprocess_training_slides_to_images()
  multiprocess_training_slides_to_images()
  filter.singleprocess_apply_filters_to_images()
  tiles.singleprocess_filtered_images_to_tiles_2(image_num_list = [1])
  #tiles.summary_and_tiles(1, display=True, save_summary=True, save_data=False, save_top_tiles=True)