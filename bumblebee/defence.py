"""
Defensive part of Snorkeldink strategy
第四轮开始的防御策略
"""

def build_defences(game_state, units, is_right_opening, filter_locs, basic_destructor_locations):

    # Encryptors
    encryptor_locations = [[13, 2], [14, 2]]
    game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)

    # 先考虑增加 support 的数量
    # # Upgrade encryptors
    # game_state.attempt_upgrade(encryptor_locations)

    # first upgrade the existing basic destructors
    game_state.attempt_upgrade(basic_destructor_locations)


    # More destructors around hole/opening
    opening_destructor_locations = (
        [[2, 16], [5, 11]]  # 自己定
        if is_right_opening
        else [[25, 16], [22, 11]]    # 自己定
    )
    game_state.attempt_spawn(units.DESTRUCTOR, opening_destructor_locations)

    # Two more encryptors
    encryptor_locations = [[13, 3], [14, 3]]
    game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)
    game_state.attempt_upgrade(encryptor_locations)

    # Upgrade filter wall if additional destructors are added
    # TODO: upgrade only some of the filters
    # 需要增加 根据地方的攻击信息来决定升级 filter_locs 的顺序
    if all(map(game_state.contains_stationary_unit, opening_destructor_locations)):
        game_state.attempt_upgrade(filter_locs)

    # upgrade the opening_destructor_locations
    game_state.attempt_upgrade(opening_destructor_locations)

    # # Center Destructors
    # destructor_locations = [
    #     [17, 11],
    #     [6, 8],
    #     [10, 11],
    #     [15, 9],
    #     [12, 9],
    #     [15, 6],
    #     [12, 6],
    # ]
    # game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

    # Upgrade destructors in the back
    # game_state.attempt_upgrade([[3, 10], [24, 10]])


# def build_aiding_defences():
    # change the priority: lean towards the support, less wall, only upgrade some of the destructors
