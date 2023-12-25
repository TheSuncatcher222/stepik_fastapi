"""
Модуль создания логера.

Используется ColoredFormatter для цветового отображения уровней логирования.
Отступы сообщений от названия уровня логов синхронизированы с системными.
"""

import logging
import sys

from colorlog import ColoredFormatter

FORMAT = '%(log_color)s%(levelname)-10s%(reset)s%(message)s - %(asctime)s at %(name)s.%(funcName)s(%(lineno)d)'

FORMATTER = ColoredFormatter(
    fmt=FORMAT,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
)


def get_stream_handler():
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(FORMATTER)
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_stream_handler())
    return logger
