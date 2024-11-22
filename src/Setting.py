from turtle import Turtle

from CodingTools.Inheritance import DataClass


class Setting():
    class Player(DataClass):
        hp: int = 5
        atk: int = 1
        move_range: dict[str, tuple[int, int]] = {
            "w": (0, -1),
            "wd": (1, -1),
            "dw": (1, -1),
            "d": (1, 0),
            "sd": (1, 1),
            "ds": (1, 1),
            "s": (0, 1),
            "sa": (-1, 1),
            "as": (-1, 1),
            "a": (-1, 0),
            "wa": (-1, -1),
            "aw": (-1, -1),

        }
        atk_range: dict[str, tuple[int, int]] = {
            "W": ((-1, -1), (0, -1), (1, -1)),
            "D": ((1, -1), (1, 0), (1, 1)),
            "S": ((-1, 1), (0, 1), (1, 1)),
            "A": ((-1, -1), (-1, 0), (-1, 1)),
        }
        v_range = 3
        visibility: tuple[tuple] = tuple(
            (x, y)
            for y in range(-v_range, v_range+1)
            for x in range(-3+abs(y), 4-abs(y))
        )


    class Enemy(DataClass):
        hp: int = 2
        atk: int = 1
        move_range: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        atk_range: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        options: dict[str, int | float]
    
    class Map(DataClass):
        stage_num = 3
        ...

    class PlayMode(DataClass):
        engine = True
        ai_mode = False
        ...
