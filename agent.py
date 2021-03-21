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
        self.number_of_games = 1
        self.epsilon = 0  # for randomness
        self.gamma = 0.9  # discount rate, must be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(14, 96, 4)
        self.trainer = QTrainer(self.model, learning_rate=LEARNING_RATE, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, game_ended):
        self.memory.append((state, action, reward, next_state, game_ended))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_ends = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_ends)

    def train_short_memory(self, state, action, reward, next_state, game_ended):
        self.trainer.train_step(state, action, reward, next_state, game_ended)

    def get_action(self, state):
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
            mean_score = total_score/agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
