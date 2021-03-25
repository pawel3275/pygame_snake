import os

import tensorflow as tf
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as func

from data_collector import DataCollector


class ArtificialModel:
    def __init__(self, data_set_path):
        """
        Default constructor. Loads data set train and tast from given csv file path and provides prediction model.
        :param data_set_path: File path to the csv file with data set.
        """
        self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels = self.obtain_train_data(
            data_set_path)
        self.model = self.train_model(self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels)

    @staticmethod
    def obtain_train_data(path_to_data, should_shuffle_rows=True, label_column_name="action"):
        """
        Loads data to train and test data sets. After loading it splits loaded data to: train data set, train labels,
        test data set, test labels.
        :param path_to_data: Path to the csv file from which data will be obtained.
        :param should_shuffle_rows: Boolean value determining whether we should shuffle rows before data split.
        :param label_column_name: Name of the csv column that contains the labels.
        :return: Data frame objects for: train data set, train labels, test data set, test labels.
        """
        data = DataCollector.load_data_from_csv_to_data_frame(path_to_data)

        df_train, df_test = DataCollector.split_data_frame_to_train_and_test(data, shuffle_rows=should_shuffle_rows)

        df_train_data, df_train_labels = DataCollector.extract_labels_from_data_frame(
            df_train,
            column_name=label_column_name
        )
        df_test_data, df_test_labels = DataCollector.extract_labels_from_data_frame(
            df_test,
            column_name=label_column_name
        )

        df_train_labels = df_train_labels.to_numpy()

        df_test_labels = df_test_labels.to_numpy()

        return (df_train_data, df_train_labels, df_test_data, df_test_labels)

    @staticmethod
    def train_model(dataset_train, dataset_train_labels, dataset_test, dataset_test_labels):
        """
        Trains model using given data sets for train and testing.
        :param dataset_train: Train data set data frame.
        :param dataset_train_labels: Data frame containing labels.
        :param dataset_test: Test data set data frame.
        :param dataset_test_labels: Data frame containing test labels
        :return: trained model
        """
        dataset_train_labels = np.asarray(dataset_train_labels).astype('float32').reshape((-1, 1))
        dataset_test_labels = np.asarray(dataset_test_labels).astype('float32').reshape((-1, 1))

        dataset_train = np.expand_dims(dataset_train, axis=1)
        dataset_test = np.expand_dims(dataset_test, axis=1)
        print(dataset_train.shape)
        tf.keras.backend.clear_session()
        model = tf.keras.models.Sequential()

        # Dense layers
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(42, activation="relu"))
        model.add(tf.keras.layers.Dense(18, activation="relu"))
        model.add(tf.keras.layers.Dense(6, activation="relu"))
        model.add(tf.keras.layers.Dense(4, activation="softmax", name="output_layer"))

        model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss="sparse_categorical_crossentropy",
            metrics=['accuracy']
        )

        model.fit(dataset_train, dataset_train_labels, epochs=15, shuffle=False)

        print("Finished training")
        model.evaluate(x=dataset_test, y=dataset_test_labels, batch_size=128)

        return model


class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        Default constructor for reinforced learning.
        :param input_size: Input size for the first neural network layer.
        :param hidden_size: Size for the first and only hidden layer.
        :param output_size: Output layer size.
        """
        super().__init__()
        self.linear_1 = nn.Linear(input_size, hidden_size)
        self.linear_2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Constructs relu linear hidden later with a given size.
        :param x: Size for the linear later.
        :return: layer
        """
        x = func.relu(self.linear_1(x))
        x = self.linear_2(x)
        return x

    def save(self, file_name="model.pth"):
        """
        Saves trained model in a given path.
        :param file_name: File name for the trained model to be saved as.
        """
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        """
        Default constructor for the reinforced learning trainer object. The main purpose of this object is to perform
        training step to adjust weights accordingly to the given game step on a short and long term memory.
        :param model: Model on which training shall be performed
        :param learning_rate: Learning rate
        :param gamma: Gamma parameter to be used in bellman equation.
        """
        self.lr = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, new_state, game_ended):
        """
        Performs weights adjustments accordingly to the given states as the input parameters and performs action
        calculation to get the most valuable action, that will revolt in a highest possible reward.
        :param state: Current game state with the distances from the head.
        :param action: Performed action in a current state of the game.
        :param reward: Reward value by the given action and game state.
        :param new_state: New state of the game with the distances from the head.
        :param game_ended: Boolean value determining if the game has ended or not,
        """
        if type(action) != tuple:
            movements = [0, 0, 0, 0]
            movements[action] = 1
            action = movements
        state = torch.tensor(state, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # reshape to (1, size)
            state = torch.unsqueeze(state, 0)
            new_state = torch.unsqueeze(new_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_ended = (game_ended,)

        # Bellman equation:
        prediction = self.model(state)  # current state

        target = prediction.clone()  # Q_new
        for index in range(len(game_ended)):
            q_new = reward[index]
            if not game_ended[index]:
                q_new = reward[index] + self.gamma * torch.max(self.model(new_state[index]))

            target[index][torch.argmax(action[index]).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()
