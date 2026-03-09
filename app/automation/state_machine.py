from __future__ import annotations

import logging
from enum import Enum, auto


class BotState(Enum):
    INITIALIZING = auto()
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()


class StateMachine:
    def __init__(self) -> None:
        self.current_state = BotState.INITIALIZING
        self.logger = logging.getLogger(self.__class__.__name__)

    def transition_to(self, new_state: BotState, reason: str) -> None:
        old_state = self.current_state
        self.current_state = new_state
        self.logger.info(
            "Transição de estado",
            extra={
                "context": {
                    "from": old_state.name,
                    "to": new_state.name,
                    "reason": reason,
                }
            },
        )
