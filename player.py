import pygame


class Player:
    length = 0
    head_position_x = 0
    head_position_y = 0
    velocity = 5

    def __init__(self, head_start_position_x, head_start_position_y):
        self.head_position_x = head_start_position_x
        self.head_position_y = head_start_position_y

    def move_head_to_position(self, direction):
        if direction is "UP":
            self.head_position_y = self.head_position_y - self.velocity

        if direction is "DOWN":
            self.head_position_y = self.head_position_y + self.velocity

        if direction is "LEFT":
            self.head_position_x = self.head_position_x - self.velocity

        if direction is "RIGHT":
            self.head_position_x = self.head_position_x + self.velocity

    def draw_head(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.head_position_x, self.head_position_y), 8, 4)
