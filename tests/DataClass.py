
from CodingTools.Inheritance import DataClass


class Test(DataClass):
    """ DataClass test """
    """ values """
    # class
    a: str = "1"
    b: int = 2
    c: float = 3.

    # instance
    d: str
    e: int
    f: float

    ...


""" run process """


if __name__ == '__main__':
    test = Test(d="4", e=5)
    Test.a = "10!"
    print(test)
