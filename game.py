import pygame
from player import Player
import pygame
from data_collector import DataCollector
import numpy as np
import random


class Game:
    def __init__(self, width=250, height=250):
        pygame.display.set_caption("Snake")
        DataCollector.save_header_to_csv_file(DataCollector.csv_columns)
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.game_state = DataCollector.training_data_note
        self.reset_game()

    def reset_game(self):
        self.head_direction = random.randint(0, 3)
        self.score = 0
        self.reward = 0
        self.record = 0
        self.game_ended = False
        self.number_of_moves = 0
        self.player = Player(int(self.width / 2), int(self.height / 2))
        self.wall_collision_factor = 0.05
        self.body_collision_factor = 0.05
        self.point_is_visible = False
        self.point_position_x = self.divisible_random(10, self.width - 10, 5)
        self.point_position_y = self.divisible_random(10, self.height - 10, 5)
        self.spawn_point(self.screen)

    def spawn_point(self, screen):
        if not self.point_is_visible:
            pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
            return
        self.point_position_x, self.point_position_y = pygame.display.get_surface().get_size()
        self.point_position_x = self.divisible_random(10, self.width - 10, 5)
        self.point_position_y = self.divisible_random(10, self.height - 10, 5)
        pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
        self.point_is_visible = True

    def process_event(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.head_direction = 0  # UP

        elif key[pygame.K_s]:
            self.head_direction = 1  # DOWN

        elif key[pygame.K_a]:
            self.head_direction = 2  # LEFT

        elif key[pygame.K_d]:
            self.head_direction = 3  # RIGHT

        return

    def check_if_point_was_consumed(self):
        scale_factor = 15 # was 15
        reward = 0
        player_position_x_upper = self.player.head_position_x + scale_factor
        player_position_x_lower = self.player.head_position_x - scale_factor

        player_position_y_upper = self.player.head_position_y + scale_factor
        player_position_y_lower = self.player.head_position_y - scale_factor

        # Check if we are closer to food than we were one move ago
        vertical_food_vector = (self.player.head_position_y - self.point_position_y) / self.height
        horizontal_food_vector = (self.player.head_position_x - self.point_position_x) / self.width
        reward += (1 - abs(horizontal_food_vector))
        reward += (1 - abs(vertical_food_vector))

        if player_position_x_lower < self.point_position_x < player_position_x_upper and \
                player_position_y_lower < self.point_position_y < player_position_y_upper:
            self.score += 1
            reward = 15
            self.point_is_visible = True
            self.number_of_moves = 0
        else:
            self.point_is_visible = False

        self.game_state["vector_from_food_x"] = horizontal_food_vector
        self.game_state["vector_from_food_y"] = vertical_food_vector
        return self.point_is_visible, reward

    def check_if_collision_happend(self):
        # Check for wall left and right collision
        reward = 0
        if self.player.head_position_x <= 0 or self.player.head_position_x >= self.height:
            reward = -15
            self.game_ended = True
            return True, reward

        # Check for wall top and bottom collision
        if self.player.head_position_y <= 0 or self.player.head_position_y >= self.width:
            reward = -15
            self.game_ended = True
            return True, reward

        if self.number_of_moves >= 500:
            self.game_ended = True
            return True, reward

        # Check for body collision
        for iterator in range(1, len(self.player.nodes)):
            body_node_position_x, body_node_position_y = self.player.nodes[iterator]
            if self.player.head_position_x == body_node_position_x and self.player.head_position_y == body_node_position_y:
                reward = -15
                self.game_ended = True
                return True, reward

        return False, reward

    # Returns list, populates dict
    def obtain_distances_from_head(self):
        self.game_state["is_food_on_top"] = 0
        self.game_state["is_food_on_bottom"] = 0
        self.game_state["is_food_on_left"] = 0
        self.game_state["is_food_on_right"] = 0

        self.game_state["is_obstacle_on_top"] = 0
        self.game_state["is_obstacle_on_bottom"] = 0
        self.game_state["is_obstacle_on_left"] = 0
        self.game_state["is_obstacle_on_right"] = 0

        self.game_state["score"] = self.score
        self.game_state["action"] = self.head_direction

        vertical_food_vector = (self.player.head_position_y - self.point_position_y) / self.height
        horizontal_food_vector = (self.player.head_position_x - self.point_position_x) / self.width
        self.game_state["vector_from_food_x"] = horizontal_food_vector
        self.game_state["vector_from_food_y"] = vertical_food_vector

        vertical_wall_vector = self.get_wall_distance_factor(self.player.head_position_y / self.height)
        horizontal_wall_vector = self.get_wall_distance_factor(self.player.head_position_x / self.width)
        self.game_state["vector_from_wall_x"] = horizontal_wall_vector
        self.game_state["vector_from_wall_y"] = vertical_wall_vector

        if self.player.head_position_y < self.point_position_y:
            self.game_state["is_food_on_bottom"] = 1
        else:
            self.game_state["is_food_on_top"] = 1

        if self.player.head_position_x > self.point_position_x:
            self.game_state["is_food_on_left"] = 1
        else:
            self.game_state["is_food_on_right"] = 1

        # Check and report body collision
        for iterator in range(1, len(self.player.nodes)):
            body_node_position_x, body_node_position_y = self.player.nodes[iterator]
            if body_node_position_x + self.player.velocity == self.player.head_position_x:
                self.game_state["is_obstacle_on_left"] = 1
            if body_node_position_x - self.player.velocity == self.player.head_position_x:
                self.game_state["is_obstacle_on_right"] = 1
            if body_node_position_y + self.player.velocity == self.player.head_position_y:
                self.game_state["is_obstacle_on_top"] = 1
            if body_node_position_y - self.player.velocity == self.player.head_position_y:
                self.game_state["is_obstacle_on_bottom"] = 1

        # Check and report wall collision
        if self.player.head_position_y <= self.player.velocity:
            self.game_state["is_obstacle_on_top"] = 1
        if self.player.head_position_y >= (self.height - self.player.velocity):
            self.game_state["is_obstacle_on_bottom"] = 1

        if self.player.head_position_x <= self.player.velocity:
            self.game_state["is_obstacle_on_left"] = 1
        if self.player.head_position_x >= (self.width - self.player.velocity):
            self.game_state["is_obstacle_on_right"] = 1

        return list(self.game_state.values())

    def get_screen(self):
        return self.screen

    def set_clock_tick(self, value=30):
        self.clock.tick(value)

    def get_player(self):
        return self.player

    def play(self, model):
        prediction = 0
        while True and not self.game_ended:
            screen = self.get_screen()
            player = self.get_player()

            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()

                if not model:
                    self.process_event()

            if not model:
                player.move_head_to_position(self.head_direction, self.score)
            else:
                player.move_head_to_position(prediction, self.score)

            self.spawn_point(screen)

            self.obtain_distances_from_head()

            DataCollector.save_data_row_to_csv_file(self.game_state, DataCollector.csv_columns)

            self.check_if_point_was_consumed()

            self.check_if_collision_happend()

            self.player.apply_body_movement()

            player.draw_nodes(screen)

            pygame.display.update()

            if model:
                values = list(self.game_state.values())
                values = values[:-1]
                values = np.array(values)
                values = values[np.newaxis, ...]
                prediction = np.argmax(model.predict(values), axis=1)

            if self.game_ended:
                self.reset_game()

            self.set_clock_tick(15)

    @staticmethod
    def divisible_random(a, b, n):
        if b - a < n:
            raise Exception('{} is too big'.format(n))
        result = random.randint(a, b)
        while result % n != 0:
            result = random.randint(a, b)
        return result

    def play_for_reinforced_learning(self, direction):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()

        self.number_of_moves += 1
        self.head_direction = direction

        screen = self.get_screen()
        player = self.get_player()

        screen.fill((0, 0, 0))

        player.move_head_to_position(self.head_direction, self.score)

        self.spawn_point(screen)

        was_point_consumed, reward = self.check_if_point_was_consumed()

        game_ended, penalty = self.check_if_collision_happend()

        self.player.apply_body_movement()

        player.draw_nodes(screen)
        pygame.display.update()

        self.set_clock_tick(60)

        return (reward + penalty, game_ended, self.score)

    @staticmethod
    def get_wall_distance_factor(x):
        # Note, for the best usage pass normalized number
        # Returns max value 1 for middle of screen 250 ,250 after normalizing.
        # Return 0 for values close to 0 and 500
        # return 1 for values 250 and 250
        return round((-4 * (x * x)) + (4 * x), 4)
