from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models import LoggingConfig


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "context"):
            payload["context"] = record.context

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(config: LoggingConfig) -> None:
    config.directory.mkdir(parents=True, exist_ok=True)
    log_file = config.directory / "automation.log"

    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(config.level.upper())

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    if config.as_json:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
