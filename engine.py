import tcod as libtcod
from entity import Entity, get_blocking_entities_at_location
from game_messages import MessageLog
from input_handlers import handle_keys
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player


def main():
    # define variables for the screen size
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # define the size of the map
    map_width = 80
    map_height = 43

    # set the max and min size of the rooms, along with the max number of rooms one floor can have
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0  # default algorithm that libtcod uses
    fov_light_walls = True  # dictates whether or not to "light up" the walls seen
    fov_radius = 10

    max_monsters_per_room = 3

    # dictionary to hold the colors being used for drawing blocked/non-blocked tiles
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),  # serve as walls outside the player's field of view
        'dark_ground': libtcod.Color(50, 50, 150),  # serve as ground outside the player's field of view
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)

    # initialize the player and an npc
    # place the player right in the middle of the screen
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    # store the npc and player in a list, which will eventually hold all entities in the map
    entities = [player]

    # tell libtcod which font to use; dictate the file to read from, and the other two arguments tell libtcod which
    # type of file is being read
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen with specified width and height; title; boolean value to say full screen or not
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height)

    # create a new console to hold the HP bar and message log
    panel = libtcod.console_new(screen_width, panel_height)

    # initialize the game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    # dictates if need to recompute the field of view
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    # variables to hold keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # game loop
    while not libtcod.console_is_window_closed():
        # captures user input - will update the key and mouse variables with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # draw the entities and blit the changes to the screen
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, colors)

        fov_recompute = False

        # present everything on the screen
        libtcod.console_flush()

        # clear entities after drawing to screen - this makes it so that when entities move, they do not leave a trail behind
        clear_all(con, entities)

        # gives a way to gracefully exit proram by hitting the ESC key
        # gets any keyboard input to the program and stores in the key variable
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # move the player only on the players turn
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move

            # get destination of player's movement
            destination_x = player.x + dx
            destination_y = player.y + dy

            # check if there is something at the destination that would block the player - if not, move the player there
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                # change to enemy's turn after player's move
                game_state = GameStates.ENEMY_TURN

        # checks if the key pressed was the Esc key - if it was, then exit the loop
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen((not libtcod.console_is_fullscreen()))

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            # note that this is a for-else statement; without a break statement, this else will always happen
            else:
                game_state = GameStates.PLAYERS_TURN


# run the main function when we explicitly run the script
if __name__ == '__main__':
    main()