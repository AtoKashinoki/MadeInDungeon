"""
    CodingTools.Definition

This file contain definition values for developing system.
"""


""" imports """


from abc import ABC


""" definition class skeleton """


class DefinitionSkeleton(ABC):
    """ Definition class base """
    ...


""" protect member """


class ProtectMember(DefinitionSkeleton):
    """ Protect member definitions """
    frame: str = "_{}{}"
    ...
