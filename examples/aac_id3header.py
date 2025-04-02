#!/usr/bin/env python3
"""
aac_id3header.py

Use threefive3.aac.AacParser class to 
parse HLS aac segments for PTS in ID3 header tags. 

"""

from threefive3.aac import AacParser

ap = AacParser()
#  this is an HLS audio only segment with PTS in an ID3 header tag.
url = 'https://futzu.com/id3.aac' 
pts = ap.parse(url)
print(f'PTS : {pts}')

