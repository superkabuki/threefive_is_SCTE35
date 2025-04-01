"""
parsehlstags.py
Use the TagParser class to parse hls tags from a m3u8 file
and group the tags into a dict by segment.
"""

from threefive3.hlstags import TagParser


data={}
with open('/home/a/flat.m3u8','r') as mu:
    results=[]
    lines= mu.readlines()
    for line in lines:
        if line.startswith("#"):
            # hold tags until we find a segment
            results.append(line)
        else:
            tp=TagParser(results)
            # when we find a segment, make it a key in data
            # and a dict of the tags as the value
            data[line]=tp.tags
            # clear results for next segment
            results =[]

    for k in list(sorted(data.keys())):
        print(f'{k} : {data[k]}')
