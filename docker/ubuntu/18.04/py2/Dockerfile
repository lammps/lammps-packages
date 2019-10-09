FROM ubuntu:18.04 as builder
MAINTAINER richard.berger@outlook.com

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get -y install software-properties-common --no-install-recommends
RUN add-apt-repository -y ppa:openkim/latest
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        make \
        git \
        gcc \
        g++ \
        cmake \
        gfortran \
        openmpi-bin \
        libopenmpi-dev \
        libfftw3-dev \
        libjpeg-dev \
        libpng-dev \
        python-dev \
        libblas-dev \
        liblapack-dev \
        libeigen3-dev \
        python-virtualenv \
        libkim-api-dev \
        openkim-models

ADD lammps /tmp/lammps/

RUN mkdir -p /tmp/lammps/build && \
    cd /tmp/lammps/build && \
    cmake -C /tmp/lammps/cmake/presets/most.cmake \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr \
          -D LAMMPS_MACHINE=mpi \
          -D BUILD_LIB=on \
          -D BUILD_TOOLS=on \
          -D BUILD_SHARED_LIBS=on \
          -D PKG_USER-PLUMED=off \
          /tmp/lammps/cmake && \
    make -j 24 && \
    make install && \
    rm -rf /tmp/lammps/build /tmp/lammps/.git

FROM ubuntu:18.04
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
        python \
        libblas3 \
        liblapack3 \
        python-virtualenv \
        libkim-api-dev \
        openkim-models \
        libpython2.7 \
        ssh && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m lammps && usermod -aG rdma lammps

COPY --from=builder /tmp/lammps /home/lammps
COPY --from=builder /usr/bin/lmp_mpi /usr/bin/lmp_mpi
COPY --from=builder /usr/lib/x86_64-linux-gnu/liblammps.so.0 /usr/lib/x86_64-linux-gnu/liblammps.so.0
COPY --from=builder /usr/lib/x86_64-linux-gnu/liblammps.so /usr/lib/x86_64-linux-gnu/liblammps.so
COPY --from=builder /usr/include/lammps/ /usr/include/lammps/
COPY --from=builder /usr/lib/x86_64-linux-gnu/pkgconfig/liblammps.pc /usr/lib/x86_64-linux-gnu/pkgconfig/liblammps.pc
COPY --from=builder /usr/share/cmake/Modules/FindLAMMPS.cmake /usr/share/cmake/Modules/FindLAMMPS.cmake
COPY --from=builder /usr/share/man/man1/lmp_mpi.1 /usr/share/man/man1/lmp_mpi.1
COPY --from=builder /usr/bin/binary2txt /usr/bin/binary2txt
COPY --from=builder /usr/bin/msi2lmp /usr/bin/msi2lmp
COPY --from=builder /usr/share/man/man1/msi2lmp.1 /usr/share/man/man1/msi2lmp.1
COPY --from=builder /usr/share/lammps /usr/share/lammps
COPY --from=builder /usr/lib/python2.7/dist-packages/lammps.py /usr/lib/python2.7/dist-packages/lammps.py
RUN chown -R lammps:lammps /home/lammps/

USER lammps
WORKDIR /home/lammps
CMD /usr/bin/lmp_mpi
