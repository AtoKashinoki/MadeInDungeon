"""
    CodingTools.Definition

This file contain definition values for developing systems.
"""


""" imports """


from abc import ABC


""" definition class skeleton """


class DefinitionSkeleton(ABC):
    """ Definition class base """
    ...


""" system """


class OS(DefinitionSkeleton):
    """ OS system definitions """
    Unix: str = "posix"
    Windows: str = "nt"
    ...


class SystemKey(DefinitionSkeleton):
    """ System definitions """
    REBOOT = 2
    ...


""" protect member """


class ProtectMember(DefinitionSkeleton):
    """ Protect member definitions """
    frame: str = "_{}{}"
    ...


""" index """


class Index(DefinitionSkeleton):
    """ Index definitions """
    X, Y, Z = range(3)
    ...


""" Msvcrt """


class Msvcrt(DefinitionSkeleton):
    """ msvcrt definitions """

    class Key(DefinitionSkeleton):
            """ msvcrt ord keys definitions """

            """ special keys """
            BackSpace = 8
            BS = BackSpace
            Enter = 13
            Space = 32
            Ins = 82
            Del = 83

            """ number keys """
            n0, n1, n2, n3, n4, n5, n6, n7, n8, n9 = range(48, 48+10)

            """ alphabet keys """
            A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = \
                range(65, 65+26)
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = \
                range(97, 97+26)

            """ symbol keys """
            s1, s2, s3, s4, s5, s6, s7, s8, s9 = range(33, 33+9)
            Comma, Hyphen, Dot, Slash = range(44,44+ 4)
            Colon, SemiColon = range(58, 58+2)
            At = 64
            BracketT, BackSlash, BracketE = range(91, 91+3)

            """ Arrow keys """
            Top, Left, Right, Bottom = 72, 75,  77, 80

            ...
    alphabet: str = (
        "A", "B", "C", "D", "E", "F", "G", "H", "I",
        "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z",
        "a", "b", "c", "d", "e", "f", "g", "h", "I",
        "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x", "y", "z",
    )

    alphabet_keys: tuple[int] = tuple([
        Key.A, Key.B, Key.C, Key.D, Key.E, Key.F, Key.G, Key.H, Key.I,
        Key.J, Key.K, Key.L, Key.M, Key.N, Key.O, Key.P, Key.Q, Key.R,
        Key.S, Key.T, Key.U, Key.V, Key.W, Key.X, Key.Y, Key.Z,
        Key.a, Key.b, Key.c, Key.d, Key.e, Key.f, Key.g, Key.h, Key.i,
        Key.j, Key.k, Key.l, Key.m, Key.n, Key.o, Key.p, Key.q, Key.r,
        Key.s, Key.t, Key.u, Key.v, Key.w, Key.x, Key.y, Key.z,
    ])

    alphabet_dict: dict[int, str] = \
        dict(zip(alphabet_keys, alphabet))

    rev_alphabet_dict: dict[int, str] = \
        dict(zip(alphabet, alphabet_keys))

    ...

