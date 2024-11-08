"""
    MadeInDungeon.Texture

This file contain texture processes of MadeInDungeon.
"""


""" imports """


""" processes  """


def convert(_map: list[list[int]]) -> list[list[str]]:
    return [
        [
            "　" if d <= -3 else
            "🔲" if d == -1 else
            " ◰" if d == -2 else
            "No"
            for d in line
        ]
        for line in _map
    ]

