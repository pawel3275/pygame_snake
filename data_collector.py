import csv
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import preprocessing


class DataCollector:
    training_data_note = {
        "vector_from_food_x": 0,
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
        "score": 0,
        "action": ""
    }

    csv_columns = [
        "vector_from_food_x",
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
        "score",
        "action"
    ]

    @staticmethod
    def save_header_to_csv_file(csv_columns, filename="gameDataset.csv"):
        """
        Saves header of csv_columns to csv file specified in input param.
        :param csv_columns: csv columns in lsit format to be inserted to the csv file.
        :param filename: csv file path.
        """
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

    @staticmethod
    def save_data_row_to_csv_file(data_row, csv_columns, filename="gameDataset.csv"):
        """
        Puts data row specified in input to a file.
        :param data_row: List of values to be written to a csv file.
        :param csv_columns: Csv columns,
        :param filename: Path to the csv file.
        """
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(data_row)

    @staticmethod
    def load_data_from_csv_to_np_array(file_path, delimiter=",", keep_header=True):
        """
        Loads the whole csv data and returns it as a numpy array type.
        :param file_path: Path to the
        :param delimiter: delimeter used in the csv file
        :param keep_header: Bool to determine whether to keep csv header or not for the first array values.
        :return: Numpy array with the values.
        """
        return np.genfromtxt(file_path, dtype=float, delimiter=delimiter, names=keep_header)

    @staticmethod
    def load_data_from_csv_to_data_frame(file_path):
        """
        Loads data specified in csv file path as param and returns it as pandas data frame.
        :param file_path: Path to the csv file
        :return: Data frame with values from csv file.
        """
        return pd.read_csv(file_path)

    @staticmethod
    def split_data_frame_to_train_and_test(data_frame, percent_test_ratio=20, shuffle_rows=False):
        """
        Splits the data set to the training and test by a given ratio.
        :param data_frame: Data frame containing values to be split.
        :param percent_test_ratio: Percent value of what is the percent of the test values.
        :param shuffle_rows: If true, then we will shuffle rows inside given data set before split.
        :return: data frame objects for test and training.
        """
        if shuffle_rows:
            data_frame = shuffle(data_frame)

        total_number_of_rows = data_frame.shape[0]
        test_rows_number = int(total_number_of_rows * percent_test_ratio / 100)
        train_rows_number = total_number_of_rows - test_rows_number

        df_train = data_frame[:train_rows_number]
        df_test = data_frame[test_rows_number:]

        return (df_train, df_test)

    @staticmethod
    def extract_labels_from_data_frame(data_frame, column_number=-1, column_name=""):
        """
        Extracts labels from the data frame and deleted whole labels column returning data set without it. You can
        provide either column name or the column number to this function in order to cut it out, no need for two at the
        same time.
        :param data_frame: data set containing labels column.
        :param column_number: Column where labels are located.
        :param column_name: Column name with labels.
        :return: data set without labels column, and labels as the second data set.
        """
        if column_name == "" and column_number == -1:
            print("Error provide column number or column name!")
            return (data_frame, 0)

        if column_number != -1:
            labels = data_frame[data_frame.column[column_number]]
            del data_frame[data_frame.column[column_number]]
            return (data_frame, labels)

        elif column_name != "":
            labels = data_frame[column_name]
            del data_frame[column_name]
            return (data_frame, labels)

    @staticmethod
    def normalize_data_frame_data(data_frame):
        """
        Performes normalization of values to a given data frame.
        :param data_frame: data set on which normalization of values shall be performed.
        :return: data set with scaled values after normalization.
        """
        min_max_scaler = preprocessing.MinMaxScaler()
        data_frame_scaled = min_max_scaler.fit_transform(data_frame)
        return pd.DataFrame(data_frame_scaled)
