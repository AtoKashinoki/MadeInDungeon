"""
    MadeInDungeon.MapGenerator

This file contain Map generator of MadeInDungeon.
"""


""" imports """


""" processes """


def test(_mx, _my):
    dungeon_map = [
        [
            0 if 0 < x < _mx-1 and 0 < y < _my-1 else 1
            for x in range(_mx)
        ]
        for y in range(_my)
    ]
    dungeon_map[5][5] = 2

    return dungeon_map

def clear_floor(_mx, _my):
    dungeon_map = [
        [
            0 if 0 < x < _mx-1 and 0 < y < _my-1 else 1
            for x in range(_mx)
        ]
        for y in range(_mx)
    ]
    dungeon_map[3][3] = -3

    return dungeon_map