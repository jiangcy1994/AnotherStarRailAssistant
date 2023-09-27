import ctypes
from functools import partial
from time import sleep

import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from utils.logs import logger

__all__ = ['WindowCtl']


class WindowCtl:
    _hwnd: int
    _class_name: str | int
    _window_name: str | int
    _window_rect: list[int]

    def __init__(self, class_name: str | int = 0, window_name: str | int = 0):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()

        if class_name == 0 and window_name == 0:
            error_str: str = 'can not set both class_name and window_name 0'
            logger.error(error_str)
            raise ValueError(error_str)
        self._hwnd = 0
        self._class_name = class_name
        self._window_name = window_name
        self._window_rect = [0, 0, 0, 0]

        self.set_foreground = partial(win32gui.SetForegroundWindow, self.hwnd)

    @property
    def hwnd(self) -> int:
        if self._hwnd == 0:
            self._hwnd = win32gui.FindWindow(self.class_name, self.window_name)
            if self._hwnd == 0:
                error_str: str = 'can not FindWindow with class_name: {0}, window_name: {1}'.format(self.class_name,
                                                                                                    self.window_name)
                logger.error(error_str)
                raise ValueError(error_str)
        return self._hwnd

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def window_name(self) -> str:
        return self._window_name

    @property
    def window_rect(self) -> list[int]:
        if self._window_rect == [0, 0, 0, 0]:
            self._window_rect = win32gui.GetWindowRect(self.hwnd)
        return self._window_rect

    @property
    def window_width(self) -> int:
        return self.window_rect[2] - self.window_rect[0]

    @property
    def window_height(self) -> int:
        return self.window_rect[3] - self.window_rect[1]

    @property
    def screenshot(self) -> np.ndarray:
        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        src_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        mem_dc = src_dc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(src_dc, self.window_width, self.window_height)
        mem_dc.SelectObject(bmp)
        mem_dc.BitBlt((0, 0), (self.window_width, self.window_height), src_dc, (0, 0), win32con.SRCCOPY)
        img_np = np.fromstring(bmp.GetBitmapBits(True), dtype='uint8')
        img_np.shape = (self.window_height, self.window_width, 4)
        logger.debug('image taken with size ({0}, {1})'.format(self.window_width, self.window_height))
        return img_np

    @staticmethod
    def mouse_click(x: int, y: int, delay: float, button: str = 'LEFT') -> None:
        win32api.SetCursorPos((x, y))
        button_list = ['LEFT', 'MIDDLE', 'RIGHT']
        if button not in button_list:
            error_str: str = 'can not accept button {0}, select in {1}'.format(button, button_list)
            logger.error(error_str)
            raise ValueError(error_str)
        win32api.mouse_event(win32con.__dict__.get('MOUSEEVENTF_' + button + 'DOWN'), 0, 0)
        sleep(delay)
        win32api.mouse_event(win32con.__dict__.get('MOUSEEVENTF_' + button + 'UP'), 0, 0)
        logger.debug('mouse {0} button click at ({1}, {2}) with delay {3} s'.format(button, x, y, delay))

    @staticmethod
    def mouse_move(dx: int = 0, dy: int = 0) -> None:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)
        logger.debug('mouse move with (dx, dy): ({0}, {1})'.format(dx, dy))

    @staticmethod
    def keyboard_press(key: str, delay: float) -> None:
        vk_num = WindowCtl.vk_num_map(key)
        win32api.keybd_event(vk_num, 0, 0, 0)
        sleep(delay)
        win32api.keybd_event(vk_num, win32con.KEYEVENTF_KEYUP, 0, 0)
        logger.debug('keyboard {0} key press with delay {1} s'.format(key, delay))

    @staticmethod
    def vk_num_map(key: str) -> int:
        if len(key) == 0:
            error_str: str = 'can not key_num with no key'
            logger.error(error_str)
            raise ValueError(error_str)
        if len(key) == 1:
            return ord(key.upper())
        result = win32con.__dict__.get('VK_' + key)
        if result is None:
            error_str: str = 'can not key_num with Key: {0}'.format(key)
            logger.error(error_str)
            raise ValueError(error_str)
        return result
