"""
    MadeInDungeon.Texture

This file contain texture processes of MadeInDungeon.
"""


""" imports """


""" processes  """


def convert(_map: list[list[int]]) -> list[list[str]]:
    return [
        [
            "🔲" if d in (-1, -3) else
            "階" if d == -2 else
            "🔑" if d == -5 else
            "💎" if d == -4 else
            "　"
            for d in line
        ]
        for line in _map
    ]

