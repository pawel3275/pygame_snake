import pygame


width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

global circle_position
circle_position = (int(width/2), int(height/2))
global velocity
velocity = 5
global direction
direction = "UP"


def process_event(event):
    if event.type is pygame.QUIT:
        pygame.quit()

    key = pygame.key.get_pressed()

    global direction
    if key[pygame.K_w]:
        print("Direction UP")
        direction = "UP"
        return

    if key[pygame.K_s]:
        print("Direction DOWN")
        direction = "DOWN"
        return

    if key[pygame.K_a]:
        print("Direction LEFT")
        direction = "LEFT"
        return

    if key[pygame.K_d]:
        print("Direction RIGHT")
        direction = "RIGHT"
        return


def handle_direction():
    global direction
    global circle_position
    circle_position_x, circle_position_y = circle_position
    if direction is "UP":
        circle_position = circle_position_x, circle_position_y - velocity

    if direction is "DOWN":
        circle_position = circle_position_x, circle_position_y + velocity

    if direction is "LEFT":
        circle_position = circle_position_x - velocity, circle_position_y

    if direction is "RIGHT":
        circle_position = circle_position_x + velocity, circle_position_y


while True:
    for event in pygame.event.get():
        process_event(event)

    screen.fill((0, 0, 0))
    handle_direction()
    pygame.draw.circle(screen, (255, 0, 0), circle_position, 3, 2)
    pygame.display.update()

    clock.tick(40)



