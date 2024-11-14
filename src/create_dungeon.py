import random
from CodingTools.Types import Position
from src.Object import Enemy, Player

class Leaf:
    # MIN_LEAF_SIZE：リーフの分割を行う際の最小サイズを指定している。
    # 各リーフがこれより小さく分割されることはなく、最小でもこのサイズを確保するようにしてるよ。
    # この値を下げると、より小さな部屋が生成され、細かく分割されたダンジョンが生成する。
    MIN_LEAF_SIZE = 6
    # MAX_LEAF_SIZE：リーフの分割を行うかどうかを決定する際の最大サイズを指定してる。
    # リーフの幅や高さがこの値を超えている場合、さらに分割される可能性があるが、
    # このサイズ以下なら、分割されずそのまま部屋や通路として利用される可能性が高くなる。
    MAX_LEAF_SIZE = 18

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
                # 部屋の大きさをランダムで決定
                room_width = random.randint(3, min(self.width - 2, 5))
                room_height = random.randint(3, min(self.height - 2, 5))
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


def create_enemy(_room_number, _room_space:list[tuple], _enemies):
    if _room_space == []:
        return
    
    elif len(_room_space) == 1:
        _pos = _room_space[0]
        _enemies.append(Enemy(_pos, 0, _room_number))
        _room_space.pop()

    else:
        dice = random.randint(0, len(_room_space)-1)
        _pos = _room_space[dice]
        _enemies.append(Enemy(_pos, 0, _room_number))
        _room_space.pop(dice)

    return _pos

def generate_dungeon(width, height, _enemies):
    _enemies = []
    root = Leaf(0, 0, width, height)
    leaves = [root]
    _room_dic = dict()#[部屋番号]:{(x, y, w, h)}
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
    -3    : 柱 
    -4    : 宝
    -5    : 鍵
    -6    : 道
    -7~-n : 部屋番号
    """
    # 部屋と認識されている場所に番号を入れる
    root.create_rooms(0)
    room_number = -7

    # 壁の数値として-1を入れる
    dungeon = [[-1 for _ in range(width)] for _ in range(height)]

    for leaf in leaves:
        if leaf.room:
            (x, y, w, h) = leaf.room
            _room_dic[room_number] = (x, y, w, h)

            center_coordinates = []  # 外周を除いた真ん中の部分の座標を入れるリスト
            count_room_number = 0  # 部屋のマス数の合計
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = room_number
                    count_room_number += 1
                    
                    if i != x and i != (x + w) - 1 and j != y and j != (y + h) - 1:  # 外周を除く
                        center_coordinates.append([i, j])

            if len(center_coordinates) != 0:  # 3*3以外の場合
                if count_room_number >= 20:
                    # 部屋の合計マス数が25以上であれば柱を2個生成する
                    for i in range(2):
                        pillar_coordinates = center_coordinates.pop(random.randint(
                            0, len(center_coordinates)-1))
                        dungeon[pillar_coordinates[1]
                                ][pillar_coordinates[0]] = -3
                else:
                    pillar_coordinates = center_coordinates.pop(random.randint(
                        0, len(center_coordinates)-1))
                    dungeon[pillar_coordinates[1]][pillar_coordinates[0]] = 3
            elif len(center_coordinates) == 0:  # 3*3の場合
                pillar_coordinates = center_coordinates[0][0]
                dungeon[pillar_coordinates[1]][pillar_coordinates[0]] = -3
            room_number += -1  # 部屋番号を入れる(-4~-n)

        for hall in leaf.halls:
            (x, y, w, h) = hall
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = -6  # 道-3

    room_number += 1
    
    # ここで階段の生成
    create_stair_done = False
    while not create_stair_done:
        stair_room = random.randint(room_number, -7)
        matching_coordinates_stair = []  # 階段のある部屋のマスすべての部屋の座標を取得

        """一回り小さい部屋受け取り"""
        for x in range((_room_dic[stair_room][0] + 1), (_room_dic[stair_room][0]) + _room_dic[stair_room][2] - 1):
            for y in range((_room_dic[stair_room][1] + 1), (_room_dic[stair_room][1]) + _room_dic[stair_room][3] -1):
                if dungeon[y][x] == -3:
                    pass

                else:

                    matching_coordinates_stair.append((x, y))
        if matching_coordinates_stair == []:#3*3の部屋が選ばれるかつ真ん中にはしらがあると、空になるから、それを除外
            continue
        else:create_stair_done = True
    
    if len(matching_coordinates_stair) >= 2:
        rand = random.randint(0, len(matching_coordinates_stair)-1)
    else:
        rand = 0
 
    stair_pos = matching_coordinates_stair[rand]

    dungeon[stair_pos[1]][stair_pos[0]] = -2

    # ここで鍵の位置を決めてる
    key_room_done = False
    while not key_room_done:#会談と違う部屋を選択するまで
        _key_room = random.randint(room_number, -7)
        if _key_room == stair_room:
            continue
        else:
            key_room_done = True

    matching_coordinates_key_room = []  # 鍵のある部屋のマスすべての部屋の座標を取得
    for x in range((_room_dic[_key_room][0] ), (_room_dic[_key_room][0] + _room_dic[_key_room][2] )):
        for y in range((_room_dic[_key_room][1] ), (_room_dic[_key_room][1] + _room_dic[_key_room][3])):
            
            if dungeon[y][x] != -3:
                matching_coordinates_key_room.append((x, y))
    
    rand = random.randint(0, len(matching_coordinates_stair)-1)
    key_pos = matching_coordinates_key_room[rand]
    dungeon[key_pos[1]][key_pos[0]] = -5

    """
    敵の生成/今気づいたけど関数分けれるやん
    for 文で部屋番号を取り出す。
    if文で、部屋の広さに応じて敵の人数を調整する
    部屋の中で柱、会談、鍵以外のマスを_room_spaceに格納。
    create_enemy関数に渡す。
    """
    room_numbers = _room_dic.keys()

    for _room_number in room_numbers:#

        _room_space = []
        now_room = _room_dic[_room_number]
        
        if now_room[2] * now_room[3] == 12 or now_room[2] * now_room[3] == 15:
            for x in range((now_room[0]), (now_room[0] + now_room[2])):
                for y in range((now_room[1]), (now_room[1] + now_room[3])):
                    if dungeon[y][x] != -2 or dungeon[y][x] != -5 or dungeon[y][x] != -3:
                        _room_space.append((x, y))
            enemy_pos = create_enemy(_room_number, _room_space, _enemies)
            if enemy_pos:
                dungeon[enemy_pos[1]][enemy_pos[0]] = -99
        
        elif now_room[2] * now_room[3] == 16 or now_room[2] * now_room[3] == 20:
            for x in range((now_room[0]), (now_room[0] + now_room[2])):
                for y in range((now_room[1]), (now_room[1] + now_room[3])):
                    if dungeon[y][x] != -2 or dungeon[y][x] != -5 or dungeon[y][x] != -3:
                        _room_space.append((x, y))
            enemy_pos = create_enemy(_room_number, _room_space, _enemies)
            if enemy_pos:
                dungeon[enemy_pos[1]][enemy_pos[0]] = -99
            if random.random() > 0.5:
                enemy_pos = create_enemy(_room_number, _room_space, _enemies)
                if enemy_pos:
                    dungeon[enemy_pos[1]][enemy_pos[0]] = -99
        
        elif now_room[2] * now_room[3] >= 25:
            for x in range((now_room[0]), (now_room[0] + now_room[2])):
                for y in range((now_room[1]), (now_room[1] + now_room[3])):
                    if dungeon[y][x] != -2 or dungeon[y][x] != -5 or dungeon[y][x] != -3:
                        _room_space.append((x, y))
            enemy_pos = create_enemy(_room_number, _room_space, _enemies)
            if enemy_pos:
                dungeon[enemy_pos[1]][enemy_pos[0]] = -99
            enemy_pos = create_enemy(_room_number, _room_space, _enemies)
            if enemy_pos:
                dungeon[enemy_pos[1]][enemy_pos[0]] = -99
        else:pass

    """プレイヤーをせいせいする"""
    player_done = False
    while not player_done:
        player_room_done = False
        while not player_room_done:#会談と違う部屋を選択するまで
            Player_room = random.randint(room_number, -7)
            if Player_room == _key_room:
                continue
            else:
                player_room_done = True

    
        player_room = []  # 鍵のある部屋のマスすべての部屋の座標を取得
        for x in range((_room_dic[Player_room][0] ), (_room_dic[Player_room][0] + _room_dic[Player_room][2] )):
            for y in range((_room_dic[Player_room][1] ), (_room_dic[Player_room][1] + _room_dic[Player_room][3])):
               
                if dungeon[y][x] != -3 and dungeon[y][x] != -2 and dungeon[y][x] != -99 :
                    player_room.append((x, y))
        if player_room == []:
            continue
        elif len(player_room) == 1:
            dice = False
            player_done = True

        else:
            dice = True
            player_done = True
        
    if dice:
        rand = random.randint(0, len(player_room)-1)

    else:
        rand = 0

    player_pos = player_room[rand]
    #key_coordinates = matching_coordinates_key_room[random.randint(0, len(matching_coordinates_key_room)) - 1]
    Player(player_pos, 0, Player_room)
    dungeon[player_pos[1]][player_pos[0]] = -100

    return dungeon


def display_dungeon(_dungeon, _player, _enemies):
    _dungeon = \
        [
            [
                "🔲" if cell in (-1, -3) else
                "階" if cell == -2 else
                "🔑" if cell == -5 else
                "　"
                for cell in row
            ]
            for row in _dungeon
        ]

    _dungeon[_player.position.y][_player.position.x] = "😀"

    [
        _dungeon[y].__setitem__(x, "👹")
        for x, y in map(lambda x: x.position, _enemies)
        if not _player.visibility_map[y][x] == -101
    ]

    for row in _dungeon:
        print("".join(row))


# ダンジョンのサイズ
dungeon_width = 25
dungeon_height = 20

def run(_player):
    _dungeon = generate_dungeon(dungeon_width, dungeon_height, [])
    _enemies = []
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            if _dungeon[y][x] == -100:
                _player.position = Position(x, y)
                _player.item_key = False
            elif _dungeon[y][x] == -99:
                _enemies.append(Enemy((x, y), 0, 0))
    return _dungeon, _player, _enemies


if __name__ == '__main__':
    dungeon, player, enemies = run()
    display_dungeon(
        dungeon,
        player,
        enemies
    )
