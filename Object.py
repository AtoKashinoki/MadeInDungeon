from CodingTools.Types import Position
from Setting import Setting
import random
from copy import deepcopy
import math 
import random

class Object:
    position: Position

    def __init__(self, _pos: tuple):
        self.position = Position(*_pos)

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
    
    def check_enemy(self, enemys):#enemysは敵のクラスのリスト
        for idx in range(len(enemys)):
            if self.position == enemys[idx].position:
                return 1
        return 0

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
                    self.position = Position(now_pos)
                    continue
                done = True
                ...

        except KeyError:
            self.move_process(_map)
        
        return
class Enemy(Charactor):
    def __init__(self, _pos, _direction, _section, _type: str):
        super().__init__(
            _pos,#tuple 
            Setting.Enemy.hp,
            Setting.Enemy.atk,
            Setting.Enemy.move_range,
            Setting.Enemy.atk_range,
            _direction,
            _section,
        )
#        self.mode = Setting.Enemy.options
        self.type = _type
        self.__mode = False
        self.move_count = 0
        return
    
    def move_process(self, _map, _player, _Enemys):

        now_pos = (self.position.x, self.position.y)

        if self.__mode :#プレイヤーを追いかけるモードの時
            if ((self.position.x - _player.position.x) + (self.position.y - _player.position.y) == 1):
                _player.hp -= 1
            
            else:
                result_search = self.breadth_first_search(_map, _player)#返り血は、タプル（次のマスからゴールまでのマス、[0]が次のマス）
                move = tuple([
                    _rs - _p
                    for _rs, _p in zip(result_search[-2], self.position)
                ])
                self.position.move(move)
                if self.check_wall(_map) or self.check_enemy(_Enemys):
                    self.position = Position(now_pos)
                    return
                
        else:#プレイヤーを追いかけないとき
            print(_player.section)
            if self.section == _player.section:
                self.__mode = True
                self.move_process(_map, _player, _Enemys)

            while True:
                self.position.move((random.randint(-1, 1), random.randint(-1, 1)))
                if self.check_wall(_map):
                    self.position = Position(now_pos)
                else:
                    break
            
    def search_direction(self, _map, poses:list , distance, goal):
        direction = ((0, 1), (0, -1), (1, 0), (-1, 0))
        to_poses = []
        for pos in poses:
            for dir in direction:
                to_pos = deepcopy(pos).move(dir)
                if _map[to_pos.y][to_pos.x] <= -3:
                    _map[to_pos.y][to_pos.x] = distance
                    to_poses.append(to_pos)
        
        if len(to_poses) == 0:
            return _map, False
        
        if sum([goal.x == t[0] and goal.y == t[1] for t in to_poses]) > 0:
            return _map, True

        _map, flag = self.search_direction(_map, to_poses, distance + 1, goal)
        if flag: return _map, True

        return _map, False
        
    def breadth_first_search(self, _map, goal: Player):
        direction = ((0, 1), (0, -1), (1, 0), (-1, 0))
        _map[self.position.y][self.position.x] = 1
        _map = self.search_direction(_map, [self.position, ], 2, goal.position)
        result_route = []
        now_pos = goal.position
        print(_map)
        now_number = _map[0][goal.position.y][goal.position.x]
        print(self.position, "AA")
        #print(_map)
        while True:
            route = []

            for dir in direction:
                _to_pos = deepcopy(now_pos).move(dir)
                if _map[0][_to_pos.y][_to_pos.x] == now_number -1:
                    route.append(_to_pos)

            print(result_route)
            if self.position in result_route:
                print("V")
                break
            if len(route) == 2:
                result_route.append(route[0]) if random.randint(0, 1) > 0.5 else result_route.append(route[1])
            else:
                result_route.append(route[0])

            now_number -= 1
            now_pos = result_route[-1]
        return result_route
            
    
if __name__ == '__main__':
    map_ = \
        [
            [
                -5 if 0 < x < 24 and 0 < y < 19 else -1
                for x in range(25)
            ] 
            for y
             in range(20)
        ]
    
    enemy = Enemy((13, 12), 0, 0, "")
    enemy.move_process(map_, Player((5, 5), 0, 0), [])
    print(enemy.position)
    
    for line in map_:
        print(line)
