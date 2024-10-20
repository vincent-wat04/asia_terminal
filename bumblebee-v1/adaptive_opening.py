import random
from operator import itemgetter


"""
Adaptive defence
Assesses the enemy's defence and decides which side of the wall should
have an opening so that our EMPs attack weaker side.
"""


def build_defences_with_adaptive_opening(
    game_state, units, is_right_opening, filter_locs
):

    # Place destructors that attack enemy units
    # 下面的 destructor_locations 是基本保障   共 32 SPs
    basic_destructor_locations = [[0, 13], [3, 10], [4, 12], [7, 9], [20, 9], [23, 12], [24, 10], [27, 13]]
    game_state.attempt_spawn(units.DESTRUCTOR, basic_destructor_locations)
    save_cores = False

    # Save up cores until all wall-destructors are built
    if not all(map(game_state.contains_stationary_unit, basic_destructor_locations)):
        save_cores = True

    # if game_state.turn_number < 4:
    #     return [], True, save_cores, basic_destructor_locations

    # Find the weaker side of enemy's defence
    # Open up wall defence towards that side

    final_filter_locs = list(filter_locs)

    if game_state.turn_number % 4 == 0:
        is_right_opening = should_right_be_open(game_state, units)

    if is_right_opening:
        remove_filter_at = [[26, 13], [22, 12], [18, 13], [19, 13], [20, 13], [21, 13], [22, 13]] # 2 holes and line of walls
        final_filter_locs.extend([[1, 13], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13]])

    else:
        remove_filter_at = [[1, 13], [5, 12], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13]] # 2 holes and line of walls
        final_filter_locs.extend([[26, 13], [18, 13], [19, 13], [20, 13], [21, 13], [22, 13]])

    game_state.attempt_remove(remove_filter_at)

    final_filter_locs.sort(key=itemgetter(0), reverse=(not is_right_opening))

    game_state.attempt_spawn(units.FILTER, final_filter_locs)

    # upgrade the wall at the hole, done in defence (round >= 1)

    # then upgrade the destructors (round >= 1)
    return final_filter_locs, is_right_opening, save_cores, basic_destructor_locations
    


"""
Assess enemy defence & identify weaker side (for opening)
Author @RKJ (blame me for the mistakes)
"""


def should_right_be_open(game_state, units, weights=None):
    if not weights:
        # filter is worth 1 badness pt, destructor - 6 badness pts.
        weights = [1, 6]

    weights_by_def_unit = dict(zip([units.FILTER, units.DESTRUCTOR], weights))

    left_strength, right_strength = (0, 0)

    for location in game_state.game_map:
        if game_state.contains_stationary_unit(location):
            for unit in game_state.game_map[location]:
                if unit.player_index == 1 and (
                    unit.unit_type == units.DESTRUCTOR or unit.unit_type == units.FILTER
                ):
                    if location[0] < 10:
                        left_strength += weights_by_def_unit[unit.unit_type]
                    elif location[0] > 17:
                        right_strength += weights_by_def_unit[unit.unit_type]

    # Return side with less strength
    if left_strength > right_strength:
        right = True
    elif left_strength < right_strength:
        right = False
    else:
        right = bool(random.randint(0, 1))
    return right
