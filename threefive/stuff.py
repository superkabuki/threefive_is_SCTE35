"""
stuff.py functions and such common to threefive.

print2, atohif, iso8601, red, blue
"""

import datetime
from sys import stderr

ERR = (
    LookupError,
    ValueError,
    OSError,
    TypeError,
    IndexError,
    NameError,
    AttributeError,
    KeyError,
)

write2 = True


def rmap(data, amap):
    """
    rmap multiple replaces applied to a string.
    works like translate but smoother
    data: string
    amap: dict

    returns string
    """
    data = data.strip()
    for k, v in amap.items():
        data = data.replace(k, v)
    return data


def _type2string(atype):
    """
    _type2string turn <class 'int'> into the string 'int'
    """
    replace_map = {
        "<class '": "",
        "'>": "",
    }
    return rmap(str(atype), replace_map)


def badtype(data, shouldbe):
    """
    badtype show red message that we have a wrong type.
    data can be anything.
    shouldbe is a string like "int", or "SpliceCommand"
    data: anything
    shouldbe: type
    """
    t = _type2string(type(data))
    s = _type2string(shouldbe)
    red(f"Xml needs to be a {s} not {t}")
    return False


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


def codec_detect(data):
    """
    codec_detect decode bytes by trying multiple encodings.
    """
    codecs = [
        "utf8",
        "latin1",
        "ascii",
        "big5",
        "euc_kr",
        "koi8_r",
        "koi8_t",
        "cp437",
        "cp1250",
        "cp1251",
        "utf16",
        "utf32",
    ]
    for codec in codecs:
        try:
            data = data.decode(encoding=codec)
            return codec, data
        except:
            pass


def clean(data):
    """
    clean strip and if it's a byte string
    convert to a string
    """
    if isinstance(data, bytes):
        codec, data = codec_detect(data)
    if not isinstance(data, str):
        badtype(data, str)
    else:
        data = data.strip()
    return data


def ishex(data):
    """
    ishex determine if a string is a hex value.
    """
    if isinstance(data, str):
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
    if data[0] in ["{", b"{"]:
        if data[-1] in ["}", b"}"]:
            return True
    return False


def isxml(data):
    """
    isxml determine if a string or bytestring
    is xml.
    """
    data = clean(data)
    if data[0] in ["<", b"<"]:
        if data[-1] in [">", b">"]:
            return True
    return False


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
