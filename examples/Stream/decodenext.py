"""
next.py demonstrates how to use Stream.decode_next() to grab and process
the next SCTE-35 Cue in an MPEGTS stream.

Here, if the Cue Splice Command is a Splice Insert, we print the Splice Command vars,
but you trigger any action you like, this is just an example. 

"""
import sys
from threefive3 import Stream
from threefive3.new_reader import reader

def do():
    arg = sys.argv[1]
    with reader(arg) as tsdata:
        st = Stream(tsdata)
        while True :
            cue = st.decode_next()
            if not cue:
                return False
            if cue:
                if cue.command.command_type ==5:
                    print(cue.command)



if __name__ == "__main__":
    do()
