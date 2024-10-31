"""
    CodingTools

This module contain processes for developing systems.
"""


""" imports """


try:
    from . import Definition
    ...
except ImportError as er:
    Definition = ImportError(er)
    ...


try:
    from . import Types
    ...
except ImportError as er:
    Types = ImportError(er)
    ...


try:
    from . import Function
    ...
except ImportError as er:
    Function = ImportError(er)
    ...


try:
    from . import Inheritance
    ...
except ImportError as er:
    Inheritance = ImportError(er)
    ...

