import random
import torch
from collections import deque
from artificial_model import LinearQNet, QTrainer
from game import Game
from plotter import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:
    def __init__(self):
        """
        Default constructor.
        """
        self.number_of_games = 1
        self.epsilon = 0  # for randomness
        self.gamma = 0.9  # discount rate, must be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(14, 96, 4)
        self.trainer = QTrainer(self.model, learning_rate=LEARNING_RATE, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, game_ended):
        """
        Appends to the memory (deque) given values as the input params for the agent to remember.
        :param state: Current game state as a list with values.
        :param action: Action performed for the game step frame.
        :param reward: Reward for given action.
        :param next_state: Next state of the game after performing certain action.
        :param game_ended: Boolean value describing if the game has already ended or not.
        """
        self.memory.append((state, action, reward, next_state, game_ended))

    def train_long_memory(self):
        """
        Trains long memory by sampling (or not if the batch size is smaller then memory) memory values. Per each
        collected value from memory performs training step, that adjusts weights of neural network accordingly to the
        given states. IMPORTANT: this is LONG memory, meaning we are training network using batches with states.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_ends = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_ends)

    def train_short_memory(self, state, action, reward, next_state, game_ended):
        """
        Trains short memory depending on the given state. IMPORTANT: this is SHORT memory training, meaning that we are
        adjusting weights in the neural network in accordance to the single game state, not the whole batch.
        :param state: Current game state with distances obtained from the head as a list.
        :param action: Performed action in a current movement.
        :param reward: Reward for a given movement.
        :param next_state: New game state with distances after performing given action.
        :param game_ended: Boolean value describing if the game has ended or not.
        """
        self.trainer.train_step(state, action, reward, next_state, game_ended)

    def get_action(self, state):
        """
        Simple getter for the action to be performed by the snake. IMPORTANT: for the first few games we need to do
        "exploring" hence the epsilon value is provided. At first, because of the epsilon check movement can be random,
        but this is because we are trying to find the most optimized path that will grant us biggest reward.
        :param state: Game state list with distances obtained from the head.
        :return: Action (direction) to be performed by snake.
        """
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.number_of_games
        if random.randint(0, 200) < self.epsilon:
            final_move = random.randint(0, 3)
        else:
            state_0 = torch.tensor(state, dtype=torch.float)
            predicted_move = self.model(state_0)
            final_move = torch.argmax(predicted_move).item()

        return final_move


def train_reinforced_learning():
    """
    Plays snake using reinforced learning.
    """
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    num_of_moves = 0
    agent = Agent()
    game = Game()

    while True:
        num_of_moves += 1
        # Get current state
        current_state = game.obtain_distances_from_head()
        # Get action
        final_action = agent.get_action(current_state)

        # perform move and get new state
        reward, game_ended, score = game.play_for_reinforced_learning(final_action)
        new_state = game.obtain_distances_from_head()

        # train short memory
        agent.train_short_memory(current_state, final_action, reward, new_state, game_ended)

        # remember
        agent.remember(current_state, final_action, reward, new_state, game_ended)

        if game_ended:
            # train the experienced replay memory.
            # plot the result
            agent.number_of_games += 1
            agent.train_long_memory()
            game.reset_game()

            if score > best_score:
                best_score = score
                agent.model.save()

            print("Game", agent.number_of_games, " Score:", score, " Current record", best_score)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
