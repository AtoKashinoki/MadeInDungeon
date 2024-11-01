from CodingTools.Types import Position
from Setting import Setting
import random
from copy import deepcopy
import math 

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
        return

    def check_wall(self, _map: list[list[int, ...], ...]):
        return _map[self.position[0]][self.position[1]] == 1

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

    def move_process(self, _map):
        try:
            now_pos = deepcopy(self.position)
            done = False
            while not done:
                self.position.move(self.move_range[input("Enter move direction: ")])
                if self.check_wall(_map):
                    self.position = now_pos
                    continue
                done = True
                ...

        except KeyError:
            self.move_process(_map)
        return

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
        self._mode = False
        return
    
    def move_process(self, _mode, _map, _player):
        now_pos = (self.position.x, self.position.y)

        if _mode :
            if ((self.position.x - _player.position.x) + (self.position.y - _player.position.y) == 1):
                pass
        elif not _mode:
            while True:
                self.position.move((random.randint(-1, 1), random.randint(-1, 1)))
                if self.check_wall(_map):
                    self.position = now_pos
                else:
                    break

    ...


if __name__ == '__main__':

    pos = Position(2)
    enemy = []
    print(pos)
    print(type(pos.data))
    player = Player(pos, 0, 0)
    player.move_process("N")
    print(player.position)
