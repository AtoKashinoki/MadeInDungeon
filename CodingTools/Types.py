"""
    CodingTools.Types

This file contain types for developing systems.
"""


""" imports """


""" Position """




from .Definition import Index
class Position(object):
    """ Manage position type """

    """ values """
    # instance
    __dimension: int
    __data: list[int | float]

    """ properties """
    @property
    def dimension(self): return self.__dimension
    @property
    def data(self) -> tuple: return tuple(self.__data)
    @property
    def x(self) -> int | float: return self.__data[Index.X]
    @property
    def y(self) -> int | float: return self.__data[Index.Y]
    @property
    def z(self) -> int | float: return self.__data[Index.Z]
    """ processes """
    # instance

    def __init__(self, *args: int) -> None:
        """ Initialize value """
        self.__dimension = len(args)
        self.__data = args
        return

    def __repr__(self):
        return f"{self.data}"

    def __setitem__(self, index: int, value: int | float) -> None:
        """ Set position value """
        self.__data[index] = value
        return

    def __getitem__(self, index: int) -> int | float:
        """ Get position value """
        return self.__data[index]

    def __iter__(self) -> iter:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    def move(self, movement: tuple[int, ...]) -> None:
        """ Move position to next position """
        self.__data = [
            _pos + _diff for _pos, _diff in zip(self.__data, movement)
        ]
        return self
    
    def __eq__(self, value: tuple) -> bool:
        return self.__data[0] == value[0] and self.__data[1] == value[1]

    ...
