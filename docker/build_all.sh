#!/bin/bash
docker build -t lammps/lammps:centos7 -f centos7_openmpi_py3/Dockerfile .
docker build -t lammps/lammps:rocky8 -f rocky8_openmpi_py3/Dockerfile .
docker build -t lammps/lammps:ubuntu18.04 -f ubuntu18.04_openmpi_py3/Dockerfile .
docker build -t lammps/lammps:ubuntu20.04 -f ubuntu20.04_openmpi_py3/Dockerfile .
