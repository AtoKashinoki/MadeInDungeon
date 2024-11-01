"""
    MadeInDungeon.Game

This file contain game class of MadeInDungeon.
"""


""" imports """


from copy import deepcopy
from Object import Player
import MapGenerator
import Texture


""" Game processes """



def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map =MapGenerator.test(20, 15)
    game_loop(d_map, player)

    return d_map


def game_loop(d_map, player: Player):
    done = False
    while not done:
        print_map = Texture.convert(deepcopy(d_map))
        print_map[player.position[1]][player.position[0]] = "▲"
        texture = "{}" * len(d_map[0])
        [print(texture.format(*_line)) for _line in print_map]
        print(player.position)
        player.move_process(d_map)
        if d_map[player.position[0]][player.position[1]] == 2:
            break

        # Enemy processes

        if player.hp <= 0:
            break

    return
