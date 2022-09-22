import unittest
from tile_crop_main import *

#To remove unnecessary IBM code see index.html of the coverage report and delete unused lines
#To re-run coverage, pip3 install coverage, run "coverage run -m --source= tile_crop_test" then "coverage html" and open the report

class Test(unittest.TestCase):

    #Runs function without saving files, save=False
    def test_return(self):
        self.assertEqual(multiple_images_to_folders_of_labelled_png([1], 100, save=False), [[1,(18,16)]])

if __name__ == '__main__':
    unittest.main()