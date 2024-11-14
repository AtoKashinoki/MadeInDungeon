"""
    MadeInDungeon.Game

This file contain game class of MadeInDungeon.
"""

""" imports """


from copy import deepcopy
from src import create_dungeon
from src import Texture
from src.Engine import ApplicationEngine, Exit
from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from src.Object import Player, Enemy


""" Game processes """


start_text = (
    "\n\n\n"
    "~~MadeInDungeon~~\n"
    "\n\n"
    "セカイに突然現れたダンジョン「アビス」\n"
    "「アビス」には不思議な力を持つ遺物が眠っているとされ\n"
    "多くの探索家がこのダンジョンに潜っていった\n"
    "しかし\n"
    "その最果てからの帰還者はいまだにいない\n"
    "\n"
    "あなたは「アビス」に挑戦する新たな探索家として立ち上がる...\n"
    "\n\n\n"
    "[Enter] 次へ"
)

rule = (
    "\n\n\n"
    "移動 -> wasdキー（小文字入力）\n"
    "   移動は斜めも可 （「wa」など）\n"
    "攻撃 -> WASDキー（大文字入力）\n"
    "\n\n\n"
    "[Enter] 「アビス」に潜る"
)

def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map, player, enemies = create_dungeon.run(player)

    if not 2 == sum([
        d_map[y][x] in (-2, -5)
        for y in range(len(d_map))
        for x in range(len(d_map[y]))
    ]):
        hierarchy_process(player)
        return player

    player = game_loop(d_map, player, enemies)
    return  player


def print_map(_map, player, enemies):
    create_dungeon.display_dungeon(_map, player, enemies)
    # _print_map = Texture.convert(deepcopy(d_map))
    # _print_map[player.position[1]][player.position[0]] = "〇"
    # texture = "{}" * len(d_map[0])
    # [print(texture.format(*_line)) for _line in _print_map]
    # print(player.position)
    return


def game_loop(d_map, player: Player, enemies: list[Enemy]):
    player.reset_visibility(d_map)
    player.update_visibility(d_map)

    print_map(player.visibility_map, player, enemies)

    done = False
    while not done:
        player.move_process(d_map, enemies)

        enemies = [
            enemy
            for enemy in enemies
            if enemy.hp > 0
        ]

        if d_map[player.position.y][player.position.x] == -2:
            return player

        [enemy.move_process(d_map, player, enemies) for enemy in enemies]

        if player.hp <= 0:
            return player

        player.update_visibility(d_map)
        print_map(player.visibility_map, player, enemies)
        print(f"{player.position=}")
        print(f"{player.hp=}")

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
    print(start_text, end="")
    input()
    print(rule, end="")
    input()
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
