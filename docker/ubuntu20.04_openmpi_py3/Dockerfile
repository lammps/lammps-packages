FROM lammps/buildenv:ubuntu20.04 as builder
MAINTAINER richard.berger@outlook.com

ADD lammps /tmp/lammps/

RUN mkdir -p /tmp/lammps/build-serial && \
    cd /tmp/lammps/build-serial && \
    cmake -C /tmp/lammps/cmake/presets/most.cmake \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr \
          -D CMAKE_INSTALL_SYSCONFDIR=/etc \
          -D LAMMPS_MACHINE=serial \
          -D BUILD_MPI=off \
          -D BUILD_LAMMPS_SHELL=on \
          -D LAMMPS_EXCEPTIONS=on \
          -D BUILD_TOOLS=on \
          -D BUILD_SHARED_LIBS=on \
          -D Python_EXECUTABLE=/usr/bin/python3 \
          /tmp/lammps/cmake && \
    make -j 8 && \
    make install && \
    tar czvf /tmp/lammps-serial.tgz -T install_manifest.txt

RUN mkdir -p /tmp/lammps/build-openmpi && \
    cd /tmp/lammps/build-openmpi && \
    cmake -C /tmp/lammps/cmake/presets/most.cmake \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr \
          -D CMAKE_INSTALL_SYSCONFDIR=/etc \
          -D LAMMPS_MACHINE=mpi \
          -D LAMMPS_EXCEPTIONS=on \
          -D BUILD_TOOLS=on \
          -D BUILD_SHARED_LIBS=on \
          -D PKG_USER-PLUMED=off \
          -D Python_EXECUTABLE=/usr/bin/python3 \
          /tmp/lammps/cmake && \
    make -j 8 && \
    make install && \
    tar czvf /tmp/lammps-mpi.tgz -T install_manifest.txt

FROM ubuntu:20.04
MAINTAINER richard.berger@outlook.com
ENV DEBIAN_FRONTEND noninteractive
ENV LAMMPS_POTENTIALS=/usr/share/lammps/potentials
ENV MSI2LMP_LIBRARY=/usr/share/lammps/frc_files

RUN apt-get update -y
RUN apt-get -y install software-properties-common --no-install-recommends
RUN add-apt-repository -y ppa:openkim/latest
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        openmpi-bin \
        libfftw3-bin \
        libjpeg8 \
        libpng-tools \
        python3 \
        liblapack3 \
        python3-venv \
        libkim-api-dev \
        openkim-models \
        libpython3.6 \
        hdf5-tools \
        less \
        libblas3 \
        libfftw3 \
        libgsl \
        libhdf5-serial \
        libhwloc \
        libjpeg \
        liblapack \
        libnetcdf \
        libomp \
        libopenblas \
        libnuma \
        libpng \
        libproj \
        libreadline \
        libvtk6 \
        libyaml \
        libzstd \
        mpi-default-bin \
        python3-dev \
        python3-pip \
        python3-pkg-resources \
        python3-setuptools \
        rsync \
        ssh \
        vim-nox \
        voro++ \
        valgrind \
        gdb \
        zstd \
        libkim-api-dev \
        openkim-models && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m lammps && usermod -aG rdma lammps

COPY --from=builder /tmp/lammps-serial.tgz /tmp/
COPY --from=builder /tmp/lammps-mpi.tgz /tmp/
RUN tar -xvzf /tmp/lammps-serial.tgz -C / && rm -f /tmp/lammps-serial.tgz
RUN tar -xvzf /tmp/lammps-mpi.tgz -C / && rm -f /tmp/lammps-mpi.tgz
RUN chown -R lammps:lammps /home/lammps/

USER lammps
WORKDIR /home/lammps
CMD /usr/bin/lmp_mpi
