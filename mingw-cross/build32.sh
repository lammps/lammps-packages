#!/bin/sh

if [ $# -ne 1 ] ; then
   echo "Usage: $0 <revision>"
   exit 1
fi

for m in no mpi ; do \
    python3 cmake-win-on-linux.py -v yes -r "$1" -p ${m} -t omp -b 32 -a yes
    python3 cmake-win-on-linux.py -v yes -r "$1" -p ${m} -t omp -b 32 -a no
    python3 cmake-win-on-linux.py -v yes -r "$1" -p ${m} -t omp -b 32 -a no -y yes
done
