# threefive commonly used classes. 
#### threefive is Object Oriented. Almost all of threefive is contained in classes. Inheritance is intentionally shallow, subclassing is limit to a depth of two. These are the classes you are most likely to use. The Cue class and the Stream class will be used most often..
<br>
All of the classes shown can be imported from directly threefive.

# SCTE-35 Specific Stuff
### Most SCTE-35 objects are subclassed from SCTE35Base
* SCTE35Base
    * [__Cue__](threefive/cue.py)
    * SpliceInfoSection 
    * SpliceCommand
        * BandwidthReservation
        * PrivateCommand
        * SpliceNull
        * TimeSignal
            * SpliceInsert
   * SpliceDescriptor
        * AvailDescriptor
        * DtmfDescriptor
        * DVBDASDescriptor
        * SegmentationDescriptor 
        * TimeDescriptor

## All upids are either Upid instances or a subclass of Upid.
* Upid
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
* __Stream__
    * Segment
    * SixFix
       * SuperKabuki

### Other MPEGTS classes.
* IFramer
* Socked(socket.socket)
* PMT

### Multicast Sender/Server
* GumS

### HLS related classes
* AacParser
* HlsParser
* TagParser

### Bitwise decoder and encoder classes
* Bitn
* NBin

### Xml
* UltraXmlParser
* NameSpace
* Node
    * Comment
* NodeConverter
* NodeList(list)
