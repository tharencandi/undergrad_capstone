import sys
import os.path
from os import path
import src.CNN.dataset as dataset

"""
    Run various functions of the CNN src code.

    Current functionality is limited to dataset creation.

    TO DO: add prediction

"""
def main():
    if len(sys.argv) > 3:

        function = sys.argv[1] #train or test
        dataset_type = sys.argv[2] 
        folder = sys.argv[3].strip()
        if (folder[-1] != '/'):
            folder += "/"
        if not path.exists(folder):
            os.mkdir(folder)

        if dataset_type.lower() == "nbl":

            imgs, lbls, comp_labels, v_imgs, v_lbls, v_comp_labels = dataset.load_dataset()
            if function == "train":
                dataset.gen_NBL((imgs, lbls), folder)
            elif function == "test":
                dataset.gen_NBL((v_imgs, v_lbls), folder)
            else:
                print("\nincorrect use.\npython3 dataset.py (train | test) (NBL | NBD_SN) relative_folder_location")
        elif dataset_type.lower() == "nbd_sn":
            imgs, lbls, comp_labels, v_imgs, v_lbls, v_comp_labels = dataset.load_dataset()
           

            if function == "train":
                dataset.gen_NBD_and_SN((imgs, lbls, comp_labels), folder)
            elif function == "test":
                dataset.gen_NBD_and_SN((v_imgs, v_lbls, v_comp_labels), folder)
            else:
                print("\nincorrect use.\npython3 dataset.py (train | test) (NBL | NBD_SN) relative_folder_location")
        else:
            print("\ndataset not found. specify NBL or NBD_SN.")
        

    else:
        print("\nincorrect use.\npython3 dataset.py (train | test) (NBL | NBD_SN) relative_folder_location")



if __name__ == "__main__":
    main()