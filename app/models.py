from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class EmulatorConfig:
    name: str
    window_title: str
    monitor_index: int
    enabled: bool = True


@dataclass(slots=True)
class LoggingConfig:
    level: str
    directory: Path
    as_json: bool = True


@dataclass(slots=True)
class RuntimeConfig:
    loop_interval_seconds: float
    save_failure_screenshots: bool
    artifacts_directory: Path


@dataclass(slots=True)
class AppSettings:
    logging: LoggingConfig
    runtime: RuntimeConfig
    emulators: list[EmulatorConfig]
