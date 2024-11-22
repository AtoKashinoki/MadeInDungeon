"""
    GameLoopEngine.AI

This file contain game AI skeleton.
"""


""" import """
from abc import ABC, abstractmethod
from src.Object import Enemy, PlayerStatus

""" AI skeleton """


class AISkeleton(ABC):
    """ AI base """

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def __move_process__(
            self,
            _visibility_map: tuple[tuple[int]],
            _player_status: PlayerStatus,
            _enemies: tuple[Enemy, ...],
    ) -> str: ...
    ...


""" AI selector """


""" debug """


if __name__ == '__main__':
    """ test code """
    ...
