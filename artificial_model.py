import tensorflow as tf
import numpy as np
from data_collector import DataCollector


class ArtificialModel:
    def __init__(self):
        self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels = self.obtain_train_data()
        self.model = self.train_model(self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels)

    @staticmethod
    def obtain_train_data(path_to_data="D:\\scratch\\snake\\gameDataset_1.csv", should_shuffle_rows=True,
                          label_column_name="action"):
        data = DataCollector.load_data_from_csv_to_data_frame(path_to_data)

        df_train, df_test = DataCollector.split_data_frame_to_train_and_test(data, shuffle_rows=should_shuffle_rows)

        df_train_data, df_train_labels = DataCollector.extract_labels_from_data_frame(df_train,
                                                                                      column_name=label_column_name)
        df_test_data, df_test_labels = DataCollector.extract_labels_from_data_frame(df_test,
                                                                                    column_name=label_column_name)

        df_train_labels = DataCollector.update_labels_to_int_values(df_train_labels)
        df_train_labels = df_train_labels.to_numpy()

        df_test_labels = DataCollector.update_labels_to_int_values(df_test_labels)
        df_test_labels = df_test_labels.to_numpy()

        return df_train_data, df_train_labels, df_test_data, df_test_labels

    @staticmethod
    def train_model(dataset_train, dataset_train_labels, dataset_test, dataset_test_labels):
        dataset_train_labels = np.asarray(dataset_train_labels).astype('float32').reshape((-1, 1))
        dataset_test_labels = np.asarray(dataset_test_labels).astype('float32').reshape((-1, 1))

        dataset_train = np.expand_dims(dataset_train, axis=1)
        dataset_test = np.expand_dims(dataset_test, axis=1)

        tf.keras.backend.clear_session()
        model = tf.keras.models.Sequential()

        # Dense layers
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(42, activation="relu"))
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(6, activation="relu"))
        model.add(tf.keras.layers.Dense(4, activation="softmax", name="output_layer"))

        model.compile(optimizer=tf.keras.optimizers.Adam(),
                      loss="sparse_categorical_crossentropy",
                      metrics=['accuracy'])

        model.fit(dataset_train, dataset_train_labels, epochs=15, shuffle=False)

        print("Finished training")
        model.evaluate(x=dataset_test, y=dataset_test_labels, batch_size=128)

        return model
