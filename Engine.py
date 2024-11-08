"""
    MadeInDungeon.AppEngine

This file contain application engine processes.
"""


""" imports """


from os import system
from abc import ABC, abstractmethod
from typing import Literal
from time import time
from threading import Thread
import msvcrt
from CodingTools.Inheritance import DataClass
from CodingTools.Definition import SystemKey


""" errors """


class Exit(Exception): ...


""" Input system """


class Input(ABC):
    """ Input class base """
    @abstractmethod
    def update(self) -> None:
        """ Update input data"""
        return
    @abstractmethod
    def get(self) -> tuple:
        """ Return press keys """
        return NotImplemented
    @abstractmethod
    def reset(self) -> None:
        """ Reset input data """
        return


class MsvcrtSet(Input):
    """ msvcrt input class """

    """ values """
    # constants

    # instances
    __pressed_keys: set

    """ properties """
    @property
    def pressed(self) -> tuple: return self.get()

    """ processes """
    def __init__(self):
        """ Initialize input system """
        self.__pressed_keys = set()
        return

    def get(self) -> tuple:
        """ Return press key """
        return tuple(self.__pressed_keys)

    def check_press(self):
        if msvcrt.kbhit():
            self.__pressed_keys.add(ord(msvcrt.getch()))
            ...
        return

    def update(self) -> None:
        """ update input keys """
        Thread(target=self.check_press).start()
        return

    def reset(self) -> None:
        """ reset input keys """
        self.__pressed_keys = set()
        return

    ...


class MsvcrtList(Input):
    """ msvcrt input class """

    """ values """
    # instances
    __pressed_keys: list

    """ processes """
    def __init__(self):
        """ Initialize input system """
        self.__pressed_keys = list()
        return

    def get(self) -> tuple:
        """ Return press key """
        return MsvcrtSet.get(self)

    def check_press(self):
        if msvcrt.kbhit():
            self.__pressed_keys.append(ord(msvcrt.getch()))
            ...
        return

    def update(self) -> None:
        """ update input keys """
        Thread(target=self.check_press).start()
        return

    def reset(self) -> None:
        """ reset input keys """
        self.__pressed_keys = list()
        return

    ...


""" rendering system"""


class Rendering(ABC):
    """ Rendering class base """
    @abstractmethod
    def print(
            self,
            *values: object,
            sep = " ", end = "\n",
            file: str | None = None,
            flush: Literal[False] = False,
    ) -> None:
        """ print text """
        return
    @abstractmethod
    def render(self, __rendering__) -> None:
        """ render function """
        return

    ...


class Console(Rendering):
    """ render in console """

    """ values """
    # constants

    # instances
    __frame_text: str

    """ properties """

    """ processes """

    def __init__(self):
        self.__frame_text = ""
        return

    def print(
            self,
            *values: object,
            sep = " ", end = "\n",
            file: str | None = None,
            flush: Literal[False] = False,
    ) -> None:
        str_values = map(str, values)
        self.__frame_text += sep.join(str_values) + end
        return

    def render(self, __rendering__) -> None:
        system('cls')
        self.__frame_text = ""
        __rendering__()
        print(self.__frame_text, end="")
        return

    ...


""" app engine class """


class ApplicationEngine(ABC):
    """ Application skeleton class """

    """ values """
    # instance
    class Config(DataClass):
        fps: int
        input_sys = Msvcrt
        rendering_sys = Console
        ...

    __config: Config = None
    __input: tuple
    __rendering_sys: Rendering | None = None
    __reboot_flag: bool

    """ properties """
    @property
    def input(self) -> tuple:
        return self.__input

    """ methods """

    # abstract
    @abstractmethod
    def __update__(self, ):
        """ Execute frame processing """
        return

    @abstractmethod
    def __rendering__(self, ):
        """ Execute rendering processing """
        return

    # instance
    def __init__(self, _fps: int = 10):
        """ Initialize application engine """
        self.__config = self.Config()
        self.__config.fps = _fps
        self.__input = tuple()
        self.__rendering_sys = Console()
        self.__reboot_flag = False
        return

    def print(
            self,
            *values: object,
            sep = " ", end = "\n",
            file: str | None = None,
            flush: Literal[False] = False,
    ) -> None:
        self.__rendering_sys.print(
            *values,
            sep = sep, end = end,
            file = file, flush = flush
        )
        return

    def __running_process(self) -> None:
        """ running process """
        one_frame_time = 1 / self.__config.fps
        pre_update_time = time()
        input_sys = self.__config.input_sys()
        self.__rendering_sys = self.__config.rendering_sys()

        done = False
        while not done:
            # input update
            input_sys.update()

            # frame process
            now = time()
            if now - pre_update_time < one_frame_time:
                continue
            pre_update_time = now

            self.__input = input_sys.get()

            # frame process
            try:
                self.__update__()
                ...
            except Exit:
                done = True
                ...

            # rendering
            self.__rendering_sys.render(self.__rendering__)

            # input reset
            input_sys.reset()

            # reboot process
            if self.__reboot_flag: done = True
            ...
        return

    def exe(self) -> int:
        """ execute game engine """
        self.__running_process()
        if self.__reboot_flag: return SystemKey.REBOOT
        return 0

    def reboot(self):
        """ reboot game engine """
        self.__reboot_flag = True
        return