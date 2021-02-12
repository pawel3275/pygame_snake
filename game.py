import pygame
from player import Player
import pygame
from score import Score
from data_collector import DataCollector
import numpy as np
from artificial_model import ArtificialModel


class Game:
    def __init__(self, width=500, height=500):
        pygame.display.set_caption("Snake")
        self.width = width
        self.height = height
        self.head_direction = "UP"
        self.score = 0
        self.game_ended = False
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.player = Player(int(width / 2), int(height / 2))
        self.collector = DataCollector()
        self.scoreboard = Score()

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
            print("Point has been consumed")
            self.score += 1
            return True
        else:
            return False

    def check_for_wall_collision(self, player):
        if player.head_position_x <= 0 or player.head_position_x >= 500:
            #self.game_ended = True
            print("GAME ENDED")
            print("Score:", self.score)

        if player.head_position_y <= 0 or player.head_position_y >= 500:
            #self.game_ended = True
            print("GAME ENDED")
            print("Score:", self.score)

        pass

    def check_for_body_collision(self, player):
        for iterator in range(1, len(player.nodes)):
            node_position_x, node_position_y = player.nodes[iterator]

            if player.head_position_x == node_position_x and player.head_position_y == node_position_y:
                # self.game_ended = True
                print("Head Collided with: ", iterator, node_position_x, node_position_y)
                print("GAME ENDED YOU ATE YOURSELF")
                print("Score:", self.score)
        pass

    def obtain_distances_from_head(self, player, point_position_x, point_position_y):
        node_to_fill = {}
        current_direction = self.head_direction

        vertical_food_vector = (player.head_position_y - point_position_y) / 500  # pretend we normalize things for now
        horizontal_food_vector = (player.head_position_x - point_position_x) / 500  # pretend we normalize things for now

        vertical_wall_vector = ArtificialModel.get_wall_distance_factor(player.head_position_y / 500)
        horizontal_wall_vector = ArtificialModel.get_wall_distance_factor(player.head_position_x / 500)

        node_to_fill["distance_from_food_x"] = horizontal_food_vector
        node_to_fill["distance_from_food_y"] = vertical_food_vector
        node_to_fill["distance_from_wall_x"] = horizontal_wall_vector
        node_to_fill["distance_from_wall_y"] = vertical_wall_vector
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

            self.scoreboard.spawn_point(screen)
            data_node = self.obtain_distances_from_head(player,
                                                        self.scoreboard.point_position_x,
                                                        self.scoreboard.point_position_y)
            self.collector.append_data_node(data_node)
            self.scoreboard.point_is_visible = self.check_for_point_consumption(player,
                                                                                self.scoreboard.point_position_x,
                                                                                self.scoreboard.point_position_y)
            self.check_for_wall_collision(player)
            self.check_for_body_collision(player)
            pygame.display.update()

            if model:
                values = list(data_node.values())
                values = values[:-1]
                values = np.array(values)
                values = values[np.newaxis, ...]
                prediction = np.argmax(model.predict(values), axis=1)

            if self.game_ended:
                self.collector.save_data_as_csv()
                pygame.quit()

            self.set_clock_tick(15)
