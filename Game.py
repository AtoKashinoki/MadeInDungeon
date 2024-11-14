"""
    MadeInDungeon.Game

This file contain game class of MadeInDungeon.
"""

""" imports """


from copy import deepcopy
from Object import Player
import create_dungeon
import Texture
from Engine import ApplicationEngine, Exit
from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from Object import Player, Enemy


""" Game processes """



def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map, player, enemies = create_dungeon.run(player)
    enemies = [enemies[0], ]
    player = game_loop(d_map, player, enemies)
    return  player


def print_map(d_map, player, enemies):
    create_dungeon.display_dungeon(d_map, player, enemies)
    # _print_map = Texture.convert(deepcopy(d_map))
    # _print_map[player.position[1]][player.position[0]] = "〇"
    # texture = "{}" * len(d_map[0])
    # [print(texture.format(*_line)) for _line in _print_map]
    # print(player.position)
    return


def game_loop(d_map, player, enemies: list[Enemy]):

    print_map(d_map, player, enemies)

    done = False
    while not done:
        player.move_process(d_map, enemies)
        if d_map[player.position.y][player.position.x] == -2:
            return player

        [enemy.move_process(d_map, player, enemies) for enemy in enemies]

        if player.hp <= 0:
            return player

        print_map(d_map, player, enemies)

    return


class GameLoop(ApplicationEngine):
    def __init__(self, d_map, player):
        super().__init__()
        self.d_map = d_map
        self.player = player
        self.game_over = False
        return

    def __update__(self):
        if Key.Ins in self.input: self.reboot()
        if Key.Del in self.input: raise Exit

        self.player.move_process(self.d_map, [])
        if self.d_map[self.player.position[0]][self.player.position[1]] == -2:
            raise Exit

        # Enemy processes

        if self.player.hp <= 0:
            raise Exit

        return

    def __rendering__(self):
        player = self.player
        print_map = Texture.convert(deepcopy(self.d_map))
        print_map[player.position[1]][player.position[0]] = "〇"
        texture = "{}" * len(self.d_map[0])
        [self.print(texture.format(*_line)) for _line in print_map]
        self.print(player.position)
        return

    ...


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
