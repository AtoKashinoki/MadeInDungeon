from CodingTools.Inheritance import DataClass


class Setting():
    class Player(DataClass):
        hp: int
        atk: int
        move_range: dict[str, tuple[int, int]]
        atk_range: dict[str, tuple[int, int]]

    class Enemy(DataClass):
        hp: int
        atk: int
        move_range: dict[str, tuple[int, int]]
        atk_range: dict[str, tuple[int, int]]
        options: dict[str, int | float]