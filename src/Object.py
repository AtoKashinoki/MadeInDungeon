from CodingTools.Types import Position
from src.Setting import Setting
from copy import deepcopy
import random


class Object:
    position: Position

    def __init__(self, _pos: tuple):
        self.position = Position(*_pos)


class Charactor(Object):
    hp: int
    atk: int
    move_range: dict[str, tuple[int, int]]
    atk_range: dict[str, [int, int]]
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
        return _map[self.position[1]][self.position[0]] in (-1, -2, -3)

    def check_enemy(self, _enemies):  # enemysは敵のクラスのリスト
        count = 0
        for idx in range(len(_enemies)):
            if self.position == _enemies[idx].position:
                count += 1
        return count


class Player(Charactor):
    __visibility_map: list[list[int]] | None

    def __init__(self):
        super().__init__(
            (0, 0),  # tuple
            Setting.Player.hp,
            Setting.Player.atk,
            Setting.Player.move_range,
            Setting.Player.atk_range,
            0,
            0,
        )
        self.visibility = Setting.Player.visibility
        self.__visibility_map = None
        self.item_key = False
        self.f_attack = False
        self.f_attack_hit = False
        self.f_get_key = False
        self.f_clear = False
        self.item_diamond = False
        self.max_items = Setting.Player.max_item
        self.max_hp = Setting.Player.max_hp
        self.items = []
        self.f_get_apple = 0

        self.move = False
    
        return

    @property
    def visibility_map(self): return tuple([
        *map(tuple, self.__visibility_map)
    ])

    def reset_visibility(self, d_map):#-101にぷれいやーが見えている範囲であることを定義する。
        self.__visibility_map = \
            [
                [
                    -101
                    for _ in range(len(d_map[y]))
                ]
                for y in range(len(d_map))
            ]
        return

    def update_visibility(self, d_map):#マップの更新をしてプレイヤーのみえる範囲が増える
        if not self.f_clear:
            [
                self.__visibility_map[self.position.y+y].__setitem__(
                    self.position.x+x,
                    d_map[self.position.y+y][self.position.x+x]
                )
                for x, y in self.visibility
                if 0 <= self.position.x+x < len(d_map[y])
                if 0 <= self.position.y+y < len(d_map)
            ]
            ...
        else:
            self.__visibility_map = d_map
            ...
        return

    def move_process(self, _map, _enemies):
        self.section = _map[self.position[1]][self.position[0]]
        now_pos = deepcopy(self.position)

        done = False
        while not done:
            key = input("Enter Move or Attack direction: ")

            if key in self.move_range:
                self.position.move(self.move_range[key])
                if _map[self.position[1]][self.position[0]] == -2 and self.item_key:
                    return
                if _map[self.position[1]][self.position[0]] == -4:
                    self.item_diamond = True
                    return
                if self.check_wall(_map) or self.check_enemy(_enemies) > 0:
                    self.position = deepcopy(now_pos)
                    continue
                if _map[self.position[1]][self.position[0]] == -5:
                    self.f_get_key = True
                    self.item_key = True
                    _map[self.position[1]][self.position[0]] = -6
                    ...

                if _map[self.position[1]][self.position[0]] == -103:
                    self.f_get_apple += 1
                    _map[self.position[1]][self.position[0]] = -6

                return

            elif key in self.atk_range:
                self.f_attack = True
                for _dir in self.atk_range[key]:
                    for _enemy in _enemies:
                        if _enemy.position == tuple([_rs + _p for _rs, _p in zip(_dir, self.position)]):
                            _enemy.hp -= 1
                            self.f_attack_hit = True
                return

        return

    def game_loop_mp(self, _map, _enemies, input_key):
        self.section = _map[self.position[1]][self.position[0]]
        now_pos = deepcopy(self.position)

        key = input_key

        if key in self.move_range:
            self.position.move(self.move_range[key])
            if _map[self.position[1]][self.position[0]] == -2 and self.item_key:
                return ()
            if _map[self.position[1]][self.position[0]] == -4:
                self.item_diamond = True
                return ()
            if self.check_wall(_map) or self.check_enemy(_enemies) > 0:
                self.position = deepcopy(now_pos)
                return ()
            if _map[self.position[1]][self.position[0]] == -5:
                if not len(self.items) == self.max_items:
                    self.f_get_key = True
                    self.item_key = True
                    _map[self.position[1]][self.position[0]] = -6
                    self.items.append("🔑")
                ...

            if _map[self.position[1]][self.position[0]] == -103:
                if not len(self.items) == self.max_items:
                    self.f_get_apple += 1
                    _map[self.position[1]][self.position[0]] = -6
                    self.items.append("🍎")
                ...

            self.move = True
            return ()

        elif key in self.atk_range:
            self.f_attack = True
            attacking = []
            for _dir in self.atk_range[key]:
                for _enemy in _enemies:
                    if _enemy.position == tuple([_rs + _p for _rs, _p in zip(_dir, self.position)]):
                        _enemy.hp -= 1
                        self.f_attack_hit = True
                attacking.append(_dir)
            self.move = True
            return attacking

        return ()
    
    def use_item(self, number:int):
        if len(self.items) > number-1:
            index = number - 1
            if self.items[index] == "🍎":
                self.recovery_hp(1)
                del self.items[index]

        return
    
    def recovery_hp(self, _hp_rec):
        if self.hp >= self.max_hp:
            return
        
        self.hp += _hp_rec
        return


class Enemy(Charactor):
    def __init__(self, _pos, _direction, _section):
        self.type = "2move" if 0 == random.randrange(5) else None
        hp = Setting.Enemy.hp
        if self.type == "2move":
            hp -= 1
        super().__init__(
            _pos,  # tuple
            hp,
            Setting.Enemy.atk,
            Setting.Enemy.move_range,
            Setting.Enemy.atk_range,
            _direction,
            _section,
        )
#        self.mode = Setting.Enemy.options
        self.__mode = False
        self.move_count = 0
        self.f_attack = False
        self.f_clear = False
        return

    def move_process(self, _map, _player, _enemies):

        self.section = _map[self.position[1]][self.position[0]]
        now_pos = deepcopy(self.position)

        if self.__mode:  # プレイヤーを追いかけるモードの時
            if abs(self.position.x - _player.position.x) + abs(self.position.y - _player.position.y) == 1:
                self.f_attack = True
                _player.hp -= 1

            else:
                move_num = 1
                if self.type == "2move":
                    move_num += 1
                for _ in range(move_num):
                    if abs(self.position.x - _player.position.x) + abs(self.position.y - _player.position.y) == 1:
                        break
                    result_search = self.breadth_first_search(
                        _map, _player)  # 返り血は、タプル（次のマスからゴールまでのマス、[0]が次のマス）
                    move = tuple([
                        _rs - _p
                        for _rs, _p in zip(result_search, self.position)
                    ])

                    self.position.move(move)
                    if self.check_wall(_map) or self.check_enemy(_enemies) > 1:
                        self.position = now_pos
                        return

        else:  # プレイヤーを追いかけないとき
            if not self.section == -6 and self.section == _player.section:
                self.__mode = True
                return

            key = tuple(self.move_range.keys())[
                random.randrange(len(self.move_range))]
            self.position.move(self.move_range[key])
            if self.check_wall(_map) or self.position == _player.position:
                self.position = now_pos
            else:
                ...

    def search_direction(self, _map, poses: list, distance, goal):
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
        if flag:
            return _map, True

        return _map, False

    def breadth_first_search(self, _map, goal: Player):
        direction = ((0, 1), (0, -1), (1, 0), (-1, 0))
        _search_map = deepcopy(_map)

        # 幅優先探査　距離計算
        _search_map[goal.position.y][goal.position.x] = 1
        counter = 0
        done = False
        while not done:
            counter += 1

            search_poses = [
                (x, y)
                for y in range(len(_search_map))
                for x in range(len(_search_map[y]))
                if _search_map[y][x] == counter
            ]

            if len(search_poses) == 0:
                break

            to_poses = [
                (x+dx, y+dy)
                for x, y in search_poses
                for dx, dy in direction
                if _search_map[y+dy][x+dx] < -3
            ]

            next_c = counter+1
            [
                _search_map[y].__setitem__(x, next_c)
                for x, y in to_poses
            ]

            ...

        # 幅優先探査　ルート計算
        counter = _search_map[self.position.y][self.position.x]
        route = [(self.position.x, self.position.y)]

        done = False
        while not done:
            counter -= 1

            x, y = route[-1]
            next_r = [
                (x+dx, y+dy)
                for dx, dy in direction
                if _search_map[y+dy][x+dx] == counter
            ]

            if len(next_r) == 0 or counter <= 0:
                break

            route.append(next_r[random.randrange(len(next_r))])
            ...

        if len(route) == 1:
            return route[0]

        return route[1]

    ...


class AI(Player):
    """ AI player class """

    """ values """
    __ai_process = None

    def __init__(self, ai_process):
        super().__init__()
        self.__ai_process = ai_process
        return

    def game_loop_mp(self, _map, _enemies, _):

        visibility_poss = (
            (x, y)
            for y in range(len(_map))
            for x in range(len(_map[y]))
            if not self.visibility_map[y][x] == -101
        )

        visibility_enemies = tuple(
            _enemy
            for _enemy in _enemies
            if _enemy.position in visibility_poss
        )

        player_status = PlayerStatus(self)

        input_key: str = self.__ai_process.__move_process__(
            self.visibility_map,
            player_status,
            visibility_enemies,
        )

        return super().game_loop_mp(_map, _enemies, input_key)

    ...


class PlayerStatus:
    hp: int
    atk: int
    move_range: dict[str, tuple[int, int]]
    atk_range: dict[str, [int, int]]
    position: Position

    def __init__(self, player: Player):
        """ Setting values """
        self.hp = player.hp
        self.atk = player.atk
        self.move_range = player.move_range
        self.atk_range = player.atk_range
        self.position = player.position
        return

    ...

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
    enemy.move_process(map_, Player(), [])
    print(enemy.position)

    for line in map_:
        print(line)
