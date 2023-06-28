# -*- coding: utf-8 -*-
"""Custom Logger Using Loguru."""

import json
import logging
import sys
from pathlib import Path

from django.conf import settings
from loguru import logger

from utils.logger.logger_telegram import log_to_telegram


class InterceptHandler(logging.Handler):
    """Intercept logs from other loggers."""

    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        """Emit log record."""
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


class CustomizeLogger:
    """Customize logger."""

    @classmethod
    def make_logger(cls, config_path: Path):
        """Make logger."""
        config = cls.load_logging_config(config_path)
        logging_config = config.get("logger")

        logger = cls.customize_logging(
            level=logging_config.get("level"),
            format=logging_config.get("format"),
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        level: str,
        format: str,
    ):
        """Customize logging."""
        logger.remove()

        if settings.TELEGRAM_LOGGING_ENABLED:
            logger.add(
                log_to_telegram,
                backtrace=True,
                level=logging.ERROR,
                format=format,
            )
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logging.getLogger("uvicorn.server").handlers.clear()
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in [
            "uvicorn",
            "uvicorn.error",
            "uvicorn.access",
            "uvicorn.lifespan",
            "uvicorn.server",
            "fastapi",
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        """Load logging config from json file."""
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
