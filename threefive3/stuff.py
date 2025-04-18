"""
stuff.py functions and such common to threefive3.

print2, atohif, iso8601, red, blue
"""

import datetime
from sys import stderr

ERR = (LookupError,ValueError,OSError,TypeError,IndexError,
         NameError,AttributeError,KeyError)

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


def clean(data):
    """
    clean strip and if it's a byte string
    convert to a string
    """
    if not isinstance(data,(str,bytes)):
        return data
    data=data.strip()
    if isinstance(data,bytes):
        try:
            data=data.decode()
        except ERR:
            pass
    return  data


def ishex(data):
    """
    ishex determine if a string is a hex value.
    """
    if isinstance(data,str):
        hexed = "0123456789abcdef"
        data = data.lower().strip("0x")
        return all([c in hexed for c in data])
    return False


def isjson(data):
    """
    isjson determine if a string or bytestring
    is json.
    """
    data = clean(data)
    if data[0] in ['{' , b'{']:
        if data[-1] in ['}',b'}']:
            return True
    return  False

def isxml(data):
    """
    isxml determine if a string or bytestring
    is xml.
    """
    data = clean(data)
    if data[0] in ['<',b'<']:
        if data[-1] in ['>',b'>']:
            return True
    return  False

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
    return False


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
