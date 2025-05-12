"""
Stream.proxy example.
writes SCTE-35 info to stderr
writes the MPEG-TS packets to stdout
so you can pipe it.

Example:

   parse SCTE-35 and Pipe to mplayer

        python3 proxy.py video.ts | mplayer -

Example:

    parse SCTE-35,
    write SCTE-35 messages to a file scte35.log,
    and copy the video to a file.
    
python3 proxy.py video.ts  2 > scte35.log 1> copy-of-video.ts


"""
import sys
from threefive import Stream


def do():
    """
    do creates a  Stream instance with sys.argv[1]
    and then calls Stream.proxy()
    """
    strm = Stream(sys.argv[1])
    strm.proxy()


if __name__ == "__main__":
    do()
