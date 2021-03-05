from game import Game
from artificial_model import ArtificialModel


def runAI():
    print("AI MODE")

    default_model = ArtificialModel()
    main_game = Game()
    main_game.play(default_model.model)


if __name__ == '__main__':
    print("**********************************************")
    print("***                AI Snake                ***")
    print("**********************************************")
    print("1. Play game and collect data.")
    print("2. Run AI.")
    # choice = input("Choose option: ")
    # choice = "1"
    # if choice == "1":
    while True:
        main_game = Game()
        main_game.play(None)
        # else:
        #runAI()
