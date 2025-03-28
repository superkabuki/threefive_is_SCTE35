from base64 import b64decode, b64encode



class BitMaker:

    def __init__(self,data):
        self.data =data
        self.bites=b''

    def fix_bad_b64(self, data):
        """
        fix_bad_b64 fixes bad padding on Base64
        """
        while len(data) % 4 != 0:
            data = data + '='
        return data

    def _int_bits(self):
        """
        _int_bits convert SCTE-35 from integer to bytes.
        """
        length = self.data.bit_length() >> 3
        self.bites = int.to_bytes(data, length, byteorder="big")
        return self.bites

    def _hex_bits(self):
        """
        _hex_bits convert a SCTE-35 Cue from hex to bytes.
        """
        try:
            i = int(self.data, 16)
            i_len = i.bit_length() >> 3
            self.bites = int.to_bytes(i, i_len, byteorder="big")
            return self.bites
        except (LookupError, TypeError, ValueError):
            if self.data[:2].lower() == "0x":
                self.data = data[2:]
            if self.data[:2].lower() == "fc":
                self.bites=bytes.fromhex(self.data)
                return self.bites
        return False

    def _b64_bits(self):
        """
        _b64_bits decode base64 to bytes
        """
        try:
            self.bites= b64decode(self.fix_bad_b64(self.data))
            return self.bites
        except (LookupError, TypeError, ValueError):
            return  False
        
    def _byte_bits(self):
        self._pkt_bits()
        self.bites = self.idxsplit(self.data, b"\xfc")
        return self.bites

    def _str_bits(self):
        if self.data.isdigit():
            self.data = int(self.data)
            return self._int_bits()
        if self.data.strip()[0] == "<":
            return self._xml_bits()
        hx=self._hex_bits()
        if hx:
            return hx
        return self._b64_bits() 

    def _pkt_bits(self):
        """
        _pkt_bits parse raw mpegts SCTE-35 packet
        """
        if self.data.startswith(b"G"):
            self.data=self.data.split(b"\x00\x00\x01\xfc", 1)[-1]

    def _xml_bits(self):
        """
        _from_xml converts xml to data that can
        be loaded by a Cue instance.
        """
        spliton = "Binary"
        if "scte35:Binary" in self.data:
            spliton = "scte35:Binary"
        if spliton in self.data:
            self.data = self.data.split(f"<{spliton}>")[1].split(f"</{spliton}>")[0]
            return self._b64_bits()

    def mk_bits(self):
        """
        _mk_bits Converts a variety of data formats
        to raw bytes for a Cue instance to process.
        """
        typemap = {bytes: self._byte_bits,
                             int:self._int_bits,
                             str:self._str_bits,}
        isa= type(self.data)
        if isa in typemap:
            return typemap[isa]()
        return False






    
