import pygame
from player import Player
from score import Score

width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.head_direction = "UP"

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

    @staticmethod
    def check_for_point_consumption(player_position_x, player_position_y, point_position_x, point_position_y):
        scale_factor = 8
        player_position_x_upper = player_position_x + scale_factor
        player_position_x_lower = player_position_x - scale_factor

        player_position_y_upper = player_position_y + scale_factor
        player_position_y_lower = player_position_y - scale_factor

        if point_position_x < player_position_x_upper and point_position_x > player_position_x_lower and point_position_y < player_position_y_upper and point_position_y > player_position_y_lower:
            print("Point has been consumed")
            return True
        else:
            return False


p1 = Player(int(width / 2), int(height / 2))
main_game = Game()
scoreboard = Score()
while True:
    for event in pygame.event.get():
        main_game.process_event(event)

    screen.fill((0, 0, 0))
    p1.move_head_to_position(main_game.head_direction)
    p1.draw_head(screen)

    scoreboard.spawn_point(screen)
    scoreboard.point_is_visible = Game.check_for_point_consumption(p1.head_position_x, p1.head_position_y, scoreboard.point_position_x, scoreboard.point_position_y)
    pygame.display.update()

    clock.tick(40)



