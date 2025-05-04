# Sassy
##### _SCTE-35 As a Service and Stuff_

### If you just want to decode SCTE-35 data into JSON, try Sassy.

### Sassy accepts both GET and POST request.
| Method| URL                                                              |
|-------|------------------------------------------------------------------|
| POST  | https://iodisco.com/cb/sassy  POST scte35=your_urlencoded_scte35 |
| GET   | https://iodisco.com/cb/sassy?scte35=your_urlencoded_scte35       |


### POST to https://iodisco.com/cb/sassy
* POST urlencoded SCTE-35 base64 to sassy and receive a JSON response
```js
curl -d 'scte35=%2FDA0AAGRZOeYAAAABQb%2BhJ8vqAAeAhxDVUVJ%2F%2F%2F%2F%2F3%2F%2FAAZv8wABCGZ1bWF0aWNhEAEAiZ5ZMw%3D%3D'  https://iodisco.com/cb/sassy
```

* POST SCTE-35 hex to sassy and receive a JSON response
```js
curl  -d 'scte35=0xfc302f00019164e7980000000506fe849f2fa80019021743554549ffffffff7fbf010866756d6174696361100100ae05fd2e'  https://iodisco.com/cb/sassy
```


* response
```js
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 74825.294489,
        "cw_index": "0x00",
        "tier": "0x00",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 25,
        "crc": "0xae05fd2e"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 24722.499289
    },
    "descriptors": [
        {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "descriptor_length": 23,
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id": "0xffffffff",
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": true,
            "segmentation_message": "Program Start",
            "segmentation_type_id": 16,
            "segmentation_upid_length": 8,
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Type 0x01 is deprecated, use MPU type 0x0C",
            "segmentation_upid": "fumatica",
            "segment_num": 1,
            "segments_expected": 0
        }
    ]
}
```

### Format for GET requests https://iodisco.com/cb/sassy?scte35=your_data_goes_here

* pass a Hex encoded SCTE-35 string to sassy and get back JSON

```sh

curl  'https://iodisco.com/cb/sassy?scte35=0xfc302f00019164e7980000000506fe849f2fa80019021743554549ffffffff7fbf010866756d6174696361100100ae05fd2e'
```

* Url Encoded Base64
```sh
curl  https://iodisco.com/cb/sassy?scte35=%2FDA0AAGRZOeYAAAABQb%2BhJ8vqAAeAhxDVUVJ%2F%2F%2F%2F%2F3%2F%2FAAZv8wABCGZ1bWF0aWNhEAEAiZ5ZMw%3D%3D
```

* Url Encoded SCTE-35 Xml
```sh
curl  'https://iodisco.com/cb/sassy?scte35=<scte35%3ASpliceInfoSection+xmlns%3Ascte35%3D"https%3A%2F%2Fscte.org%2Fschemas%2F35"++ptsAdjustment%3D"6734276504"+protocolVersion%3D"0"+sapType%3D"3"+tier%3D"0">%0D%0A+++<scte35%3ATimeSignal>%0D%0A++++++<scte35%3ASpliceTime+ptsTime%3D"2225024936"%2F>%0D%0A+++<%2Fscte35%3ATimeSignal>%0D%0A+++<!--+Program+Start+-->%0D%0A+++<scte35%3ASegmentationDescriptor+segmentationEventId%3D"4294967295"+segmentationEventCancelIndicator%3D"false"+segmentationEventIdComplianceIndicator%3D"true"+segmentationTypeId%3D"16"+segmentNum%3D"1"+segmentsExpected%3D"0"+segmentationDuration%3D"108000000">%0D%0A++++++<!--+Type+0x01+is+deprecated%2C+use+MPU+type+0x0C+-->%0D%0A++++++<scte35%3ASegmentationUpid+segmentationUpidType%3D"1"+segmentationUpidFormat%3D"text">fumatica<%2Fscte35%3ASegmentationUpid>%0D%0A+++<%2Fscte35%3ASegmentationDescriptor>%0D%0A<%2Fscte35%3ASpliceInfoSection>%0D%0A'
```

* SCTE-35 Integer
```sh
curl https://iodisco.com/cb/sassy?scte35=2796939353925477353583331785016283158157950476543952866345909366225726773747734084060868182760626453032945319846467331444852945475891
```


* response
```js
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 74825.294489,
        "cw_index": "0x00",
        "tier": "0x00",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 25,
        "crc": "0xae05fd2e"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 24722.499289
    },
    "descriptors": [
        {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "descriptor_length": 23,
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id": "0xffffffff",
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": true,
            "segmentation_message": "Program Start",
            "segmentation_type_id": 16,
            "segmentation_upid_length": 8,
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Type 0x01 is deprecated, use MPU type 0x0C",
            "segmentation_upid": "fumatica",
            "segment_num": 1,
            "segments_expected": 0
        }
    ]
}
```
