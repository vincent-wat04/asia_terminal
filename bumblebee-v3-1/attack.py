# EMP可以用于赚取structures，也是防御手段
def demolisher_line_strategy(self, units, game_state):
    """
    Build a line of the cheapest stationary unit so our demolisher can attack from long range.
    """
    if self.is_right_opening:
        game_state.attempt_spawn(units.FILTER, [[2, 13], [25, 13], [18, 11]])
        emp_location = [[4, 9]]
        remove_wall_at = [[20, 11], [21, 11]]

    else:
        game_state.attempt_spawn(units.FILTER, [[2, 13], [25, 13], [9, 11]])
        emp_location = [[23, 9]]
    
    game_state.attempt_remove(remove_wall_at)
    game_state.attempt_spawn(units.EMP, emp_location, 1000)

def set_attacker(self, units, game_state):
    max_ping_num = int(game_state.get_resource(1))//int(game_state.type_cost(units.PING)[1])
    if self.is_right_opening:
        # ping_location = [[12, 1], [11, 2]]
        ping_location = [[12, 1]]
        remove_wall_at = [[20, 11], [21, 11]]
    else:
        # ping_location = [[15, 1], [16, 2]]
        ping_location = [[15, 1]]
        remove_wall_at = []
    # game_state.attempt_spawn(units.PING, ping_location, max_ping_num//2)
    game_state.attempt_remove(remove_wall_at)
    game_state.attempt_spawn(units.PING, ping_location, max_ping_num)

def endgame_attacker(self, units, game_state):
    # speed up the attacks
    # 增加supports
    max_ping_num = int(game_state.get_resource(1))//int(game_state.type_cost(units.PING)[1])
    if game_state.turn_number % 2 == 1:
        ping_location = [[12, 1], [5, 8]]
        game_state.attempt_spawn(units.PING, ping_location, max_ping_num//2)

def endgame(game_state):
        if game_state.my_health >= 15 and game_state.enemy_health <= 8:
            return True
        return False
