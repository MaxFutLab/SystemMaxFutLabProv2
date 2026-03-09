from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from app.models import AppSettings, EmulatorConfig, LoggingConfig, RuntimeConfig


DEFAULT_SETTINGS_PATH = Path("config/settings.json")


def load_settings(settings_path: Union[str, Path] = DEFAULT_SETTINGS_PATH) -> AppSettings:
    settings_file = Path(settings_path)
    raw = json.loads(settings_file.read_text(encoding="utf-8"))

    logging_cfg = raw["logging"]
    runtime_cfg = raw["runtime"]

    emulators = [
        EmulatorConfig(
            name=item["name"],
            window_title=item["window_title"],
            monitor_index=item["monitor_index"],
            enabled=item.get("enabled", True),
        )
        for item in raw["emulators"]
    ]

    return AppSettings(
        logging=LoggingConfig(
            level=logging_cfg.get("level", "INFO"),
            directory=Path(logging_cfg.get("directory", "logs")),
            as_json=logging_cfg.get("json", True),
        ),
        runtime=RuntimeConfig(
            loop_interval_seconds=float(runtime_cfg.get("loop_interval_seconds", 1.0)),
            save_failure_screenshots=bool(runtime_cfg.get("save_failure_screenshots", True)),
            artifacts_directory=Path(runtime_cfg.get("artifacts_directory", "artifacts")),
        ),
        emulators=emulators,
    )
