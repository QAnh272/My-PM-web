import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ensure_logs_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def configure_logger(
    name: str | None = None,
    level: int | str = logging.INFO,
    logfile: str | None = None,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    console: bool = True,
) -> logging.Logger:
    """Configure and return a logger with rotating file and console handlers."""

    if isinstance(level, str):
        level = logging._nameToLevel.get(level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        logger.setLevel(level)
        return logger

    fmt = "%(asctime)s %(levelname)s [%(name)s] %(module)s.%(funcName)s:%(lineno)d - %(message)s"
    formatter = logging.Formatter(fmt)

    if logfile is None:
        proj = _project_root()
        logs_dir = proj / "logs"
        _ensure_logs_dir(logs_dir)
        logfile = str(logs_dir / "app.log")

    try:
        fh = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        pass

    if console:
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    logger.propagate = False

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    return configure_logger(name=name)


__all__ = ["get_logger", "configure_logger"]
