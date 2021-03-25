import os.path

import agent
from game import Game
from artificial_model import ArtificialModel


def run_basic_artificial_mode(data_set_path):
    print("AI MODE")
    default_model = ArtificialModel(data_set_path)
    Game(250, 250, False).play(default_model.model)


def run_reinforced_learning_mode():
    agent.train_reinforced_learning()


def run_normal_snake_mode():
    Game().play(None)


if __name__ == '__main__':
    print("**********************************************")
    print("***                AI Snake                ***")
    print("**********************************************")
    print("1. Play game and collect data.")
    print("2. Run AI. (Requires data set path with data to train!)")
    print("3. Run reinforced learning.")
    choice = input("Choose option: ")
    if choice == "1":
        run_normal_snake_mode()

    elif choice == "2":
        data_set_path = input("Specify training data set path: ")
        data_set_path = data_set_path.replace("\"", "")
        if os.path.isfile(data_set_path):
            run_basic_artificial_mode(data_set_path)
        else:
            print("Data set file does not exist.")

    elif choice == "3":
        run_reinforced_learning_mode()
