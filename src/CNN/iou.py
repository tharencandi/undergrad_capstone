import numpy as np

def get_iou(mask, true_mask):
    if mask.shape != true_mask.shape:
        return -1
    intersection = 0
    union =  0
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i,j,0] != 0 and true_mask[i,j,0] != 0:
                intersection += 1
            if mask[i,j,0] != 0 or true_mask[i,j,0] != 0:
                union += 1
    return intersection/union