import pygame
from player import Player

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
            print("Direction UP")
            self.head_direction = "UP"
            return

        if key[pygame.K_s]:
            print("Direction DOWN")
            self.head_direction = "DOWN"
            return

        if key[pygame.K_a]:
            print("Direction LEFT")
            self.head_direction = "LEFT"
            return

        if key[pygame.K_d]:
            print("Direction RIGHT")
            self.head_direction = "RIGHT"
            return


p1 = Player(int(width/2), int(height/2))
main_game = Game()
while True:
    for event in pygame.event.get():
        main_game.process_event(event)

    screen.fill((0, 0, 0))
    p1.move_head_to_position(main_game.head_direction)
    p1.draw_head(screen)
    pygame.display.update()

    clock.tick(40)



