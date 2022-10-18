import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras import Model
from keras.regularizers import L2
from enum import Enum

"""
    CNN MODELS - BASIC UNET and DRAN

    TO MAKE:
    MDRAN
"""
PREACTIVE = True
L2_FACTOR = 1e-5

class myInitialiers(Enum):
    myHeNormal = 1
    myHeUniform = 2

# This is a bug fix for the Keras MeanIoU metric 
# From https://stackoverflow.com/questions/61824470/dimensions-mismatch-error-when-using-tf-metrics-meaniou-with-sparsecategorical
class UpdatedMeanIoU(tf.keras.metrics.MeanIoU):
  def __init__(self,
               y_true=None,
               y_pred=None,
               num_classes=None,
               name=None,
               dtype=None):
    super(UpdatedMeanIoU, self).__init__(num_classes = num_classes,name=name, dtype=dtype)

  def update_state(self, y_true, y_pred, sample_weight=None):
    y_pred = tf.math.argmax(y_pred, axis=-1)
    return super().update_state(y_true, y_pred, sample_weight)


#RESNET-50 identity residual block
def identity_block(x, filters,  initialiser=myInitialiers.myHeUniform):

    if initialiser == myInitialiers.myHeNormal:
        initializer = tf.keras.initializers.HeNormal()
    elif initialiser == myInitialiers.myHeUniform:
        initializer = tf.keras.initializers.HeUniform()

    # copy tensor to variable called x_skip
    x_skip = x
    filter_1, filter_2 = filters
    # block 1
    if PREACTIVE:
        x = layers.BatchNormalization(axis=3)(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D( filter_1, (1,1),strides=(1,1), padding = 'valid', kernel_initializer=initializer)(x)
    else:
        x = layers.Conv2D(filter_1, (1,1),strides=(1,1), padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.BatchNormalization(axis=3)(x)
        x = layers.Activation('relu')(x)
    # block 2 - bottleneck (but size kept same with padding)
    if PREACTIVE:
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filter_1, (3, 3), strides=(1, 1), padding='same', kernel_initializer=initializer)(x)
    else:
        x = layers.Conv2D(filter_1, (3, 3), strides=(1, 1), padding='same', kernel_initializer=initializer)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
    # block 3
    x = layers.Conv2D(filter_2, (1,1),strides=(1,1), padding = 'valid', kernel_initializer=initializer)(x)
    x = layers.BatchNormalization(axis=3)(x)
    # Add Residue
    x = layers.Add()([x, x_skip])
    x = layers.Activation('relu')(x)
    return x

def resize(x, size):
    x = layers.UpSampling2D((size//x.shape[1], size //x.shape[2]), interpolation='nearest')(x)
    
    return x

# DRAN decoder unit
# All the convolution operations in the decoder use no padding and a stride 1
def decoder(x, decoder_num, initialiser=myInitialiers.myHeUniform):

    if initialiser == myInitialiers.myHeNormal:
        initializer = tf.keras.initializers.HeNormal()
    elif initialiser == myInitialiers.myHeUniform:
        initializer = tf.keras.initializers.HeUniform()

    if decoder_num == 1:
        x = layers.Conv2D(256, (5,5), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(256, (3,3), groups=64, strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(128, (1,1), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
    elif decoder_num == 2:
        x = layers.Conv2D(512, (5,5), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(512, (3,3), groups=128, strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(256, (1,1), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
    elif decoder_num == 3:
        x = layers.Conv2D(1024, (5,5), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(1024, (3,3), groups=256, strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.Conv2D(512, (1,1), strides = 1, padding = 'valid', kernel_initializer=initializer)(x)
    
    #for the MDRAN
    elif decoder_num == 4:
        #"We note that decoder4 uses padding convolution"
        x = layers.Conv2D(128, (5,5), padding='same', strides=1, kernel_initializer=initializer)(x)
        print(x.shape)
        x = layers.Conv2D(256, (3,3),padding='same',strides=1,groups=64, kernel_initializer=initializer)(x)
        print(x.shape)
        x = layers.Conv2D(256, (1,1), strides=1, padding = 'same', kernel_initializer=initializer)(x)
        print(x.shape)
    return x
 

 # Convolution residual block for RESNET-50
 # NOT pre-activated resnet
def convolutional_block(x,s, filters, initialiser=myInitialiers.myHeUniform):

    if initialiser == myInitialiers.myHeNormal:
        initializer = tf.keras.initializers.HeNormal()
    elif initialiser == myInitialiers.myHeUniform:
        initializer = tf.keras.initializers.HeUniform()

    # copy tensor to variable called x_skip
    x_skip = x
    filter_1, filter_2 = filters
    # block 1
    if PREACTIVE:
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filter_1, (1,1), strides=(s, s), padding = 'valid', kernel_initializer=initializer)(x)
    else:
        x = layers.Conv2D(filter_1, (1,1), strides=(s, s), padding = 'valid', kernel_initializer=initializer)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
    # block 2
    if PREACTIVE:
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filter_1, (3,3), strides=(1,1), padding = 'same', kernel_initializer=initializer)(x)
    else:
        x = layers.Conv2D(filter_1, (3,3), strides=(1,1), padding = 'same', kernel_initializer=initializer)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
    # block 3
    x = layers.Conv2D(filter_2, (1,1), strides = (1,1), padding="valid", kernel_initializer=initializer)(x)
    x = layers.BatchNormalization()(x)
    x_skip = layers.Conv2D(filter_2, (1,1), strides=(s,s), padding = "valid", kernel_initializer=initializer)(x_skip)
    x_skip = layers.BatchNormalization()(x_skip)
    # Add Residue
    x = layers.Add()([x, x_skip])
    x = layers.Activation('relu')(x)
    return x


#https://www.tensorflow.org/tutorials/images/segmentation#optional_imbalanced_classes_and_class_weights
def add_sample_weights(image, label, weights_ls):
  # The weights for each class, with the constraint that:
  # sum(class_weights) == 1.0
  class_weights = tf.constant(weights_ls)
  class_weights = class_weights/tf.reduce_sum(class_weights)

  # Create an image of `sample_weights` by using the label at each pixel as an 
  # index into the `class weights` .
  sample_weights = tf.gather(class_weights, indices=tf.cast(label, tf.int32))

  return image, label, sample_weights


# modified from resnet34 from link
# implementing DRAN - uses modified pre-activated RESNET for contracting path (from article we have data from)

# resnet34: https://www.analyticsvidhya.com/blog/2021/08/how-to-code-your-resnet-from-scratch-in-tensorflow/#h2_9 
def DRAN(shape = (102, 102, 3), classes = 2, initialiser=myInitialiers.myHeUniform) -> Model:
    # Step 1 (Setup Input Layer)
    x_input = tf.keras.layers.Input(shape)
    #x = layers.ZeroPadding2D((3, 3))(x_input)
    x= x_input
    #modified pre-activated res-net used for contracting layers

    if initialiser == myInitialiers.myHeNormal:
        initializer = tf.keras.initializers.HeNormal()
    elif initialiser == myInitialiers.myHeUniform:
        initializer = tf.keras.initializers.HeUniform()

    # Initial Conv layer
    #  modified pre-activated resnet: NO maxPool, stride 1 NO PADDING
    # batch -> relu -> conv 
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation('relu')(x)
    x = tf.keras.layers.Conv2D(64, kernel_size=7, strides=1, padding='valid', kernel_initializer=initializer)(x)
    
   
    # Define size of sub-blocks and initial filter size (es-net 50s)
    block_layers = [3, 4, 6, 3]
    filters = (64, 256)
    connections = []

    # Add the Resnet Blocks
    for i in range(len(block_layers)):
        # One Residual/Convolutional Block followed by Identity blocks
        # The filter size will go on increasing by a factor of 2

        #strides = 1
        if i == 0:
            x = convolutional_block(x, 1, filters)
            x = identity_block(x, filters)
            x = identity_block(x, filters)
        else:
            x = convolutional_block(x, 2, filters)
            for j in range(block_layers[i] - 1):
                x = identity_block(x, filters)

        
        connections.append(x)

        filters = (filters[0]*2, filters[1]*2)

    #decoding layers

    #decoder 4 = convolution transpose 2x2, 1024, stride 2
    connections.reverse()

    x = layers.Conv2DTranspose(1024, (2,2), strides=2)(connections[0])
    

    #decoder 3 and 2 = contracting + last decode -> batch -> relu -> decode -> resize
    x = layers.Add()([x, connections[1]])
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = decoder(x, 3)
    x = resize(x, 36)

    
    cropped = layers.Cropping2D(cropping=6)(connections[2])
    x = layers.Add()([x, cropped])
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = decoder(x, 2)
    x = resize(x, 60)

    #decoder 1 = batch -> relu -> decode -> batch -> relu
    cropped = layers.Cropping2D(cropping=18)(connections[3])
    x = layers.Add()([x, cropped])
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = decoder(x, 1)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)


    #final output - 1x1, 2, softmax
    x = layers.Conv2D(2, (1,1), activation="softmax", kernel_initializer=initializer)(x)
    
    model = tf.keras.models.Model(inputs = x_input, outputs = x, name = "dran")
    return model

def save_default_model():
    model = DRAN()
    model.compile(optimizer=keras.optimizers.Adam(),
                            loss="sparse_categorical_crossentropy",
                            metrics=[UpdatedMeanIoU(num_classes=2),])
    model_config = model.to_json()
    with open("data/models/default_DRAN.json", "w") as f:
        f.write(model_config)
    


if __name__ == "__main__":
    save_default_model()