import random


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
    -4    : 鍵
    -5    : 柱 
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
            center_coordinates = []  # 外周を除いた真ん中の部分の座標を入れるリスト
            count_room_number = 0  # 部屋のマス数の合計
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = room_number
                    count_room_number += 1
                    if i != x and i != (x + w) - 1 and j != y and j != (y + h) - 1:  # 外周を除く
                        center_coordinates.append([i, j])
            # print(f"外周を除いた真ん中の部分の座標{center_coordinates}部屋のマス数の合計{
            #       count_room_number}")
            if len(center_coordinates) != 0:  # 3*3以外の場合
                if count_room_number >= 20:
                    # 部屋の合計マス数が25以上であれば柱を2個生成する
                    for i in range(2):
                        pillar_coordinates = center_coordinates.pop(random.randint(
                            0, len(center_coordinates)-1))
                        dungeon[pillar_coordinates[1]
                                ][pillar_coordinates[0]] = -5
                else:
                    pillar_coordinates = center_coordinates.pop(random.randint(
                        0, len(center_coordinates)-1))
                    dungeon[pillar_coordinates[1]][pillar_coordinates[0]] = -5
            elif len(center_coordinates) == 0:  # 3*3の場合
                pillar_coordinates = center_coordinates[0][0]
                dungeon[pillar_coordinates[1]][pillar_coordinates[0]] = -5
            room_number += -1  # 部屋番号を入れる(-4~-n)

        for hall in leaf.halls:
            (x, y, w, h) = hall
            for i in range(x, x + w):
                for j in range(y, y + h):
                    dungeon[j][i] = -6  # 道-3

    # ここで階段の生成
    stair_room = random.randint(room_number, -7)
    matching_coordinates_stair = []  # 階段のある部屋のマスすべての部屋の座標を取得
    inner_stair_room = []
    for j in range(len(dungeon)):
        for i in range(len(dungeon[j])):
            if dungeon[j][i] == stair_room:
                matching_coordinates_stair.append([i, j])
    for j in range(len(matching_coordinates_stair)):
        for i in range(len(matching_coordinates_stair[j])):
            if i != 0 and i != len(matching_coordinates_stair[i]) and j != 0 and j != len(matching_coordinates_stair):
                inner_stair_room.append(matching_coordinates_stair[j])
    stair_coordinates = inner_stair_room[random.randint(
        0, len(inner_stair_room)) - 1]
    dungeon[stair_coordinates[1]][stair_coordinates[0]] = -2
    print(f"##{room_number}")
    print(f"##{stair_room}")
    print(f"matching_coordinates_stair{matching_coordinates_stair}")
    print(f"inner_stair_room{inner_stair_room}")

    # ここで鍵の位置を決めてる
    key_room = random.randint(room_number, -7)
    matching_coordinates_key_room = []  # 鍵のある部屋のマスすべての部屋の座標を取得
    for j in range(len(dungeon)):
        for i in range(len(dungeon[j])):
            if dungeon[j][i] == key_room:
                matching_coordinates_key_room.append([i, j])
            elif dungeon[j][i] == -5:
                pass
    key_coordinates = matching_coordinates_key_room[random.randint(0, len(matching_coordinates_key_room)) - 1]
    dungeon[key_coordinates[1]][key_coordinates[0]] = -4

    return dungeon


def display_dungeon(dungeon):
    for row in dungeon:
        print(" ".join(f"{cell:2}" for cell in row))
    for row in dungeon:
        display_row = ""
        for cell in row:
            if cell == -1:
                display_row += "🔲"
            elif cell == -2:
                display_row += "＃"  # 階段:全角スペース
            elif cell == -4:
                display_row += "＄"
            elif cell == -5:
                display_row += "＠"  # 柱S
            elif cell == -6:
                display_row += "　"  # 道:全角スペース
            else:
                display_row += "　"  # 他の数値はそのまま表示
        print(display_row)


# ダンジョンのサイズ
dungeon_width = 25
dungeon_height = 20

if __name__ == '__main__':
    dungeon = generate_dungeon(dungeon_width, dungeon_height)
    display_dungeon(dungeon)