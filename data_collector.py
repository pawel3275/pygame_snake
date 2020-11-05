import csv

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

    def collect_data_from_gameplay(self, training_node):
        self.training_data_movement.append(training_node)

    def parse_action_into_num(self, action):
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

    def save_data_as_csv(self, node_data, filename="gameDataset.csv"):
        with open(filename, newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.dict_data)
            writer.writeheader()
            for data in node_data:
                writer.writerow(data)

    def load_data_from_csv(self, file_path):
        pass