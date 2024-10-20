import json
import math
import random
import warnings
from collections import namedtuple
from sys import maxsize
import copy

import gamelib
from adaptive_opening import build_defences_with_adaptive_opening, should_right_be_open, should_attack_middle
from defence import build_defences
from attack import endgame, set_attacker, endgame_attacker, demolisher_line_strategy


"""
Strategy-code for the final version of Snorkeldink-V69
"""


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write("Random seed: {}".format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES
        # wall, support, turret, scout, demolisher, interceptor
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        # Initial setup
        Units = namedtuple("Units", "FILTER ENCRYPTOR DESTRUCTOR PING EMP SCRAMBLER")
        self.units = Units(FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER)

        # Initially assume right side is vulnerable
        self.is_right_opening = True

        self.frontier_filter_locs = [
            [1, 13],
            [2, 13],
            [3, 13],
            [4, 13],
            [5, 12],
            [6, 11],
            [7, 11],
            [8, 11],
            [11, 11],
            [12, 11],
            [13, 11],
            [14, 11],
            [15, 11],
            [16, 11],
            [18, 11],
            [19, 11],
            [20, 11],
            [21, 11],
            [22, 12],
            [23, 13],
            [24, 13],
            [25, 13],
            [26, 13],
        ]

        self.core_filter_locs = [
            [1, 13],
            [3, 13],
            [4, 13],
            [6, 11],
            [7, 11],
            [8, 11],
            [23, 13],
            [24, 13],
            [26, 13],
            [19, 11],
            [20, 11],
            [21, 11],
        ]

        # walls 在opening前要保持
        # 24 SPs required
        # 不用放满  两边都可以留空  因为第一轮只有墙也只能挨打，放了也白放；第一轮结束掌握攻击方向后再放另一侧的墙，同时布满destructor
        self.filter_locs = [
            [1, 13],
            [3, 13],
            [4, 13],
            [5, 12],
            [6, 11],
            [7, 11],
            [8, 11],
            [10, 11],
            [11, 11],
            [12, 11],
            [13, 11],
            [14, 11],
            [15, 11],
            [16, 11],
            [17, 11],
            [19, 11],
            [20, 11],
            [21, 11],
            [22, 12],
            [23, 13],
            [24, 13],
            [26, 13],
        ]

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write(
            f"Performing turn {game_state.turn_number} of bumblebee-v2 algo strategy"
        )

        # Comment or remove this line to enable warnings.
        game_state.suppress_warnings(True)

        # Calculate next moves based on strategy
        self.strategy(game_state)

        # Submit the moves
        game_state.submit_turn()

    def strategy(self, game_state):

        # Initial wall defence
        # Adaptive opening side selection

        # opening 时只有防御 不会进攻 同时通过
        # 先全部建成walls 然后
        filter_locs, self.is_right_opening, save_cores, basic_destructor_locations = build_defences_with_adaptive_opening(
            game_state, self.units, self.is_right_opening, self.filter_locs, self.core_filter_locs
        )

        if game_state.turn_number >= 1:
            # 攻击在前，因为攻击会用到SPs
            # Offense
            if endgame(game_state):
                endgame_attacker(self, self.units, game_state)

            else:
                # 以下是每4轮判断一次
                if game_state.turn_number % 4 == 0:
                    is_right_opening = should_right_be_open(game_state, self.units)

                    if is_right_opening:
                        remove_filter_at = [[9, 11]]

                    else:
                        remove_filter_at = [[18, 11]]

                    # # 造成拥堵 -> 使得SCRAMBLER self-destruct
                    # game_state.attempt_spawn(units.SCRAMBLER, [12, 1], num = 2)

                    game_state.attempt_remove(remove_filter_at)


                if game_state.turn_number % 4 == 1:
                    demolisher_line_strategy(self, self.units, game_state)
                    
                if game_state.turn_number % 4 == 2:
                    # self.is_right_opening = should_right_be_open(game_state, self.units)
                    # if self.is_right_opening:
                    #     if should_attack_middle:
                    #         game_state.attempt_remove([9, 11])
                    #     else:
                    #         game_state.attempt_remove([25, 13])
                    # else:
                    #     if should_attack_middle:
                    #         game_state.attempt_remove([18, 11])
                    #     else:
                    #         game_state.attempt_remove([2, 13])
                    self.best_attack_point = self.least_damage_spawn_location(game_state, self.frontier_filter_locs)
                    game_state.attempt_remove(self.best_attack_point)

                if game_state.turn_number % 4 == 3:
                    #TODO: 最好改成 spawn 把 frontier 全部封上
                    # if should_right_be_open(game_state, self.units):
                    #     if should_attack_middle:
                    #         game_state.attempt_spawn(self.units.FILTER, [[25, 13], [18, 11], [2, 13]]) 
                    #     else:
                    #         game_state.attempt_spawn(self.units.FILTER, [[9, 11], [18, 11], [2, 13]])  
                    # else:
                    #     if should_attack_middle:
                    #         game_state.attempt_spawn(self.units.FILTER, [[9, 11], [25, 13], [2, 13]]) 
                    #     else:
                    #         game_state.attempt_spawn(self.units.FILTER, [[9, 11], [25, 13], [2, 13]])   
                    self.attack_frontier = [loc for loc in self.frontier_filter_locs if loc != self.best_attack_point]
                    game_state.attempt_spawn(self.units.PING, self.attack_frontier)
                    set_attacker(self, self.units, game_state)
            
            # Defence
            if not save_cores:
                build_defences(
                    game_state, self.units, self.is_right_opening, filter_locs, basic_destructor_locations
                )

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if (
                        unit.player_index == 1
                        and (unit_type is None or unit.unit_type == unit_type)
                        and (valid_x is None or location[0] in valid_x)
                        and (valid_y is None or location[1] in valid_y)
                    ):
                        total_units += 1
        return total_units
    
    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            # 创建 game_state 的副本
            copied_game_state = copy.deepcopy(game_state)
        
            # 移除副本中该位置的静态单位
            if copied_game_state.contains_stationary_unit(location):
                copied_game_state.game_map.remove_unit(location)  # 手动将位置置空

            path = copied_game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage_i
            damages.append(damage)

        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
