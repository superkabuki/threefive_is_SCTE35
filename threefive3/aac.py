"""
aac.py
home of the AacParser for audio only hls renditions
"""
from .new_reader import reader


ROLLOVER = 95443.717678


class AacParser:
    """
    AacParser parses aac segments.
    """

    applehead = b"com.apple.streaming.transportStreamTimestamp"

    @staticmethod
    def is_header(header):
        """
        is_header tests aac and ac3 files for ID3 headers.
        """
        if header[:3] == b"ID3":
            return True
        return False

    @staticmethod
    def id3_len(header):
        """
        id3_len parses the length value from ID3 headers
        """
        id3len = int.from_bytes(header[6:], byteorder="big")
        return id3len

    @staticmethod
    def syncsafe5(somebytes):
        """
        syncsafe5 parses PTS from ID3 tags.
        """
        lsb = len(somebytes) - 1
        syncd = 0
        for idx, bite in enumerate(somebytes):
            syncd += bite << ((lsb - idx) << 3)
        return round(syncd / 90000.0, 6)

    def parse(self, media):
        """
        aac_pts parses the ID3 header tags in aac and ac3 audio files
        """
        pts = 0
        aac = reader(media)
        header = aac.read(10)
        if self.is_header(header):
            id3len = self.id3_len(header)
            data = aac.read(id3len)
            if self.applehead in data:
                try:
                    pts = float(data.split(self.applehead)[1].split(b"\x00", 2)[1])
                except:
                    pts = self.syncsafe5(data.split(self.applehead)[1][:9])
        return round((pts % ROLLOVER), 6)

