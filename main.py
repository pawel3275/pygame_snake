import pygame
from player import Player
from score import Score

width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

movement_coords_history = []


class Game:
    def __init__(self):
        self.head_direction = "UP"
        self.score = 0

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
            print("GAME ENDED")
            print("Score:", self.score)

        if player.head_position_y <= 0 or player.head_position_y >= 500:
            print("GAME ENDED")
            print("Score:", self.score)

        pass

    def check_for_body_collision(self, player):
        for iterator in range(1, len(player.nodes)):
            node_position_x, node_position_y = player.nodes[iterator]

            if player.head_position_x == node_position_x and player.head_position_y == node_position_y:
                print("Head Collided with: ", iterator, node_position_x, node_position_y)
                print("GAME ENDED YOU ATE YOURSELF")
                print("Score:", self.score)

        pass


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
    scoreboard.point_is_visible = main_game.check_for_point_consumption(p1,
                                                                        scoreboard.point_position_x,
                                                                        scoreboard.point_position_y)
    main_game.check_for_wall_collision(p1)
    main_game.check_for_body_collision(p1)
    pygame.display.update()

    clock.tick(15)
