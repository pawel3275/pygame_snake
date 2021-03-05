import pygame
from player import Player
import pygame
from data_collector import DataCollector
import numpy as np
from artificial_model import ArtificialModel
import random


class Game:
    def __init__(self, width=500, height=500):
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.reset_game()

    def reset_game(self):
        self.head_direction = "UP"
        self.score = 0
        self.game_ended = False
        self.player = Player(int(self.width / 2), int(self.height / 2))
        self.collector = DataCollector()
        self.wall_collision_factor = 0.05
        self.body_collision_factor = 0.05
        self.point_is_visible = False
        self.point_position_x = 250
        self.point_position_y = 200
        self.spawn_point(self.screen)

    def spawn_point(self, screen):
        if not self.point_is_visible:
            pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
            return
        self.point_position_x, self.point_position_y = pygame.display.get_surface().get_size()
        self.point_position_x = random.randint(0, self.point_position_x - 15)
        self.point_position_y = random.randint(0, self.point_position_y - 15)
        pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
        self.point_is_visible = True

    def process_event(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.head_direction = "UP"
            return

        if key[pygame.K_s]:
            self.head_direction = "DOWN"
            return

        if key[pygame.K_a]:
            self.head_direction = "LEFT"
            return

        if key[pygame.K_d]:
            self.head_direction = "RIGHT"
            return

    def check_for_point_consumption(self, player, point_position_x, point_position_y):
        scale_factor = 15
        player_position_x_upper = player.head_position_x + scale_factor
        player_position_x_lower = player.head_position_x - scale_factor

        player_position_y_upper = player.head_position_y + scale_factor
        player_position_y_lower = player.head_position_y - scale_factor

        if player_position_x_lower < point_position_x < player_position_x_upper and \
                player_position_y_lower < point_position_y < player_position_y_upper:
            self.score += 10
            return True
        else:
            return False

    def check_for_collision(self, player):
        # Check for wall left and right collision
        if player.head_position_x <= 0 or player.head_position_x >= 500:
            self.score -= 10
            self.game_ended = True
            return True

        # Check for wall top and bottom collision
        if player.head_position_y <= 0 or player.head_position_y >= 500:
            self.score -= 10
            self.game_ended = True
            return True

        # Check for body collision
        for iterator in range(1, len(player.nodes)):
            node_position_x, node_position_y = player.nodes[iterator]

            if player.head_position_x == node_position_x and player.head_position_y == node_position_y:
                self.score -= 10
                self.game_ended = True
                return True

        return False

    def obtain_distances_from_head(self, player, point_position_x, point_position_y):
        node_to_fill = {}
        current_direction = self.head_direction

        vertical_food_vector = (player.head_position_y - point_position_y) / 500  # pretend we normalize things for now
        horizontal_food_vector = (
                                         player.head_position_x - point_position_x) / 500  # pretend we normalize things for now

        vertical_wall_vector = self.get_wall_distance_factor(player.head_position_y / 500)
        horizontal_wall_vector = self.get_wall_distance_factor(player.head_position_x / 500)

        node_to_fill["mode"] = 2  # DataCollector.possible_modes[2]  # by default eat

        node_to_fill["distance_from_food_x"] = horizontal_food_vector
        node_to_fill["distance_from_food_y"] = vertical_food_vector
        node_to_fill["distance_from_wall_x"] = horizontal_wall_vector
        node_to_fill["distance_from_wall_y"] = vertical_wall_vector

        top = abs(float(player.body_distances["top"]))
        bottom = abs(float(player.body_distances["bottom"]))
        left = abs(float(player.body_distances["left"]))
        right = abs(float(player.body_distances["right"]))

        node_to_fill["distance_from_body_top"] = top
        node_to_fill["distance_from_body_bottom"] = bottom
        node_to_fill["distance_from_body_left"] = left
        node_to_fill["distance_from_body_right"] = right

        if (top < self.body_collision_factor and current_direction != "DOWN") or \
                (bottom < self.body_collision_factor and current_direction != "UP") or \
                (left < self.body_collision_factor and current_direction != "RIGHT") or \
                (right < self.body_collision_factor and current_direction != "LEFT"):
            node_to_fill["mode"] = 0  # DataCollector.possible_modes[0]  # collision ahead, report it

        if horizontal_wall_vector < self.wall_collision_factor or vertical_wall_vector < self.wall_collision_factor:
            node_to_fill["mode"] = 1  # DataCollector.possible_modes[1]  # collision ahead, report it

        node_to_fill["score"] = self.score
        node_to_fill["action"] = current_direction

        return node_to_fill

    def get_screen(self):
        return self.screen

    def set_clock_tick(self, value=15):
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
                    self.collector.save_data_as_csv()
                    pygame.quit()

                if not model:
                    self.process_event()

            if not model:
                player.move_head_to_position(self.head_direction, self.score)
            else:
                direction = DataCollector.parse_num_into_action(prediction)
                self.head_direction = direction
                player.move_head_to_position(direction, self.score)

            player.draw_nodes(screen)

            self.spawn_point(screen)
            data_node = self.obtain_distances_from_head(player,
                                                        self.point_position_x,
                                                        self.point_position_y)
            self.collector.append_data_node(data_node)
            self.point_is_visible = self.check_for_point_consumption(player,
                                                                     self.point_position_x,
                                                                     self.point_position_y)
            self.check_for_collision(player)
            pygame.display.update()

            if model:
                values = list(data_node.values())
                values = values[:-1]
                values = np.array(values)
                values = values[np.newaxis, ...]
                prediction = np.argmax(model.predict(values), axis=1)

            if self.game_ended:
                self.reset_game()
                #self.collector.save_data_as_csv()
                #pygame.quit()

            self.set_clock_tick(15)

    @staticmethod
    def get_wall_distance_factor(x):
        # Note, for the best usage pass normalized number
        # Returns max value 1 for middle of screen 250 ,250 after normalizing.
        # Return 0 for values close to 0 and 500
        # return 1 for values 250 and 250
        return round((-4 * (x * x)) + (4 * x), 4)
