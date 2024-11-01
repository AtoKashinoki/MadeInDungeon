from Game import hierarchy_process
from Object import Player
from CodingTools.Types import Position

if __name__ == '__main__':
    player: Player = Player(Position(2), 0, 0)
    hierarchy_process(player)
    ...
