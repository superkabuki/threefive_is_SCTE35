# threefive commonly used classes and inheritance.
This shows the inheritence of classes. <br>
All of the classes shown can be imported from directly threefive.

## Most SCTE-35 objects are subclassed from SCTE35Base
* SCTE35Base
    * Cue
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

## Most MPEGTS parsers are either a Stream instance or subclass of Stream.
* Stream
    * Segment
    * SixFix
       * SuperKabuki

## Other MPEGTS classes.
* GumS
* IFramer
* Socked(socket.socket)
* PMT

## HLS related classes
* AacParser
* HlsParser
* TagParser

## Bitwise decoder and encoder classes
* Bitn
* NBin

## Xml
* UltraXmlParser
* NameSpace
* Node
    * Comment
* NodeConverter
* NodeList(list)
