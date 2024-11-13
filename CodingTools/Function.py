"""
    CodingTools.Function

This file is contain functions for developing systems.
"""


""" imports """


from abc import ABC
import os
from .Definition import ProtectMember, OS, Msvcrt


""" Error  """


class UnknownError(Exception): ...


""" Functions skeleton """


class FunctionsSkeleton(ABC):
    """ Functions class base """
    ...


""" System """


class System(FunctionsSkeleton):
    """ System functions """

    @staticmethod
    def run_python(file: str) -> int:
        """ Run python file """
        run_com: str = ""

        match os.name:
            case OS.Unix: run_com = "python3 {}"
            case OS.Windows: run_com = "python3 {}"
            case _: raise UnknownError("This os unknown.")

        return os.system(run_com.format(file))

    ...


""" Convert """


class Convert(FunctionsSkeleton):
    """ Convert functions """

    @staticmethod
    def protect_member_from(_type: type, _name: str) -> str:
        """ convert protect member from type and name """
        return ProtectMember.frame.format(
            _type.__name__, _name
        )

    ...
