import csv
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import preprocessing
import os

class DataCollector:
    training_data_note = {"vector_from_food_x": 0,
                          "vector_from_food_y": 0,
                          "vector_from_wall_x": 0,
                          "vector_from_wall_y": 0,
                          "is_food_on_top": 0,
                          "is_food_on_bottom": 0,
                          "is_food_on_left": 0,
                          "is_food_on_right": 0,
                          "is_obstacle_on_top": 0,
                          "is_obstacle_on_bottom": 0,
                          "is_obstacle_on_left": 0,
                          "is_obstacle_on_right": 0,
                          "action": "",
                          "score": 0}

    csv_columns = ["vector_from_food_x",
                   "vector_from_food_y",
                   "vector_from_wall_x",
                   "vector_from_wall_y",
                   "is_food_on_top",
                   "is_food_on_bottom",
                   "is_food_on_left",
                   "is_food_on_right",
                   "is_obstacle_on_top",
                   "is_obstacle_on_bottom",
                   "is_obstacle_on_left",
                   "is_obstacle_on_right",
                   "action",
                   "score"]

    def __init__(self):
        pass

    @staticmethod
    def save_header_to_csv_file(csv_columns, filename="gameDataset.csv"):
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

    @staticmethod
    def save_data_row_to_csv_file(data_row, csv_columns, filename="gameDataset.csv"):
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(data_row)

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
    def update_labels_to_int_values(label_data_frame, return_as_num_array=False):
        # this is lazy and ugly, needs correction
        label_data_frame = label_data_frame.replace("UP", 0)
        label_data_frame = label_data_frame.replace("DOWN", 1)
        label_data_frame = label_data_frame.replace("LEFT", 2)
        label_data_frame = label_data_frame.replace("RIGHT", 3)

        if return_as_num_array:
            label_data_frame = DataCollector.convert_labels_to_numerical_array(label_data_frame)

        return label_data_frame

    @staticmethod
    def normalize_data_frame_data(data_frame):
        min_max_scaler = preprocessing.MinMaxScaler()
        data_frame_scaled = min_max_scaler.fit_transform(data_frame)
        return pd.DataFrame(data_frame_scaled)

    @staticmethod
    def convert_labels_to_numerical_array(label_data_frame):
        numerical_array_series = []
        for key, value in label_data_frame.items():
            numerical_array = [0, 0, 0, 0]
            numerical_array[value] = 1
            numerical_array_series.append(numerical_array)

        return numerical_array_series
