# MadeInDungeon

## data frame

### file frame

- CodingTools
  - \_\_init__.py
  - Definition.py
  - Inheritance.py
  - Type.py

- GameEngine
  - \_\_init__.py
  - Engines.py

- MadeInDungeon
  - \_\_init__.py
  - Setting.py
  - Object.py
  - MapGenerator.py
  - Game.py

### global values
 - Setting
   - Player
     - hp: int
     - atk: int
     - move_range: tuple[tuple[int, int]]
     - atk_range: tuple[tuple[int, int]]
   - Enemy
     - hp: int
     - atk: int
     - move_range: tuple[tuple[int, int]]
     - atk_range: tuple[tuple[int, int]]
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
