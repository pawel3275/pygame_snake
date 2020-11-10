import pygame
from score import Score
from data_collector import DataCollector
from game import Game


main_game = Game()
collector = DataCollector()
scoreboard = Score()

while True:
    screen = main_game.get_screen()
    player = main_game.get_player()

    for event in pygame.event.get():
        main_game.process_event(event)

    screen.fill((0, 0, 0))

    player.move_head_to_position(main_game.head_direction, main_game.score)
    player.draw_nodes(screen)

    scoreboard.spawn_point(screen)
    data_node = main_game.obtain_distances_from_head(player,
                                                     scoreboard.point_position_x,
                                                     scoreboard.point_position_y)
    collector.append_data_node(data_node)
    scoreboard.point_is_visible = main_game.check_for_point_consumption(player,
                                                                        scoreboard.point_position_x,
                                                                        scoreboard.point_position_y)
    main_game.check_for_wall_collision(player)
    main_game.check_for_body_collision(player)
    pygame.display.update()

    if main_game.game_ended:
        collector.save_data_as_csv()
        pygame.quit()

    main_game.set_clock_tick(15)


