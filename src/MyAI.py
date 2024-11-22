"""
    GameLoopEngine.MyAI

This file contain game AIs.
"""
from src.Object import Enemy, PlayerStatus

""" imports """


from src.AISkeleton import AISkeleton


""" AI classes """


class MainAI(AISkeleton):
    """ AI class """

    """ values """

    """ properties """

    """ processes """

    # instance
    def __init__(self):
        return

    def __move_process__(
            self,
            _visibility_map: tuple[tuple[int]],
            _player_status: PlayerStatus,
            _enemies: tuple[Enemy, ...],
    ) -> str:
        input_key = "W"
        return input_key

    ...


""" AI selector """


RUN_AI = MainAI()


""" debug """


if __name__ == '__main__':
    ...
