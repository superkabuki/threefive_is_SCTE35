#!/usr/bin/env python3
"""
base64toxmbin.py convert a SCTE-35 base64 encoded string to Xml+binary,
and then convert the xml+binary back to base64

"""

from threefive import Cue


HEAD ='\n\033[107;2;36m '
TAIL = '\033[0m\n'


if __name__ == "__main__":



    #  Base64 To Xml .
    b64 = "/DAWAAAAAAAAAP/wBQb+z26yLwAAXeqFJg=="
    cue = Cue(b64)  # initialize a Cue instance with the base64 string.
    exbin= cue.xmlbin()  # call the Cue.xmlbin() method
    print(f"{HEAD} base64  -> xmlbin {TAIL} ")
    print(exbin)

    # Xml  to Base64.
    cue2 = Cue(exbin)  # initialize a Cue instance with the xml output from above..
    b64out = cue2.base64()  # call the Cue.base64() method
    print(f"{HEAD} xmlbin -> base64 {TAIL}")
    print(b64out)
