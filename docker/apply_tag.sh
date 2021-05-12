#!/bin/bash
TAG=$1
docker tag lammps/lammps:centos7 lammps/lammps:${TAG}_centos7_openmpi_py3
docker tag lammps/lammps:centos8 lammps/lammps:${TAG}_centos8_openmpi_py3
docker tag lammps/lammps:ubuntu18.04 lammps/lammps:${TAG}_ubuntu18.04_openmpi_py3
docker tag lammps/lammps:ubuntu20.04 lammps/lammps:${TAG}_ubuntu20.04_openmpi_py3
