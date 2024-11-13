"""
    MadeInDungeon.run

This file contain running MadeInDungeon.
"""


""" imports """


from os import getcwd
import sys
from time import sleep
from Game import game_process


""" values """


game_file = f"{getcwd()}\\Game.py"


""" run processes """


def run_game():
    """ run game """
    print("Boot MadeInDungeon")
    sleep(2**-2)
    game_process()
    return 0

if __name__ == '__main__':
    exit_code = run_game()
    sys.exit(exit_code)
