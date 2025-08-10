# threefive commonly used classes. 
#### threefive is Object Oriented. Almost all of threefive is contained in classes. Inheritance is intentionally shallow, subclassing is limit to a depth of two. These are the classes you are most likely to use. The Cue class and the Stream class will be used most often.
<br>
All of the classes shown can be imported from directly threefive.

# SCTE-35 Specific Stuff
### Most SCTE-35 objects are subclassed from SCTE35Base
* SCTE35Base
    * [__Cue__](threefive/cue.py)
    * [SpliceInfoSection](threefive/section.py) 
    * [SpliceCommand](threefive/commands.py)
        * BandwidthReservation
        * PrivateCommand
        * SpliceNull
        * TimeSignal
            * SpliceInsert
   * [SpliceDescriptor](threefive/descriptors.py)
        * AvailDescriptor
        * DtmfDescriptor
        * DVBDASDescriptor
        * SegmentationDescriptor 
        * TimeDescriptor

## All upids are either Upid instances or a subclass of Upid.
* [Upid](threefive/upids.py)
    * AirId
    * Atsc
    * Mid
    * Mpu
    * Eidr
    * NoUpid
    * Isan
    * Umid

# SCTE-35 Related stuff
### Most MPEGTS parsers are either a Stream instance or subclass of Stream.
* [__Stream__](threefive/stream.py)
    * [Segment](threefive/segment.py)
    * [SixFix](threefive/sixfix.py)
       * [SuperKabuki](threefive/superkabuki.py)

### Other MPEGTS classes.
* [IFramer](threefive/iframes.py)
* Socked(socket.socket)
* PMT

### Multicast Sender/Server
* [GumS](threefive/gums.py)

### HLS related classes
* [AacParser](threefive/aac.py)
* [HlsParser](threefive/hls.py)
* [TagParser](threefive/hlstags.py)

### Bitwise decoder and encoder classes
* [Bitn](threefive/bitn.py)
* [NBin](threefive/bitn.py)

### Xml
* [UltraXmlParser](threefive/uxp.py)
* [NameSpace](threefive/xml.py)
* [Node](threefive/xml.py)
    * [Comment](threefive/xml.py)
* [NodeConverter](threefive/uxp.py)
* [NodeList](threefive/xml.py)
