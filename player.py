import pygame


class Player:
    def __init__(self, head_start_position_x, head_start_position_y):
        self.length = 0
        self.velocity = 5
        self.nodes = []
        self.head_position_x = head_start_position_x
        self.head_position_y = head_start_position_y
        self.nodes.append((head_start_position_x, head_start_position_y))

    def move_head_to_position(self, direction, score):
        if len(self.nodes) <= score:
            self.nodes.append((self.head_position_x, self.head_position_y))

        if direction is 0:
            self.head_position_y = self.head_position_y - self.velocity

        if direction is 1:
            self.head_position_y = self.head_position_y + self.velocity

        if direction is 2:
            self.head_position_x = self.head_position_x - self.velocity

        if direction is 3:
            self.head_position_x = self.head_position_x + self.velocity

    def apply_body_movement(self):
        for iterator in reversed(range(0, len(self.nodes))):
            self.nodes[iterator] = self.nodes[iterator - 1]

        self.nodes[0] = (self.head_position_x, self.head_position_y)

    def draw_nodes(self, screen):
        for node in self.nodes:
            position_x, position_y = node
            pygame.draw.circle(screen, (255, 0, 0), (position_x, position_y), 8, 4)

