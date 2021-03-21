from game import Game
from artificial_model import ArtificialModel
import agent


def run_basic_AI_mode():
    print("AI MODE")
    default_model = ArtificialModel()
    Game().play(default_model.model)


def run_reinforced_learning():
    agent.train_reinforced_learning()


def run_normal_snake():
    main_game = Game()
    main_game.play(None)


if __name__ == '__main__':
    print("**********************************************")
    print("***                AI Snake                ***")
    print("**********************************************")
    print("1. Play game and collect data.")
    print("2. Run AI. (Requires data set path with data to train!)")
    print("3. Run reinforced learning.")
    choice = input("Choose option: ")
    if choice == "1":
        data_set_path = input("Specify input data set path: ")
        main_game = Game()
        main_game.play(None)

    elif choice == "2":
        run_basic_AI_mode()

    elif choice == "3":
        run_reinforced_learning()
