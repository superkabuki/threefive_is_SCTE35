# Xml
<pre>
    I pulled xml support a few months ago, I wasn't happy with the implementation. 
One out of every seven lines of code was xml specific, there was xml code everywhere.
It was all way too clunky. Everytime I touched one part of the code, something else would break.
 
 The xml parser worked completely different from the xml generator.
 Now, generating and parsing xml both use the Node class, it's much cleaner.
</pre>


# `Q.`Why would you write a xml parser for threefive3? 
 
# `A.` quadratic blowup and billion laughs for starters. 

*  These are very old attacks, __over ten years old__,  and the [__python xml parsers are all vunerable__](https://docs.python.org/3/library/xml.html#xml-vulnerabilities) to both attacks.
 That's not good. That causes me a lot of concern. __If you know it's vumerable, don't document that it's broke, fix it__.

* __I'd fix the parsers__ for them, but __I've been banned from python's github repo__ for __criticizing PEP 668__ ( --break-system-packages), and trying to __start a mutiny__, but that's a story for another time.


# Meet the new xml parser, Ultra Xml Parser Supreme.

This is the fourth xml parser I've written for threeefive3, and the first one I actually like. 
The big difference is that when the xml data is parsed, it's marshaled into a threefive3.xml.Node instance.
My previous parsers took a lot of code in comparison to the size of threefive3. Parsing into a Node instance, 
allowed me to work in more general terms, each SCTE-35 object required a lot less specific code. Upids are good example. 
There used to be twenty Xml specific methods, about 120 lines, now there's four methods in 33 lines.

### Why do you care about any of this?
My point is that you shouldn't have to care, and you should expect code to not be vunerable to silly ass ten year old attacks. 

# How does Xml work with threefive3?

# Decoding 
### Cli
```js
a@fu:~/threefive3$ cat ~/xml3.xml

<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="1" availsExpected="1" outOfNetworkIndicator="true" uniqueProgramId="39321">
      <scte35:Program>
         <scte35:SpliceTime ptsTime="6554297154"/>
      </scte35:Program>
      <scte35:BreakDuration autoReturn="true" duration="10798788"/>
   </scte35:SpliceInsert>
   <!-- Provider Placement Opportunity Start -->
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="93" segmentNum="0" segmentsExpected="0" subSegmentNum="0 subSegmentsExpected="0" segmentationDuration="10800000">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- Type 0x01 is deprecated, use MPU type 0x0C -->
      <scte35:SegmentationUpid segmentationUpidType="1" segmentationUpidFormat="hexbinary">futronica</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
* decode the xml into json and write to a file
* threefive3 outputs SCTE-35 data to stderr aka 2 , stdout is used for piping video and such.
  ```js
  threefive3 < ~/xml3.xml 2> json.json
  ```
* decode the xml into hex
  ```js
  threefive3 < ~/xml3.xml hex
  0xfc303a00000003289800fff00f05000000017faffe00a4c6c499990101001a021843554549000000007f800109667574726f6e6963615d0000a6ac3c8d

  ```
### lib
* read the xml data in from a file
```py3
>>>> from threefive3 import reader
>>>> data = reader('/home/a/xml5.xml').read()
```
* load the data into a Cue instance
```py3
>>>> from threefive3 import Cue
>>>> cue=Cue(data)
```
* to see the data, call cue.show()
```py3
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 42,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x98767c66"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": false,
        "break_duration": 75.0,
        "splice_event_id": 18,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": false,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 18,
        "avails_expected": 255
    },
    "descriptors": [
        {
            "tag": 0,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 18,
            "descriptor_length": 8
        }
    ]
}
```
* This is why I love the new xml parser,that's all there is to it.
* That's everything you need to know to parse SCTE-35 xml with threefive3.


# Encoding 
### Cli
* Encoding with the cli is easy, pass your SCTE-35 data to threefive3 and just add the xml keyword
* if you had SCTE-35 in JSON format in a file like this
```js
a@fu:~/threefive3$ cat ~/json2.json
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 52,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 2.3,
        "cw_index": "0x0",
        "tier": 4095,
        "splice_command_length": 10,
        "splice_command_type": 5,
        "descriptor_loop_length": 25,
        "crc": "0xe2f9395d"
    },
    "command": {
        "command_length": 10,
        "command_type": 5,
        "name": "SpliceInsert",
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": false,
        "program_splice_flag": false,
        "duration_flag": false,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 39321,
        "avail_num": 1,
        "avails_expected": 255
    },
    "descriptors": [
        {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id": "0x0",
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": false,
            "archive_allowed_flag": false,
            "device_restrictions": "Restrict Group 0",
            "segmentation_message": "Provider Placement Opportunity End",
            "segmentation_type_id": 53,
            "segmentation_upid_length": 13,
            "segmentation_upid_type": 12,
            "segmentation_upid_type_name": "MPU",
            "segmentation_upid": {
                "format_identifier": "DOOM",
                "private_data": "5375706572446f6f6d"
            },
            "segment_num": 0,
            "segments_expected": 0,
            "descriptor_length": 23
        }
    ]
}
```
* to generate xml output
```js
a@fu:~/threefive3$ threefive3 < ~/json2.json xml
```
```xml
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="1" availsExpected="255" outOfNetworkIndicator="false" uniqueProgramId="39321"/>
   <!-- Provider Placement Opportunity End -->
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="53" segmentNum="0" segmentsExpected="0">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- MPU -->
      <scte35:SegmentationUpid segmentationUpidType="12" segmentationUpidFormat="hexbinary" formatIdentifier="1146048333" privateData="1539542133359170776941">444f4f4d5375706572446f6f6d</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
* you can parse MPEGTS and output SCTE-35 as xml
```js
threefive3 video.ts xml
``` 
### lib
* If you want to make a TimeSignal
```py3
>>>> from threefive3 import TimeSignal, Cue
>>>> t =TimeSignal()
>>>> t
{'command_length': 0, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': None, 'pts_time': None}
```
* set the vars for the TimeSignal
```py3
>>>> t.time_specified_flag=True

>>>> t.pts_time=15345.123903
```
* render the TimeSignal as xml
```xml
>>>> t.xml()
<scte35:TimeSignal >
   <scte35:SpliceTime ptsTime="1381061151"/>
</scte35:TimeSignal>
```
* add the TimeSignal to a Cue and render as xml
*  (threefive3 automatically generates the Splice Info Section if needed)
```py3
>>>> cue=Cue()
>>>> cue.command =t
>>>> cue.encode()
>>>> print(cue.xml())
```
```xml
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="1381061151"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```
* make an Avail Splice Descriptor and add it to the Cue
* When you call encode() on a threefive3 object, it ctells you if you've got something wrong
```py3
>>>> from threefive3 import AvailDescriptor
>>>> avd =AvailDescriptor()
>>>> avd
{'tag': 0, 'identifier': 'CUEI', 'name': 'Avail Descriptor', 'bites': None, 'private_data': None, 'provider_avail_id': None}
>>>> avd.provider_avail_id="fumatica"
>>>> avd.encode()
  provider_avail_id is fumatica, it should be type int, 32 bit(s) long.  # <--- threefive3 points out your mistakes

>>>> avd.provider_avail_id=1234
>>>> avd.encode()
```
* append the Avail Splice Descriptor to cue.descriptors
* cue.descriptors is a list
```py3
>>>> cue.descriptors.append(avd)
```
* When ever you make a change to cue, call cue.encode() and it recalculate everything for you
```
>>>> cue.encode()
```
* print cue.xml() to see the new xml
```xml
>>>> print(cue.xml())
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="1381061151"/>
   </scte35:TimeSignal>
   <scte35:AvailDescriptor providerAvailId="1234"/>
</scte35:SpliceInfoSection>
```
 
* [Code stolen from here](https://gist.github.com/jordanpotti/04c54f7de46f2f0f0b4e6b8e5f5b01b0)
* 
![image](https://github.com/user-attachments/assets/121edabe-947f-47b9-a5ad-ed7b0b393474)

