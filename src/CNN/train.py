from distutils.log import Log
from gc import callbacks
import tensorflow as tf
from tensorflow import keras
from keras import layers
#import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import os
import sys
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt
from enum import Enum
import keras_tuner as kt

cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))

from CNN.augmentation import augment
from CNN.cnn_model import * 
"""
    DO NOT MODIFY
"""
IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)

class functions(Enum):
    SINGLE_TRAIN = 1
    GRID_SEARCH = 2
    HYPERBAND = 3
# _______________________________________________#

"""
    paramaters for grid and single train.
"""
LEARNING_RATE = 1e-4
VAL_TEST_SPLIT = 0.5
ES_PATIENCE = 20
LR_PATIENCE = 8
LR_FACTOR = 0.1
MIN_LR = 1e-6
WEIGHT_INIT = myInitialiers.myHeNormal
CELL_CLASS_WEIGHT = 1
BG_CLASS_WEIGHT = 1

"""
    paramaters for single train and hyperband search. 
"""
EPOCHS = 100
BATCH_SIZE = 16


"""
    I/O config
"""
MODEL_SAVE_LOCATION = "data/models"
MODEL_FILE_NAME = "test_model.model"
TRAIN_LOCATION = "data/NBL"
TEST_LOCATION = "data/NBL_test"
LOG_DIR = "data/models/log"

"""
    example output file name 
    f"/b_10_e50_preTrue_wheNorm_le0.001(_extra_meta_data).extension"
    leave blank if not wanted.
"""
OUTPUT_FILES_NAME_MODIFIER = "extra_meta_data"


FUNC = functions.SINGLE_TRAIN

if not os.path.exists(LOG_DIR):
    try: 
        os.mkdir(LOG_DIR)
    except FileExistsError:
        print(f"error creating {LOG_DIR} parent folder does not exist.")
        exit(0)
if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(MODEL_SAVE_LOCATION):
	print(f"creating {MODEL_SAVE_LOCATION}")
	os.mkdir(MODEL_SAVE_LOCATION)


def save_weights(model, epochs, batch_size, is_preactive, init):
    base_name = f"/b_{batch_size}_e{epochs}_pre{is_preactive}_w{init}_le{LEARNING_RATE}"
    if OUTPUT_FILES_NAME_MODIFIER != "":
        base_name += "_" + OUTPUT_FILES_NAME_MODIFIER
    model.save_weights (
        MODEL_SAVE_LOCATION + base_name + ".h5"
    )

def hyper_model_builder(hp):
   
    hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
    hp_weight_init = hp.Choice('inititial_weights', values=[myInitialiers.myHeNormal.value, myInitialiers.myHeUniform.value])
    model = DRAN(initialiser=myInitialiers(hp_weight_init))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                                loss="sparse_categorical_crossentropy",
                                metrics=[UpdatedMeanIoU(num_classes=2),])
    return model

def hyperband(train, val):
    train = train.batch(BATCH_SIZE)
    val = val.batch(BATCH_SIZE)
    tuner = kt.Hyperband(hyper_model_builder,
                        objective=kt.Objective("val_updated_mean_io_u", direction="max"),
                        max_epochs=70,
                        factor=3,
                        directory='my_dir',
                        project_name='intro_to_kt')

    #stop early if validation set loss too high
    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=ES_PATIENCE)


    tuner.search(train, epochs=50, validation_data=val, callbacks=[stop_early])

    # Get the optimal hyperparameters
    best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

    print(f"""
    The optimal learning rate for the optimizer
    is {best_hps.get('learning_rate')}.
    """)

def grid_search(epochs, batch_sizes, train_set, val_set, test_set, save=False, evaluate_on_every_epoch=False, early_stopping=False):
    """
        trains all combinations of epochs and batch sizes and logs all information, and records "best" combination.

        (highest miou of test set.)

        configure early stopping with earlyStopping = True, and patience = x
    """
    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=ES_PATIENCE, restore_best_weights=True, verbose=1)
    
    best_perfomance = 0
    best_para = (None, None)
    log = "b,e,result\n"
    dic_model_history = {}
    for b in batch_sizes:
        train = train_set.batch(b)
        va  = val_set.batch(b)
        test = test_set.batch(b)

        for e in epochs:
            print("log: ", log)
            print("best_perfomance so far: ", best_perfomance)
            print("best_para so far: ", best_para)
            print("batch size: {}, epochs: {}".format(b, e))
            
            model = DRAN(initialiser=WEIGHT_INIT)

            
            model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                            loss="sparse_categorical_crossentropy",
                            metrics=[UpdatedMeanIoU(num_classes=2),])


            if early_stopping:
                model_history = model.fit (
                    train, 
                    epochs=e, 
                    validation_data=va, 
                    shuffle=True, 
                    callbacks=[stop_early]
                )
            else:
                model_history = model.fit (
                    train, 
                    epochs=e, 
                    validation_data=va, 
                    shuffle=True, 
                    callbacks=[stop_early]
                )

            
            if save:
                save_weights(model, e, b, PREACTIVE, WEIGHT_INIT)
            
            for key, val in model_history.history.items():
                if 'val_updated_mean_io_u' in key:
                    val_updated_mean_io_u = val
            dic_model_history["b{}e{}".format(b, e)] = model_history

            result = model.evaluate(test)
            mean_iou = result[1]
            print("batch size: {}, epochs: {}, mean iou: {}".format(b, e, mean_iou))
            log += f"{b},{e},{result}\n"
            #log.append((b,e,result,model_history.history))

            if evaluate_on_every_epoch:
                best_same_batch = max(val_updated_mean_io_u)
                best_epoch_same_batch = val_updated_mean_io_u.index(best_same_batch)+1

                if best_same_batch >= best_perfomance:
                    best_perfomance = best_same_batch
                    best_para = (b, best_epoch_same_batch)
            else:
                if mean_iou >= best_perfomance:
                    best_perfomance = mean_iou
                    best_para = (b, e)
    return best_para, log, dic_model_history


def single_train(train, val, test):

    train = train.batch(BATCH_SIZE)
    val = val.batch(BATCH_SIZE)
    test = test.batch(BATCH_SIZE)

    model = DRAN(initialiser=WEIGHT_INIT)
    model.compile (
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="sparse_categorical_crossentropy",
        metrics=[UpdatedMeanIoU(num_classes=2),]
    )
    

    # Model weights are saved at the end of every epoch, if it's the best seen
    # so far.
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=MODEL_SAVE_LOCATION + "/checkpoint",
        save_weights_only=True,
        monitor='val_updated_mean_io_u',
        mode='max',
        save_best_only=True
    )

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOG_DIR)
    
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=LR_FACTOR,
                              patience=LR_PATIENCE, min_lr=MIN_LR)
    
    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=ES_PATIENCE, restore_best_weights=True, verbose=1)
    
    
    print("commencing training...")
    model_history = model.fit (
        train, epochs=EPOCHS, validation_data=val, shuffle=True, callbacks=[reduce_lr,stop_early, tensorboard_callback,model_checkpoint_callback])
    
    
    result = model.evaluate(test)
    print(f"test set evaluation {result}")

    print("saving weights")
    save_weights(model, EPOCHS, BATCH_SIZE, PREACTIVE, WEIGHT_INIT.name)

    base_name = f"/b_{BATCH_SIZE}_e{EPOCHS}_pre{PREACTIVE}_w{WEIGHT_INIT}_le{LEARNING_RATE}"
    if OUTPUT_FILES_NAME_MODIFIER != "":
        base_name += "_" + OUTPUT_FILES_NAME_MODIFIER
    name += '.log'
    with open(LOG_DIR + name, "w") as l:    
        l.write(str(model_history.history))


def load_dataset(percentage_split):
    """
        loads datasets. location of train and test images 
        are from TRAIN_LOCATION and TEST_LOCATION.

        if percentage split is a value (0,1) then it will split
        the validation set into val and test sets (shuffled first).
        else, test set returned is None

        returns tensorflow datasets: train, val, test

        all datasets have:
        - shuffling applied
        - batch size BATCH_SIZE
        - weights [BG_CLASS_WEIGHTS, FG_CLASS_WEIGHTS]
    """


    if not (percentage_split > 0 and percentage_split < 1):
        percentage_split = 0

    print("loading dataset...")
    imgs = []
    masks = []
    num_train = sum('mask' in s for s in os.listdir(TRAIN_LOCATION)) 
    num_test = sum('mask' in s for s in os.listdir(TEST_LOCATION)) 
    imgs, masks = augment(TRAIN_LOCATION, TRAIN_LOCATION, num_train)
    v_imgs, v_masks = augment(TEST_LOCATION, TEST_LOCATION, num_test)

    print("converting to tf dataset...")
    imgs = np.array(imgs)
    masks = np.array(masks)
    v_imgs = np.array(v_imgs)
    v_masks = np.array(v_masks)

    print("train images", len(imgs), imgs.shape)
    print("train masks", len(masks), masks.shape)
    print("validation images", len(v_imgs), v_imgs.shape)
    print("validation masks", len(v_masks), v_masks.shape)

    imgs,masks,weights = add_sample_weights(imgs,masks,[BG_CLASS_WEIGHT,CELL_CLASS_WEIGHT])

    train_dataset = tf.data.Dataset.from_tensor_slices((imgs, masks, weights))
    train_dataset = train_dataset.shuffle(len(imgs))
    val_and_test_dataset = tf.data.Dataset.from_tensor_slices((v_imgs, v_masks))
    val_and_test_dataset = val_and_test_dataset.shuffle(len(v_imgs))

    if percentage_split != 0:
        split = int(percentage_split * (len(v_imgs) / BATCH_SIZE))
        val_dataset = val_and_test_dataset.take(split)
        test_dataset = val_and_test_dataset.skip(split)

        print(f"val and train split is ({len(val_dataset)} | {len(test_dataset)}) elements")
    else:
        val_dataset = val_and_test_dataset
        test_dataset = None

    return train_dataset, val_dataset, test_dataset

def accuracy_plot(history,title, save=False, show=True):
    """
    history: History object generated by .fit()
    """
    for k,v in history.history.items(): 
        if k.startswith('updated_mean_io_u'):
            updated_mean_io_u = v
    for k,v in history.history.items(): 
        if k.startswith('val_updated_mean_io_u'):
            val_updated_mean_io_u = v
    plt.plot(updated_mean_io_u)
    plt.plot(val_updated_mean_io_u)
    plt.title(title)
    plt.ylabel('updated_mean_io_u')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    if show:
        plt.show()
    if save:
        plt.savefig(f"{LOG_DIR}/{title}")


def loss_plot(history, title, save=False, show=True):
    """
    history: History object generated by .fit()
    """
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title(title)
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    if show:
        plt.show()
    if save:
        plt.savefig(f"{LOG_DIR}/{title}")
        
def gen_plots_for_histories(hist_dict):
    for key in hist_dict:
        base_title = f"{key}_pre{PREACTIVE}_w{WEIGHT_INIT.name}_lr{LEARNING_RATE}"
        acc_title = base_title + "_ACC.png"
        loss_title = base_title + "_LOSS.png"
        accuracy_plot(hist_dict[key], acc_title, save=True, show=False)
        loss_plot(hist_dict[key], loss_title, save=True, show=False)

def main():

    print("\n\n---\n\tcurrently executing: ", FUNC, ".\n\tIf this was not intended please change the constant FUNC.\n---\n\n")
    
    if not os.path.exists(MODEL_SAVE_LOCATION):
        try:
            os.mkdir(MODEL_SAVE_LOCATION)
        except FileNotFoundError:
            print(f"parent directory in {MODEL_SAVE_LOCATION} does not exist. Cannot create folder")
            exit(1)

    train, val, test = load_dataset(VAL_TEST_SPLIT)

    if FUNC == functions.SINGLE_TRAIN:
        single_train(train, val, test)
    elif FUNC == functions.GRID_SEARCH: 
        print("performing grid search...")
        best, log, hist_dict = grid_search([70], [8,16,32,40], train, val, test, save=False, evaluate_on_every_epoch=True)
        for key in hist_dict:
            base = f"{key}_pre{PREACTIVE}_w{WEIGHT_INIT.name}_lr{LEARNING_RATE}"
            if OUTPUT_FILES_NAME_MODIFIER != "":
                base += "_" + OUTPUT_FILES_NAME_MODIFIER
            with open(f"{LOG_DIR}/{base}.log", "w") as log_file:
                log_file.write(hist_dict[key])

    elif FUNC == functions.HYPERBAND:
        hyperband(train, val)


if __name__ == "__main__":
    main()





