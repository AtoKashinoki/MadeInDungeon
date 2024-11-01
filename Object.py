from CodingTools.Types import Position
from CodingTools.Inheritance import DataClass


class Setting():
    class Player(DataClass):
        hp: int = 3
        atk: int = 1
        move_range: dict[str, tuple[int, int]] = {
            "N": (0, -1),
            "NE": (1, -1),
            "E": (1, 0),
            "SE": (1, 1),
            "S": (0, 1),
            "SW": (-1, 1),
            "W": (-1, 0),
            "NS": (-1, -1)

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
class Object:
    position: Position

    def __init__(self, _pos: Position):
        self.position = _pos

class Charactor(Object):
    hp: int 
    atk: int
    move_range: tuple[tuple[int, int]]
    atk_range: tuple[tuple[int, int]]
    direction: int
    section: int

    def __init__(self, _pos, _hp, _atk, _move_range, _atk_range, _direction, _section):
        super().__init__(_pos)
        self.hp = _hp
        self.atk = _atk
        self.move_range = _move_range
        self.atk_range = _atk_range
        self.direction = _direction
        self.section = _section

class Player(Charactor):
    def __init__(self, _pos):
        super().__init__(
            _pos,#int 
            Setting.Player.hp,
            Setting.Player.atk,
            Setting.Player.move_range,
            Setting.Player.atk_range,
        )

    def move_process(self, input):
        if (input in self.move_range):
            ...


pos = Position()
player = Player(pos)
player.move_process("N")
print(player)
