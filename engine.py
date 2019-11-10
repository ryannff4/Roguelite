import tcod as libtcod
from input_handlers import handle_keys


def main():
    # define variables for the screen size
    screen_width = 80
    screen_height = 50

    # place the player right in the middle of the scren
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # tell libtcod which font to use; dictate the file to read from, and the other two arguments tell libtcod which
    # type of file is being read
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen with specified width and height; title; boolean value to say full screen or not
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height)

    # variables to hold keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        # captures user input - will update the key and mouse variables with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # choose the con variable as the console; set color for our @ symbol;
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)



        # con defines the console to print to; next two arguments are the x and y coordinates
        # background is sent to 'none'
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        # present everything on the screen
        libtcod.console_flush()

        # gives a way to gracefully exit proram by hitting the ESC key
        # gets any keyboard input to the program and stores in the key variable
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        # checks if the key pressed was the Esc key - if it was, then exit the loop
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen((not libtcod.console_is_fullscreen()))


# run the main function when we explicitly run the script
if __name__ == '__main__':
    main()