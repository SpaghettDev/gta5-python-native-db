"""very simple logging mini-module"""
from enum import Enum
from datetime import datetime


class LogModes(Enum):
    """Enum containing log modes"""
    ON = 1
    VERBOSE = 2
    OFF = 3
    #
    ERROR = 4


LOGGING_MODE = LogModes.ON


def log(message: str, mode: LogModes = LOGGING_MODE):
    """Logs message if logging is on, and logs time if verbose"""
    if LOGGING_MODE == LogModes.ON:
        print(message)
    elif LOGGING_MODE == LogModes.VERBOSE and mode == LogModes.VERBOSE:
        print(f"[{str(datetime.now().time())}]: {message}")
