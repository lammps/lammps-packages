#!/bin/bash

# Usage on Fedora 32 MinGW container from lammps-testing
git clone git@github.com:microsoft/msix-packaging.git

cd msix-packaging
./makelinux.sh --pack

export PATH=$PWD/.vs/bin:$PATH

# unpack MSIX package
makemsix unpack -p LAMMPS-64bit-MPI.msix -d LAMMPS -ac -ss

# replace assets
cp Assets/* LAMMPS/Assets/

# repackage MSIX
makemsix pack -d LAMMPS -p LAMMPS-64bit-MPI-new.msix
