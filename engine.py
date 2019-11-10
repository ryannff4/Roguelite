import tcod as libtcod


def main():
    # define variables for the screen size
    screen_width = 80
    screen_height = 50

    # tell libtcod which font to use; dictate the file to read from, and the other two arguments tell libtcod which
    # type of file is being read
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen with specified width and height; title; boolean value to say full screen or not
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    # game loop
    while not libtcod.console_is_window_closed():
        # set color for our @ symbol; the 0 defines the console to be drawn to
        libtcod.console_set_default_foreground(0, libtcod.white)

        # 0 defines the console to print to; next two arguments 1, 1 are the x and y coordinates
        # @ is the symbol to print, and background is sent to 'none'
        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)

        # present everything on the screen
        libtcod.console_flush()

        # gives a way to gracefully exit proram by hitting the ESC key
        # gets any keyboard input to the program and stores in the key variable
        key = libtcod.console_check_for_keypress()

        # checks if the key pressed was the Esc key - if it was, then exit the loop
        if key.vk == libtcod.KEY_ESCAPE:
            return True


# run the main function when we explicitly run the script
if __name__ == '__main__':
    main()