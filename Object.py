from CodingTools.Types import Position
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

