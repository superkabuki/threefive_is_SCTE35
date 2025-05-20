# Sassy
##### _SCTE-35 As a Service and Stuff_

## If you just want to decode SCTE-35 data into JSON, try Sassy.
## If you just want to encode JSON into SCTE-35, Try Sassy
## Sassy accepts both POST and GET requests and even works in your browser..

* [POST](#post)
* [GET](#get)
* [Browser](#browser)

## `URLs`

| Method| URL                                                              |
|-------|------------------------------------------------------------------|
| POST  | https://iodisco.com/cb/sassy  POST scte35=your_urlencoded_scte35 |
| GET   | https://iodisco.com/cb/sassy?scte35=your_urlencoded_scte35       |


## `POST`

* POST to https://iodisco.com/cb/sassy
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
## POST Encode
* you can edit the output from Sassy and send it back to sassy for encoding.

```js
curl -d '{"info_section": {"table_id": "0xfc", "section_syntax_indicator": false, "private": false,
"sap_type": "0x03", "sap_details": "No Sap Type", "section_length": 37, "protocol_version": 0, "encrypted_packet": false, "encryption_algorithm": 0, "pts_adjustment": 0.0, "cw_index": "0x00", "tier": "0x0fff", "splice_command_length": 20,
"splice_command_type": 5, "descriptor_loop_length": 0, "crc": "0xc0f22992"},
 "command": {"command_length": 20, "command_type": 5, "name": "Splice Insert", "time_specified_flag": true, "pts_time": 100.0,
"break_auto_return": true, "break_duration": 60.0, "splice_event_id": 1, "splice_event_cancel_indicator": false, "out_of_network_indicator": true, "program_splice_flag": true, "duration_flag": true, "splice_immediate_flag": false,
"event_id_compliance_flag": true, "unique_program_id": 1, "avail_num": 0, "avails_expected": 0},
 "descriptors": []}'
-i https://iodisco.com/cb/sassy
```
* __output__ (notice "hex" and "base64" at the end of the json) 
```js
HTTP/2 200 
server: nginx
date: Tue, 20 May 2025 04:07:28 GMT
content-type: application/json
fumatic-for-the-people: All Signs Point to Yes
access-control-allow-methods: GET, POST, OPTIONS
access-control-expose-headers: Content-Length
access-control-allow-origin: origin-list
vary: Origin

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 37,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xc0f22992"
    },
    "command": {
        "command_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 100.0,
        "break_auto_return": true,
        "break_duration": 60.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": [],
    "hex": "0xfc302500000000000000fff01405000000017feffe00895440fe005265c0000100000000c0f22992",  #  <--Hex encoded
    "base64": "/DAlAAAAAAAAAP/wFAUAAAABf+/+AIlUQP4AUmXAAAEAAAAAwPIpkg=="  #   <-- Base64 encoded
}

```


### `GET`

* Format for GET requests https://iodisco.com/cb/sassy?scte35=your_data_goes_here

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
### GET Encode SCTE-35
```js
https://iodisco.com/cb/sassy?scte35={%22info_section%22:%20{%22table_id%22:%20%220xfc%22,%20%22section_syntax_indicator%22:%20false,%20%22private%22:%20false,%20%22sap_type%22:%20%220x01%22,%20%22sap_details%22:%20%22Type%202%20Closed%20GOP%20with%20leading%20pictures%22,%20%22section_length%22:%2037,%20%22protocol_version%22:%200,%20%22encrypted_packet%22:%20false,%20%22encryption_algorithm%22:%200,%20%22pts_adjustment%22:%2053.1,%20%22cw_index%22:%20%220x00%22,%20%22tier%22:%20%220x0fff%22,%20%22splice_command_length%22:%2020,%20%22splice_command_type%22:%205,%20%22descriptor_loop_length%22:%200,%20%22crc%22:%20%220x98d7e52c%22},%20%22command%22:%20{%22command_length%22:%2020,%20%22command_type%22:%205,%20%22name%22:%20%22Splice%20Insert%22,%20%22time_specified_flag%22:%20true,%20%22pts_time%22:%20100.0,%20%22break_auto_return%22:%20true,%20%22break_duration%22:%2060.0,%20%22splice_event_id%22:%201,%20%22splice_event_cancel_indicator%22:%20false,%20%22out_of_network_indicator%22:%20true,%20%22program_splice_flag%22:%20true,%20%22duration_flag%22:%20true,%20%22splice_immediate_flag%22:%20false,%20%22event_id_compliance_flag%22:%20true,%20%22unique_program_id%22:%201,%20%22avail_num%22:%200,%20%22avails_expected%22:%200},%20%22descriptors%22:%20[]}
```
* __output__ (notice "hex" and "base64" at the end of the json) 
```js
HTTP/2 200 
server: nginx
date: Tue, 20 May 2025 04:07:28 GMT
content-type: application/json
fumatic-for-the-people: All Signs Point to Yes
access-control-allow-methods: GET, POST, OPTIONS
access-control-expose-headers: Content-Length
access-control-allow-origin: origin-list
vary: Origin

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 37,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xc0f22992"
    },
    "command": {
        "command_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 100.0,
        "break_auto_return": true,
        "break_duration": 60.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": [],
    "hex": "0xfc302500000000000000fff01405000000017feffe00895440fe005265c0000100000000c0f22992",  #  <--Hex encoded
    "base64": "/DAlAAAAAAAAAP/wFAUAAAABf+/+AIlUQP4AUmXAAAEAAAAAwPIpkg=="  #   <-- Base64 encoded
}

```


## `Browser`
* Open in your browser: https://iodisco.com/cb/sassy?scte35=0xfc302f00019164e7980000000506fe849f2fa80019021743554549ffffffff7fbf010866756d6174696361100100ae05fd2e

 

* Open in your browser https://iodisco.com/cb/sassy?scte35={%22info_section%22:%20{%22table_id%22:%20%220xfc%22,%20%22section_syntax_indicator%22:%20false,%20%22private%22:%20false,%20%22sap_type%22:%20%220x01%22,%20%22sap_details%22:%20%22Type%202%20Closed%20GOP%20with%20leading%20pictures%22,%20%22section_length%22:%2037,%20%22protocol_version%22:%200,%20%22encrypted_packet%22:%20false,%20%22encryption_algorithm%22:%200,%20%22pts_adjustment%22:%2053.1,%20%22cw_index%22:%20%220x00%22,%20%22tier%22:%20%220x0fff%22,%20%22splice_command_length%22:%2020,%20%22splice_command_type%22:%205,%20%22descriptor_loop_length%22:%200,%20%22crc%22:%20%220x98d7e52c%22},%20%22command%22:%20{%22command_length%22:%2020,%20%22command_type%22:%205,%20%22name%22:%20%22Splice%20Insert%22,%20%22time_specified_flag%22:%20true,%20%22pts_time%22:%20100.0,%20%22break_auto_return%22:%20true,%20%22break_duration%22:%2060.0,%20%22splice_event_id%22:%201,%20%22splice_event_cancel_indicator%22:%20false,%20%22out_of_network_indicator%22:%20true,%20%22program_splice_flag%22:%20true,%20%22duration_flag%22:%20true,%20%22splice_immediate_flag%22:%20false,%20%22event_id_compliance_flag%22:%20true,%20%22unique_program_id%22:%201,%20%22avail_num%22:%200,%20%22avails_expected%22:%200},%20%22descriptors%22:%20[]}

![image](https://github.com/user-attachments/assets/a015819d-f8c9-4255-8fcc-0aebbe110392)
