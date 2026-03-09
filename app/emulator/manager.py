from __future__ import annotations

import logging

from app.models import EmulatorConfig


class EmulatorInstance:
    def __init__(self, config: EmulatorConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(f"emulator.{config.name}")

    def activate(self) -> None:
        self.logger.info(
            "Ativando instância de emulador",
            extra={"context": {"window_title": self.config.window_title}},
        )


class EmulatorManager:
    def __init__(self, configs: list[EmulatorConfig]) -> None:
        self.instances = [EmulatorInstance(cfg) for cfg in configs if cfg.enabled]
        self.logger = logging.getLogger(self.__class__.__name__)

    def list_active(self) -> list[EmulatorInstance]:
        self.logger.info(
            "Instâncias ativas carregadas",
            extra={"context": {"count": len(self.instances)}},
        )
        return self.instances
