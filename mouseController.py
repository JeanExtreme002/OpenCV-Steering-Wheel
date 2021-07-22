from win32api import GetCursorPos, GetSystemMetrics, SetCursorPos
from threading import Thread
import time

__all__ = ("MouseController",)

class MouseController(Thread):

    __pause = False
    __stop = False

    def __init__(self, steering_wheel):
        super().__init__(target = self.__move_mouse)
        self.__steering_wheel = steering_wheel
        self.__screen_width = GetSystemMetrics(0)

    def __get_cursor_position(self):
        return self.__get_position_x(), self.__get_position_y()

    def __get_position_x(self):
        return int(self.__screen_width / 2 - self.__screen_width / 2 / 100 * self.__steering_wheel.get_percent())

    def __get_position_y(self):
        return GetCursorPos()[1]

    def __move_mouse(self):
        while not self.__stop:
            if not self.__pause:
                SetCursorPos(self.__get_cursor_position())
            time.sleep(0.01)

    def pause(self):
        self.__pause = True

    def resume(self):
        self.__pause = False

    def start(self):
        self.__pause = False
        self.__stop = False
        super().start()

    def stop(self):
        self.__stop = True
