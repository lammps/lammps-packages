#!/bin/sh

if [ $# -ne 1 ] ; then
   echo "Usage: $0 <revision>"
   exit 1
fi

for b in 64 32 ; do \
    for m in no mpi ; do \
        python3 cmake-win-on-linux.py -v yes -r unstable -p ${m} -t omp -b ${b} -a yes
    done
done

for b in 64 32 ; do \
    for m in no mpi ; do \
        python3 cmake-win-on-linux.py -v yes -r unstable -p ${m} -t omp -b ${b} -a no
    done
done

for b in 64 ; do \
    for m in no ; do \
        python3 cmake-win-on-linux.py -v yes -r unstable -p ${m} -t omp -b ${b} -a msix
    done
done
