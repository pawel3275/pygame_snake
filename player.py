import pygame


class Player:
    length = 0
    head_position_x = 0
    head_position_y = 0
    velocity = 5
    nodes = []

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
        for node in self.nodes:
            position_x, position_y = node
            pygame.draw.circle(screen, (255, 0, 0), (position_x, position_y), 8, 4)





