import tcod as libtcod


# param: key; user input by key
# return: handle different possibilities of user actions by returning a dictionary, which the engine will read and decide what to do
def handle_keys(key):
    key_char = chr(key.c)

    # movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'i':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the game
        return {'exit': True}

    # no key was pressed, return an empty dictionary
    return {}