from __future__ import annotations

import logging

import pyautogui


class InputController:
    def __init__(self, action_delay: float = 0.1) -> None:
        self.action_delay = action_delay
        self.logger = logging.getLogger(self.__class__.__name__)
        pyautogui.PAUSE = action_delay

    def click(self, x: int, y: int) -> None:
        pyautogui.click(x=x, y=y)
        self.logger.info("Clique executado", extra={"context": {"x": x, "y": y}})

    def press_key(self, key: str) -> None:
        pyautogui.press(key)
        self.logger.info("Tecla pressionada", extra={"context": {"key": key}})
