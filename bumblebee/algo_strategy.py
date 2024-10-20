import json
import math
import random
import warnings
from collections import namedtuple
from sys import maxsize

import gamelib
from adaptive_opening import build_defences_with_adaptive_opening
from defence import build_defences
from attack import endgame, set_attacker, endgame_attacker


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

        # walls 在opening前要保持
        # 24 SPs required
        # 不用放满  两边都可以留空  因为第一轮只有墙也只能挨打，放了也白放；第一轮结束掌握攻击方向后再放另一侧的墙，同时布满destructor
        self.filter_locs = [
            [2, 13],
            [3, 13],
            [4, 13],
            [5, 12],
            [6, 11],
            [7, 10],
            [8, 10],
            [9, 10],
            [10, 10],
            [11, 10],
            [12, 10],
            [13, 10],
            [14, 10],
            [15, 10],
            [16, 10],
            [17, 10],
            [18, 10],
            [19, 10],
            [20, 10],
            [21, 11],
            [22, 12],
            [23, 13],
            [24, 13],
            [25, 13],
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
            f"Performing turn {game_state.turn_number} of Snorkeldink-V69 algo strategy"
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
            game_state, self.units, self.is_right_opening, self.filter_locs
        )

        if game_state.turn_number >= 1:
            # if not endgame():
            # Defence
            if not save_cores:
                build_defences(
                    game_state, self.units, self.is_right_opening, filter_locs, basic_destructor_locations
                )

            # else:
            #     build_aiding_defences()



            # Offense
            if not endgame(game_state):
                set_attacker(self, self.units, game_state)
            else:
                endgame_attacker(self, self.units, game_state)
            # if self.is_right_opening:
            #     emp_location = [[4, 9]]
            # else:
            #     emp_location = [[23, 9]]
            # game_state.attempt_spawn(EMP, emp_location, 1000)


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


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
