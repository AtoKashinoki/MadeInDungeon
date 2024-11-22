"""
    MadeInDungeon.test

This file contain MadeInDungeon test process.
"""


""" imports """


import sys
from src.Engine import ApplicationEngine, Exit
from CodingTools.Definition import Msvcrt
from src.create_dungeon import test
Key = Msvcrt.Key


""" processes """


class TypeWriter(ApplicationEngine):
    __typed: str
    def __init__(self):
        super().__init__(_fps=10)
        self.__typed = ""
        return

    def __update__(self, ):
        if Key.Ins in self.input: self.reboot()
        if Key.Del in self.input: raise Exit
        return

    def __rendering__(self, ):
        self.print(f"input_keys{self.input}")
        return

    ...


if __name__ == '__main__':
    test()