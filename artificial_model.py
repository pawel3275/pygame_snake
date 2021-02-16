import tensorflow as tf
import numpy as np


class ArtificialModel:
    def train_model(self, dataset_train, dataset_train_labels, dataset_test, dataset_test_labels):
        dataset_train_labels = np.asarray(dataset_train_labels).astype('float32').reshape((-1, 1))
        dataset_test_labels = np.asarray(dataset_test_labels).astype('float32').reshape((-1, 1))

        tf.keras.backend.clear_session()
        model = tf.keras.models.Sequential()

        # Dense layers
        model.add(tf.keras.layers.Dense(8, activation="tanh"))
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(42, activation="relu"))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Dense(32, activation="relu"))
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(6, activation="relu"))
        model.add(tf.keras.layers.Dense(4, activation="softmax", name="output_layer"))

        model.compile(optimizer=tf.keras.optimizers.Adam(),
                      loss="sparse_categorical_crossentropy",
                      metrics=['accuracy'])

        model.fit(dataset_train, dataset_train_labels, epochs=30, shuffle=True)

        print("Finished training")
        model.evaluate(x=dataset_test, y=dataset_test_labels, batch_size=128)

        return model

    @staticmethod
    def get_wall_distance_factor(x):
        # Note, for the best usage pass normalized number
        # Returns max value 1 for middle of screen 250 ,250 after normalizing.
        # Return 0 for values close to 0 and 500
        return round((-4 * (x * x)) + (4 * x), 4)
