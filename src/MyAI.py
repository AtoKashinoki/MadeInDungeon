"""
    GameLoopEngine.MyAI

This file contain game AIs.
"""


""" imports """
from src.Object import Enemy, PlayerStatus
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
            _visibility_map: tuple[tuple[int]],#プレイヤーの見えてるMAP
            _player_status: PlayerStatus,#
            _enemies: tuple[Enemy, ...],#MAP上で見えている敵のクラスのタプル=敵の位置わかるね＝
    ) -> str:
        input_key = "W"#ここに行動したいやつを入力する.
        return input_key
    #上記のやつつくれ

    ...


""" AI selector """


RUN_AI = MainAI()


""" debug """


if __name__ == '__main__':
    ...
