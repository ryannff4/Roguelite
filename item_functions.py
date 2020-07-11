import tcod as libtcod

from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]    # take the entity using the item as the first argument
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False,
                        'message': Message('You are already at full health', libtcod.yellow)
                        })
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True,
                        'message': Message('Your wounds start to feel better!')
                        })
    return results
