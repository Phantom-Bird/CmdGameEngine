# copy from https://www.cnblogs.com/WhXcjm/p/14644044.html

from ctypes import pointer, Structure, windll
from ctypes.wintypes import WORD, SHORT, SMALL_RECT
import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12


class COORD(Structure):
    _fields_ = [("X", SHORT), ("Y", SHORT)]

    def __init__(self, x, y):
        self.X = x
        self.Y = y


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                ("wAttributes", WORD), ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]


def gotoxy(x, y):
    hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleCursorPosition(hOut, COORD(x, y))


def getxy():
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(hOut, pointer(csbi))
    return csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y

def delln(n):
    gotoxy(0, getxy()[1] - n)