"""
Ultra Xml Parser.... Supreme
"""

from .segmentation import table20, table22
from .stuff import ERR
from .upids import upid_map
from .xml import Node, iter_attrs


def mk_attrs(line):
    """
    mk_attrs parses the current line for attributes
    """
    line = (
        line.replace('"', "")
        .replace("<", "")
        .replace("/>", "")
        .replace(">", "")
        .strip()
    )
    attrs = {y[0]: y[1] for y in [x.split("=") for x in line.split(" ") if "=" in x]}
    return iter_attrs(attrs)


def mk_tag(data):
    """
    mk_tag parse out the
    next available xml tag from data
    """
    return data[1:].split(" ", 1)[0].strip()


def mk_line(exemel):
    """
    mk_line grabs the next '<' to '>' section of xml
    """
    line = exemel.split(">", 1)[0] + ">"
    exemel = exemel.replace(line, "", 1).strip()
    return line, exemel


def mk_node(tag, line, exemel):
    """
    mk_node marshal xml data
    into a  threefive3.xml.Node instance.

    """
    ns = None
    attrs = mk_attrs(line)
    if ":" in tag:
        ns, tag = tag.split(":", 1)
    tag=tag.strip('>')
    node = Node(tag, attrs=attrs, ns=ns)
    if not exemel.startswith("<"):
        node.value = exemel.split("<", 1)[0]
        exemel = exemel.replace(node.value, "", 1).strip()
    return node, exemel


def starttag(line, node, openlist):
    """
    starttag self-terminating nodes
    are added as children to the last
    node in openlist.
    open nodes (nodes that aren't self-terminating)
    are appended to openlist
    """
    if line.endswith("/>"):
        openlist[-1].add_child(node)
    else:
        openlist.append(node)
    return openlist


def endtag(openlist):
    """
    endtag when a node is closed
    pop it off openlist and then
    add it as a child to the last node
    in openlist, if any nodes are still in
    openlist
    """
    final = False
    closed = openlist.pop()
    if openlist:
        openlist[-1].add_child(closed)
    else:
        final = closed
    return final


def parsexml(exemel):
    """
    parsexml parse xml into a node instance and
    children.
    """
    final = False
    openlist = []
    exemel = exemel.replace("\n", "").strip()
    while exemel:
        line, exemel = mk_line(exemel)
        if not line.startswith("<!--"):
            tag = mk_tag(line)
            if "/" not in tag:
                node, exemel = mk_node(tag, line, exemel)
                openlist = starttag(line, node, openlist)
            else:
                final = endtag(openlist)
    return final


def xmlspliceinfosection(node):
    """
    spliceinfosection parses exemel for info section data
    and returns a loadable dict
    """
    if "SpliceInfoSection" in node.name:
        node.attrs["tier"] = hex(node.attrs["tier"])
        return node.attrs
    return {}


def xmlcommand(node):
    """
    command parses exemel for a splice command
    and returns a loadable dict

    """
    cmap = {
        "TimeSignal": xmltimesignal,
        "SpliceInsert": xmlspliceinsert,
        "PrivateCommand": xmlprivatecommand,
    }
    for child in node.children:
        if child.name in cmap:
            out = cmap[child.name](child)
            return out
    return {}


def xmltimesignal_children(node):
    for child in node.children:
        splice_time = xmlsplicetime(child)
        node.attrs.update(splice_time)
    return node


def xmltimesignal(node):
    """
    timesignal parses exemel for TimeSignal data
    and creates a loadable dict for the Cue class.
    """
    setme = {
        "name": "Time Signal",
        "command_type": 6,
    }

    node.attrs.update(setme)
    node = xmltimesignal_children(node)
    return node.attrs


def xmlprivatecommand(node):
    """
    privatecommand parses exemel for PrivateCommand
    data and creates a loadable dict for the Cue class.
    """
    setme = {
        "command_type": 255,
        "private_bytes": pc.value,
    }

    node.attrs.update(setme)
    return node.attrs


def xmlsplicetime(node):
    """
    splicetime parses xml from a splice command
    to get pts_time, sets time_specified_flag to True
    """
    if node.name == "SpliceTime":
        return {
            "pts_time": node.attrs["pts_time"],
            "time_specified_flag": True,
        }
    return {}


def xmlbreakduration(node):
    """
    breakduration parses xml for break duration, break_auto_return
    and sets duration_flag to True.
    """
    if node.name == "BreakDuration":
        return {
            "break_duration": node.attrs["duration"],
            "break_auto_return": node.attrs["auto_return"],
            "duration_flag": True,
        }
    return {}


def xmlspliceinsert_children(node):
    for child in node.children:
        splice_time = xmlsplicetime(child)
        node.attrs.update(splice_time)
        if "pts_time" in node.attrs:
            node.attrs["program_splice_flag"] = True
        break_duration = xmlbreakduration(child)
        node.attrs.update(break_duration)
    return node


def xmlspliceinsert(node):
    """
    spliceinsert parses exemel for SpliceInsert data
    and creates a loadable dict for the Cue class.
    """
    setme = {
        "command_type": 5,
        "event_id_compliance_flag": True,
        "program_splice_flag": False,
        "duration_flag": False,
    }
    node.attrs.update(setme)
    node = xmlspliceinsert_children(node)
    return node.attrs


def xmldeliveryrestrictions(node):
    if node.name == "DeliveryRestrictions":
        setme = {
            "delivery_not_restricted_flag": False,
            "device_restrictions": table20[node.attrs["device_restrictions"]],
        }
        node.attrs.update(setme)
        return node.attrs
    return {}


def xmlupid(node):
    """
    upids parses out upids from a splice descriptors xml
    """
    if node.name == "SegmentationUpid":
        try:
            seg_upid = bytes.fromhex(node.value.lower().replace("0x", ""))
        except ERR:
            seg_upid = node.value
        seg_upid_type = node.attrs["segmentation_upid_type"]
        return {
            "segmentation_upid": node.value,
            "segmentation_upid_type": seg_upid_type,
            "segmentation_upid_type_name": upid_map[seg_upid_type][0],
            "segmentation_upid_length": len(seg_upid),
        }
    return {}


def xmlsegmentationdescriptor_children(node):
    for child in node.children:
        dr = xmldeliveryrestrictions(child)
        node.attrs.update(dr)
        the_upid = xmlupid(child)
        node.attrs.update(the_upid)
    return node


def xmlsegmentation_message(node):
    if node.attrs["segmentation_type_id"] in table22:
        node.attrs["segmentation_message"] = table22[node.attrs["segmentation_type_id"]]
    return node


def xmlsegmentationdescriptor(node):
    """
    segmentationdescriptor creates a dict to be loaded.
    """
    setme = {
        "tag": 2,
        "identifier": "CUEI",
        "name": "Segmentation Descriptor",
        "segmentation_event_id_compliance_indicator": True,
        "program_segmentation_flag": True,
        "segmentation_duration_flag": False,
        "delivery_not_restricted_flag": True,
        "segmentation_event_id": hex(node.attrs["segmentation_event_id"]),
    }
    node.attrs.update(setme)
    node = xmlsegmentation_message(node)
    node = xmlsegmentationdescriptor_children(node)
    return node.attrs


def xmlavaildescriptor(node):
    setme = {
        "tag": 0,
        "identifier": "CUEI",
    }
    node.attrs.update(setme)
    return node.attrs


def xmltimedescriptor(node):
    setme = {
        "tag": 3,
        "identifi er": "CUEI",
    }
    node.attrs.update(setme)
    return node.attrs


def xmldescriptors(node):
    dmap = {
        "AvailDescriptor": xmlavaildescriptor,
        # "DTMFDescriptor",
        "SegmentationDescriptor": xmlsegmentationdescriptor,
        "TimeDescriptor": xmltimedescriptor,
    }
    dscripts = []
    for child in node.children:
        if child.name in dmap:
            dscripts.append(dmap[child.name](child))
    return dscripts


def xml2cue(ex):
    bignode = parsexml(ex)
    if isinstance(bignode, Node):
        return {
            "info_section": xmlspliceinfosection(bignode),
            "command": xmlcommand(bignode),
            "descriptors": xmldescriptors(bignode),
        }
    return False
