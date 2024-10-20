def wipe_out_structure(self, units, game_state):
    if strong_enemy_frontline_defence(self, units, game_state):
        boom_up(self, units, game_state)
    else:
        demolisher_line_strategy(self, units, game_state)

def boom_up(self, units, game_state):
    if self.is_right_opening:
        # TODO: make sure the frontline is complete
        game_state.attempt_spawn(units.FILTER, [22, 12], [5, 12], [1, 13])
        game_state.attempt_spawn(units.SCRAMBLER, [12, 1], 2)
    else:
        # TODO: make sure the frontline is complete
        game_state.attempt_spawn(units.FILTER, [22, 12], [5, 12], [26, 13])
        game_state.attempt_spawn(units.SCRAMBLER, [15, 1], 2)

# EMP可以用于赚取structures，也是防御手段
def demolisher_line_strategy(self, units, game_state):
    """
    Build a line of the cheapest stationary unit so our demolisher can attack from long range.
    """
    if self.is_right_opening:
        emp_location = [[26, 12]]
        # 先封住边界
        game_state.attempt_spawn(units.FILTER, [[1, 13], [26, 13]])
        # 增加 encryptor 支持
        game_state.attempt_spawn(units.ENCRYPTOR, [8, 9])

    else:
        emp_location = [[1, 12]]
        # 先封住边界
        game_state.attempt_spawn(units.PING, [[1, 13], [26, 13]])
        # 增加 encryptor 支持
        game_state.attempt_spawn(units.ENCRYPTOR, [19, 9])
    
    game_state.attempt_spawn(units.EMP, emp_location, 1000)

def set_attacker(self, units, game_state):
    game_state.attempt_spawn(self.units.FILTER, [[1, 13], [26, 13]])
    max_ping_num = int(game_state.get_resource(1))//int(game_state.type_cost(units.PING)[1])
    if self.is_right_opening:
        if should_attack_middle(self, units, game_state):
            filter_location = [[18, 13], [19, 13], [20, 13], [21, 13], [22, 13]]
            game_state.attempt_spawn(units.FILTER, filter_location)
            ping_location = [[15, 1], [16, 2]]
        else:
            ping_location = [[12, 1], [11, 2]]
    else:
        if should_attack_middle(self, units, game_state):
            filter_location = [[5, 13], [6, 13], [7, 13], [8, 13], [9, 13]]
            game_state.attempt_spawn(units.FILTER, filter_location)
            ping_location = [[12, 1], [11, 2]]
        else:
            ping_location = [[15, 1], [16, 2]]
    game_state.attempt_spawn(units.PING, ping_location, max_ping_num//2)

def endgame_attacker(self, units, game_state):
    # speed up the attacks
    # 增加supports
    max_ping_num = int(game_state.get_resource(1))/int(game_state.type_cost(units.PING)[1])
    if game_state.turn_number % 2 == 1:
        if self.is_right_opening:
            ping_location = [[12, 1], [5, 8]]
        else:
            ping_location = [[15, 1], [22, 8]]
        game_state.attempt_spawn(units.PING, ping_location, max_ping_num//2)

def endgame(game_state):
    if game_state.my_health >= 15 and game_state.enemy_health <= 8:
        return True
    return False

# TODO: needs to modify the condition below based on the efficiency of boom_up() combat performance

def strong_enemy_frontline_defence(self, units, game_state, weights = None):
    # 判断前线是否structure较多，在 demolisher 的垂直攻击范围内(4)
    if not weights:
        # filter is worth 1 badness pt, destructor - 6 badness pts.
        weights = [1, 6]

    weights_by_def_unit = dict(zip([units.FILTER, units.DESTRUCTOR], weights))

    frontline_strength = 0

    for location in game_state.game_map:
        if game_state.contains_stationary_unit(location):
            for unit in game_state.game_map[location]:
                if unit.player_index == 1 and (
                    unit.unit_type == units.DESTRUCTOR or unit.unit_type == units.FILTER
                ):
                    if location[1] >= 14 and location[1] <= 16:
                        frontline_strength += weights_by_def_unit[unit.unit_type]

    if frontline_strength >= 48:
        return True
    
    return False

def should_attack_middle(self, units, game_state, weights = None):
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