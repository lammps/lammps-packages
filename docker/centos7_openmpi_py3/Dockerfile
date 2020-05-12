FROM centos:7 as builder
MAINTAINER richard.berger@outlook.com

RUN yum update -y && yum install -y epel-release
RUN yum -y install vim-enhanced \
                   ccache gcc-c++ gcc-gfortran clang gdb valgrind-openmpi \
                   make cmake cmake3 ninja-build patch which file git Lmod \
                   libpng-devel libjpeg-devel openmpi-devel python36-devel \
                   hdf5-devel python36-virtualenv python36-pip \
                   netcdf-devel netcdf-openmpi-devel \
                   python-virtualenv fftw-devel voro++-devel eigen3-devel gsl-devel openblas-devel enchant \
                   blas-devel lapack-devel

ENV PATH=/usr/lib64/openmpi/bin${PATH:+:}${PATH}
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH}

ADD lammps /tmp/lammps

RUN mkdir -p /tmp/lammps/build && \
    cd /tmp/lammps/build && \
    git checkout $VERSION && \
    cmake3 -C /tmp/lammps/cmake/presets/most.cmake \
          -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_CXX_STANDARD=11 \
          -D CMAKE_INSTALL_PREFIX=/usr \
          -D LAMMPS_MACHINE=mpi \
          -D BUILD_TOOLS=on \
          -D BUILD_SHARED_LIBS=on \
          -D Python_EXECUTABLE=/usr/bin/python3 \
          -D PKG_USER-PLUMED=off \
          /tmp/lammps/cmake && \
    make -j 24 && \
    make install && \
    rm -rf /tmp/lammps/build /tmp/lammps/.git

FROM centos:7
MAINTAINER richard.berger@outlook.com
RUN useradd -m lammps
RUN yum update -y && yum install -y epel-release && yum -y install \
                   gdb valgrind-openmpi \
                   patch which file git Lmod \
                   libpng libjpeg openmpi python \
                   hdf5 python-pip \
                   netcdf-openmpi \
                   python-virtualenv fftw voro++ gsl openblas enchant \
                   blas lapack && yum clean -y all
COPY --from=builder /tmp/lammps /home/lammps
COPY --from=builder /usr/bin/lmp_mpi /usr/bin/lmp_mpi
COPY --from=builder /usr/lib64/liblammps_mpi.so.0 /usr/lib64/liblammps_mpi.so.0
COPY --from=builder /usr/lib64/liblammps_mpi.so /usr/lib64/liblammps_mpi.so
COPY --from=builder /usr/include/lammps/ /usr/include/lammps/
COPY --from=builder /usr/lib64/pkgconfig/liblammps_mpi.pc /usr/lib64/pkgconfig/liblammps_mpi.pc
COPY --from=builder /usr/lib64/cmake/LAMMPS/LAMMPS_Targets.cmake /usr/lib64/cmake/LAMMPS/LAMMPS_Targets.cmake
COPY --from=builder /usr/lib64/cmake/LAMMPS/LAMMPS_Targets-release.cmake /usr/lib64/cmake/LAMMPS/LAMMPS_Targets-release.cmake
COPY --from=builder /usr/lib64/cmake/LAMMPS/LAMMPSConfig.cmake /usr/lib64/cmake/LAMMPS/LAMMPSConfig.cmake
COPY --from=builder /usr/lib64/cmake/LAMMPS/LAMMPSConfigVersion.cmake /usr/lib64/cmake/LAMMPS/LAMMPSConfigVersion.cmake
COPY --from=builder /usr/share/man/man1/lmp_mpi.1 /usr/share/man/man1/lmp_mpi.1
COPY --from=builder /usr/bin/binary2txt /usr/bin/binary2txt
COPY --from=builder /usr/bin/msi2lmp /usr/bin/msi2lmp
COPY --from=builder /usr/share/man/man1/msi2lmp.1 /usr/share/man/man1/msi2lmp.1
COPY --from=builder /usr/share/lammps /usr/share/lammps
COPY --from=builder /usr/lib64/python3.6/site-packages/lammps.py /usr/lib64/python3.6/site-packages/lammps.py
RUN chown -R lammps:lammps /home/lammps/

ENV LAMMPS_POTENTIALS=/usr/share/lammps/potentials
ENV PATH=/usr/lib64/openmpi/bin${PATH:+:}${PATH}
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH}
USER lammps
WORKDIR /home/lammps
CMD /usr/bin/lmp_mpi
