import pygame


class Player:
    length = 0
    head_position_x = 0
    head_position_y = 0
    velocity = 5
    nodes = []

    body_distances = {"top": -1,
                      "bottom": 1,
                      "left": -1,
                      "right": 1}

    def __init__(self, head_start_position_x, head_start_position_y):
        self.head_position_x = head_start_position_x
        self.head_position_y = head_start_position_y
        self.nodes.append((head_start_position_x, head_start_position_y))

    def move_head_to_position(self, direction, score):
        if len(self.nodes) <= score:
            self.nodes.append((self.head_position_x, self.head_position_y))

        if direction is "UP":
            self.head_position_y = self.head_position_y - self.velocity

        if direction is "DOWN":
            self.head_position_y = self.head_position_y + self.velocity

        if direction is "LEFT":
            self.head_position_x = self.head_position_x - self.velocity

        if direction is "RIGHT":
            self.head_position_x = self.head_position_x + self.velocity

        for iterator in reversed(range(0, len(self.nodes))):
            pos_before_movement_x, pos_before_movement_y = self.nodes[iterator - 1]
            self.nodes[iterator] = pos_before_movement_x, pos_before_movement_y

        self.nodes[0] = (self.head_position_x, self.head_position_y)

    def draw_nodes(self, screen):
        self.body_distances["top"] = -1
        self.body_distances["bottom"] = 1
        self.body_distances["left"] = -1
        self.body_distances["right"] = 1

        for node in self.nodes:
            position_x, position_y = node
            if position_x == self.head_position_x or position_y == self.head_position_y:
                self.populate_vectors_in_respect_to_head(position_x, position_y)

            pygame.draw.circle(screen, (255, 0, 0), (position_x, position_y), 8, 4)

    def populate_vectors_in_respect_to_head(self, position_x, position_y):
        # TODO: refacor this function and closest_hit parameters, if they will take effect during training.
        vertical = (position_y - self.head_position_y) / 500
        horizontal = (position_x - self.head_position_x) / 500

        if horizontal == 0 and vertical == 0:
            return

        if horizontal == 0 and 0 > vertical > self.body_distances["top"]:  # node on the top
            self.body_distances["top"] = vertical
            return

        if horizontal == 0 and 0 < vertical < self.body_distances["bottom"]:  # node on the bottom
            self.body_distances["bottom"] = vertical
            return

        if vertical == 0 and 0 > horizontal > self.body_distances["left"]:  # node on the left
            self.body_distances["left"] = horizontal
            return

        if vertical == 0 and 0 < horizontal < self.body_distances["right"]:  # node on the right
            self.body_distances["right"] = horizontal
            return
