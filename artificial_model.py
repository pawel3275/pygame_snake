from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


class ArtificialModel:
    def train_model(self, dataset_train, dataset_train_labels, dataset_test, dataset_test_labels):
        # Dirty non working model for now
        model = Sequential()
        model.add(Dense(128, activation="relu", input_shape=(dataset_train.shape[0], dataset_train.shape[1])))
        model.add(Dense(96))
        model.add(Dense(52))
        model.add(Dense(4))
        model.compile(optimizer='adam', loss='mse')

        model.fit(dataset_train, dataset_test_labels, epochs=20, verbose=0)
