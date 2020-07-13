import tcod as libtcod

from components.inventory import Inventory
from entity import Entity, get_blocking_entities_at_location
from game_messages import MessageLog, Message
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
    max_items_per_room = 2

    # dictionary to hold the colors being used for drawing blocked/non-blocked tiles
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),  # serve as walls outside the player's field of view
        'dark_ground': libtcod.Color(50, 50, 150),  # serve as ground outside the player's field of view
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    # initialize the player and an npc
    # place the player right in the middle of the screen
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
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
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)

    # dictates if need to recompute the field of view
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    # variables to hold keyboard and mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    # game loop
    while not libtcod.console_is_window_closed():
        # captures user input - will update the key and mouse variables with what the user inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # draw the entities and blit the changes to the screen - only render the item inventory when the game state is in the inventory state
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)

        fov_recompute = False

        # present everything on the screen
        libtcod.console_flush()

        # clear entities after drawing to screen - this makes it so that when entities move, they do not leave a trail behind
        clear_all(con, entities)

        # gives a way to gracefully exit proram by hitting the ESC key
        # gets any keyboard input to the program and stores in the key variable
        action = handle_keys(key, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
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

        # if the player did not move and performed the pickup action by pressing the key 'g'...
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            # loop through each entity on the map, check if it is an item and occupies the same space as the player
            for entity in entities:
                # if the entity is an item and in the same position as the player
                if entity.item and entity.x == player.x and entity.y == player.y:
                    # add the item to the inventory and append the results to player_turn_results
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break # makes it so the player only picks up one item at a time
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # take the index selected, use the item selected
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # checks if the key pressed was the Esc key - if it was, then exit the loop
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen((not libtcod.console_is_fullscreen()))

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

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