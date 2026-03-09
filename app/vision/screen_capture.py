from __future__ import annotations

import logging
from dataclasses import dataclass

import mss
import numpy as np


@dataclass(slots=True)
class CapturedFrame:
    monitor_index: int
    image_bgr: np.ndarray


class ScreenCaptureService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def capture_monitor(self, monitor_index: int) -> CapturedFrame:
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            raw = np.array(sct.grab(monitor))
            bgr = raw[:, :, :3]

        self.logger.debug(
            "Captura de tela concluída",
            extra={"context": {"monitor_index": monitor_index, "shape": bgr.shape}},
        )
        return CapturedFrame(monitor_index=monitor_index, image_bgr=bgr)
