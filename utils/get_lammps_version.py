#!/bin/python
from __future__ import print_function
from datetime import datetime
import os
import argparse

def get_lammps_version(lammps_dir):
    with open(os.path.join(lammps_dir, 'src/version.h'), 'r') as f:
        line = f.readline()
        start_pos = line.find('"')+1
        end_pos = line.find('"', start_pos)
        datestr = line[start_pos:end_pos]
        return datetime.strptime(datestr, "%d %b %Y")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lammps_dir', help='LAMMPS base directory')
    args = parser.parse_args()
    print(get_lammps_version(args.lammps_dir).strftime("%Y%m%d"))
