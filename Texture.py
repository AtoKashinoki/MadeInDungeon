"""
    MadeInDungeon.Texture

This file contain texture processes of MadeInDungeon.
"""


""" imports """


""" processes  """


def convert(_map: list[list[int]]) -> list[list[str]]:
    return [
        [
            "　" if d == 0 else
            " ◰" if d == 2 else
            "■"
            for d in line
        ]
        for line in _map
    ]

