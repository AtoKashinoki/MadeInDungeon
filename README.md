# MadeInDungeon

## List of technologies used
<p style="display: inline">
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</p>

## data frame

### file frame

### modules

- CodingTools
  - \_\_init__.py
    CodingTools初期化処理
  - Definition.py
    今回のプログラムに利用する共通定数
  - Inheritance.py
    DataClassの定義
  - Type.py
    Positionクラスの定義

#### MadeInDungeon


- Definition.py
  ゲームの定数の定義
- Setting.py
  ゲームの設定ファイル
- Texture.py
  ゲームの見た目に関するファイル
- Object.py
  オブジェクトのクラス
- MapGenerator.py
  マップ生成に関するプロセス
- Game.py
  ゲーム管理に関するプロセス
- Engines.py
  ゲーム実行アプリケーション

### global values
 - Setting
   - Player
     - hp: int
     - atk: int
     - move_range: dict[str, tuple[int, int]]
     - atk_range: dict[str, tuple[int, int]]
   - Enemy
     - hp: int
     - atk: int
     - move_range: dict[str, tuple[int, int]]
     - atk_range: dict[str, tuple[int, int]]
     - options: dict[str, int | float]
   - Map
     - size: tuple[int, int]  

### object class
- Object
  - position: Pos


- Charactor(Object)
  - hp: int
  - atk: int
  - move_range: tuple[tuple[int, int]]
  - atk_range: tuple[tuple[int, int]]
  - direction: int
  - section: int

- Player(Charactor)
  - None

- Enemy(Charactor)
  - None


- MapObject(Object)
  - key_integer: int

- Wall(MapObject)
  - None

- Stairs(MapObject)
  - None

- Key(MapObject)
  - None

- Section(MapObject)
  - None


- Map
  - generator: function
