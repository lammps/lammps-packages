#!/usr/bin/env python

# script to build repository RPM packages for LAMMPS
# (c) 2017 Axel Kohlmeyer <akohlmey@gmail.com>

from __future__ import print_function
import sys,os,shutil,glob,re,subprocess,tarfile,gzip,time

# helper functions

def error(str=None):
    if not str: print(helpmsg)
    else: print(sys.argv[0],"ERROR:",str)
    sys.exit()

def system(cmd):
    try:
        txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        print("Command '%s' returned non-zero exit status" % e.cmd)
        error(e.output.decode('UTF-8'))
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

# record location and name of python script
homedir, exename = os.path.split(fullpath(sys.argv[0]))
builddir = fullpath('.')

rpmbuildflags  = r"-D'%_topdir " + homedir + "' "
rpmbuildflags += r"-D'%packager LAMMPS Packages <packages@lammps.org>' "
rpmbuildflags += "--macros=" + builddir + "/pkgmacros "

txt = system("rpmbuild -ba " + rpmbuildflags + "SPECS/lammps-fedora-repo.spec")
print(txt)

txt=system(r"rpmsign --addsign -D'%_gpg_name LAMMPS Packages <packages@lammps.org>' RPMS/lammps-fedora-repo-2-2.noarch.rpm")
print(txt)




