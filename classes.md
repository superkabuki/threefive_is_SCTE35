# threefive3 commonly used classes and inheritance.

## Most SCTE-35 objects are subclassed from SCTE35Base

* class SCTE35Base
    * Cue
    * SpliceCommand

         *  BandwidthReservation
         *  PrivateCommand
         *  SpliceNull
         *  TimeSignal

            *  SpliceInsert
           
    * SpliceDescriptor
        * AvailDescriptor
        * DtmfDescriptor
        * DVBDASDescriptor
        * SegmentationDescriptor
        * TimeDescriptor
    
   * SpliceInfoSection

## All upids are either Upid instances or a subclass of Upid.

* class Upid
    * AirId
    * Atsc
    *  Mid
    *   Mpu
    *   Eidr
    * NoUpid
    * Isan
    * Umid

## Most MPEGTS parsers are either a Stream instance or subclass of Stream.

* class Stream
    * Segment
    * SixFix
    * SuperKabuki

## Other MPEGTS classes.

* class GumS
* class IFramer
* class Socked(socket.socket)

## HLS related classes

* class AacParser
* class HlsParser
* class TagParser

## Bitwise decoder and encoder classes

* class Bitn
* class NBin


