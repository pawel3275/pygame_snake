import pygame

from player import Player
import numpy as np
import random

from .data_collector import DataCollector


class Game:
    def __init__(self, width=250, height=250, save_header_to_file=True):
        """
        Basic constructor of the game class. Initializes player, board and inserts header to the csv file during init.
        :param width: width of the board.
        :param height: height of the board
        :param save_header_to_file: True for saving csv header, false to skip it.
        """
        pygame.display.set_caption("Snake")

        if save_header_to_file:
            DataCollector.save_header_to_csv_file(DataCollector.csv_columns)

        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.game_state = DataCollector.training_data_note
        self.reset_game()

    def reset_game(self):
        """
        Resets board and game to the initial state.
        """
        self.head_direction = random.randint(0, 3)
        self.score = 0
        self.reward = 0
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
        """
        Sprawns point in random location on board. Value of spawn has to be between 10 and (width oo height)-10
        :param screen: Pointer to the current screen board.
        :return: None
        """
        if not self.point_is_visible:
            pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
            return
        self.point_position_x, self.point_position_y = pygame.display.get_surface().get_size()
        self.point_position_x = self.divisible_random(10, self.width - 10, 5)
        self.point_position_y = self.divisible_random(10, self.height - 10, 5)
        pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
        self.point_is_visible = True

    def process_event(self):
        """
        Does event processing during the game. Takes care of player head direction depending on the input value.
        0:UP
        1:DOWN
        2:LEFT
        3:RIGHT
        """
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.head_direction = 0  # UP

        elif key[pygame.K_s]:
            self.head_direction = 1  # DOWN

        elif key[pygame.K_a]:
            self.head_direction = 2  # LEFT

        elif key[pygame.K_d]:
            self.head_direction = 3  # RIGHT

    def check_if_point_was_consumed(self):
        """
        Does the initial check of the point consumption. During calculations takes under consideration special factor
        to check the head boundaries. For example if point is spawned at location 100:100 then we accept that point was
        consumed as 100+-factor:100=-factor, this way we don't need exact head to be in position of the point. If the
        point was consumed we return visibility as False and reward for reinforced learning
        :return: Point visibility and reward for reinforced learning agent
        """
        scale_factor = 15
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
        """
        Checks if the collision of the player has happened with the wall and/or body. Depending on the collision reward
        for reinforced agent is returned as penalty negative value with the game over state.
        :return: Penalty if the collision happened and boolean value to end the game
        """
        # Check for wall left and right collision
        penalty = 0
        if self.player.head_position_x <= 0 or self.player.head_position_x >= self.height:
            penalty = -15
            self.game_ended = True

        # Check for wall top and bottom collision
        if self.player.head_position_y <= 0 or self.player.head_position_y >= self.width:
            penalty = -15
            self.game_ended = True

        if self.number_of_moves >= 500:
            self.game_ended = True

        # Check for body collision
        for i in range(1, len(self.player.nodes)):
            body_node_position_x, body_node_position_y = self.player.nodes[i]
            if self.player.head_position_x == body_node_position_x and self.player.head_position_y == body_node_position_y:
                penalty = -15
                self.game_ended = True

        return self.game_ended, penalty

    def obtain_distances_from_head(self):
        """
        Returns and populates the game state both for the reinforced learning agent and normal game itself. Distances to
        the wall, body and point are calculated here and dictionary with game state is populated.
        step 1:
            We check for the point position calculation line equation vector to check where it is located according to
            the head position. Additionally we populate 4 values from dictionary is_food_on_top/bottom/right/left.
        step 2:
            We do the same calculation of vector to the wall. The closer values are to the value of 0, the closer we
            are to the wall, value of 1 means we are exactly in the middle of the screen. We also populate the obstacle
            dictionary values if we are very close to the wall. Value of 1 in the obstacle_top_bottom_right_left means
            that there is collision ahead.
        Step 3:
            We iterate over every snake body node and check if there is any collision ahead. If the collision could
            happen in the next move we report is as the obstacle.

        Achtung 1! The collision depends strictly on the player velocity factor, we need to report it right before next
        move for the reinforced learning.

        Achtung 2! Since it's not important to distinguish obstacles between wall and body we treat them the same, as
        just an obstacle.
        :return: Returns the populated dictionary as the list with values for the reinforced learning.
        """
        # Initialize zero values
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

        # Step 1: check for food placement
        vertical_food_vector = (self.player.head_position_y - self.point_position_y) / self.height
        horizontal_food_vector = (self.player.head_position_x - self.point_position_x) / self.width
        self.game_state["vector_from_food_x"] = horizontal_food_vector
        self.game_state["vector_from_food_y"] = vertical_food_vector

        if self.player.head_position_y < self.point_position_y:
            self.game_state["is_food_on_bottom"] = 1
        else:
            self.game_state["is_food_on_top"] = 1

        if self.player.head_position_x > self.point_position_x:
            self.game_state["is_food_on_left"] = 1
        else:
            self.game_state["is_food_on_right"] = 1

        # Step 2: check for wall distance factor
        vertical_wall_vector = self.get_wall_distance_factor(self.player.head_position_y / self.height)
        horizontal_wall_vector = self.get_wall_distance_factor(self.player.head_position_x / self.width)
        self.game_state["vector_from_wall_x"] = horizontal_wall_vector
        self.game_state["vector_from_wall_y"] = vertical_wall_vector

        if self.player.head_position_y <= self.player.velocity:
            self.game_state["is_obstacle_on_top"] = 1
        if self.player.head_position_y >= (self.height - self.player.velocity):
            self.game_state["is_obstacle_on_bottom"] = 1

        if self.player.head_position_x <= self.player.velocity:
            self.game_state["is_obstacle_on_left"] = 1
        if self.player.head_position_x >= (self.width - self.player.velocity):
            self.game_state["is_obstacle_on_right"] = 1

        # Step 3: Check and report body collision
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

        return list(self.game_state.values())

    def set_clock_tick(self, value=30):
        """
        Sets the clock tick to the given value.
        :param value: Value to use per the clock tick per each frame. By default it's 30.
        """
        self.clock.tick(value)

    def play(self, model):
        """
        Main game loop function, if the model is present in params, then he will make predictions for the movements.
        :param model: Model which will do predictions of the movements. Provide value of 'None' for default mode
        """
        while not self.game_ended:
            self.set_clock_tick(15)

            screen = self.screen
            player = self.player

            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()

                if not model:
                    self.process_event()

            self.spawn_point(screen)

            if not model:
                self.obtain_distances_from_head()
                DataCollector.save_data_row_to_csv_file(self.game_state, DataCollector.csv_columns)
                player.move_head_to_position(self.head_direction, self.score)
            else:
                game_state_values = np.asarray(self.obtain_distances_from_head(), dtype=np.float32)
                game_state_values = np.delete(game_state_values, 13)  # Get rid of action
                game_state_values = np.expand_dims(game_state_values, axis=0)  # Expand dims to 1, 13 tensor
                game_state_values = np.expand_dims(game_state_values, axis=0)  # Expand dims to 1, 1, 13 tensor
                prediction_values = model.predict(game_state_values)  # Retrieve array with predictions
                max_predicted_value = np.argmax(prediction_values)  # Obtain argmax index for predictions
                player.move_head_to_position(max_predicted_value, self.score)

            self.check_if_point_was_consumed()

            self.check_if_collision_happend()

            self.player.apply_body_movement()

            player.draw_nodes(screen)

            pygame.display.update()

            if self.game_ended:
                self.reset_game()

    @staticmethod
    def divisible_random(a, b, n):
        """
        Generates random number between values of 'a' and 'b', which is divisible by 'c'.
        :param a: Start value
        :param b: End value
        :param n: Value by which generated number has to be divisible by.
        :return:
        """
        if b - a < n:
            raise Exception(f"{n} is too big")
        result = random.randint(a, b)
        while result % n != 0:
            result = random.randint(a, b)
        return result

    def play_for_reinforced_learning(self, direction):
        """
        THIS IS NOT GAME LOOP FUNCTION.
        Function performs ONLY ONE move and populates the game state for the reinforced learning. Thing about this
        function as one step of the game, we need to perform action and gather game state to perform second action based
        on reward or returned penalty.
        :param direction: Direction for the snake to head for.
        :return: Sum of rewards and penalty (penalty is always negative), bool if the game has ended, and game score
        """
        self.set_clock_tick(60)

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

        return (reward + penalty, game_ended, self.score)

    @staticmethod
    def get_wall_distance_factor(x):
        """
        Takes an value of position and returns the factor of distance to the wall. Closer we are to wall, then closer
        return value to 0. Value of 1 shall be returned for the middle of the screen position.
        :param x: Position value
        :return: Value between 0 and 1
        """
        # Note, for the best usage pass normalized number
        # Returns max value 1 for middle of screen 250 ,250 after normalizing.
        # Return 0 for values close to 0 and 500
        # return 1 for values 250 and 250
        return round((-4 * (x * x)) + (4 * x), 4)
