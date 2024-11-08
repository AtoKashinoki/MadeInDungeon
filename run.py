"""
    MadeInDungeon.run

This file contain running MadeInDungeon.
"""


""" imports """


from os import getcwd
import sys
from time import sleep
from CodingTools.Function import System
from Engine import SystemKey


""" values """


game_file = f"{getcwd()}\\test.py"


""" run processes """


def run_game():
    """ run game """
    print("Boot MadeInDungeon")
    sleep(2**-2)
    _exit_code = System.run_python(game_file)
    if _exit_code == SystemKey.REBOOT:
        print("reboot game")
        run_game()
        ...
    return _exit_code

if __name__ == '__main__':
    exit_code = run_game()
    sys.exit(exit_code)
