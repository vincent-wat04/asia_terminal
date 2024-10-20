import random
from operator import itemgetter
import gamelib


"""
Adaptive defence
Assesses the enemy's defence and decides which side of the wall should
have an opening so that our EMPs attack weaker side.
"""


def build_defences_with_adaptive_opening(
    game_state, units, is_right_opening, filter_locs, core_filter_locs
):

    # Place destructors that attack enemy units
    # 下面的 destructor_locations 是基本保障   共 32 SPs
    opening_destructor_locations = [[4, 12], [10, 11], [17, 11], [23, 12]]
    game_state.attempt_spawn(units.DESTRUCTOR, opening_destructor_locations)
    game_state.attempt_upgrade(opening_destructor_locations)

    save_cores = False

    basic_destructor_locations = [[0, 13], [27, 13]]
    game_state.attempt_spawn(units.DESTRUCTOR, basic_destructor_locations)

    # Save up cores until all wall-destructors are built
    fixed_destructor_locations = opening_destructor_locations + basic_destructor_locations
    if not all(map(game_state.contains_stationary_unit, fixed_destructor_locations)):
        save_cores = True

    # 以下代码使得destructor会优先于wall放置，实际应先有wall
    # if game_state.turn_number < 4:
    #     return [], True, save_cores, basic_destructor_locations

    # Find the weaker side of enemy's defence
    # Open up wall defence towards that side

    final_filter_locs = list(filter_locs)

    final_filter_locs.sort(key=itemgetter(0), reverse=(not is_right_opening))

    game_state.attempt_spawn(units.FILTER, final_filter_locs)

    if not all(map(game_state.contains_stationary_unit, fixed_destructor_locations)):
        game_state.attempt_upgrade(core_filter_locs)

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

def should_attack_middle(units, game_state, weights = None):
    if not weights:
        # filter is worth 1 badness pt, destructor - 6 badness pts.
        weights = [1, 6]

    weights_by_def_unit = dict(zip([units.FILTER, units.DESTRUCTOR], weights))

    middle_strength = 0
    for location in game_state.game_map:
        if game_state.contains_stationary_unit(location):
            for unit in game_state.game_map[location]:
                if unit.player_index == 1 and (
                    unit.unit_type == units.DESTRUCTOR or unit.unit_type == units.FILTER
                ):
                    if location[0] >= 10 and location[0] <= 18:
                        middle_strength += weights_by_def_unit[unit.unit_type]

    if middle_strength <= 20:
        return True
    
    return False