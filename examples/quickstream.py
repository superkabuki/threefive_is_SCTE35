"""
Quickstream.py

    This is to show how the  Cue class can parse raw mpegts SCTE-35 packets directly.
    my_mpegts_parser() iterates packets in an mpegts stream looking for SCTE-35 packets
    in a SCTE-35 pid, and when it finds one, it calls parseSCTE35(pkt) to parse the packet. 

  *  sys.argv[1] is the file or stream

  * sys.argv[2] is the SCTE-35 pid

  * Run it like this:

        python3 quickstream.py video.ts 259


 * if you don't know the SCTE-35 pid run

    threefive show video.ts

* look for a line with SCTE-35 in it like:
            
            483      [0x1e3]        0x86  SCTE-35  
      
* Then you'd run:

                python3 quickstream.py video.ts 483


* SCTE-35 data will be printed in JSON format.


"""

from functools import partial
import sys
from threefive import Cue
from threefive.new_reader import reader


def parse_pid(pkt):
    """
    parse a pid from a mpegts packet
    """
    return (pkt[1] & 15) << 8 | pkt[2]


def parseSCTE35(pkt):
    """
    parseSCTE35 parses a raw mpegts SCTE-35 packet

    if you already have an mpegts parser,
    When you find a SCTE-35 packet
    this is all the code you need to parse it .

    """
    cue = Cue(pkt)
    if cue.bites:
        cue.show()


def my_mpegts_parser():
    """
    my_mpegts_parser is your pretend mpegts parser,
    it iterates mpegts packets and when it finds a SCTE-35 packet,
    it calls parseSCTE35(pkt) to parse the SCTE-35..

     sys.argv[1] is the file or stream

     sys.argv[2] is the SCTE-35 pid

     Run it like this:

     python3 quickstream.py video.ts 259

    """
    scte35pid = int(sys.argv[2])
    with reader(sys.argv[1]) as tsdata:
        for pkt in iter(partial(tsdata.read, 188), b""):
            if parse_pid(pkt) == scte35pid:
                parseSCTE35(pkt)


if __name__ == "__main__":
    my_mpegts_parser()
