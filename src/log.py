"""very simple logging mini-module"""
from enum import Enum
from datetime import datetime
from typing import Union


class LogModes(Enum):
    """Enum containing log modes"""
    ON = 1
    VERBOSE = 2
    OFF = 3

class LogTypes(Enum):
    NORMAL = 1
    ERROR = 2

LOGGING_MODE = LogModes.ON


def colorify(val: str, color: str) -> str:
    """Function that takes a string and adds colors to it.

    Args:
        * val (str): The string to add color to.
        * color (str): The color.

    Returns:
        str
    """
    color_code = {
        "byellow": "\033[1;33m",
        "custom": "\033[0;34;47m",
        "magenta": "\033[35m",
        "yellow": "\033[33m",
        "green": "\033[32m",
        "black": "\033[30m",
        "white": "\033[37m",
        "blue": "\033[34m",
        "cyan": "\033[96m",
        "cyan2": "\033[36m",
        "red": "\033[91m"
    }
    return color_code[color.lower()] + str(val) + "\033[0m"



def log(
    message: str,
    type: LogTypes = LogTypes.NORMAL,
    mode: LogModes = LOGGING_MODE,
    is_inp: bool = False,
    color: Union[str, None] = None
    ):
    """Logs message if logging is on, and logs time if verbose

    Args:
        * message (str): the message to log.
        * type (LogTypes): the type of the log (either NORMAL or ERROR), defaults to NORMAL
        * mode (LogModes): the mode, verbose, etc, defaults to LOGGING_MODE
        * is_input (bool): should we ask for input after logging, defaults to False
        * color (str | None): the color of the log, defaults to None

    Returns:
        str | None: string if is_input
    """
    if mode == LogModes.ON:
        if not color:
            print(
                colorify(message, "red")
                if type == LogTypes.ERROR
                else colorify(message, "byellow"),
                end="" if is_inp else "\n"
            )
            if is_inp:
                return input()
        else:
            print(colorify(message, color), end="" if is_inp else "\n")
            if is_inp:
                return input()

        return

    if LOGGING_MODE == LogModes.VERBOSE and mode == LogModes.VERBOSE:
        verbose_message = f"[{str(datetime.now().time())}]: {message}"
        if not color:
            print(
                colorify(verbose_message, "red")
                if type == LogTypes.ERROR
                else colorify(verbose_message, "cyan"),
                end="" if is_inp else "\n"
            )
            if is_inp:
                return input()
        else:
            print(colorify(verbose_message, "byellow"), end="" if is_inp else "\n")
            if is_inp:
                return input()
