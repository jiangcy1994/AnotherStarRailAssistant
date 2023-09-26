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

    def set_foreground(self) -> None:
        win32gui.SetForegroundWindow(self.hwnd)

    def mouse_click(self, x: int, y: int, delay: float, button: str = 'L') -> None:
        self.set_cursor_pos(x, y)
        if button == 'L':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            sleep(delay)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif button == 'R':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            sleep(delay)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    @staticmethod
    def set_cursor_pos(x: int, y: int) -> None:
        win32api.SetCursorPos([x, y])

    @staticmethod
    def get_cursor_pos() -> (int, int):
        return win32api.GetCursorPos()

    @staticmethod
    def mouse_move(dx: int, dy: int, delay: float) -> None:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)
        sleep(delay)

    @staticmethod
    def keyboard_click(key: str, delay: int) -> None:
        key_num = _key_num_map(key)
        win32api.keybd_event(key_num, 0, 0, 0)
        sleep(delay)
        win32api.keybd_event(key_num, win32con.KEYEVENTF_KEYUP, 0, 0)


def _key_num_map(key: str) -> int:
    if len(key) < 0:
        return 0
    if len(key) == 1:
        return ord(key.upper())
    if key.upper() == 'TAB':
        return ord('\t')
    if key.upper().startswith('F'):
        return 111 + int(key[1:])
    return 0
