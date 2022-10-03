from predict import predict_image, val_mask_to_bin
from iou import get_iou
import cv2 as cv
import numpy as np
import os


"""
model and model weights used defined at top of predict.py
"""
def predict_validation_set(n, save_location):
    iou_sum = 0
    out_str = "iou,\n"
    count = 0

    if not os.path.isdir(save_location):
        print(f"making save directory: {save_location}")
        os.mkdir(save_location)
    
    for i in range(1,n+1):
        img = cv.imread("data/validation/image{:02d}.png".format(i))
    
        mask = predict_image(img)
        mask= cv.cvtColor(np.float32(mask),cv.COLOR_GRAY2RGB)
        true_mask =  cv.imread("data/validation/image{:02d}_mask.png".format(i))
        true_mask = val_mask_to_bin(true_mask)

        vis = np.concatenate((img, true_mask, mask), axis=1)
        cv.imwrite(f'{save_location}/out_combined_{i}.png', vis)
        print(f"\nResult saved as out_combined_{i}.png in {save_location}!\n")
        
        accuracy = get_iou(mask, true_mask)
        iou_sum += accuracy*100
        out_str += str(accuracy) + ",\n"
        count += 1

    f = open(f"{save_location}/results.csv", "w")
    f.write(out_str)
    f.close()
    print("mean iou: " + str(iou_sum / count))

if __name__ == "__main__":
    predict_validation_set(18, "data/results")