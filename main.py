from __future__ import annotations

import argparse
import logging

from app.automation.runner import AutomationRunner
from app.utils.config_loader import load_settings
from app.utils.logging_config import configure_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automação modular de emuladores Android")
    parser.add_argument(
        "--config",
        default="config/settings.json",
        help="Caminho do arquivo de configuração JSON",
    )
    parser.add_argument(
        "--mode",
        choices=["once", "loop"],
        default="once",
        help="Executa um ciclo único ou loop contínuo",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings(settings_path=args.config)
    configure_logging(settings.logging)

    logging.getLogger(__name__).info("Aplicação inicializada")

    runner = AutomationRunner(settings)
    if args.mode == "once":
        runner.run_once()
    else:
        runner.run_forever()


if __name__ == "__main__":
    main()
