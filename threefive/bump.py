"""
threefive/bump.py

provides the function bumped to adjust pts in a SCTE-35 MPEGTS packet
bumped takes a packet and a float that is the amount to adjust  the SCTE-35 pts,

if the Cue in the packet has cue.command.pts_time:

    cue.command.pts_time is adjusted directly  like this:

    cue.command.pts_time = bump + cue.info_section.pts_adjustment+ cue.command.pts_time
    cue.info_section.pts_adjustment = 0.0

if the Cue in the packet doesn't have cue.command.pts_time:

        cue.info_section.pts_adjustment=bump + cue.info_section.pts_adjustment

final values are modolo`ed to the ROLLOVER.

"""
import io

import sys

from .cue import Cue
from .stuff import blue
from .stream import Stream

ROLLOVER = 95443.717678


def bump_pts_time(cue, bump):
    """
    bump_pts_time add bump directly to cue.command.pts_time
    """
    bumped = cue.command.pts_time + cue.info_section.pts_adjustment + bump
    cue.info_section.pts_adjustment = 0.0
    cue.command.pts_time = bumped % ROLLOVER


def bump_pts_adjust(cue, bump):
    """
    bump_pts_adjust add bump to cue.command.pts_adjustment
    """
    bumped = cue.info_section.pts_adjustment + bump
    cue.info_section.pts_adjustment = bumped % ROLLOVER


def show_bump(pay, cue):
    """
    show_bump show the Cue with adjusted pts.
    """ 
    blue("Cue adjusted")
   # cue.show()
    #blue(f"stop {len(pay)}")


def bump_pts(pay, bump):
    """
    bump_pts adjust SCTE-35 pts by bump
    """
    #blue(f" start {len(pay)}")
    cue = Cue(pay)
    if cue.command.pts_time:
        bump_pts_time(cue, bump)
    else:
        bump_pts_adjust(cue, bump)
    bites=cue.bytes()
    show_bump(pay, cue)
    return cue.bytes()


def repad(pkt):
    """
    repad add padding to packet as needed.
    """
    pad = b"\xff"
    padsize = 188 - len(pkt)
    pkt = pkt + (pad * padsize)
   # blue(f"pkt {len(pkt)}")
    return pkt


def bumped(pkt, bump):
    """
    bumped adjust the pts_time in the Cue in the pkt by bump,
    bump is a float in seconds.
    """
    if b"\xfc" in pkt:
        pre = pkt.split(b"\x00\x00\x01\xfc")[-1]
        tail = pre[pre.index(b"\xfc") :]
        head = pkt.replace(tail, b"")
        #blue(f"head {len(head)}")
        tail = bump_pts(tail, bump)
        pkt = repad(head + tail)
    return pkt


class BumpStream(Stream):
    """
    Bump Stream class

        Adjust SCTE-35 PTS times  in MPEGTS
    """

    def _pts(self, pkt, pid):
        if self._pusi_flag(pkt):
            self._chk_pts(pkt, pid)

    def _scte35(self, pkt, pid, bump):
        if self._pid_has_scte35(pid):
            cue = self._parse_scte35(pkt, pid)
##            if cue:
##                cue.show()
            pkt = bumped(pkt, bump)
        return pkt

    def parse(self, pkt, bump):
        """
        parse packets for tables and SCTE-35,
        adjust SCTE-35 PTS by bump.
        return modified pkt.
        """
        pid = self._parse_info(pkt)
      #  self._pts(pkt, pid)
        pkt = self._scte35(pkt, pid, bump)
        return pkt


    def bump_scte35(self, bump):
        """
        bump_scte_35 adjust pts of the SCTE-35 by bump
        """
        bump = float(bump)
        num_pkts = 2420
        for chunk in self.iter_pkts(num_pkts):
            pkts = [self.parse(chunk[i : i + self.PACKET_SIZE], bump)
             for i in range(0, len(chunk), self.PACKET_SIZE)
            ]
            sys.stdout.buffer.write(b"".join(pkts))
            sys.stdout.buffer.flush()

        return False
