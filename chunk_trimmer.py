#!/usr/bin/python3

from nbt.region import RegionFile

import os
import sys


scriptpath = sys.argv.pop(0)

# Default argument values
region_file = None
cutoff_ticks = 1200 # 60 seconds (20 ticks per second * 60)
dry_run = False

# Get arguments
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

# Get list of files to trim
files = []
if region_file is not None:
    files = [region_file]
else:
    files = os.listdir()

# Delete all chunks in files less inhabited than the cutoff number of ticks
for file in files:
    region = RegionFile(file)
    chunks = region.get_chunks()
    for chunk in chunks:
        x = chunk['x']
        z = chunk['z']
        try:
            chunk_nbt = region.get_chunk(x, z)
        except Exception as e:
            print("Error with file {} chunk {},{}".format(file, x, z), file=sys.stderr)
            raise e
        inhabited_time = chunk_nbt['Level']['InhabitedTime'].value
        if inhabited_time < cutoff_ticks:
            if not dry_run:
                region.unlink_chunk(x, z)
            print("{},{},{},{}".format(file, x, z, inhabited_time))
