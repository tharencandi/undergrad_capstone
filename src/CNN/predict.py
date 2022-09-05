import cv2 as cv
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cnn_model

IMG_SIZE = (102, 102)
# hacky script to see result




model = tf.keras.models.load_model('data/models/model_76', custom_objects = {"UpdatedMeanIoU": cnn_model.UpdatedMeanIoU})
model.load_weights('data/models/new_weights.h5')

for i in range(1,18):
   
    img = cv.imread("data/validation/image{:02d}.png".format(i))
    img = img[0:200,0:200]
    
    s_img = cv.resize(img, IMG_SIZE)

    T = np.float32([[1, 0, -(100-(54//2))], [0, 1, -(100-(54//2))]])
    img = cv.warpAffine(img, T, (54,54))
    
    n_img = np.reshape(s_img, (-1, 102, 102, 3)) 
    
    #d = tf.data.Dataset.from_tensor_slices([s_img])
    #d = d.batch(1)
    mask = model.predict(n_img)
    print(n_img.shape)
    mask = mask[0]

    mask_img = np.zeros((54, 54))

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            
            if mask[y][x][1] > mask[y][x][0]:
                mask_img[y][x] = 255
            else:
                mask_img[y,x] = 0
            

    mask_large = cv.resize(mask_img,(img.shape[1], img.shape[0]))
    #a,b = dataset.decode_label("data/NBL/image0003_mask.txt")
    true_mask =  cv.imread("data/validation/image{:02d}_mask.png".format(i))
    
    T = np.float32([[1, 0, -((100)-(54//2))], [0, 1, -((100)-(54//2))]])
    true_mask = cv.warpAffine(true_mask, T, (54,54))


    mask_large = cv.cvtColor(np.float32(mask_large),cv.COLOR_GRAY2RGB)
    vis = np.concatenate((img, true_mask, mask_large), axis=1)
    vis = cv.resize(vis, (vis.shape[1]*4, vis.shape[0]*4))
    cv.imwrite(f'data/results/out{i}.png', vis)
 