#!/usr/bin/env python

# Script to build windows installer packages for LAMMPS
# (c) 2017 Axel Kohlmeyer <akohlmey@gmail.com>

from __future__ import print_function
import sys,os,shutil,glob,re,subprocess,tarfile,gzip,time,inspect
try: from urllib.request import urlretrieve as geturl
except: from urllib import urlretrieve as geturl

try:
    import multiprocessing
    numcpus = multiprocessing.cpu_count()
except:
    numcpus = 1

# helper functions

def error(str=None):
    if not str: print(helpmsg)
    else: print(sys.argv[0],"ERROR:",str)
    sys.exit()

def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))

def getexe(url,name):
    gzname = name + ".gz"
    geturl(url,gzname)
    with gzip.open(gzname,'rb') as gz_in:
      with open(name,'wb') as f_out:
        shutil.copyfileobj(gz_in,f_out)
    gz_in.close()
    f_out.close()
    os.remove(gzname)

def system(cmd):
    try:
        txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        print("Command '%s' returned non-zero exit status" % e.cmd)
        error(e.output.decode('UTF-8'))
    return txt.decode('UTF-8')

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

# record location and name of python script
homedir, exename = os.path.split(os.path.abspath(inspect.getsourcefile(lambda:0)))

# default settings help message and default settings

bitflag = '64'
parflag = 'no'
thrflag = 'omp'
revflag = 'stable'
verbose = False
gitdir  = os.path.join(homedir,"lammps")

helpmsg = """
Usage: python %s -b <bits> -j <cpus> -p <mpi> -t <thread> -r <rev> -v <yes|no> -g <folder>

Flags (all flags are optional, defaults listed below):
  -b : select Windows variant (default value: %s)
    -b 32       : build for 32-bit Windows
    -b 64       : build for 64-bit Windows
  -j : set number of CPUs for parallel make (default value: %d)
    -j <num>    : set to any reasonable number or 1 for serial make
  -p : select message passing parallel build (default value: %s)
    -p mpi      : build an MPI parallel version with MPICH2 v1.4.1p1
    -p no       : build a serial version using MPI STUBS library
  -t : select thread support (default value: %s)
    -t omp      : build with threads via OpenMP enabled
    -t no       : build with thread support disabled
  -r : select LAMMPS source revision to build (default value: %s)
    -r stable   : download and build the latest stable LAMMPS version
    -r unstable : download and build the latest patch release LAMMPS version
    -r master   : download and build the latest development snapshot
    -r patch_<date> : download and build a specific patch release
    -r <sha256> : download and build a specific snapshot version
  -v : select output verbosity
    -v yes      : print progress messages and output of make commands
    -v no       : print only progress messages
  -g : select folder with git checkout of LAMMPS sources
    -g <folder> : use LAMMPS checkout in <folder>  (default value: %s)

Example:
  python %s -r unstable -t omp -p mpi
""" % (exename,bitflag,numcpus,parflag,thrflag,revflag,gitdir,exename)

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
    elif argv[i] == '-j':
        numcpus = int(argv[i+1])
    elif argv[i] == '-p':
        parflag = argv[i+1]
    elif argv[i] == '-t':
        thrflag = argv[i+1]
    elif argv[i] == '-r':
        revflag = argv[i+1]
    elif argv[i] == '-v':
        if argv[i+1] in ['yes','Yes','Y','y','on','1','True','true']:
            verbose = True
        elif argv[i+1] in ['no','No','N','n','off','0','False','false']:
            verbose = False
        else:
            error("\nUnknown verbose keyword:",argv[i+1])
    elif argv[i] == '-g':
        gitdir = fullpath(argv[i+1])
    else:
        print("\nUnknown flag:",argv[i])
        error()
    i+=2

# checks
if bitflag != '32' and bitflag != '64':
    error("Unsupported bitness flag %s" % bitflag)
if parflag != 'no' and parflag != 'mpi':
    error("Unsupported parallel flag %s" % parflag)
if thrflag != 'no' and thrflag != 'omp':
    error("Unsupported threading flag %s" % thrflag)

# test for valid revision name format: branch names, release tags, or commit hashes
rev1 = re.compile("^(stable|unstable|master)$")
rev2 = re.compile(r"^(patch|stable)_\d+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{4}$")
rev3 = re.compile(r"^[a-f0-9]{40}$")
if not rev1.match(revflag) and not rev2.match(revflag) and not rev3.match(revflag):
    error("Unsupported revision flag %s" % revflag)

# create working directory
builddir = os.path.join(fullpath('.'),"tmp-%s-%s-%s-%s" % (bitflag,parflag,thrflag,revflag))
shutil.rmtree(builddir,True)
try:
    os.mkdir(builddir)
except:
    error("Cannot create temporary build folder: %s" % builddir)

# check for prerequisites and set up build environment
if bitflag == '32':
    cc_cmd = which('i686-w64-mingw32-gcc')
    cxx_cmd = which('i686-w64-mingw32-g++')
    fc_cmd = which('i686-w64-mingw32-gfortran')
    ar_cmd = which('i686-w64-mingw32-ar')
    size_cmd = which('i686-w64-mingw32-size')
    nsis_cmd = which('makensis')
    lmp_size = 'smallsmall'
else:
    cc_cmd = which('x86_64-w64-mingw32-gcc')
    cxx_cmd = which('x86_64-w64-mingw32-g++')
    fc_cmd = which('x86_64-w64-mingw32-gfortran')
    ar_cmd = which('x86_64-w64-mingw32-ar')
    size_cmd = which('x86_64-w64-mingw32-size')
    nsis_cmd = which('makensis')
    lmp_size = 'smallbig'

print("""
Settings: building LAMMPS revision %s for %s-bit Windows
Message passing  : %s
Multi-threading  : %s
Home folder      : %s
Source folder    : %s
Build folder     : %s
C compiler       : %s
C++ compiler     : %s
Fortran compiler : %s
Library archiver : %s
""" % (revflag,bitflag,parflag,thrflag,homedir,gitdir,builddir,cc_cmd,cxx_cmd,fc_cmd,ar_cmd))

# create/update git checkout
if not os.path.exists(gitdir):
    txt = system("git clone https://github.com/lammps/lammps.git %s" % gitdir)
    if verbose: print(txt)

os.chdir(gitdir)
txt = system("git fetch origin")
if verbose: print(txt)
txt = system("git checkout %s" % revflag)
if verbose: print(txt)
if revflag == "master" or revflag == "stable" or revflag == "unstable":
    txt = system("git pull")
    if verbose: print(txt)

# switch to build folder
os.chdir(builddir)

# download what is not automatically downloaded by CMake
print("Downloading third party tools")
url='http://download.lammps.org/thirdparty'
print("FFMpeg")
getexe("%s/ffmpeg-win%s.exe.gz" % (url,bitflag),"ffmpeg.exe")
print("gzip")
getexe("%s/gzip.exe.gz" % url,"gzip.exe")

if parflag == "mpi":
    mpiflag = "on"
else:
    mpiflag = "off"

if thrflag == "omp":
    ompflag = "on"
else:
    ompflag = "off"

print("Configuring build with CMake")
cmd = "mingw%s-cmake -G Ninja -D CMAKE_BUILD_TYPE=Release" % bitflag
cmd += " -D ADD_PKG_CONFIG_PATH=%s/mingw%s-pkgconfig" % (homedir,bitflag)
cmd += " -C %s/mingw%s-pkgconfig/addpkg.cmake" % (homedir,bitflag)
cmd += " -C %s/cmake/presets/mingw-cross.cmake %s/cmake" % (gitdir,gitdir)
cmd += " -DBUILD_SHARED_LIBS=on -DBUILD_MPI=%s -DBUILD_OPENMP=%s" % (mpiflag,ompflag)
cmd += " -DWITH_GZIP=on -DWITH_FFMPEG=on -DLAMMPS_EXCEPTIONS=on"
cmd += " -DINTEL_LRT_MODE=c++11 -DBUILD_LAMMPS_SHELL=on"

print("Running: ",cmd)
txt = system(cmd)
if verbose: print(txt)

print("Compiling")
system("ninja")
print("Done")

print("Building PDF manual")
os.chdir(os.path.join(gitdir,"doc"))
txt = system("make pdf")
if verbose: print(txt)
shutil.move("Manual.pdf",os.path.join(builddir,"LAMMPS-Manual.pdf"))
print("Done")

# switch back to build folder and copy/process files for inclusion in installer
print("Collect and convert files for the Installer package")
os.chdir(builddir)
shutil.copytree(os.path.join(gitdir,"examples"),os.path.join(builddir,"examples"),symlinks=False)
shutil.copytree(os.path.join(gitdir,"bench"),os.path.join(builddir,"bench"),symlinks=False)
shutil.copytree(os.path.join(gitdir,"tools"),os.path.join(builddir,"tools"),symlinks=False)
shutil.copytree(os.path.join(gitdir,"python"),os.path.join(builddir,"python"),symlinks=False)
shutil.copytree(os.path.join(gitdir,"potentials"),os.path.join(builddir,"potentials"),symlinks=False)
shutil.copy(os.path.join(gitdir,"README"),os.path.join(builddir,"README.txt"))
shutil.copy(os.path.join(gitdir,"LICENSE"),os.path.join(builddir,"LICENSE.txt"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","colvars-refman-lammps.pdf"),os.path.join(builddir,"Colvars-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"tools","createatoms","Manual.pdf"),os.path.join(builddir,"CreateAtoms-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","kspace.pdf"),os.path.join(builddir,"Kspace-Extra-Info.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","pair_gayberne_extra.pdf"),os.path.join(builddir,"PairGayBerne-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","pair_resquared_extra.pdf"),os.path.join(builddir,"PairReSquared-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","PDLammps_overview.pdf"),os.path.join(builddir,"PDLAMMPS-Overview.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","PDLammps_EPS.pdf"),os.path.join(builddir,"PDLAMMPS-EPS.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","PDLammps_VES.pdf"),os.path.join(builddir,"PDLAMMPS-VES.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","SPH_LAMMPS_userguide.pdf"),os.path.join(builddir,"SPH-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","SMD_LAMMPS_userguide.pdf"),os.path.join(builddir,"SMD-Manual.pdf"))
shutil.copy(os.path.join(gitdir,"doc","src","PDF","USER-CGDNA.pdf"),os.path.join(builddir,"CGDNA-Manual.pdf"))

# prune outdated inputs, too large files, or examples of packages we don't bundle
for d in ['accelerate','kim','mscg','USER/quip','USER/vtk']:
    shutil.rmtree(os.path.join("examples",d),True)
for d in ['FERMI','KEPLER']:
    shutil.rmtree(os.path.join("bench",d),True)
shutil.rmtree("tools/msi2lmp/test",True)
os.remove("python/install.py")
os.remove("potentials/C_10_10.mesocnt")
os.remove("potentials/TABTP_10_10.mesont")
os.remove("examples/USER/mesont/C_10_10.mesocnt")
os.remove("examples/USER/mesont/TABTP_10_10.mesont")

# convert text files to CR-LF conventions
txt = system("unix2dos LICENSE.txt README.txt tools/msi2lmp/README")
if verbose: print(txt)
txt = system("find bench examples potentials python tools/msi2lmp/frc_files -type f -print | xargs unix2dos")
if verbose: print(txt)
# mass rename README to README.txt
txt = system('for f in $(find tools bench examples potentials python -name README -print); do  mv -v $f $f.txt; done')
if verbose: print(txt)
print("Done")

print("Configuring and building installer")
os.chdir(builddir)
shutil.move("OpenCL/lib_win%s/libOpenCL.dll" % bitflag,builddir)
shutil.copy(os.path.join(homedir,"installer","lammps.nsis"),builddir)
shutil.copytree(os.path.join(homedir,"installer","envvar"),os.path.join(builddir,"envvar"),symlinks=False)

# define version flag of the installer:
# - use current timestamp, when pulling from master (for daily builds)
# - parse version from src/version.h when pulling from stable, unstable, or specific tag
# - otherwise use revflag, i.e. the commit hash
version = revflag
if revflag == 'stable' or revflag == 'unstable' or rev2.match(revflag):
  with open(os.path.join(gitdir,"src","version.h"),'r') as v_file:
    verexp = re.compile(r'^.*"(\w+) (\w+) (\w+)".*$')
    vertxt = v_file.readline()
    verseq = verexp.match(vertxt).groups()
    version = "".join(verseq)
elif revflag == 'master':
    version = time.strftime('%Y-%m-%d')

if bitflag == '32':
    mingwdir = '/usr/i686-w64-mingw32/sys-root/mingw/bin/'
    libgcc = 'libgcc_s_dw2-1.dll'
elif bitflag == '64':
    mingwdir = '/usr/x86_64-w64-mingw32/sys-root/mingw/bin/'
    libgcc = 'libgcc_s_seh-1.dll'

if parflag == 'mpi':
    shutil.move("lmp.exe","lmp_mpi.exe")
    txt = system("makensis -DMINGW=%s -DVERSION=%s-MPI -DBIT=%s -DLIBGCC=%s -DLMPREV=%s lammps.nsis" % (mingwdir,version,bitflag,libgcc,revflag))
    if verbose: print(txt)
else:
    shutil.move("lmp.exe","lmp_serial.exe")
    txt = system("makensis -DMINGW=%s -DVERSION=%s -DBIT=%s -DLIBGCC=%s -DLMPREV=%s lammps.nsis" % (mingwdir,version,bitflag,libgcc,revflag))
    if verbose: print(txt)

# clean up after successful build
os.chdir('..')

print("Cleaning up...")
shutil.rmtree(builddir,True)
print("Done.")

