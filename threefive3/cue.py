"""
threefive3.Cue Class
"""

from base64 import b64decode, b64encode
import json
from .stuff import red, blue
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .crc import crc32
from .words import minusone, zero, one, two, three, four, eight
from .words import eleven, fourteen, sixteen, equalsign


class Cue(SCTE35Base):
    """
    The threefive3.Cue class handles parsing
    SCTE 35 message strings.
    Example usage:

    >>>> import threefive3
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive3.Cue(Base64)
    >>>> cue.show()

    * A cue instance can be initialized with
     Base64, Bytes, Hex, Int, Json, or Xml+binary data.

    * Instance variables can be accessed via dot notation.

    >>>> cue.command
    {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
    'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089


    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a instance passed from a Stream instance
        """
        self.command = None
        self.descriptors = []
        self.info_section = SpliceInfoSection()
        self.bites = None
        if data:
            self.bites = self._mk_bits(data)
            self.packet_data = packet_data
            self.decode()

    def __repr__(self):
        return str(self.__dict__)

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data

        * decode doesn't need to be called directly
           unless you initialize a Cue without data.
        """
        bites = self.bites
        self.descriptors = []
        self.command, self.descriptors= self.info_section.decode(bites)
        return True

    def _get_packet_data(self, scte35_dict):
        if self.packet_data:
            scte35_dict["packet_data"] = self.packet_data.get()
        return scte35_dict

    def get(self):
        """
        Cue.get returns the SCTE-35 Cue
        data as a dict of dicts.
        """
        if self.command and self.info_section:
            scte35_data = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            scte35_data = self._get_packet_data(scte35_data)
            return scte35_data
        return False

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def _int_bits(self, data):
        """
        _int_bits convert a SCTE-35 Cue from integer to bytes.
        """
        length = data.bit_length() >> three
        bites = int.to_bytes(data, length, byteorder="big")
        return bites

    def _hex_bits(self, data):
        """
        _hex_bits convert a SCTE-35 Cue from hex to bytes.
        """
        try:
            i = int(data, sixteen)
            i_len = i.bit_length() >> three
            bites = int.to_bytes(i, i_len, byteorder="big")
            return bites
        except (LookupError, TypeError, ValueError):
            if data[:two].lower() == "0x":
                data = data[two:]
            if data[:two].lower() == "fc":
                return bytes.fromhex(data)
        return b""

    def _b64_bits(self, data):
        """
        _b64_bits decode base64 to bytes
        """
        try:
            return b64decode(self.fix_bad_b64(data))
        except (LookupError, TypeError, ValueError):
            return data

    def _str_bits(self, data):
        try:
            self.load(data)
            return self.bites
        except (LookupError, TypeError, ValueError):
            hex_bits = self._hex_bits(data)
            if hex_bits:
                return hex_bits
        return self._b64_bits(data)

    def _pkt_bits(self, data):
        """
        _pkt_bits parse raw mpegts SCTE-35 packet
        """
        if data.startswith(b"G"):
            return data.split(b"\x00\x00\x01\xfc", one)[minusone]
        return data

    def _mk_bits(self, data):
        """
        cue._mk_bits Converts
        Hex and Base64 strings into bytes.
        """
        bites = data
        if isinstance(data, dict):
            self.load(data)
            return self.bites
        if isinstance(data, bytes):
            data = self._pkt_bits(data)
            bites = self.idxsplit(data, b"\xfc")
            return bites
        if isinstance(data, int):
            return self._int_bits(data)
        if isinstance(data, str):
            return self._str_bits(data)

    def _assemble(self):
        dscptr_bites = self._unloop_descriptors()
        dll = len(dscptr_bites)
        self.info_section.descriptor_loop_length = dll
        cmd_bites = self.command.encode()
        cmdl = self.command.command_length = len(cmd_bites)
        self.info_section.splice_command_length = cmdl
        self.info_section.splice_command_type = self.command.command_type
        # 11 bytes for info section + command + 2 descriptor loop length
        # + descriptor loop + 4 for crc
        self.info_section.section_length = eleven + cmdl + two + dll + four
        self.bites = self.info_section.encode()
        self.bites += cmd_bites
        self.bites += int.to_bytes(
            self.info_section.descriptor_loop_length, two, byteorder="big"
        )
        self.bites += dscptr_bites

    def base64(self):
        """
        base64 Cue.base64() converts SCTE35 data
        to a base64 encoded string.
        """
        if self.command:
            self._assemble()
            self._encode_crc()
            return b64encode(self.bites).decode()
        return False

    def bytes(self):
        """
        get_bytes returns Cue.bites
        """
        return self.bites

    def encode(self):
        """
        encode is an alias for base64
        """
        return self.base64()

    def fix_bad_b64(self, data):
        """
        fix_bad_b64 fixes bad padding on Base64
        """
        while len(data) % four != zero:
            data = data + equalsign
        return data

    def int(self):
        """
        int returns self.bites as an int.
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def hex(self):
        """
        hex returns self.bites as
        a hex string
        """
        return hex(self.int())

    def encode_as_hex(self):
        """
        encode_as_hex backward compatibility
        """
        return self.hex()

    def _encode_crc(self):
        """
        _encode_crc encode crc32
        """
        crc_int = crc32(self.bites)
        self.info_section.crc = hex(crc_int)
        self.bites += int.to_bytes(crc_int, four, byteorder="big")

    def _unloop_descriptors(self):
        """
        _unloop_descriptors
        for each descriptor in self.descriptors
        encode descriptor tag, descriptor length,
        and the descriptor into all_bites.bites
        """
        all_bites = NBin()
        dbite_chunks = [dsptr.encode() for dsptr in self.descriptors]
        for chunk, dsptr in zip(dbite_chunks, self.descriptors):
            dsptr.descriptor_length = len(chunk)
            all_bites.add_int(dsptr.tag, eight)
            all_bites.add_int(dsptr.descriptor_length, eight)
            all_bites.add_bites(chunk)
        return all_bites.bites

    def _load_info_section(self, gonzo):
        """
        load_info_section loads data for Cue.info_section
        isec should be a dict.
        if 'splice_command_type' is included,
        an empty command instance will be created for Cue.command
        """
        if "info_section" in gonzo:
            self.info_section.load(gonzo["info_section"])

    def _load_command(self, gonzo):
        """
        load_command loads data for Cue.command
        cmd should be a dict.
        if 'command_type' is included,
        the command instance will be created.
        """
        if "command" not in gonzo:
            self._no_cmd()
            return False
        cmd = gonzo["command"]
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
            self.command.load(cmd)

    def _load_descriptors(self, dlist):
        """
        Load_descriptors loads descriptor data.
        dlist is a list of dicts
        if 'tag' is included in each dict,
        a descriptor instance will be created.
        """
        if not isinstance(dlist, list):
            red("descriptors should be a list")
        for dstuff in dlist:
            dscptr = descriptor_map[dstuff["tag"]]()
            dscptr.load(dstuff)
            self.descriptors.append(dscptr)

    def load(self, gonzo):
        """
        Cue.load loads SCTE35 data for encoding.
        gonzo is a dict or json
        with any or all of these keys
        gonzo = {
            'info_section': {dict} ,
            'command': {dict},
            'descriptors': [list of {dicts}],
            }

        * load doesn't need to be called directly
          unless you initialize a Cue without data.

        """
        if isinstance(gonzo, bytes):
            gonzo = gonzo.decode()
        if isinstance(gonzo, str):
            if gonzo.isdigit():
                gonzo = int(gonzo)
                self.bites = self._int_bits(int(gonzo))
                self.decode()
                return self.bites
            if gonzo.strip()[zero] == "<":
                self._from_xml(gonzo)
                return self.bites
            gonzo = json.loads(gonzo)
        self._load_info_section(gonzo)
        self._load_command(gonzo)
        self._load_descriptors(gonzo["descriptors"])
        self.encode()
        return self.bites

    def _no_cmd(self):
        """
        _no_cmd raises an exception if no splice command.
        """
        red("A splice command is required")

    def _from_xml(self, gonzo):
        """
        _from_xml converts xml to data that can
        be loaded by a Cue instance.
        """

        if isinstance(
            gonzo, str
        ):  # a string  is returned for Binary xml tag, make sense?
            spliton = "Binary"
            if "scte35:Binary" in gonzo:
                spliton = "scte35:Binary"
            if spliton in gonzo:
                dat = gonzo.split(f"<{spliton}>")[1].split(f"</{spliton}>")[0]
                self.bites = self._mk_bits(dat)
                self.decode()
            else:
                blue("Only xml+binary format supported ")
        else:
            blue("xmlbin data needs to be str instance")

    def xmlbin(self):
        """
        xml returns a threefive3.Node instance
        which can be edited as needed or printed.
        xmlbin

        """
        return f"""<scte35:Signal xmlns:scte35="https://scte.org/schemas/35">
    <scte35:Binary>{self.base64()}</scte35:Binary>
</scte35:Signal>"""
