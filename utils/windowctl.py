from time import sleep

import win32api
import win32con
import win32gui

from utils.logs import logger

__all__ = ['WindowsCtl']


class WindowsCtl:
    _hwnd: int
    _window_name: str | int
    _class_name: str | int

    def __int__(self, class_name: str | int, window_name: str | int):
        if class_name == 0 and window_name == 0:
            error_str: str = 'Can Not Set Both class_name and window_name 0'
            logger.error(error_str)
            raise ValueError(error_str)
        self._hwnd = 0
        self._class_name = class_name
        self._window_name = window_name

    @property
    def hwnd(self) -> int:
        if self._hwnd == 0:
            self._hwnd = win32gui.FindWindow(self.class_name, self.window_name)
            if self._hwnd == 0:
                error_str: str = 'Can Not FindWindow with class_name: {0}, window_name: {1}'.format(self.class_name,
                                                                                                    self.window_name)
                logger.error(error_str)
                raise ValueError(error_str)
        return self._hwnd

    @property
    def class_name(self) -> str:
        return self._class_name

    @class_name.setter
    def class_name(self, name: str) -> None:
        self._class_name = name
        self._hwnd = 0

    @property
    def window_name(self) -> str:
        return self._window_name

    @window_name.setter
    def window_name(self, name: str) -> None:
        self._window_name = name
        self._hwnd = 0

    def get_focus(self) -> int:
        return win32api.SendMessage(self.hwnd, win32con.WM_SETFOCUS, 0, 0)

    def mouse_click(self, x: int, y: int, delay: float, button: str = 'L') -> None:
        point = win32api.MAKELONG(x, y)
        if button == 'L':
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, point)
            sleep(delay)
            win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, point)
        elif button == 'R':
            win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONDOWN, 0, point)
            sleep(delay)
            win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, point)

    def keyboard_click(self, key: str, delay: int) -> None:
        key = key.upper()
        key_num = int(key_num_map(key))
        num = win32api.MapVirtualKey(key_num, 0)
        dparam = 1 | (num << 16)
        uparam = 1 | (num << 16) | (1 << 30) | (1 << 31)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, 0, dparam)
        sleep(delay)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, uparam)


def key_num_map(key: str) -> int:
    if len(key) < 0:
        return 0
    if len(key) == 1:
        return ord(key.upper())
    if key.upper() == 'TAB':
        return ord('\t')
    if key.upper().startswith('F'):
        return 111 + int(key[1:])
    return 0
