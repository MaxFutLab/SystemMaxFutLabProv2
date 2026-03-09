from __future__ import annotations

import logging
import time
from datetime import UTC, datetime
from pathlib import Path

import cv2

from app.automation.state_machine import BotState, StateMachine
from app.emulator.manager import EmulatorManager
from app.input.controller import InputController
from app.models import AppSettings
from app.vision.detector import VisionDetector
from app.vision.screen_capture import ScreenCaptureService


class AutomationRunner:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self.logger = logging.getLogger(self.__class__.__name__)
        self.state_machine = StateMachine()
        self.emulator_manager = EmulatorManager(settings.emulators)
        self.screen_capture = ScreenCaptureService()
        self.vision = VisionDetector()
        self.input_controller = InputController()

    def run_once(self) -> None:
        self.state_machine.transition_to(BotState.IDLE, "Estrutura inicial carregada")

        for emulator in self.emulator_manager.list_active():
            emulator.activate()
            frame = self.screen_capture.capture_monitor(emulator.config.monitor_index)
            self.logger.info(
                "Ciclo executado",
                extra={
                    "context": {
                        "emulator": emulator.config.name,
                        "monitor": frame.monitor_index,
                        "resolution": frame.image_bgr.shape,
                    }
                },
            )

        self.state_machine.transition_to(BotState.RUNNING, "Loop principal finalizado")

    def run_forever(self) -> None:
        interval = self.settings.runtime.loop_interval_seconds
        self.logger.info(
            "Iniciando execução contínua",
            extra={"context": {"interval_seconds": interval}},
        )

        while True:
            try:
                self.run_once()
            except Exception as exc:  # fluxo global de segurança
                self.state_machine.transition_to(BotState.ERROR, "Falha no loop")
                self.logger.exception("Erro no loop principal", extra={"context": {"error": str(exc)}})
                if self.settings.runtime.save_failure_screenshots:
                    self._save_failure_screenshot()
            time.sleep(interval)

    def _save_failure_screenshot(self) -> None:
        artifacts_dir = self.settings.runtime.artifacts_directory
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        filename = datetime.now(UTC).strftime("failure_%Y%m%d_%H%M%S.png")
        path = artifacts_dir / filename

        frame = self.screen_capture.capture_monitor(monitor_index=1)
        cv2.imwrite(str(path), frame.image_bgr)
        self.logger.info("Screenshot de falha salvo", extra={"context": {"path": str(path)}})
