"""
    CodingTools.Function

This file is contain functions for developing systems.
"""


""" imports """


from abc import ABC
from .Definition import ProtectMember


""" Functions skeleton """


class FunctionsSkeleton(ABC):
    """ Functions class base """
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
