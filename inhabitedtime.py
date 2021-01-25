#!/usr/bin/python3

from nbt.region import RegionFile

import sys


scriptpath = sys.argv.pop(0)
region_file = sys.argv.pop(0)

max_inhabited_time = 0

region = RegionFile(region_file)
for chunk in region.get_chunks():
    real_chunk = region.get_chunk(chunk['x'], chunk['z'])
    for chunk_item in real_chunk.items():
        if chunk_item[0] == 'Level':
            for level_item in chunk_item[1].items():
                if level_item[0] == 'InhabitedTime':
                    inhabited_time = level_item[1].value
                    if inhabited_time > max_inhabited_time:
                        max_inhabited_time = inhabited_time
                    break
            break
print(max_inhabited_time)
