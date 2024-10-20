
def set_attacker(self, units, game_state):
    max_ping_num = int(game_state.get_resource(1))//int(game_state.type_cost(units.PING)[1])
    if game_state.turn_number % 3 == 1:
        ping_location = [[15, 1], [12, 1]]
        game_state.attempt_spawn(units.PING, ping_location, max_ping_num//2)

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
