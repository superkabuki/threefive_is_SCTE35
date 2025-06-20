<details><summary>MPEGTS</summary>
* MPEGTS streams can be local file, http(s), multicast, or  stdin. 

* cli
```js
threefive https://example.com/video.ts
```
* wildcards work too.
```js
threefive /mpegts/*.ts
```

* lib
```py3

from threefive import Cue
data = '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
cue=Cue(data)
cue.show())
```

</details>

---




<details><summary>Base64</summary>

* cli
```js
threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```
* lib
```py3

from threefive import Cue
data = '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
cue=Cue(data)
cue.show())
```

</details>

---

<details><summary>Bytes</summary>

* cli
	* Bytes don't work on the cli

* lib
```py3

from threefive import Cue
data =  b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\xc0D\xa0\x00\x00\x00\xb5k\x88'
cue=Cue(data)
cue.show()
```

</details>

---

<details><summary>Hex</summary>

* Can be a hex literal or hex string or bytes.

* cli
```js
threefive  0xfc301600000000000000fff00506fed605225b0000b0b65f3b
```
* lib
```py3

from threefive import Cue
data =  0xfc301600000000000000fff00506fed605225b0000b0b65f3b
cue=Cue(data)
cue.show())
```



</details>

---

<details><summary>Int</summary>

* Can be a literal integer or string or bytes.

* cli
```js
threefive  1583008701074197245727019716796221243043855984942057168199483b
```
* lib
```py3

from threefive import Cue
data =  1583008701074197245727019716796221243043855984942057168199483
cue=Cue(data)
cue.show()
```


</details>

---

<details><summary>JSON</summary>

* cli
	* 	put JSON SCTE-35 in a file and redirect it into threefive 
```js
threefive  < json.json
```
* lib

```py3

 from threefive import Cue
 data = '''{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xb56b88"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 140.005333
    },
    "descriptors": []
}
'''
cue=Cue(data)
cue.show()
```

</details>

---

<details><summary>Xml</summary>

* cli
	* put xml SCTE-35 in a file and redirect it into threefive 
	```js
	threefive < xmlbin.xml
	```
* lib
```py3
from threefive import Cue
data =  '''
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35" 
        ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="12600480"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
'''
cue=Cue(data)

cue.show()
```


</details>

---

<details><summary>Xml+binary</summary>

* cli
	* write xml+binary to a file and redirect it to threefive
```js
threefive < xmlbin.xml
```
* lib
```py3

from threefive import Cue
data = '''<scte35:Signal xmlns:scte35="https://scte.org/schemas/35">
    <scte35:Binary>/DAWAAAAAAAAAP/wBQb+AMBEoAAAALVriA==</scte35:Binary>
</scte35:Signal>
'''
cue=Cue(data)
cue.show())
```

</details>

---

<details><summary></summary>



</details>
