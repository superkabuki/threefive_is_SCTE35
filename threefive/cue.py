"""
threefive.Cue Class
"""

from base64 import b64decode, b64encode
import json
from .stuff import clean, red, ishex, isjson, isxml, ERR
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map
from .crc import crc32
from .segmentation import table22
from .words import (
    minusone,
    zero,
    one,
    two,
    three,
    four,
    eight,
    eleven,
    fourteen,
    sixteen,
    equalsign,
)
from .xml import Node
from .uxp import xml2cue


class Cue(SCTE35Base):
    """
    The threefive.Cue class handles parsing
    SCTE 35 message strings.
    Example usage:

    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)
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
        self.dash_data = None
        self.decode()

    def __repr__(self):
        return str(self.__dict__)

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data

        *decode doesn't need to be called directly
           unless you initialize a Cue without data.
        """
        bites = self.bites
        self.descriptors = []
        while bites:
            bites = self.mk_info_section(bites)
            bites = self._set_splice_command(bites)
            bites = self._mk_descriptors(bites)
            if bites:
                crc = hex(int.from_bytes(bites[zero:four], byteorder="big"))
                self.info_section.crc = crc
                return True
        return False

    def _descriptor_loop(self, loop_bites):
        """
        Cue._descriptor_loop parses all splice descriptors
        """
        tag_n_len = two
        while len(loop_bites) > tag_n_len:
            spliced = splice_descriptor(loop_bites)
            sd_size = tag_n_len + spliced.descriptor_length
            loop_bites = loop_bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def _get_packet_data(self, scte35_dict):
        if self.packet_data:
            scte35_dict["packet_data"] = self.packet_data.get()
        return scte35_dict

    def get(self):
        """
        Cue.get returns the SCTE-35 Cue
        data as a dict of dicts.
        """
        scte35_data = False
        if self.command and self.info_section:
            scte35_data = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            scte35_data = self._get_packet_data(scte35_data)
        return scte35_data

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def bytes(self):
        """
        get_bytes returns Cue.bites
        """
        return self.bites

    def fix_bad_b64(self, data):
        """
        fix_bad_b64 fixes bad padding on Base64
        """
        while len(data) % four != zero:
            data = data + equalsign
        return data

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
        i = int(data, sixteen)
        return self._int_bits(i)

    def _b64_bits(self, data):
        """
        _b64_bits decode base64 to bytes
        """
        try:
            return b64decode(self.fix_bad_b64(data))
        except ERR:
            return red("Bad Base64")

    def _str_bits(self, data):
        if isxml(data) or isjson(data):
            self.load(data)
            return self.bites
        if ishex(data):
            return self._hex_bits(clean(data))
        data = data.strip()
        if data.isdigit():
            return self._int_bits(int(data))
        return self._b64_bits(data)

    def _pkt_bits(self, data):
        """
        _pkt_bits parse raw mpegts SCTE-35 packet
        """
        if data.startswith(b"G"):
            return data.split(b"\x00\x00\x01\xfc", one)[minusone]
        return data

    def _byte_bits(self, data):
        if isxml(data) or isjson(data):
            self.load(data)
        else:
            data = self._pkt_bits(data)
            self.bites = self.idxsplit(data, b"\xfc")
        return self.bites

    def _node_bits(self, data):
        data = data.mk()
        self._from_xml(data)
        return self.bites

    def _dict_bits(self, data):
        self.load(data)
        return self.bites

    def _mk_bits(self, data):
        """
        cue._mk_bits converts
        several SCTE-35 formats into bytes.
        """
        type_map = {
            Node: self._node_bits,
            dict: self._dict_bits,
            str: self._str_bits,
            bytes: self._byte_bits,
            int: self._int_bits,
        }
        td = type(data)
        if td in type_map.keys():
            return type_map[td](data)

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptor_loop
        """
        while bites:
            dll = (bites[zero] << eight) | bites[one]
            self.info_section.descriptor_loop_length = dll
            bites = bites[two:]
            self._descriptor_loop(bites[:dll])
            return bites[dll:]
        return False

    def mk_info_section(self, bites):
        """
        Cue.mk_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = fourteen
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        Cue._set_splice_command parses
        the command section of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return red(f"Splice Command type {sct} not recognized")
        iscl = self.info_section.splice_command_length
        cmd_bites = bites[:iscl]
        self.command = command_map[sct](cmd_bites)
        self.command.command_length = iscl
        self.command.decode()
        del self.command.bites
        return bites[iscl:]

    # encode related

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

    def encode(self):
        """
        encode is an alias for base64
        """
        return self.base64()

    def int(self):
        """
        int returns self.bites as an int.
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def encode_as_int(self):
        """
        encode_as_int backward compatibility
        """
        return self.int()

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
            return self._no_cmd()
        cmd = gonzo["command"]
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
            self.command.load(cmd)
        return "command_type" in cmd

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

    def _no_cmd(self):
        """
        _no_cmd raises an exception if no splice command.
        """
        return red("A splice command is required")

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
            gonzo = clean(gonzo)
        if isinstance(gonzo, str):
            if isxml(gonzo):
                self._from_xml(gonzo)
                return self.bites
            gonzo = json.loads(gonzo)
        self._load_info_section(gonzo)
        self._load_command(gonzo)
        self._load_descriptors(gonzo["descriptors"])
        self.encode()
        return self.bites

    def _from_xml(self, gonzo):
        """
        _from_xml converts xml to data that can
        be loaded by a Cue instance.
        """
        gonzo = clean(gonzo)
        if "Binary" in gonzo:
            dat = gonzo.split("Binary>", 1)[1].split("<", 1)[0]
            self.bites = self._mk_bits(dat)
            self.decode()
        elif "SpliceInfoSection" in gonzo:
            self.load(xml2cue(gonzo))
        else:
            self.bites = b""
        return self.bites

    def _xml_segmentation_comment(self, dscptr, sis):
        if dscptr.segmentation_type_id in table22:
            comment = f"{table22[dscptr.segmentation_type_id]}"
        else:
            comment = (
                f"Segmentation type id {dscptr.segmentation_type_id} is not in table 22"
            )
        sis.addcomment(comment)

    def _xml_mk_descriptor(self, sis, ns):
        """
        _mk_descriptor_xml make xml nodes for descriptors.
        """
        for dscptr in self.descriptors:
            if dscptr.has("segmentation_type_id"):
                self._xml_segmentation_comment(dscptr, sis)
            sis.addchild(dscptr.xml(ns=ns))
        return sis

    def xml(self, ns="scte35"):
        """
        xml returns a threefive.Node instance
        which can be edited as needed or printed.
        xmlbin
        """
        sis = self.info_section.xml(ns=ns)
        cmd = self.command.xml(ns=ns)
        sis.addchild(cmd)
        sis = self._xml_mk_descriptor(sis, ns)
        return sis  # xml retuns a Node instance. now

    def xmlbin(self, ns="scte35"):
        """
        xml returns a threefive.Node instance
        which can be edited as needed or printed.
        xmlbin

        """
        return f"""<{ns}:Signal xmlns:{ns}="https://scte.org/schemas/35">
    <{ns}:Binary>{self.base64()}</{ns}:Binary>
</{ns}:Signal>"""
