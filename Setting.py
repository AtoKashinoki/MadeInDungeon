from CodingTools.Inheritance import DataClass


class Setting():
    class Player(DataClass):
        hp: int = 3
        atk: int = 1
        move_range: dict[str, tuple[int, int]] = {
            "W": (0, -1),
            "WD": (1, -1),
            "D": (1, 0),
            "SD": (1, 1),
            "S": (0, 1),
            "SA": (-1, 1),
            "A": (-1, 0),
            "WA": (-1, -1)

        }
        atk_range: dict[str, tuple[int, int]] = {
            "N": ((-1, -1), (0, -1), (1, -1)),
            "E": ((1, -1), (1, 0), (1, 1)),
            "S": ((-1, 1), (0, 1), (1, 1)),
            "W": ((-1, -1), (-1, 0), (-1, 1)),
        }

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
