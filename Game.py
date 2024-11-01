from Object import Player


def create_map():
    dungeon_map = [
        [
            0 if 0 < x < 19 and 0 < y < 19 else 1
            for x in range(20)
        ]
        for y in range(20)
    ]
    dungeon_map[5][5] = 2

    return dungeon_map


def hierarchy_process(player: Player):
    # ダンジョンを生成して変数に保管
    d_map = create_map()
    game_loop(d_map, player)

    return d_map


def game_loop(d_map, player: Player):
    done = False
    while not done:
        [print(_line) for _line in d_map]
        print(player.position)
        player.move_process(input("input move direction: "))
        if d_map[player.position[0]][player.position[1]] == 2:
            break

        """ Enemies process """

        if player.hp <= 0:
            break

    return
