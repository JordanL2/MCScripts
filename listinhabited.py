#!/usr/bin/python3

from nbt.nbt import *
from nbt.region import *

import sys


scriptpath = sys.argv.pop(0)
region_file = sys.argv.pop(0)

region = RegionFile(region_file)
chunks = region.get_chunks()
for chunk in chunks:
    x = chunk['x']
    z = chunk['z']
    chunk_nbt = region.get_chunk(x, z)
    print(x, z, chunk_nbt['Level']['InhabitedTime'])
