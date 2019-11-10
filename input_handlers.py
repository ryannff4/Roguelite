import tcod as libtcod


# param: key; user input by key
# return: handle different possibilities of user actions by returning a dictionary, which the engine will read and decide what to do
def handle_keys(key):
    # movement keys
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move':(0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move':(-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move':(1, 0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the game
        return {'exit': True}

    # no key was pressed, return an empty dictionary
    return {}