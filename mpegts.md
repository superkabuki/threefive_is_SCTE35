# MPEGTS and SCTE-35 and threefive

Parsing SCTE-35 from MPEGTS was my top priority when I started working on threefive.
<br>
I decided  on the following criteria. 
___
### 1. Fast

High end __4K video__ usually has a __bitrate__ between __5 and 12 MB/sec__ <br>
__python3__ and threefive parses MPEGTS around __400 MB/sec__. <br>
__pypy3__ and threefive parses MPEGTS over __1 GB/sec__. 
___
### 2. Easy

```py3
from threefive import Stream

video = https://example.com/video.ts
st =Stream(video)
st.decode()
```
__Four lines of code__. 
___



# the threefive cli and MPEGTS.

* __Decode SCTE-35 from MPEGTS__ 
```py3
a@fu:~$ threefive plp0.ts 
```
* the __default output is json__. You can change the output format with keywords.

* __base64__
```py3
a@fu:~$ threefive plp0.ts  base64
```
* __bytes__
```py3
a@fu:~$ threefive plp0.ts bytes
```
* __hex__
```py3
a@fu:~$ threefive plp0.ts hex
```
* __xml__
```py3
a@fu:~$ threefive plp0.ts xml
```
* __xml+bin__
```py3
a@fu:~$ threefive plp0.ts xmlbin
```
### More Cli MPEGTS tools 

* __hls__         SCTE-35 HLS decode
```smalltalk
threefive hls https://example.com/master.m3u8
```
* __iframes__      Show MPEGTS iframes
```smalltalk
    threefive iframes video.ts
```
* __inject__  SuperKabuki SCTE-35 MPEGTS Packet Injection Engine
```smalltalk
    threefive inject help
```
* __mcast__        Multicast sender(server)
```smalltalk
  threefive mcast video.ts
```
* __packets__     Print raw SCTE-35 packets
```smalltalk
    threefive packets udp://@235.35.3.5:3535
```
* __proxy__       Parse a MPEGTS stream and copy it to stdout
```smalltalk
    threefive proxy video.ts
```
* __pts__         Print PTS from MPEGTS video
```smalltalk
    threefive pts video.ts
```
* __sidecar__     Create a SCTE-35 sidecar file
```smalltalk
    threefive sidecar video.ts
```
* __sixfix__      Fix SCTE-35 data mangled by ffmpeg
```smalltalk
    threefive sixfix video.ts
```
* __show__        Probe MPEGTS video
```smalltalk
    threefive show video.ts
```
