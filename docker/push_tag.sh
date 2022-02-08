#!/bin/bash
TAG=$1
docker push lammps/lammps:${TAG}_centos7_openmpi_py3
docker push lammps/lammps:${TAG}_rockylinux8_openmpi_py3
docker push lammps/lammps:${TAG}_ubuntu18.04_openmpi_py3
docker push lammps/lammps:${TAG}_ubuntu20.04_openmpi_py3
