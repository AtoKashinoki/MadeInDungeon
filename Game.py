from Object import Player
from copy import deepcopy


def create_map(_mx, _my):
    dungeon_map = [
        [
            0 if 0 < x < _mx-1 and 0 < y < _my-1 else 1
            for x in range(_mx)
        ]
        for y in range(_my)
    ]
    dungeon_map[5][5] = 2

    return dungeon_map


def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map = create_map(20, 15)
    game_loop(d_map, player)

    return d_map


def convert_texture(_map: list[list[int]]) -> list[list[str]]:
    return [
        [
            "　" if d == 0 else
            " ◰" if d == 2 else
            "🔲"
            for d in line
        ]
        for line in _map
    ]


def game_loop(d_map, player: Player):
    done = False
    while not done:
        print_map = convert_texture(deepcopy(d_map))
        print_map[player.position[1]][player.position[0]] = " ▲"
        texture = "{}" * len(d_map[0])
        [print(texture.format(*_line)) for _line in print_map]
        print(player.position)
        player.move_process(d_map)
        if d_map[player.position[0]][player.position[1]] == 2:
            break

        """ Enemies process """

        if player.hp <= 0:
            break

    return
