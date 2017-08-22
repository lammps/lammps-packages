#!/usr/bin/env python

# script to build RPM packages for LAMMPS
# (c) 2017 Axel Kohlmeyer <akohlmey@gmail.com>

from __future__ import print_function
import sys,os,shutil,glob,re,subprocess,tarfile,gzip,time
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

def system(cmd):
    try:
        txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        print("Command '%s' returned non-zero exit status" % e.cmd)
        error(e.output.decode('UTF-8'))
    return txt.decode('UTF-8')

def getsrctar(url):
    tmp = 'tmp.tar.gz'
    geturl(url,tmp)
    tar = tarfile.open(tmp)
    tar.extractall()
    tar.close()
    os.remove(tmp)

def getexe(url,name):
    gzname = name + ".gz"
    geturl(url,gzname)
    with gzip.open(gzname,'rb') as gz_in:
      with open(name,'wb') as f_out:
        shutil.copyfileobj(gz_in,f_out)
    gz_in.close()
    f_out.close()
    os.remove(gzname)

def patch(name):
    patchfile = "%s/patches/%s.patch" % (homedir,name)
    if os.path.exists(patchfile):
        print("Patching:",name,system("patch -p0 < %s" % patchfile))

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

rpmbuildflags  = r"-D'%_topdir " + builddir + "' "
rpmbuildflags += "--macros=" + builddir + "/pkgmacros "

txt = system("rpmbuild -bb " + rpmbuildflags + "SPECS/lammps-fedora-repo.spec")
print(txt)

txt=system(r"rpmsign --addsign -D'%_gpg_name LAMMPS Packages <packages@lammps.org>' RPMS/lammps-fedora-repo-2-2.noarch.rpm")
print(txt)




