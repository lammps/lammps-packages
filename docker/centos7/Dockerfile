FROM centos:7 as builder

RUN yum update -y && yum install -y epel-release
RUN yum install -y make gcc gcc-c++ gcc-gfortran cmake3 git
RUN yum install -y openmpi-devel libpng-devel libjpeg-devel openmpi-devel fftw-devel zlib-devel python-devel blas-devel lapack-devel hdf5-devel netcdf-devel eigen3-devel

ENV PATH=/usr/lib64/openmpi/bin${PATH:+:}${PATH}
ENV LD_LIBRARY_PATH=/usr/lib64/openmpi/lib${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH}

COPY lammps /tmp/lammps
RUN mkdir build

WORKDIR /tmp/build
RUN cmake3 -C /tmp/lammps/cmake/presets/all_on.cmake \
         -D CMAKE_BUILD_TYPE=Release \
         -D CMAKE_INSTALL_PREFIX=/usr \
         -D DOWNLOAD_VORO=on \
         -D PKG_MSCG=off \
         -D PKG_USER-LB=off \
         -D PKG_LATTE=off \
         -D PKG_KIM=off \
         -D PKG_USER-QUIP=off \
         -D PKG_USER-QMMM=off \
         -D PKG_USER-H5MD=off \
         -D PKG_USER-VTK=off \
         -D PKG_GPU=off \
         -D PKG_KOKKOS=off \
         -D PKG_USER-INTEL=off \
         -D PKG_USER-OMP=on \
         -D PKG_MPIIO=on \
         -D BUILD_MPI=on \
         -D BUILD_LIB=on \
         -D BUILD_SHARED_LIBS=on \
         -D BUILD_OMP=off \
         /tmp/lammps/cmake
RUN make -j8 install

FROM centos:7
RUN useradd -m lammps
RUN yum update -y && yum install -y epel-release && yum install -y fftw libjpeg libpng python blas lapack hdf5 openmpi netcdf && yum clean -y all
COPY --from=builder /usr/bin/lmp /usr/bin/lmp
COPY --from=builder /usr/share/lammps /usr/share/lammps
COPY --from=builder /usr/lib64/python2.7/site-packages/lammps.py /usr/lib64/python2.7/site-packages/lammps.py
COPY --from=builder /usr/lib64/liblammps.so.0 /usr/lib64/liblammps.so.0
COPY --from=builder /usr/lib64/liblammps.so /usr/lib64/liblammps.so
COPY --from=builder /usr/include/lammps/library.h /usr/include/lammps/library.h
COPY --from=builder /usr/lib64/pkgconfig/liblammps.pc /usr/lib64/pkgconfig/liblammps.pc
COPY --from=builder /usr/share/cmake/Modules/FindLAMMPS.cmake /usr/share/cmake/Modules/FindLAMMPS.cmake
COPY --from=builder /usr/share/man/man1/lmp.1 /usr/share/man/man1/lmp.1
COPY --from=builder /tmp/lammps/examples /home/lammps/examples
COPY --from=builder /tmp/lammps/bench /home/lammps/bench
COPY --from=builder /tmp/lammps/LICENSE /home/lammps/LICENSE

ENV LD_LIBRARY_PATH /usr/lib64/openmpi/lib
ENV LAMMPS_POTENTIALS /usr/share/lammps/potentials
USER lammps
WORKDIR /home/lammps
CMD /bin/bash
