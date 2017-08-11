#!/usr/bin/env python

# script to build windows installer packages for LAMMPS
# (c) 2017 Axel Kohlmeyer <akohlmey@gmail.com>

from __future__ import print_function
import sys,os,shutil,glob,re,subprocess
try: from urllib.request import urlretrieve as geturl
except: from urllib import urlretrieve as geturl

# helper functions

def error(str=None):
    if not str: print(helpmsg)
    else: print(sys.argv[0],"ERROR:",str)
    sys.exit()

def system(cmd):
    txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    return txt.decode('UTF-8')

def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# default settings help message and default settings

bitflag = '64'
dirflag = fullpath('.')
parflag = 'mpi'
thrflag = 'no'
verflag = 'stable'

helpmsg = """
Usage: python build-win-on-linux.py -b <bits> -d <dir> -p <mpi> -t <thread> -v <version>

Flags (all flags are optional, defaults listed below):
  -b : select Windows variant (default value: %s)
    -b 32 : build for 32-bit Windows
    -b 64 : build for 64-bit Windows
  -d : select build directory (default value: %s)
    -d <path> : point to any valid writable folder
  -p : select message passing parallel build (default value: %s)
    -p mpi    : build an MPI parallel version with MPICH2 v1.4.1p1
    -p no     : build a serial version using MPI STUBS library
  -t : select thread support (default value: %s)
    -t omp    : build with threads via OpenMP enabled
    -t no     : build with thread support disabled
  -v : select LAMMPS source version to build (default value: %s)
    -v stable   : download and build the latest stable LAMMPS version
    -v unstable : download and build the latest patch release LAMMPS version
    -v master   : download and build the latest development snapshot
    -v patch_<date> : download and build a specific patch release
    -v <sha256> : download and build a specific snapshot version

Example:
  python build-win-on-linux.py -v unstable -t omp -p mpi
""" % (bitflag,dirflag,parflag,thrflag,verflag)


# parse arguments

argv = sys.argv
argc = len(argv)
i = 1

while i < argc:
    if i+1 >= argc:
        print("\nMissing argument to flag:",argv[i])
        error()
    if argv[i] == '-b':
        bitflag = argv[i+1]
    elif argv[i] == '-d':
        dirflag = fullpath(argv[i+1])
    elif argv[i] == '-p':
        parflag = argv[i+1]
    elif argv[i] == '-t':
        thrflag = argv[i+1]
    elif argv[i] == '-v':
        verflag = argv[i+1]
    else:
        print("\nUnknown flag:",argv[i])
        error()
    i+=2

# checks
if bitflag != '32' and bitflag != '64':
    error("Unsupported bitness flag %s" % bitflag)
if parflag != 'serial' and parflag != 'mpi':
    error("Unsupported parallel flag %s" % parflag)
if thrflag != 'no' and thrflag != 'omp':
    error("Unsupported threading flag %s" % thrflag)
# XXX add support to test for explicit patch labels and commit hashes
if verflag != 'stable' and verflag != 'unstable' \
   and verflag != 'master':
    error("Unsupported version flag %s" % verflag)

# create working directory
buildpath = "%s/tmp-%s-%s-%s-%s" % (dirflag,bitflag,parflag,thrflag,verflag)
if not os.path.isdir(dirflag):
    error("Invalid build path %s" % dirflag)
else:
    shutil.rmtree(buildpath,True)
    try:
        os.mkdir(buildpath)
    except:
        error("Cannot create temporary build  path: %s" % buildpath)

# check for prerequisites and set up build environment
if bitflag == '32':
    cc_cmd = which('i686-w64-mingw32-gcc')
    cxx_cmd = which('i686-w64-mingw32-g++')
    fc_cmd = which('i686-w64-mingw32-gfortran')
    ar_cmd = which('i686-w64-mingw32-ar')
    size_cmd = which('i686-w64-mingw32-size')
    nsis_cmd = which('makensis')
else:
    cc_cmd = which('x86_64-w64-mingw32-gcc')
    cxx_cmd = which('x86_64-w64-mingw32-g++')
    fc_cmd = which('x86_64-w64-mingw32-gfortran')
    ar_cmd = which('x86_64-w64-mingw32-ar')
    size_cmd = which('x86_64-w64-mingw32-size')
    nsis_cmd = which('makensis')

print("""
Settings: building LAMMPS %s for %s-bit Windows, %s version with %s threading
Build folder     : %s
C compiler       : %s
C++ compiler     : %s
Fortran compiler : %s
Library archiver : %s
""" % (verflag,bitflag,parflag,thrflag,buildpath,cc_cmd,cxx_cmd,fc_cmd,ar_cmd))

# record current working directory and switch to build folder
curpath = fullpath('.')
os.chdir(buildpath)

# download some stuff
print("Downloading sources and tools")
url='http://download.lammps.org/thirdparty'
print("FFMpeg")
geturl("%s/ffmpeg-win%s.exe.gz" % (url,bitflag),"ffmpeg.exe.gz")
print("MPICH2")
geturl("%s/mpich2-win%s-devel.tar.gz" % (url,bitflag),"mpich.tar.gz")
print("gzip")
geturl("%s/gzip.exe.gz" % url,"gzip.exe.gz")
print("OpenCL")
geturl("%s/opencl-win-devel.tar.gz" % url,"opencl.tar.gz")
print("Eigen3")
geturl("%s/eigen-3.3.4.tar.gz" % url,"eigen.tar.gz")
print("Voro++")
geturl("%s/voro++-0.4.6.tar.gz" % url,"voro++.tar.gz")
print("LAMMPS")
geturl("https://github.com/lammps/lammps/archive/%s.tar.gz" % verflag,\
       "lammps.tar.gz")

print("Unpacking")
system("gunzip gzip.exe.gz")
system("gunzip ffmpeg.exe.gz")
system("tar -xzf mpich.tar.gz")
os.remove("mpich.tar.gz")
system("tar -xzf opencl.tar.gz")
os.remove("opencl.tar.gz")
system("tar -xzf eigen.tar.gz")
os.remove("eigen.tar.gz")
system("tar -xzf voro++.tar.gz")
os.remove("voro++.tar.gz")
system("tar -xzf lammps.tar.gz")
os.remove("lammps.tar.gz")

print("Building Voro++")
vorodir = glob.glob('voro++*')[0]
os.chdir(vorodir)
patchfile = "%s/patches/voro++.patch" % curpath
if os.path.exists(patchfile):
    print(system("patch -p0 < %s" % patchfile))
print(system("make -C src CXX=%s CFLAGS='-O3' AR=%s clean voro++" % (cxx_cmd,ar_cmd)))
shutil.move('src/voro++',"%s/voro++.exe" % buildpath)
os.chdir(buildpath)

print("Building LAMMPS libraries")
error("xxx")
# clean up after successful build
os.chdir(curpath)
print("Cleaning up...")
shutil.rmtree(buildpath,True)
print("Done.")
