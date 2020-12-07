import csv
import pandas as pd
import numpy as np
from sklearn.utils import shuffle


class DataCollector:
    training_data_movement = []
    training_data_note = {"distance_from_food_top": 0,
                          "distance_from_food_bottom": 0,
                          "distance_from_food_left": 0,
                          "distance_from_food_right": 0,
                          "distance_from_wall_top": 0,
                          "distance_from_wall_left": 0,
                          "distance_from_wall_right": 0,
                          "distance_from_wall_bottom": 0,
                          "distance_from_body_top": 0,
                          "distance_from_body_left": 0,
                          "distance_from_body_right": 0,
                          "distance_from_body_bottom": 0,
                          "action": ""}

    csv_columns = ["distance_from_food_top",
                   "distance_from_food_bottom",
                   "distance_from_food_left",
                   "distance_from_food_right",
                   "distance_from_wall_top",
                   "distance_from_wall_left",
                   "distance_from_wall_right",
                   "distance_from_wall_bottom",
                   "distance_from_body_top",
                   "distance_from_body_left",
                   "distance_from_body_right",
                   "distance_from_body_bottom",
                   "action"]

    def __init__(self):
        pass

    def append_data_node(self, training_node):
        self.training_data_movement.append(training_node)

    @staticmethod
    def parse_action_into_num(action):
        if action == "UP":
            return 0
        if action == "DOWN":
            return 1
        if action == "LEFT":
            return 2
        if action == "RIGHT":
            return 3

    def preprocess_captured_data(self):
        pass

    def save_data_as_csv(self, filename="gameDataset.csv"):
        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writeheader()
            for data in self.training_data_movement:
                writer.writerow(data)

    @staticmethod
    def load_data_from_csv_to_np_array(file_path, delimiter=",", keep_header=True):
        return np.genfromtxt(file_path, dtype=float, delimiter=delimiter, names=keep_header)

    @staticmethod
    def load_data_from_csv_to_data_frame(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def split_data_frame_to_train_and_test(data_frame, percent_test_ratio=20, shuffle_rows=False):
        if shuffle_rows:
            data_frame = shuffle(data_frame)

        total_number_of_rows = data_frame.shape[0]
        test_rows_number = int(total_number_of_rows * percent_test_ratio / 100)
        train_rows_number = total_number_of_rows - test_rows_number

        df_train = data_frame[:train_rows_number]
        df_test = data_frame[test_rows_number:]

        return df_train, df_test

    @staticmethod
    def extract_labels_from_data_frame(data_frame, column_number=-1, column_name=""):
        if column_name == "" and column_number == -1:
            print("Error provide column number or column name!")
            return data_frame, 0

        if column_number != -1:
            labels = data_frame[data_frame.column[column_number]]
            del data_frame[data_frame.column[column_number]]
            return data_frame, labels

        elif column_name != "":
            labels = data_frame[column_name]
            del data_frame[column_name]
            return data_frame, labels

    @staticmethod
    def update_labels_to_int_values(label_data_frame):
        label_data_frame = label_data_frame.replace("UP", 0)
        label_data_frame = label_data_frame.replace("DOWN", 1)
        label_data_frame = label_data_frame.replace("LEFT", 2)
        label_data_frame = label_data_frame.replace("RIGHT", 3)
        return label_data_frame
