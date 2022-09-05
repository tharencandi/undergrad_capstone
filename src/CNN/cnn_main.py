import sys
import os.path
from os import path

import dataset

def main():
    if len(sys.argv) > 2:
        cmd = sys.argv[1]
        folder = sys.argv[2].strip()
        if (folder[-1] != '/'):
            folder += "/"
        if not path.exists(folder):
            os.mkdir(folder)
        if cmd.lower() == "nbl":

            imgs, lbls, comp_labels, v_imgs, v_lbls, v_comp_labels = dataset.load_dataset()
            dataset.gen_NBL((imgs, lbls), folder)
        elif cmd.lower() == "nbd_sn":
            imgs, lbls, comp_labels, v_imgs, v_lbls, v_comp_labels = dataset.load_dataset()
            dataset.gen_NBD_and_SN((imgs, lbls, comp_labels), folder)
        else:
            print("\ndataset not found. specify NBL or NBD_SN.")
        

    else:
        print("\nincorrect use.\npython3 dataset.py (train | test) (NBL | NBD_SN) relative_folder_location")



if __name__ == "__main__":
    main()