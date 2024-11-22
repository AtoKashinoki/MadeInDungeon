# MadeInDungeon

## List of technologies used
<p style="display: inline">
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</p>

## Table of Contents
1. [ProjectName](#ProjectName)
2. [Overview](#Overview)
3. [Requirement](#Requirement)
4. [DataFrame](#DataFrame)
5. [Author](#Author)

<a id="ProjectName"></a>

## ProjectName

Made In Dungeon

<a id="Overview"></a>

## OverView

The goal is to create a dungeon game, “Made in Dungeon”.

<a id="Requirement"></a>

## Requirement

|       Language        | version    |
| --------------------- | ---------- |
| Python                | 3.10.0     |


<a id="DataFrame"></a>

## DataFrame

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

<a id="Author"></a>

## Author
泉龍真

小松学翔

齊藤旭宏

柏木空翔

<p align="right">(<a href="#top">トップへ</a>)</p>
