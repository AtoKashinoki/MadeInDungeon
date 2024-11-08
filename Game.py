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


""" Game processes """



def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map = create_dungeon.generate_dungeon(25, 20)
    game_loop = GameLoop(d_map, player)
    player = game_loop.exe()
    return  player


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

        self.player.move_process(self.d_map)
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


if __name__ == '__main__':
    hierarchy_process(Player((0, 0), 0, 0))
    ...
