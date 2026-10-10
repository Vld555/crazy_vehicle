"""Логирование шагов тестов с учётом вложенности вызовов.

Лог пишется в консоль и в файл ``tests/logs/test_<время>.log``.
"""

import contextvars
import functools
import logging
import os
import sys
from datetime import datetime

_LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

_formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S")

_file_handler = logging.FileHandler(
    os.path.join(_LOG_DIR, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    encoding="utf-8",
)
_file_handler.setFormatter(_formatter)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_formatter)

_logger = logging.getLogger("walking_hut_tests")
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _logger.addHandler(_file_handler)
    _logger.addHandler(_console_handler)
_logger.propagate = False

_depth = contextvars.ContextVar("_depth", default=0)
_INDENT = "    "


def _log(message: str) -> None:
    _logger.info(f"{_INDENT * _depth.get()}{message}")


def begin_test(test_name: str) -> None:
    """Открывает блок лога теста."""
    _depth.set(0)
    _log(f"===== START {test_name} =====")


def end_test() -> None:
    """Закрывает блок лога теста."""
    _depth.set(0)
    _log("===== END =====")


def step(text: str) -> None:
    """Пишет в лог шаг сценария."""
    _log(f"[STEP] {text}")


def logger(func):
    """Логирует вызов функции, её аргументы, результат или исключение."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        shown = [repr(a) for a in args[1:]] + [f"{k}={v!r}" for k, v in kwargs.items()]
        _log(f"-> {func.__qualname__}({', '.join(shown)})")
        token = _depth.set(_depth.get() + 1)
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            _depth.reset(token)
            _log(f"<- {func.__qualname__} raised {type(error).__name__}: {error}")
            raise
        _depth.reset(token)
        _log(f"<- {func.__qualname__} = {result!r}")
        return result

    return wrapper
