from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
import numpy as np

class ArtificialModel:
    def train_model(self, dataset_train, dataset_train_labels, dataset_test, dataset_test_labels):
        # Dirty non working model for now

        dataset_train_labels = np.asarray(dataset_train_labels).astype('float32').reshape((-1, 1))
        # dataset_test_labels = np.asarray(dataset_test_labels).astype('float32').reshape((-1, 1))

        print(dataset_train.shape[0], dataset_train.shape[1])
        model = Sequential()
        model.add(Dense(128, activation="relu"))
        model.add(Dense(96, activation="relu"))
        model.add(Dense(40, activation="relu"))
        model.add(Dense(26, activation="relu"))
        model.add(Dense(14, activation="relu"))
        model.add(Dense(4, activation="softmax"))

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.BinaryCrossentropy(),
                      metrics=['accuracy'])

        model.fit(dataset_train, dataset_train_labels, epochs=20)
