[__Install__](#install) |[__Cli__](#the-cli-tool) | [__HLS__](https://github.com/superkabuki/threefive3/blob/main/hls.md) | [__Cue__ Class](https://github.com/superkabuki/threefive3/blob/main/cue.md) | [__Stream__ Class](https://github.com/superkabuki/threefive3/blob/main/stream.md) | [__Online SCTE-35 Parser__](https://iodisco.com/scte35) | [__Encode__](https://github.com/superkabuki/threefive3/blob/main/encode.md) | [__Examples__](https://github.com/superkabuki/threefive3/tree/main/examples)
 <pre> 
 Myself and several others spent five years developing threefive, 
 and then I got F2A'ed out of the github account.
 threefive3 is the next step.
  
 Welcome to the show.
  
 Adrian
  
</pre>

# The threefive3 SCTE-35 Cli Super Tool 
# and python3 library.

✅ SCTE-35 __Parser__  ✅ SCTE-35 __Encoder__    ✅ SCTE-35 __HLS__     ✅ SCTE-35 __Xml+binary__     ✅ SCTE-35 __Cli__     ✅  SCTE-35 __library__


* Parses __SCTE-35__ from MPEGTS, HLS, XML+Binary, Base64, Bytes, Hex, Integers, or JSON.
* Encode __SCTE-35__ to Base64, Bytes, Hex, Int, JSON, or Xml+binary.
* Built-in network support for HTTP(S), UDP, and Multicast.
* Automatic AES decryption for HLS.
* All HLS __SCTE-35__ Tags are Supported.

# Latest release is v3.0.35 
_Released Thursday April 3rd, 2025 4am EDT_
> Stay up to date, only the latest release is supported.

# Checkout the Super Cool SCTE-35 [__Examples__](https://github.com/superkabuki/threefive3/tree/main/examples)

## MPEGTS streams can be parsed for SCTE-35 with three lines of code.

```py3
a@fu:~/build5/scte35/scte35$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>>> from threefive3 import Stream

>>>> strm=Stream('https://futzu.com/xaa.ts')

>>>> strm.decode()
```



# `Documentation`


* [Install](#install)

### Cli

* [SCTE-35 Cli Super Tool](#the-cli-tool) Encodes, Decodes, and Recodes. This is pretty cool, it does SCTE-35 seven different ways.
     * The cli tool comes with builtin documentation just type `threefive3 help`

### HLS
* [Advanced Parsing of SCTE-35 in HLS with threefive3](https://github.com/superkabuki/threefive3/blob/main/hls.md) All HLS SCTE-35 tags, Sidecar Files, AAC ID3 Header Timestamps, SCTE-35 filters... Who loves you baby?


### `Classes`

* [Class Structure](https://github.com/superkabuki/threefive3/blob/main/classes.md)
* 
* The python built in help is always the most up to date docs for the library.

```rebol
a@fu:~/build7/threefive3$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import Stream
>>>> help(Stream)
```

* [Cue Class](https://github.com/superkabuki/threefive3/blob/main/cue.md)  Cue is the main SCTE-35 class to use. 
* [Stream Class](https://github.com/superkabuki/threefive3/blob/main/stream.md)  The Stream class handles MPEGTS SCTE-35 streams local, Http(s), UDP, and Multicast.
___

### `| more`

* [Online SCTE-35 Parser](https://iodisco.com/scte35)  Supporte Base64, Bytes,Hex,Int, Json, Xml, and Xml+binary.

* [Encode SCTE-35](https://github.com/superkabuki/threefive3/blob/main/encode.md) Some encoding code examples. 


___

### `Install`
* python3 via pip
```rebol
python3 -mpip install threefive3
```
* pypy3 
```rebol
pypy3 -mpip install threefive3
```
* from the git repo
```rebol
git clone https://github.com/superkabuki/scte35.git
cd threefive3
make install
```
___

### `The Cli tool`

#### The cli tool installs automatically with pip or the Makefile.

* [__SCTE-35 Inputs__](#inputs)
* [__SCTE-35 Outputs__](#outputs)
* [Parse __MPEGTS__ streams for __SCTE-35__](#streams)
* [Parse __SCTE-35__ in __hls__](#hls)
* [Display __MPEGTS__ __iframes__](#iframes)
* [Display raw __SCTE-35 packets__ from __video streams__](#packets)
* [__Repair SCTE-35 streams__ changed to __bin data__ by __ffmpeg__](#sixfix)

#### `Inputs`

* Most __inputs__ are __auto-detected.__ 
* __stdin__ is __auto selected__ and __auto detected.__
* __SCTE-35 data is printed to stderr__
* __stdout is used when piping video__
* mpegts can be specified by file name or URI.
```rebol
threefive3 udp://@235.2.5.35:3535
```
* If a file comtains a SCTE-35 cue as a string( base64,hex,int,json,or xml+bin), redirect the file contents.
```rebol

  threefive3 < json.json  

 ```

* quoted strings(( base64,hex,int,json or xml+bin), can be passed directly on the command line as well.

```awk

threefive3 '/DAWAAAAAAAAAP/wBQb+ztd7owAAdIbbmw=='

```


| Input Type |     Cli Example                                                                                             |
|------------|-------------------------------------------------------------------------------------------------------------|
| __Base64__     |  `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='`
| __Hex__        |`threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b`|
| __HLS__         |`threefive3 hls https://example.com/master.m3u8`                                                             |
| __JSON__        |`threefive3 < json.json`  |
| __Xmlbin__      | `js threefive3 < xmlbin.xml`                                                                                 |

# `Streams`

|Protocol       |  Cli Example                                                                                                                                       |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|  File         |   `threefive3 video.ts`                                                                                                                            |
|  Http(s)      |   `threefive3 https://example.com/video.ts`                                                                                                        |
|  Stdin        |  `threefive3 < video.ts`            |
|  UDP Multicast|  `threefive3 udp://@235.35.3.5:9999`                                                                          |
|  UDP Unicast  |                                                                      `threefive3 udp://10.0.0.7:5555`                                              |
|  HLS          |                                                                                                    `threefive3 hls https://example.com/master.m3u8`|
|               |                                                                                                                                                    |


#### Outputs
* output type is determined by the key words __base64, bytes, hex, int, json, and xmlbin__.
* __json is the default__.
* __Any input (except HLS,) can be returned as any output__
  * examples __Base64 to Hex__ etc...) 


| Output Type | Cli Example         |
|-------------|----------------------------------------------------------|
|__Base 64__     |                                                                                                                                                                    `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  base64  `                                                                                                                                                                                                                                                                                                                                         |
| __Bytes__       |                                                                                 `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  bytes`                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Hex         | `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  hex`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Integer     |                                                                                                                                                                                                                                                       `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  int`   |
| JSON        |                                                                                                                                                                                                                                                                                                              `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b json ` |
| Xml+bin     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b xmlbin   `      |`

#### `hls`
* parse hls manifests and segments for SCTE-35
```smalltalk
threefive3 hls https://example.com/master.m3u8
```
___
#### `Iframes`
* Show iframes PTS in an MPEGTS video

```smalltalk
threefive3 iframes https://example.com/video.ts
```
___
#### `packets`   
* Print raw SCTE-35 packets from multicast mpegts video

```smalltalk
threefive3 packets udp://@235.35.3.5:3535
```
___
#### `proxy`   
* Parse a https stream and write raw video to stdout

```smalltalk
threefive3 proxy video.ts
```
___
#### `pts`    
* Print PTS from mpegts video

```smalltalk
threefive3 pts video.ts
```
___
#### `sidecar`  
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt

```smalltalk
threefive3 sidecar video.ts
```
___
#### `sixfix`  
* Fix SCTE-35 data mangled by ffmpeg

```smalltalk
threefive3 sixfix video.ts
```
___
#### `show`  

* Probe mpegts video _( kind of like ffprobe )_

```smalltalk
 threefive3 show video.ts
```
___
#### `version`     
* Show version

```smalltalk
 threefive3 version
```
___
#### `help`        
* Help
```rebol
 threefive3 help
```
___


### Stream Multicast with the threefive cli, it's easy.

* The threefive3 cli has long been a Multicast Receiver( client )
* The cli now comes with a builtin Multicast Sender( server).
* It's optimized for MPEGTS (1316 Datagrams) but you can send any video or file.
* The defaults will work in most situations, you don't even have to set the address.
* threefive3 cli also supports UDP Unicast Streaming.
  
![image](https://github.com/user-attachments/assets/6042b8e0-5d6b-4de0-b6b0-9556cecc184f)
 
```js
a@fu:~$ threefive3 mcast help
usage: threefive3 mcast [-h] [-i INPUT] [-a ADDR] [-b BIND_ADDR] [-t TTL]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or
                        "https://futzu.com/xaa.ts"
                        [default:sys.stdin.buffer]
  -a ADDR, --addr ADDR  Destination IP:Port [default:235.35.3.5:3535]
  -b BIND_ADDR, --bind_addr BIND_ADDR
                        Local IP to bind [default:0.0.0.0]
  -t TTL, --ttl TTL     Multicast TTL (1 - 255) [default:32]
a@fu:~$ 
```




### [iodisco.com/scte35](https://iodisco.com/scte35)
![image](https://github.com/user-attachments/assets/e07af2ad-29fe-4dae-8568-b168c3d5a591)


___

[Install threefive3](#install)  | [SCTE-35 HLS](https://github.com/superkabuki/threefive3/blob/main/hls.md) | [Cue Class](https://github.com/superkabuki/threefive3/blob/main/cue.md) | [Stream Class](https://github.com/superkabuki/threefive3/blob/main/stream.md) | [Online SCTE-35 Parser](https://iodisco.com/scte35) | [Encode SCTE-35](https://github.com/superkabuki/threefive3/blob/main/encode.md) 
