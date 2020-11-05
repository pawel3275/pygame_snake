import pygame
import numpy as np
from player import Player
from score import Score
from data_collector import DataCollector

width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

movement_coords_history = []


class Game:
    def __init__(self):
        self.head_direction = "UP"
        self.score = 0
        self.game_ended = False

    def process_event(self, passed_event):
        if passed_event.type is pygame.QUIT:
            pygame.quit()

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
        scale_factor = 8
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
            self.game_ended = True
            print("GAME ENDED")
            print("Score:", self.score)

        if player.head_position_y <= 0 or player.head_position_y >= 500:
            self.game_ended = True
            print("GAME ENDED")
            print("Score:", self.score)

        pass

    def check_for_body_collision(self, player):
        for iterator in range(1, len(player.nodes)):
            node_position_x, node_position_y = player.nodes[iterator]

            if player.head_position_x == node_position_x and player.head_position_y == node_position_y:
                self.game_ended = True
                print("Head Collided with: ", iterator, node_position_x, node_position_y)
                print("GAME ENDED YOU ATE YOURSELF")
                print("Score:", self.score)
        pass

    def obtain_distances_from_head(self, player, point_position_x, point_position_y):
        node_to_fill = DataCollector.training_data_note
        current_direction = self.head_direction

        # Calculate distance from wall. Should sum to height and width
        node_to_fill["distance_from_wall_top"] = abs(player.head_position_x - height)
        node_to_fill["distance_from_body_bottom"] = player.head_position_x
        node_to_fill["distance_from_wall_right"] = abs(player.head_position_y - width)
        node_to_fill["distance_from_wall_left"] = player.head_position_y

        # Calculate distance from body part
        # Fill initial zero values. Zero means there is no body part in that direction.
        node_to_fill["distance_from_body_top"] = 0
        node_to_fill["distance_from_body_bottom"] = 0
        node_to_fill["distance_from_body_left"] = 0
        node_to_fill["distance_from_body_right"] = 0

        for node in player.nodes:
            if not player.nodes:
                break

            player_node_pos_x = node[0]
            player_node_pos_y = node[1]

            if player.head_position_x == player_node_pos_x:
                # We detected our body on our top or bottom from head
                if player.head_position_y > player_node_pos_y and (node_to_fill["distance_from_body_top"] > abs(player.head_position_y - player_node_pos_y) or node_to_fill["distance_from_body_top"] == 0):
                    # our node is at the top from us
                    node_to_fill["distance_from_body_top"] = abs(player.head_position_y - player_node_pos_y)
                if player.head_position_y < player_node_pos_y and (node_to_fill["distance_from_body_bottom"] > abs(player.head_position_y - player_node_pos_y) or node_to_fill["distance_from_body_bottom"] == 0):
                    # our node is at the bottom from us
                    node_to_fill["distance_from_body_bottom"] = abs(player.head_position_y - player_node_pos_y)

            if player.head_position_y == player_node_pos_y:
                # We detected our body on our left or right from head
                if player.head_position_x > player_node_pos_x and (node_to_fill["distance_from_body_left"] > abs(player.head_position_x - player_node_pos_x) or node_to_fill["distance_from_body_left"] == 0):
                    # our node is at the right from us
                    node_to_fill["distance_from_body_left"] = abs(player.head_position_x - player_node_pos_x)

                if player.head_position_x < player_node_pos_x and (node_to_fill["distance_from_body_right"] > abs(player.head_position_x - player_node_pos_x) or node_to_fill["distance_from_body_right"] == 0):
                    # our node is at the left from us
                    node_to_fill["distance_from_body_right"] = abs(player.head_position_x - player_node_pos_x)

        # Calculate distance from food
        node_to_fill["distance_from_food_top"] = 0
        node_to_fill["distance_from_food_bottom"] = 0
        node_to_fill["distance_from_food_left"] = 0
        node_to_fill["distance_from_food_right"] = 0

        vertical = point_position_y - player.head_position_y
        horizontal = point_position_x - player.head_position_x

        if vertical > 0 and horizontal > 0:
            # right lower corner
            node_to_fill["distance_from_food_top"] = abs(vertical)
            node_to_fill["distance_from_food_right"] = abs(horizontal)

        if vertical < 0 and horizontal < 0:
            # lower upper corner
            node_to_fill["distance_from_food_bottom"] = abs(vertical)
            node_to_fill["distance_from_food_left"] = abs(horizontal)

        if vertical > 0 and horizontal < 0:
            # left lower corner
            node_to_fill["distance_from_food_top"] = abs(vertical)
            node_to_fill["distance_from_food_left"] = abs(horizontal)

        if vertical < 0 and horizontal > 0:
            # right upper corner
            node_to_fill["distance_from_food_bottom"] = abs(vertical)
            node_to_fill["distance_from_food_right"] = abs(horizontal)

        node_to_fill["action"] = current_direction

        return node_to_fill


p1 = Player(int(width / 2), int(height / 2))
main_game = Game()
scoreboard = Score()
while True:
    for event in pygame.event.get():
        main_game.process_event(event)

    screen.fill((0, 0, 0))

    p1.move_head_to_position(main_game.head_direction, main_game.score)
    p1.draw_nodes(screen)

    scoreboard.spawn_point(screen)
    data_node = main_game.obtain_distances_from_head(p1,
                                                     scoreboard.point_position_x,
                                                     scoreboard.point_position_y)

    scoreboard.point_is_visible = main_game.check_for_point_consumption(p1,
                                                                        scoreboard.point_position_x,
                                                                        scoreboard.point_position_y)
    main_game.check_for_wall_collision(p1)
    main_game.check_for_body_collision(p1)
    pygame.display.update()

    clock.tick(15)

    data
