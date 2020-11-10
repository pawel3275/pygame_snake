import csv
import pathlib


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
        current_path = pathlib.Path(__file__).parent.absolute()

        with open(filename, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writeheader()
            for data in self.training_data_movement:
                writer.writerow(data)

    def load_data_from_csv(self, file_path):
        pass