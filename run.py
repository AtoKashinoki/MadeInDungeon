from Game import game_process
from Object import Player
from CodingTools.Types import Position

if __name__ == '__main__':
    player: Player = Player(Position(1, 1), 0, 0)
    game_process(player)
    ...