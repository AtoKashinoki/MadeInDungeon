
def create_map():
    dungeon_map = [
        [
            0 if 0 < x < 19 and 0 < y < 19 else 1
            for x in range(20)
        ]
        for y in range(20)
    ]

    return dungeon_map


def hierarchy_process():
    # ダンジョンを生成して変数に保管
    d_map = create_map()

    return d_map


def game_loop(d_map):
    return


print(create_map())
