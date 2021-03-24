import pygame


class Player:
    def __init__(self, head_start_position_x, head_start_position_y):
        """
        Default constructor for the player (snake)
        :param head_start_position_x: Position X where head shall be drawn.
        :param head_start_position_y: Position Y where head shall be drawn.
        """
        self.length = 0
        self.velocity = 5
        self.nodes = []
        self.head_position_x = head_start_position_x
        self.head_position_y = head_start_position_y
        self.nodes.append((head_start_position_x, head_start_position_y))

    def move_head_to_position(self, direction, score):
        """
        Moves head to a given position depending on direction and player velocity. If we detect that score has increased
        we additionally append new node to the old head position as a new part of snake body.
        :param direction: Head direction.
        :param score: Current game score.
        """
        if len(self.nodes) <= score:
            self.nodes.append((self.head_position_x, self.head_position_y))

        if direction == 0:  # UP
            self.head_position_y = self.head_position_y - self.velocity

        if direction == 1:  # DOWN
            self.head_position_y = self.head_position_y + self.velocity

        if direction == 2:  # LEFT
            self.head_position_x = self.head_position_x - self.velocity

        if direction == 3:  # RIGHT
            self.head_position_x = self.head_position_x + self.velocity

    def apply_body_movement(self):
        """
        Updates each snake body part by moving nodes (counting from last) to be in a position of a node-1, until it
        reaches the head,
        """
        for iterator in reversed(range(0, len(self.nodes))):
            self.nodes[iterator] = self.nodes[iterator - 1]

        self.nodes[0] = (self.head_position_x, self.head_position_y)

    def draw_nodes(self, screen):
        """
        Draws nodes on a game board as red circles.
        :param screen: Screen with the game board.
        """
        for node in self.nodes:
            position_x, position_y = node
            pygame.draw.circle(screen, (255, 0, 0), (position_x, position_y), 8, 4)
