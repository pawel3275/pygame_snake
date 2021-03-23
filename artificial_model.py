import tensorflow as tf
import numpy as np
from data_collector import DataCollector

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class ArtificialModel:
    def __init__(self, data_set_path):
        self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels = self.obtain_train_data(data_set_path)
        self.model = self.train_model(self.df_train_data, self.df_train_labels, self.df_test_data, self.df_test_labels)

    @staticmethod
    def obtain_train_data(path_to_data, should_shuffle_rows=True, label_column_name="action"):
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
        print(dataset_train.shape)
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


class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear_1 = nn.Linear(input_size, hidden_size)
        self.linear_2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear_1(x))
        x = self.linear_2(x)
        return x

    def save(self, file_name="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        self.lr = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, new_state, game_ended):
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
