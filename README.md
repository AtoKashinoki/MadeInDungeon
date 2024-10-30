# MadeInDungeon

## data frame

### global values
 - Setup
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
  - position: tuple[int, int]


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
  - size: tuple[int, int]
  - revers_key: dict[int, MapObject]
  - data: list[list[int]]
