# Examples

* `aac_id3header.py` - use the __threefive.aac.AacParser__ class to parse __HLS AAC__ segments for __PTS__ in __ID3 header tags__.

* `base64toxmlbin.py`- __convert__ __base64__ encoded SCTE-35 to __xml+binary__ encoded SCTE-35 and back.
  
* `cue2vtt.py` - display SCTE-35 data on video using __WebVTT__ subtitles to __verify__ SCTE-35 __splice points__.

* `decodenext.py` - parse __MPEGTS__ streams for SCTE-35 using __Stream.decode_next()__.

* `dtmf.py` - parse __base64__ SCTE-35 with a __DTMF__ descriptor and __re-encode__ to SCTE-35 in __Hex__ format.

* `edit_break_duration.py` - change the SCTE-35 __break duration__ and __re-encode__ SCTE-35.

* `encode_time_signal.py` - __encode__ a SCTE-35 __Cue__ with a __TimeSignal__ from scratch.

* `parsehlstags.py` - use the __TagParser__ class to parse __HLS tags__ from a __m3u8__ file and group the tags by segment.

* `proxy.py` - how to use the __Stream.proxy()__ method for parsing SCTE-35 and __piping__ video.

* `quickstream.py` - how to __add SCTE-35 parsing__ for __MPEGTS__ streams to __your application__.

* `spliceinsert.py` - a SCTE-35 __Splice Insert__ example.  
