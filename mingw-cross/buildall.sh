#!/bin/sh

if [ $# -ne 1 ] ; then
   echo "Usage: $0 <revision>"
   exit 1
fi

for m in ms no; do \
    python3 cmake-win-on-linux.py -v yes -r "$1" -p ${m} -t omp -b 64 -a no
    python3 cmake-win-on-linux.py -v yes -r "$1" -p ${m} -t omp -b 64 -a no -y yes
done
python3 cmake-win-on-linux.py -v yes -r "$1" -p no -t omp -b 64 -a no -u yes
