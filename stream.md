# threefive.Stream class

Help on class Stream in module threefive.stream:
```py3
class Stream(builtins.object)
 Stream(tsdata, show_null=True)
```
```   
   Stream class for parsing MPEG-TS data.
```
   
#   Methods defined here

## Stream.__init__
   
```py3
   __init__(self, tsdata, show_null=True)
```

```
     tsdata is an file
                     file handle
                     stdin
                     http(s) uri
                     UDP unicast uri
                     Multicast uri
        You can even switch tsdata while parsing. 
        ( I do this to insert slate where commercials go ) 

       set show_null=False to exclude Splice Nulls
       
       Use like...
       
       from threefive import Stream
       strm = Stream("vid.ts",show_null=False)
       strm.decode()
   
```
##  Stream.decode
```
   decode(self, func=show_cue)
```
```
       Stream.decode reads self.tsdata to find SCTE35 packets.
       func can be set to a custom function that accepts
       a threefive.Cue instance as it's only argument.
 
```
* example
 
```py3
from threefive import Stream

myvideo="https://example.com/video.ts"
strm=Stream(myvideo)
strm.decode()
```
## Stream.decode_next

```py3
   decode_next(self)
```
```
       Stream.decode_next returns the next
       SCTE35 cue as a threefive.Cue instance.
 
```

* example

```py3
from threefive import Stream

myvideo="https://example.com/video.ts"
strm=Stream(myvideo)
while True:
    cue=strm.decode_next()
    if cue:
        print(cue.hex()) # print cue as hex string
        cue.show()  # print cue as json
        print(cue.xml()) # print cue as xml
    else:
        return false
```
## Stream.decode_pids

```py3
   decode_pids(self, scte35_pids=None, func=show_cue)
```
```
       Stream.decode_pids takes a list of SCTE-35 Pids parse
       and an optional call back function to run when a Cue is found.
       if scte35_pids is not set, all threefive pids will be parsed.
```

* example

```py3
    from threefive import Stream
    st=Stream('/home/a/video.ts')
    st.decode_pids([1105,1055])
```

## Stream.decode_start_time

```py3
   decode_start_time(self)
```
```
       decode_start_time
```

* example

 ```py3
    from threefive import Stream
    st=Stream('/home/a/video.ts')
    st.decode_start_time()

    1182681959    # returns start time in ticks

    st.as_90k(st.decode_start_time())

    13141.5047    #  returns start time in seconds.
```
## Stream.iter_pkts

```py3
   iter_pkts(self, num_pkts=1)
```
```
       iter_pkts iterates a mpegts stream into packets
 
```

* Example

```py3
   # use Stream.iter_pkts if you want to iterate packets quickly and parse things your own way.

    from threefive import Stream

       for pkt in self.iter_pkts():
            cue = self._parse(pkt)
            if cue:
                func(cue)
            sys.stdout.buffer.write(pkt)
        return False
```
```  
  pid2pcr(self, pid)
      pid2pcr takes a pid
       returns the current pcr
   
   pid2prgm(self, pid)
       pid2prgm takes a pid,
       returns the program
   
   pid2pts(self, pid)
       pid2pts takes a pid
       returns the current pts
   
   proxy(self, func=show_cue)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are print2`ed to stderr.
 |  
 |  pts(self)
 |      pts returns a dict of  program:pts
 |  
 |  show(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  show_pts(self)
 |      show_pts displays current pts by pid.
 |  
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  
 |  as_90k(ticks)
 |      as_90k returns ticks as 90k clock time
 |  
 |  mk_pts(payload)
 |      mk_pts calculate pts from payload
 |  
 |  ----------------------------------------------------------------------


```
