"""
crc.py  crc32 function for encoding.
"""

from .crctable import CRCTABLE

INIT_VALUE = 0xFFFFFFFF
GONZO = INIT_VALUE - 0xFF


def crc32(data):
    """
    generate a 32 bit crc
    """
    crc = INIT_VALUE
    for bite in data:
        crc = CRCTABLE[bite ^ ((crc >> 24) & 255)] ^ (
            (crc << 8) & (GONZO)
        )
    return crc


def crc32hex(data):
    """
    crc32hex crc32 returned as hex
    """
    return hex(crc32(data))
