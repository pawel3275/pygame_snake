import pygame
import random


class Score:
    point_is_visible = False
    point_position_x = 100
    point_position_y = 100

    def spawn_point(self, screen):
        if not self.point_is_visible:
            pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
            return
        self.point_position_x, self.point_position_y = pygame.display.get_surface().get_size()
        self.point_position_x = random.randint(0, self.point_position_x)
        self.point_position_y = random.randint(0, self.point_position_y)
        pygame.draw.circle(screen, (0, 255, 0), (self.point_position_x, self.point_position_y), 8, 4)
        print("Current prize at:", self.point_position_x, self.point_position_y)
        self.point_is_visible = True
