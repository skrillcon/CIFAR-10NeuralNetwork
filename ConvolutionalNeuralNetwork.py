import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import pickle
import time
import numpy as np

# We're loading in the data from "LoadingInOutsideDataset.py"
X = pickle.load(open("CIFAR_IMAGE_FEATURES.pickle", "rb"))
y = pickle.load(open("CIFAR_LABELS.pickle", "rb"))

# Create a 2D array of all zeros
categoricalY = np.zeros(shape=(y.size, 10))

# Populate the 2D array with the 1s in the right places so we can use categorical crossentropy
index = 0
for i in y:
    categoricalY[index][int(i) - 1] = 1
    index += 1

X = X/255.0 # Scaling image data from 0-255 to 0-1

dense_layers = [1]
dense_layer_sizes = [512]
conv_layer_sizes = [64]
conv_layers = [2]

for dense_layer in dense_layers:
    for conv_layer_size in conv_layer_sizes:
        for conv_layer in conv_layers:
            for dense_layer_size in dense_layer_sizes:
                NAME = "{}-conv-{}-nodes-{}-dense-{}-nodes-{}".format(conv_layer, conv_layer_size, dense_layer,dense_layer_size, int(time.time()))
                tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))
                print(NAME)
                model = Sequential()
                model.add(Conv2D(conv_layer_size, (3,3), input_shape=X.shape[1:])) # Add the type of layer, the window size and then the shape. Remember that the shape is X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1), we want to skip the first value as it is always -1 and was just used to determine how many feature sets there were
                model.add(Activation("relu"))
                model.add(MaxPooling2D(pool_size=(2,2)))
                model.add(Dropout(.3))

                for l in range(conv_layer-1):
                    model.add(Conv2D(conv_layer_size, (3,3))) # input shape is already defined, don't need to add a new one
                    model.add(Activation("relu"))
                    model.add(MaxPooling2D(pool_size=(2,2)))
                    model.add(Dropout(.2))

                model.add(Flatten()) # Make the 2D data 1D

                for l in range(dense_layer):
                    model.add(Dense(dense_layer_size))
                    model.add(Activation("relu"))
                    model.add(Dropout(.5))

                model.add(Dense(10)) # Output layer
                model.add(Activation("softmax"))

                model.compile(loss="sparse_categorical_crossentropy",
                                optimizer="rmsprop",
                                metrics=['sparse_categorical_accuracy'])


                model.fit(X, y, batch_size = 64, epochs=17, validation_split=0.2, callbacks=[tensorboard], shuffle=True)

                model.save("CNN.model")
