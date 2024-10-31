"""
    CodingTools.Inheritance

This file contain inheritance classes for developing system.
"""


""" imports """


from abc import ABC, abstractmethod
from .Function import Convert


""" Inheritance skeleton """


class InheritanceSkeleton(ABC):
    """ Inheritance classes base """
    ...


""" DataClass """


class DataClass(InheritanceSkeleton):
    """ DataClass base """

    """ values """
    # instance
    __texture: str = "{}"
    __value_types: set[type] = {
        int, float, str, bool, tuple, list, dict, set
    }
    __exclusion_names: set[str] = {
        "__module__",
        "__main__",
        "__annotations__",
        "__doc__"
    }

    """ properties """

    """ processes """
    # instance
    def __init__(self, add_types: tuple[type] = (), **kwargs) -> None:
        """ Initialize and assign values """
        """ initialize instance values """
        self.__texture: str = \
            DataClass.__texture.format(self.__class__.__name__)

        value_types: set = DataClass.__value_types
        [value_types.add(_type) for _type in add_types]
        self.__value_types: set = value_types

        exclusion_names = DataClass.__exclusion_names
        add_exc_names: tuple[str, ...] = (
            Convert.protect_member_from(DataClass, "__"),
            Convert.protect_member_from(self.__class__, "__"),
        )
        [exclusion_names.add(_name) for _name in add_exc_names]
        self.__exclusion_names = exclusion_names

        self.__set_values__(**kwargs)
        return

    def __repr__(self):
        """ Texture to print """
        _values = self.__get_values__()
        _texture: str = self.__texture + "{}"
        return _texture.format(_values)

    def __set_values__(self, **kwargs: dict[str, any]) -> None:
        """ Assign values """
        [
            setattr(self, _name, _value)
            for _name, _value in kwargs.items()
        ]
        return

    def __get_values__(self) -> dict[str, any]:
        """ Get values """
        keys = (
            *self.__dict__.keys(), *self.__class__.__dict__.keys()
        )
        values: dict[str, any] = {
            _name: getattr(self, _name)
            for _name in keys
        }
        return {
            _key: _value
            for _key, _value in values.items()
            if 0 == sum([
                _name in _key for _name in self.__exclusion_names
            ])
            if type(_value) in self.__value_types
        }

    def __setitem__(self, _name, _value) -> None:
        """ Assign value """
        setattr(self, _name, _value)
        return

    def __getitem__(self, _name) -> any:
        """ Get value """
        return getattr(self, _name)

    ...
