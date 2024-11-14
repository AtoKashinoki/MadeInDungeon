"""
    MadeInDungeon.Game

This file contain game class of MadeInDungeon.
"""
from src.create_dungeon import clear_loom

""" imports """


from copy import deepcopy
from src import create_dungeon
from src import Texture
from src.Engine import ApplicationEngine, Exit
from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from src.Object import Player, Enemy
from time import sleep


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

game_over = (
    "\n\n\n"
    "あなたは「アビス」遺物になった...\n"
    "\n\n\n"
    "[R+Enter] 新たな探索者を雇う\n"
    "[Enter] 終了\n"
)

game_clear = (
    "\n\n\n"
    "あなたは「アビス」の最果てにたどり着いた\n"
    "そこは今までの階層とは違い\n"
    "広く　そして　輝く結晶体が部屋全体を照らしている\n"
    "\n\n\n"
    "[Enter] 次へ",
    "\n\n\n"
    "ここまで長いこと暗闇で戦い続けていたため\n"
    "この部屋の静けさで安堵を覚える...\n"
    "\n\n"
    "しかし\n"
    "あなたは異様な点に気づく\n"
    "\n\n\n"
    "[Enter] 次へ",
    "\n\n\n"
    "何人もの人が潜ってきたダンジョンだが\n"
    "遺体一つなかった\n"
    "\n"
    "あったのはガラクタのような遺物ばかり\n"
    "\n"
    "これ以上「アビス」に進む道はない\n"
    "\n\n\n"
    "[Enter] 次へ",
    "\n\n\n"
    "疲れがあるあなたは目をつむる...\n"
    "\n\n\n"
    "[Enter] 次へ",
)


auto_text = (
    "",
    "",
    "",
    "",
    "",
    "次に目を開けたとき\n",
    "目に映ったのは　どこまでも続く大穴「アビス」だった\n",
    "",
    "",
    "",
    "",
    "",
    "A never ending MadeInDungeon\n",
    "",
    "",
    "",
    "",
    "",
    "Project MadeInDungeon\n",
    "泉龍真\n",
    "小松学翔\n",
    "齊藤旭宏\n",
    "柏木空翔\n",
    "",
    "",
    "",
    "",
    "",
    "Thank you for playing!!",
    "",
    "",
    "",
    "",
    "",
)

def hierarchy_process(player: Player, clear: bool = False):
    if not clear:
        # ダンジョンを生成して変数に保管
        d_map, player, enemies = create_dungeon.run(player)

        if not 2 == sum([
            d_map[y][x] in (-2, -5)
            for y in range(len(d_map))
            for x in range(len(d_map[y]))
        ]):
            hierarchy_process(player)
            return player
    else:
        d_map, player = create_dungeon.clear_loom(player)
        player.f_clear = True
        enemies = []

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

        """ player update """
        player.move_process(d_map, enemies)

        enemies = [
            enemy
            for enemy in enemies
            if enemy.hp > 0
        ]

        if d_map[player.position.y][player.position.x] in (-2, -4):
            return player

        """ enemy update """

        [enemy.move_process(d_map, player, enemies) for enemy in enemies]

        if player.hp <= 0:
            return player

        """ render """
        player.update_visibility(d_map)

        print()
        print("Dungeon map")
        print_map(player.visibility_map, player, enemies)
        print(f"{player.position=}")
        print(f"{player.hp=}")
        print()
        if player.f_get_key:
            print("Get key!")
            player.f_get_key = False
            ...
        if player.f_attack:
            print("Player attack!")
            player.f_attack = False
            if player.f_attack_hit:
                print("Hit!!")
                player.f_attack_hit = False
                ...
            ...
        for enemy in enemies:
            if enemy.f_attack:
                print("Enemy attack!!")
                enemy.f_attack = False
                ...
            ...

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
            print(game_over)
            if input() in ("R", "r"): game_process()
            break 
        else:
            print(f"\n\n\n{i + 1}F Clear\n\n\nNext floor...\n\n")
    else:
        hierarchy_process(player, True)
        for text in game_clear:
            print(text)
            input()
        for text in auto_text:
            sleep(0.8)
            print(text)
        sleep(5)
    return


if __name__ == '__main__':
    game_process()
    ...
