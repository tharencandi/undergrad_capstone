from gc import callbacks
import tensorflow as tf
from tensorflow import keras
from keras import layers
#import tensorflow_datasets as tfds
#import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
from cnn_model import * 
import os
from augmentation import augment
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt
from enum import Enum
import keras_tuner as kt

IMG_SIZE = (102, 102)
LBL_SIZE = (54, 54)
EPOCHS = 70
BATCH_SIZE = 32
WEIGHT_INIT = myInitialiers.myHeUniform


class functions(Enum):
    SINGLE_TRAIN = 1
    GRID_SEARCH = 2
    HYPERBAND = 3


FUNC = functions.HYPERBAND

MODEL_SAVE_LOCATION = "data/models/"
MODEL_FILE_NAME = "test_model.model"
TRAIN_LOCATION = "data/NBL"
TEST_LOCATION = "data/NBL_TEST"
CELL_CLASS_WEIGHT = 1
BG_CLASS_WEIGHT = 1
LOG_FILE = "data/models/log.txt"


def save_weights(model, epochs, batch_size, is_preactive, init):
    model.save_weights (
        MODEL_SAVE_LOCATION + 
        f"b{batch_size}_e{epochs}_pre{is_preactive}_w{init}.h5"
    )

def hyper_model_builder(hp):
    model = DRAN()
    hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
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
    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)


    tuner.search(train, epochs=50, validation_data=val, callbacks=[stop_early])

    # Get the optimal hyperparameters
    best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

    print(f"""
    The optimal learning rate for the optimizer
    is {best_hps.get('learning_rate')}.
    """)

def grid_search(epochs, batch_sizes, train_set, val_set, test_set, save=False):
    best_perfomance = 0
    best_para = (None, None)
    log = []
    for b in batch_sizes:
        for e in epochs:
            print("log: ", log)
            print("best_perfomance so far: ", best_perfomance)
            print("best_para so far: ", best_para)
            print("batch size: {}, epochs: {}".format(b, e))
            model = DRAN()

            model.compile(optimizer=keras.optimizers.Adam(),
                                loss="sparse_categorical_crossentropy",
                                metrics=[UpdatedMeanIoU(num_classes=2),])

            model_history = model.fit (
                train_set, 
                batch_size=b, epochs=e, 
                validation_data=val_set, 
                shuffle=True
            )
            
            if save:
                save_weights(model, e, b, PREACTIVE, WEIGHT_INIT)

            result = model.evaluate(test_set)
            mean_iou = result[1]
            print("batch size: {}, epochs: {}, mean iou: {}".format(b, e, mean_iou))
            log.append((b,e,result))
            if mean_iou >= best_perfomance:
                best_perfomance = mean_iou
                best_para = (b, e)
    return best_para, log


def single_train(train, val, test):

    train = train.batch(BATCH_SIZE)
    val = val.batch(BATCH_SIZE)
    test = test.batch(BATCH_SIZE)

    model = DRAN()
    model.compile (
        optimizer=keras.optimizers.Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=[UpdatedMeanIoU(num_classes=2),]
    )
    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
    print("commencing training...")
    model_history = model.fit (
        train, epochs=EPOCHS, validation_data=val, shuffle=True, callbacks=[stop_early]
    )

    result = model.evaluate(test)
    print(f"test set evaluation {result}")

    print("saving weights")
    save_weights(model, EPOCHS, BATCH_SIZE, PREACTIVE, WEIGHT_INIT.name)


def make_graph(log):
    x = [val[0] for val in log]
    y = [val[1] for val in log]
    z = [val[2][1]  for val in log]
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.invert_yaxis()
    surf = ax.plot_trisurf(x, y, z, linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(TRAIN_LOCATION):
    print("train path does not exist.")
    exit(1)
if not os.path.exists(MODEL_SAVE_LOCATION):
	print(f"creating {MODEL_SAVE_LOCATION}")
	os.mkdir(MODEL_SAVE_LOCATION)


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
    val__and_test_dataset = val_and_test_dataset.shuffle(len(v_imgs))

    if percentage_split != 0:
        split = int(percentage_split * (len(v_imgs) / BATCH_SIZE))
        val_dataset = val_and_test_dataset.take(split)
        test_dataset = val_and_test_dataset.skip(split)

        print(f"val and train split is ({len(val_dataset)} | {len(test_dataset)}) elements")
    else:
        val_dataset = val_and_test_dataset
        test_dataset = None

    return train_dataset, val_dataset, test_dataset

def accuracy_plot(history):
    """
    history: history object generated by .fit()
    """
    plt.plot(history.history['updated_mean_io_u'])
    plt.plot(history.history['val_updated_mean_io_u'])
    plt.title('model updated_mean_io_u')
    plt.ylabel('updated_mean_io_u')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

def loss_plot(history):
    """
    history: history object generated by .fit()
    """
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()


def main():
    train, val, test = load_dataset(0.5)

    if FUNC == functions.SINGLE_TRAIN:
        single_train(train, val, test)
    elif FUNC == functions.GRID_SEARCH: 
        print("performing grid search...")
        res = grid_search([30,40,50,60,70], [8,16,32,40], train, val, test, True)
    elif FUNC == functions.HYPERBAND:
        hyperband(train, val)


if __name__ == "__main__":
    main()





