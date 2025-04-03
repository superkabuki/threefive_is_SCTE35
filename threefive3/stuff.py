"""
stuff.py functions and such common to threefive3.

print2, atohif, iso8601, red, blue
"""

import datetime
from sys import stderr

write2 = True


def print2(gonzo=b""):
    """
    print2 prints to 2 aka stderr.
    """
    if write2:
        print(gonzo, file=stderr, flush=True)
    else:
        print(gonzo)


def _isfloat(value):
    return "." in value and value.replace(".", "").isdigit()


def atohif(value):
    """
    atohif converts ascii to (hex|int|float)
    """
    if isinstance(value, str):
        value = value.strip()
        value = value.strip(",")
        if "0x" in value.lower():
            value = int(value, 16)
        elif value.isdigit():
            value = int(value)
        elif _isfloat(value):
            value = float(value)
    return value


def iso8601():
    """
    return UTC time in iso8601 format.

    '2023-05-11T15:55:51.'

    """
    return f"{datetime.datetime.utcnow().isoformat()[:-4]}Z "


def red(message):
    """
    red  print error messages in red to stderr.

    """
    mesg = f" \033[107;31m {message} \033[0m "
    print2(mesg)


def blue(message):
    """
    blue  print info messages in blue to stderr.

    """
    mesg = f"\033[;107m\033[44m{message} \033[0m"
    print2(mesg)


def reblue(message):
    """
    reblue overwrites the last line in place
    """
    mesg = f"\033[;107m\033[44m{message} \033[0m"
    print(mesg, end="\r", file=stderr, flush=True)
