"""
    MadeInDungeon.Game

This file contain game class of MadeInDungeon.
"""

""" imports """


from copy import deepcopy
from Object import Player
import create_dungeon
import Texture
from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from GameLoopEngine import GameLoop


""" Game processes """


human_play_mode: bool = True



def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map = create_dungeon.generate_dungeon(25, 20)

    if human_play_mode:
        game_loop_ = GameLoop(d_map, player)
        game_loop_.exe()
        return game_loop_.player

    player = game_loop(d_map, player)
    return  player


def print_map(d_map, player):
    _print_map = Texture.convert(deepcopy(d_map))
    _print_map[player.position[1]][player.position[0]] = "〇"
    texture = "{}" * len(d_map[0])
    [print(texture.format(*_line)) for _line in _print_map]
    print(player.position)
    return


def game_loop(d_map, player):

    print_map(d_map, player)

    done = False
    while not done:
        player.move_process(d_map, [])
        if d_map[player.position[0]][player.position[1]] == -2:
            return player

        # Enemy processes

        if player.hp <= 0:
            return player

        print_map(d_map, player)

    return


def game_process():
    player = Player((5, 5), 0, 0)
    for i in range(3):
        hierarchy_process(player)
        if player.hp <= 0:
            print("Game Over")
            break 
        else:
            print(f"{i + 1}F Clear")
    else:
        pass

    return


if __name__ == '__main__':
    game_process()
    ...
