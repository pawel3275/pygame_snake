from game import Game
from data_collector import DataCollector
import os
from artificial_model import ArtificialModel


def runAI():
    print("AI MODE")
    data = DataCollector.load_data_from_csv_to_data_frame("D:\\scratch\\snake\\gameDataset_1.csv")

    df_train, df_test = DataCollector.split_data_frame_to_train_and_test(data, shuffle_rows=True)

    # Experiment, lets drop few columns
    # df_train.drop(columns=['distance_from_wall_top', 'distance_from_wall_left', 'distance_from_wall_right', 'distance_from_wall_bottom', 'distance_from_body_top', 'distance_from_body_left', 'distance_from_body_right', 'distance_from_body_bottom'])
    # df_test.drop(columns=['distance_from_wall_top', 'distance_from_wall_left', 'distance_from_wall_right', 'distance_from_wall_bottom', 'distance_from_body_top', 'distance_from_body_left', 'distance_from_body_right', 'distance_from_body_bottom'])

    df_train_data, df_train_labels = DataCollector.extract_labels_from_data_frame(df_train, column_name="action")
    df_test_data, df_test_labels = DataCollector.extract_labels_from_data_frame(df_test, column_name="action")

    df_train_labels = DataCollector.update_labels_to_int_values(df_train_labels)
    df_train_labels = df_train_labels.to_numpy()

    df_test_labels = DataCollector.update_labels_to_int_values(df_test_labels)
    df_test_labels = df_test_labels.to_numpy()

    # DO NOT NORMALIZE DATA FOR NOW
    # REASON: we need to teach model true pixel values in order to elaborate for the data set, when it will come to
    # mode later. Give it up for now, normalization will come after model optimisation, now it's not necessary.
    # df_train_data = DataCollector.normalize_data_frame_data(df_train_data)
    # df_train_labels = DataCollector.normalize_data_frame_data(df_train_labels.reshape(1, -1))

    am = ArtificialModel()
    model = am.train_model(df_train_data, df_train_labels, df_test_data, df_test_labels)

    main_game = Game()
    main_game.play(model)


if __name__ == '__main__':
    print("**********************************************")
    print("***                AI Snake                ***")
    print("**********************************************")
    print("1. Play game and collect data.")
    print("2. Run AI.")
    #choice = input("Choose option: ")
    # choice = "1"
    #if choice == "1":
    #main_game = Game()
    #main_game.play(None)
    # else:
    runAI()
