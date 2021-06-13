#!/usr/bin/python3

from nbt.region import RegionFile

import os
import sys


scriptpath = sys.argv.pop(0)

region_file = None
cutoff_ticks = 1200
dry_run = False

for a in sys.argv:
    i = a.index('=')
    k = a[0 : i]
    v = a[i + 1:]
    if k == 'file':
        region_file = v
    elif k == 'cutoff':
        cutoff_ticks = int(v)
    elif k == 'dryrun':
        if v in ['true', 'false']:
            dry_run = (v == 'true')
        else:
            fatal("No such dryrun value: '{}'".format(v))
    else:
        fatal("No such argument: '{}'".format(k))

files = []
if region_file is not None:
    files = [region_file]
else:
    files = os.listdir()

for file in files:
    region = RegionFile(file)
    chunks = region.get_chunks()
    for chunk in chunks:
        x = chunk['x']
        z = chunk['z']
        chunk_nbt = region.get_chunk(x, z)
        inhabited_time = chunk_nbt['Level']['InhabitedTime'].value
        if inhabited_time < cutoff_ticks:
            if not dry_run:
                region.unlink_chunk(x, z)
            print("{},{},{},{}:".format(file, x, z, inhabited_time))
