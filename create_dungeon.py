import random
from copy import deepcopy
from Object import Enemy
class Leaf:
    # MIN_LEAF_SIZE：リーフの分割を行う際の最小サイズを指定している。
    # 各リーフがこれより小さく分割されることはなく、最小でもこのサイズを確保するようにしてるよ。
    # この値を下げると、より小さな部屋が生成され、細かく分割されたダンジョンが生成する。
    MIN_LEAF_SIZE = 6
    # MAX_LEAF_SIZE：リーフの分割を行うかどうかを決定する際の最大サイズを指定してる。
    # リーフの幅や高さがこの値を超えている場合、さらに分割される可能性があるが、
    # このサイズ以下なら、分割されずそのまま部屋や通路として利用される可能性が高くなる。
    MAX_LEAF_SIZE = 20

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_child = None
        self.right_child = None
        self.room = None
        self.halls = []
        self.room_number = None  # 部屋番号

    def split(self):
        if self.left_child or self.right_child:
            return False

        split_horizontally = random.random() > 0.5
        if self.width > self.height and self.width / self.height >= 1.25:
            split_horizontally = False
        elif self.height > self.width and self.height / self.width >= 1.25:
            split_horizontally = True

        max_split = (
            self.height if split_horizontally else self.width) - Leaf.MIN_LEAF_SIZE
        if max_split <= Leaf.MIN_LEAF_SIZE:
            return False

        split_at = random.randint(Leaf.MIN_LEAF_SIZE, max_split)

        if split_horizontally:
            self.left_child = Leaf(self.x, self.y, self.width, split_at)
            self.right_child = Leaf(
                self.x, self.y + split_at, self.width, self.height - split_at)
        else:
            self.left_child = Leaf(self.x, self.y, split_at, self.height)
            self.right_child = Leaf(
                self.x + split_at, self.y, self.width - split_at, self.height)

        return True

    def create_rooms(self, room_number):
        if self.left_child or self.right_child:
            if self.left_child:
                self.left_child.create_rooms(room_number)
            if self.right_child:
                self.right_child.create_rooms(room_number)
            if self.left_child and self.right_child:
                self.create_hall(self.left_child.get_room(),
                                 self.right_child.get_room())
        else:
            while True:
                room_width = random.randint(3, min(self.width - 2, 6))
                room_height = random.randint(3, min(self.height - 2, 6))
                # 幅と高さの差が±1に収まるように制約を追加
                if abs(room_width - room_height) <= 1:
                    break
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)
            self.room = (self.x + room_x, self.y +
                         room_y, room_width, room_height)
            self.room_number = room_number  # 部屋に番号を割り当て

    def get_room(self):
        if self.room:
            return self.room
        elif self.left_child:
            left_room = self.left_child.get_room()
            if left_room:
                return left_room
        elif self.right_child:
            right_room = self.right_child.get_room()
            if right_room:
                return right_room
        return None

    def create_hall(self, room1, room2):
        if not room1 or not room2:
            return

        # 部屋の座標と大きさを取得
        (x1, y1, w1, h1) = room1
        (x2, y2, w2, h2) = room2

        # 部屋内のランダムな点を選ぶ
        point1 = (random.randint(x1 + 1, x1 + w1 - 2),
                  random.randint(y1 + 1, y1 + h1 - 2))
        point2 = (random.randint(x2 + 1, x2 + w2 - 2),
                  random.randint(y2 + 1, y2 + h2 - 2))

        # 廊下を作成するために、xまたはyの座標を接続する
        if random.random() < 0.5:
            # 水平方向に廊下を作成
            hall_x = min(point1[0], point2[0])
            hall_y = point1[1]
            self.halls.append(
                (hall_x, hall_y, abs(point2[0] - point1[0]) + 1, 1))  # 水平廊下
            self.halls.append(
                # 垂直廊下
                (point2[0], min(point1[1], point2[1]), 1, abs(point2[1] - point1[1]) + 1))
        else:
            # 垂直方向に廊下を作成
            hall_x = point1[0]
            hall_y = min(point1[1], point2[1])
            self.halls.append(
                (hall_x, hall_y, 1, abs(point2[1] - point1[1]) + 1))  # 垂直廊下
            self.halls.append(
                # 水平廊下
                (min(point1[0], point2[0]), point2[1], abs(point2[0] - point1[0]) + 1, 1))


def generate_dungeon(width, height):
    root = Leaf(0, 0, width, height)
    leaves = [root]

    split_successful = True
    while split_successful:
        split_successful = False
        for leaf in leaves:
            if leaf.left_child is None and leaf.right_child is None:
                if leaf.width > Leaf.MAX_LEAF_SIZE or leaf.height > Leaf.MAX_LEAF_SIZE or random.random() > 0.25:
                    if leaf.split():
                        leaves.append(leaf.left_child)
                        leaves.append(leaf.right_child)
                        split_successful = True

    """
    数値の意味
    -1    : 壁
    -2    : 階段
    -3    : 宝
    -4    : 道
    -5~-n : 部屋番号
    """
    # 部屋と認識されている場所に番号を入れる
    root.create_rooms(0)
    room_number = -5

    #壁の数値として-1を入れる
    dungeon = [[-1 for _ in range(width)] for _ in range(height)]
    room_dic = {}

    for leaf in leaves:
        if leaf.room:
            (x, y, w, h) = leaf.room
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = room_number # 部屋番号を入れる(-4~-n)
            room_dic[room_number] = (x, y, w, h)
            room_number += -1

        for hall in leaf.halls:
            (x, y, w, h) = hall
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = -4  # 道-3

    return dungeon, room_dic

def random_pos(now_room, object = True):
    """位置をランダムで決定、戻り値(部屋の横幅からランダムに選んだ値、部屋の縦幅からランダムに選んだ値)"""
    if object:
        return (random.randint(now_room[0] + 1, now_room[0] + now_room[2] - 2), random.randint(now_room[1] + 1, now_room[1] + now_room[3] - 2))# (x, y)
    
    else: return (random.randint(now_room[0], now_room[0] + now_room[2] - 1 ), random.randint(now_room[1] , now_room[1] + now_room[3] - 1 ))

def create(now_room = None, now_room_key = None, _object_key = None, _objects_pole = None, _enemies = None, _poles = 0,_enemy = 1,  key = False):
    """はしら、てき、鍵を生成する
    引数_poleで何本柱を設置するか決める
    _enemyで敵の数を決める。
    """
    if key:
        return random_pos(now_room)
    
    if _poles >= 1:
        for cnt in range(_poles):
            done = False
            while not done:
                _pos = random_pos(now_room)
                if _pos == _object_key:
                    continue
                else:done = True
            _objects_pole.append(_pos)

    for i in range(_enemy):
        done = False
        while not done:
            _pos = random_pos(now_room, False)
            if _pos in _objects_pole or _pos == _object_key:
                continue
            else:
                done = True
        _enemies.append(Enemy(_pos, 0, now_room_key, "normal"))
    return
    
def create_object(_room_dic, _objects_poles, _enemies, _object_stair, _object_key):
    """生成する部屋の選択、条件に従ってcreate関数を呼びだす"""
    _objects_poles = []
    _enemies = []
    _object_stair = []
    _room = deepcopy(_room_dic)
    keys = _room.keys()
    _object_key = (999, 999)
    
    for key in keys:#
        done = False
        now_room = _room[key]
        if now_room[2] * now_room[3] == 12:
            if random.random() > 0.95:
                _pos = create(now_room, key = True)
                _object_key = _pos

            if random.random() > 0.5:
                create(now_room, key, _object_key, _objects_poles, _enemies, 1)
            else:
                create(now_room, key, _object_key, _objects_poles, _enemies, 0, 1)

        elif now_room[2] * now_room[3] == 15:
            if random.random() > 0.95:
                _pos = create(now_room, key = True)
                _object_key = _pos

            if random.random() > 0.5:
                create(now_room, key, _object_key, _objects_poles, _enemies, 1)
            else:create(now_room, key, _object_key, _objects_poles, _enemies, 0, 1)

        elif now_room[2] * now_room[3] == 16:
            if random.random() > 0.95:
                _pos = create(now_room, key = True)
                _object_key = _pos

            if random.random() > 0.5:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 1, _enemy = 2)
            else:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 1, _enemy = 1)

        elif now_room[2] * now_room[3] == 20:
            rand = random.random()
            if random.random() > 0.95:
                _pos = create(now_room, key = True)
                _object_key = _pos

            if rand > 0.25:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 1, _enemy = 1)
            elif rand > 0.5:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 1, _enemy = 2)
            elif rand > 0.75:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 2, _enemy = 1)
            else:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 2, _enemy = 2)
        
        elif now_room[2] * now_room[3] >= 25:
            if random.random() > 0.5:create(now_room, key, _object_key, _objects_poles, _enemies, _poles = 2, _enemy = 2)
            if _object_stair == []:
                while not done :
                    _pos = random_pos(now_room)
                    if _pos in _objects_poles:
                        continue
                    else: done = True
                _object_stair = _pos, key
            done = False
            while not done:
                _pos = random_pos(now_room, False)
                if _pos in _objects_poles or _pos == _object_stair:
                    continue
                else: done = True
            _enemies.append(Enemy(_pos, 0, key, "w_action"))

    if _object_key == (999, 999):
        done = False
        print(_object_stair, "A")
        while not done:
            rand = random.randint(5, (5 + len(_room))- 1)
            if -rand == _object_stair[1]:
                continue
            else: done = True

        done = False
        while not done:
            rand = random_pos(_room[-rand], False)
            if rand in _objects_poles:
                continue
            else: done = True

        _object_key = rand

    return _objects_poles, _enemies, _object_stair, _object_key

def display_dungeon(dungeon):
    for row in dungeon:
        print(" ".join(f"{cell:2}" for cell in row))


# ダンジョンのサイズ
dungeon_width = 25
dungeon_height = 20

if __name__ == '__main__':
    enemies = []
    poles = []
    key = []
    stair = []
    dungeon, room_dic = generate_dungeon(dungeon_width, dungeon_height)
    display_dungeon(dungeon)
    print(room_dic)
    _poles , _enemies, _stair, _key = create_object(room_dic, poles, enemies, stair, key)
    print(f"{_poles}\n {_enemies}\n{_stair}\n{_key}")
    for y in range(len(dungeon)):
        for x in range(len(dungeon[y])):
            if (x, y) in _poles:
                for idx in range(len(_poles)):
                    if (x, y) == _poles[idx]:
                        dungeon[y] [x] = "p"
            elif (x, y) == _stair[0]:
                dungeon[y][x] = "s"

            elif (x, y) == _key:
                dungeon[y][x] = "k"
            
            else:
                for i in _enemies:
                    if (x, y) in i.position:
                        dungeon[y][x] = "E"


    display_dungeon(dungeon)
