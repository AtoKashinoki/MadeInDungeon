from CodingTools.Types import Position
from Setting import Setting

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
    def __init__(self, _pos, _direction, _section):
        super().__init__(
            _pos,#tuple 
            Setting.Player.hp,
            Setting.Player.atk,
            Setting.Player.move_range,
            Setting.Player.atk_range,
            _direction,
            _section
        )

    def move_process(self, input):
        self.position.move(self.move_range[f"{input}"])

class Enemy(Charactor):
    def __init__(self, _pos, _direction, _section):
        super().__init__(
            _pos,#tuple 
            Setting.Player.hp,
            Setting.Player.atk,
            Setting.Player.move_range,
            Setting.Player.atk_range,
            _direction,
            _section
        )
    def move_process():
        pass

class 

pos = Position(2)
enemy = []
print(pos)
print(type(pos.data))
player = Player(pos, 0, 0)
player.move_process("N")
print(player.position)
