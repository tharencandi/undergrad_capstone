How to use:
Put images in /src_img and corresponding masks in /src_mask.
Go to augmentation.py and change the value of n in line 201.
The value of n is the number of images in /src_img or /src_mask.
/src_img and /src_mask should have the same amount of pictures.
Make sure /result_img and /result_mask are empty.
Run augmentation.py with python3 and collect results in /result_img and /result_mask.


Naming convention:
Index should always be 4 digits padding with 0s
Index starts with 0000 then 0001, 0002, 0003... and cannot skip numbers
images:                 image0000.png
corresponding mask:     image0000_mask.png
images:                 image0001.png
corresponding mask:     image0001_mask.png
...                     ...

