FROM lammps/buildenv:centos8 as builder
MAINTAINER richard.berger@outlook.com

ADD lammps /tmp/lammps

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
    cmake3 -C /tmp/lammps/cmake/presets/most.cmake \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr \
          -D CMAKE_INSTALL_SYSCONFDIR=/etc \
          -D LAMMPS_MACHINE=mpi \
          -D LAMMPS_EXCEPTIONS=on \
          -D BUILD_TOOLS=on \
          -D BUILD_SHARED_LIBS=on \
          -D Python_EXECUTABLE=/usr/bin/python3 \
          /tmp/lammps/cmake && \
    make -j 8 && \
    make install && \
    tar czvf /tmp/lammps-mpi.tgz -T install_manifest.txt

FROM centos:8
MAINTAINER richard.berger@outlook.com
RUN useradd -m lammps
RUN dnf update -y && \
    dnf -y install epel-release dnf-utils && \
    dnf config-manager --set-enabled PowerTools && \
    dnf install -y  \
                   blas \
                   fftw \
                   file \
                   gdb \
                   gsl \
                   hdf5 \
                   kim-api-devel \
                   lapack \
                   libasan \
                   libjpeg \
                   libomp \
                   libpng \
                   libyaml \
                   libzstd \
                   mpich \
                   netcdf-cxx \
                   netcdf \
                   netcdf-mpich \
                   netcdf-openmpi \
                   openblas-devel \
                   openkim-models \
                   openmpi \
                   platform-python \
                   platform-python-devel \
                   python3-virtualenv \
                   readline \
                   valgrind \
                   vim-enhanced \
                   voro++ \
                   which \
                   zstd && \
    dnf clean -y all
COPY --from=builder /tmp/lammps-serial.tgz /tmp/
COPY --from=builder /tmp/lammps-mpi.tgz /tmp/
RUN tar -xvzf /tmp/lammps-serial.tgz -C / && rm -f /tmp/lammps-serial.tgz
RUN tar -xvzf /tmp/lammps-mpi.tgz -C / && rm -f /tmp/lammps-mpi.tgz
RUN chown -R lammps:lammps /home/lammps/

ENV LAMMPS_POTENTIALS=/usr/share/lammps/potentials
ENV PATH=/usr/lib64/openmpi/bin${PATH:+:}${PATH}
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH}
USER lammps
WORKDIR /home/lammps
CMD /usr/bin/lmp_mpi
