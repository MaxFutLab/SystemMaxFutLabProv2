from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(slots=True)
class DetectionResult:
    found: bool
    confidence: float
    position: tuple[int, int] | None = None


class VisionDetector:
    def __init__(self, match_threshold: float = 0.85) -> None:
        self.match_threshold = match_threshold
        self.logger = logging.getLogger(self.__class__.__name__)

    def detect_template(self, frame_bgr: np.ndarray, template_path: Path) -> DetectionResult:
        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
        if template is None:
            self.logger.warning(
                "Template não encontrado",
                extra={"context": {"template_path": str(template_path)}},
            )
            return DetectionResult(found=False, confidence=0.0)

        result = cv2.matchTemplate(frame_bgr, template, cv2.TM_CCOEFF_NORMED)
        _, max_value, _, max_location = cv2.minMaxLoc(result)

        found = max_value >= self.match_threshold
        detection = DetectionResult(
            found=found,
            confidence=float(max_value),
            position=(int(max_location[0]), int(max_location[1])) if found else None,
        )

        self.logger.debug(
            "Template processado",
            extra={
                "context": {
                    "template_path": str(template_path),
                    "found": detection.found,
                    "confidence": detection.confidence,
                }
            },
        )
        return detection
