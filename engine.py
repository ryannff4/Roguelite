import tcod as libtcod
from entity import Entity
from input_handlers import handle_keys
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap


def main():
    # define variables for the screen size
    screen_width = 80
    screen_height = 50
    # define the size of the map
    map_width = 80
    map_height = 45

    # dictionary to hold the colors being used for drawing blocked/non-blocked tiles
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),  # serve as walls outside the player's field of view
        'dark_ground': libtcod.Color(50, 50, 150)  # serve as ground outside the player's field of view
    }

    # initialize the player and an npc
    # place the player right in the middle of the screen
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    # store the npc and player in a list, which will eventually hold all entities in the map
    entities = [npc, player]

    # tell libtcod which font to use; dictate the file to read from, and the other two arguments tell libtcod which
    # type of file is being read
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen with specified width and height; title; boolean value to say full screen or not
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height)
    # initialize the game map
    game_map = GameMap(map_width, map_height)

    # variables to hold keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        # captures user input - will update the key and mouse variables with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # draw the entities and blit the changes to the screen
        render_all(con, entities, game_map, screen_width, screen_height, colors)

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

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        # checks if the key pressed was the Esc key - if it was, then exit the loop
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen((not libtcod.console_is_fullscreen()))


# run the main function when we explicitly run the script
if __name__ == '__main__':
    main()