%global git 1
%global commit ab51c1bd3d2ca8c54d4829d01e5804e4d587b514
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global cmake_blas_flags -DBLA_VENDOR=FlexiBLAS
%else
%global blaslib openblas
%global blasvar o
%global cmake_blas_flags -DBLAS_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so -DLAPACK_LIBRARIES=%{_libdir}/lib%{blaslib}%{blasvar}.so
%endif

Name:           lammps
%if %{git}
Version:        20210929^20210929%{shortcommit}
%else
Version:        20210929
%endif
%global         uversion %(v=%{version}; \
                  months=( "" Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec ); \
                  d=${v:6:2}; \
                  m=${v:4:2};
                  y=${v:0:4};
                  echo patch_${d#0}${months[${m#0}]}${y})
Release:        1%{?dist}
Summary:        Molecular Dynamics Simulator
License:        GPLv2
Url:            https://lammps.sandia.gov
%if %{git}
Source0:        https://github.com/lammps/lammps/archive/%{commit}/lammps-%{commit}.tar.gz#/%{name}-%{uversion}.tar.gz
%else
Source0:        https://github.com/lammps/lammps/archive/%{uversion}.tar.gz#/%{name}-%{uversion}.tar.gz
%endif
Source1:        https://github.com/google/googletest/archive/release-1.10.0.tar.gz
Source2:        https://pyyaml.org/download/libyaml/yaml-0.2.5.tar.gz
Source3:        https://download.lammps.org/thirdparty/opencl-loader-2021.09.18.tar.gz
Patch0:         https://github.com/lammps/lammps/commit/01fb33cb5dfbfb028840c4597499332e36f8695f.patch
Patch1:         https://github.com/lammps/lammps/commit/211df8b7b04fa1bce8e2ba4b151d73801b6af632.patch
Patch2:         https://github.com/lammps/lammps/pull/2986.patch
BuildRequires:  fftw-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-fortran
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  openmpi-devel
BuildRequires:  python%{python3_pkgversion}-mpi4py-openmpi
BuildRequires:  mpich-devel
BuildRequires:  python%{python3_pkgversion}-mpi4py-mpich
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  fftw3-devel
BuildRequires:  zlib-devel
BuildRequires:  gsl-devel
BuildRequires:  voro++-devel
BuildRequires:  %{blaslib}-devel
BuildRequires:  hdf5-devel
BuildRequires:  kim-api-devel
BuildRequires:  kim-api-examples
BuildRequires:  cmake3 >= 3.1
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
BuildRequires:  tbb-devel
BuildRequires:  readline-devel
%if 0%{?fedora} >= 33
%ifnarch i686 armv7hl
%global         with_kokkos 1
# kokkos needs a lot of memory
%global         _smp_mflags -j1
BuildRequires:  kokkos-devel >= 3.2
%endif
%endif
Requires:       %{name}-data

%global lammps_desc \
LAMMPS is a classical molecular dynamics code, and an acronym for Large-scale \
Atomic/Molecular Massively Parallel Simulator.\
\
LAMMPS has potentials for soft materials (biomolecules, polymers) and \
solid-state materials (metals, semiconductors) and coarse-grained or \
mesoscopic systems. It can be used to model atoms or, more generically, as a \
parallel particle simulator at the atomic, meso, or continuum scale. \
\
LAMMPS runs on single processors or in parallel using message-passing \
techniques and a spatial-decomposition of the simulation domain. The code is \
designed to be easy to modify or extend with new functionality.

%description
%{lammps_desc}

%package openmpi
Summary:        LAMMPS Open MPI binaries and libraries
Requires:       openmpi
Requires:       %{name}-data

%description openmpi
%{lammps_desc}

This package contains LAMMPS Open MPI binaries and libraries

%package mpich
Summary:        LAMMPS MPICH binaries and libraries
Requires:       mpich
Requires:       %{name}-data

%description mpich
%{lammps_desc}

This package contains LAMMPS MPICH binaries and libraries

%package -n python%{python3_pkgversion}-%{name}
Summary:        LAMMPS Python interface
Requires:       python%{python3_pkgversion}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
%{lammps_desc}

This package contains LAMMPS Python interface

%package headers
Summary:        Development headers for LAMMPS

%description headers
%{lammps_desc}

This package contains development headers for LAMMPS.

%package devel
Summary:        Development libraries for LAMMPS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-headers%{?_isa} = %{version}-%{release}

%description devel
%{lammps_desc}

This package contains development libraries for serial LAMMPS.

%package mpich-devel
Summary:        Development libraries for MPICH LAMMPS
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}
Requires:       %{name}-headers%{?_isa} = %{version}-%{release}

%description mpich-devel
%{lammps_desc}

This package contains development headers and libraries for MPICH LAMMPS.

%package openmpi-devel
Summary:        Development libraries for Open MPI LAMMPS
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires:       %{name}-headers%{?_isa} = %{version}-%{release}

%description openmpi-devel
%{lammps_desc}

This package contains development libraries for Open MPI LAMMPS.

%if 0%{?el7}
%package openmpi3
Summary:        LAMMPS Open MPI 3 binaries and libraries
BuildRequires:  openmpi3-devel
Requires:       openmpi3
Requires:       %{name}-data

%description openmpi3
%{lammps_desc}

This package contains LAMMPS Open MPI 3 binaries and libraries

%package openmpi3-devel
Summary:        Development libraries for Open MPI 3 LAMMPS
Requires:       %{name}-openmpi3%{?_isa} = %{version}-%{release}
Requires:       %{name}-headers%{?_isa} = %{version}-%{release}

%description openmpi3-devel
%{lammps_desc}

This package contains development libraries for Open MPI 3 LAMMPS.
%endif

%package data
Summary:        Data files for LAMMPS
BuildArch:      noarch

%description data
%{lammps_desc}

This package contains data files for LAMMPS.

%prep
%setup -q -n %{name}-%{uversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%global _vpath_srcdir cmake
%global _vpath_builddir ${mpi:-serial}
. /etc/profile.d/modules.sh
for mpi in '' mpich openmpi %{?el7:openmpi3} ; do
  test -n "${mpi}" && module load mpi/${mpi}-%{_arch}
  #python wrapper isn't mpi specific
  %{cmake3} \
  -C cmake/presets/all_on.cmake \
  -C cmake/presets/nolib.cmake \
  %{cmake_blas_flags} \
  -DCMAKE_TUNE_FLAGS='' \
  -DCMAKE_CUSTOM_LINKER="default" \
  -DPKG_PYTHON=ON \
  -DPKG_VORONOI=ON \
  -DPKG_ATC=ON \
  -DPKG_H5MD=ON \
  %{?with_kokkos:-DPKG_KOKKOS=ON -DEXTERNAL_KOKKOS=ON} \
  -DPKG_KIM=ON \
  -DENABLE_TESTING=ON \
  -DGTEST_URL=%{S:1} \
  -DYAML_URL=%{S:2} \
  -DOPENCL_LOADER_URL=%{S:3} \
  -DPYTHON_INSTDIR=%{python3_sitelib} \
  -DCMAKE_INSTALL_SYSCONFDIR=/etc \
  -DPKG_GPU=ON -DGPU_API=OpenCL \
  -DBUILD_OMP=ON \
  -DFFT=FFTW3 \
%ifnarch x86_64 %x86
  -DPKG_INTEL=OFF \
%endif
    -DCMAKE_INSTALL_BINDIR=${MPI_BIN:-%{_bindir}} -DCMAKE_INSTALL_LIBDIR=${MPI_LIB:-%{_libdir}} -DLAMMPS_MACHINE="${MPI_SUFFIX#_}" -DLAMMPS_LIB_SUFFIX="${MPI_SUFFIX#_}" -DCMAKE_INSTALL_MANDIR=${MPI_MAN:-%{_mandir}} \
    ${mpi:+-DBUILD_MPI=ON -DPKG_MPIIO=ON -DCMAKE_EXE_LINKER_FLAGS="%{__global_ldflags} -Wl,-rpath -Wl,${MPI_LIB} -Wl,--enable-new-dtags" -DCMAKE_SHARED_LINKER_FLAGS="%{__global_ldflags} -Wl,-rpath -Wl,${MPI_LIB} -Wl,--enable-new-dtags" $(test "$mpi" != openmpi || echo "-DMPIEXEC_PREFLAGS=--oversubscribe") } \
    $(test -z "${mpi}" && echo -DBUILD_MPI=OFF -DPKG_MPIIO=OFF -DBUILD_LAMMPS_SHELL=ON -DBUILD_TOOLS=ON)
  %cmake_build
  test -n "${mpi}" && module unload mpi/${mpi}-%{_arch}
done

%install
. /etc/profile.d/modules.sh
for mpi in '' mpich openmpi %{?el7:openmpi3} ; do
  %cmake_install
done

%check
. /etc/profile.d/modules.sh
for mpi in '' mpich openmpi %{?el7:openmpi3} ; do
  old_PYTHONPATH="${PYTHONPATH}"
  test -n "${mpi}" && module load mpi/${mpi}-%{_arch} && export PYTHONPATH="${MPI_PYTHON3_SITEARCH}:${PYTHONPATH}"
  %ctest --label-exclude force-style
  test -n "${mpi}" && module unload mpi/${mpi}-%{_arch} && export PYTHONPATH="${old_PYTHONPATH}"
done

%ldconfig_scriptlets

%files
%doc README
%license LICENSE
%{_bindir}/lmp
%{_bindir}/lammps-shell
%{_mandir}/man1/lmp.*
%{_libdir}/liblammps.so.*
%{_bindir}/msi2lmp
%{_mandir}/man1/msi2lmp.*
%{_bindir}/binary2txt
%{_bindir}/chain.x
%{_bindir}/micelle2d.x

%files devel
%{_libdir}/liblammps.so
%{_libdir}/pkgconfig/liblammps.pc
%{_libdir}/cmake/LAMMPS

%files openmpi-devel
%{_libdir}/openmpi*/lib/liblammps_openmpi.so
%{_libdir}/openmpi*/lib/pkgconfig/liblammps_openmpi.pc
%{_libdir}/openmpi*/lib/cmake/LAMMPS

%files mpich-devel
%{_libdir}/mpich*/lib/liblammps_mpich.so
%{_libdir}/mpich*/lib/pkgconfig/liblammps_mpich.pc
%{_libdir}/mpich*/lib/cmake/LAMMPS

%files -n python%{python3_pkgversion}-%{name}
%{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}-*.egg-info

%files headers
%license LICENSE
%{_includedir}/%{name}/

%files openmpi
%license LICENSE
%{_libdir}/openmpi*/bin/lmp_openmpi
%{_mandir}/openmpi*/man1/lmp_openmpi.*
%{_libdir}/openmpi*/lib/liblammps_openmpi.so.*

%if 0%{?el7}
%files openmpi3
%license LICENSE
%{_libdir}/openmpi3*/bin/lmp_openmpi3
%{_mandir}/openmpi3*/man1/lmp_openmpi3.*
%{_libdir}/openmpi3*/lib/liblammps_openmpi3.so.*

%files openmpi3-devel
%{_libdir}/openmpi3*/lib/liblammps_openmpi3.so
%{_libdir}/openmpi3*/lib/pkgconfig/liblammps_openmpi3.pc
%{_libdir}/openmpi3/lib/cmake/LAMMPS
%endif

%files mpich
%license LICENSE
%{_libdir}/mpich*/bin/lmp_mpich
%{_mandir}/mpich*/man1/lmp_mpich.*
%{_libdir}/mpich*/lib/liblammps_mpich.so.*

%files data
%license LICENSE
%{_datadir}/%{name}
%{_datadir}/icons/*
%{_datadir}/applications/lammps-shell.desktop
%config %{_sysconfdir}/profile.d/lammps.*

%changelog
* Thu Sep 30 2021 Christoph Junghans <junghans@votca.org> - 20210929-1
- Version bump to 20210929 (bug #2009115)

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 20201029-13
- Rebuild for hdf5 1.10.7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201029-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 20201029-11
- Properly set BLA_VENDOR to FlexiBLAS for cmake >= 3.19

* Tue Jun 22 2021 Christoph Junghans <junghans@votca.org> - 20201029-10
- Rebuild for kokkos

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 20201029-9
- Rebuilt for Python 3.10

* Sun May 02 2021 Christoph Junghans <junghans@votca.org> - 20201029-8
- Rebuild for kokkos-3.4.00

* Sat May 01 2021 Christoph Junghans <junghans@votca.org> - 20201029-7
- Rebuild for kokkos-3.4.00

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201029-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Christoph Junghans <junghans@votca.org> - 20201029-5
- Rebuild for kokkos-3.3.01

* Sat Dec 19 17:31:31 MST 2020 Christoph Junghans <junghans@votca.org> - 20201029-4
- Rebuild for kokkos-3.3.00

* Sat Nov 28 09:49:16 MST 2020 Christoph Junghans <junghans@votca.org> - 20201029-3
- fix build with kokkos on f33

* Sat Nov 28 07:04:04 MST 2020 Christoph Junghans <junghans@votca.org> - 20201029-2
- Rebuild for kokkos-3.2.01

* Thu Oct 29 18:37:27 MDT 2020 Christoph Junghans <junghans@votca.org> - 20201029-1
- Version bump to v20201029 (#1810251)

* Mon Sep 21 2020 Christoph Junghans <junghans@votca.org> - 20200918-1
- Version bump to v20200918

* Tue Aug 25 2020 Christoph Junghans <junghans@votca.org> - 20200821-2
- Rebuild for kokkos-3.2

* Fri Aug 21 2020 Christoph Junghans <junghans@votca.org> - 20200821-1
- Version bump to 20200821, testing next stable release

* Thu Aug 13 2020 Iñaki Úcar <iucar@fedoraproject.org> - 20200630-5
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Tue Aug 04 2020 Christoph Junghans <junghans@votca.org> - 20200630-4
- Fix out-of-source build on F33 (bug#1863958)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200630-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200630-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Christoph Junghans <junghans@votca.org> - 20200630-1
- Version bump to 20200630

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 20200505-4
- Rebuild for hdf5 1.10.6

* Sun Jun 14 2020 Christoph Junghans <junghans@votca.org> - 20200505-3
- disable march=native optimization by setting empty CMAKE_TUNE_FLAGS

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 20200505-2
- Rebuilt for Python 3.9

* Tue May 05 2020 Christoph Junghans <junghans@votca.org> - 20200505-1
- Version to 20200505 to fix bug #1830677

* Wed Mar 04 2020 Christoph Junghans <junghans@votca.org> - 20200303-1
- Version bump to 20200303 (bug #1810251) and enable kokkos

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190807-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 20190807-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 20190807-2
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Christoph Junghans <junghans@votca.org> - 20190807-1
- Version bump to 20190807

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190605-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Dave Love <loveshack@fedoraproject.org> - 20190605-4
- Add openmpi3 version for el7
- BR tbb

* Thu Jun 06 2019 Christoph Junghans <junghans@votca.org> - 20190605-3
- rebuild for kim-api fix

* Wed Jun 05 2019 Christoph Junghans <junghans@votca.org> - 20190605-2
- Enabled kim-api support

* Tue Jun 04 2019 Christoph Junghans <junghans@votca.org> - 20190605-1
- Bump version to 20190605

* Tue Feb 12 2019 Christoph Junghans <junghans@votca.org> - 20181212-3
- Fix build with gcc-9 (bug #1675247)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181212-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Christoph Junghans <junghans@votca.org> - 20181212-1
- Bump version to 20181212
- Add MPI_SUFFIX to lmp and liblammps
- Major spec clean up

* Fri Aug 24 2018 Christoph Junghans <junghans@votca.org> - 20180822-2
- Enable some more packages
- Use Openblas instead of internal lapack

* Wed Aug 22 2018 Christoph Junghans <junghans@votca.org> - 20180822-1
- Bump version to 20180822
- Dropped 979.patch got merged upstream

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180316-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 20180316-3
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 20180316-2
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Christoph Junghans <junghans@votca.org> - 20180316-1
- Bump version to 20180316 (bug #1558768) and swtich to stable
- Dropped 835.patch got merged upstream

* Thu Mar 08 2018 Christoph Junghans <junghans@votca.org> - 20180308-1
- Bump version to 20180308
- Added 835.patch

* Mon Mar 05 2018 Christoph Junghans <junghans@votca.org> - 201802222-1
- Bump version to 20180222

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180117-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Christoph Junghans <junghans@votca.org> - 20180117-2
- Rebuild for gfortran-8

* Fri Jan 26 2018 Christoph Junghans <junghans@votca.org> - 20180117-1
- Bump version to 20180117

* Fri Nov 03 2017 Christoph Junghans <junghans@votca.org> - 20171023-1
- Bump version to 20171023
- Enable OpenCL package

* Sun Sep 10 2017 Christoph Junghans <junghans@votca.org> - 20170901-1
- Bump version to 20170901, drop 573.patch merged upstream

* Thu Aug 24 2017 Christoph Junghans <junghans@votca.org> - 20170811-6
- Enable voronoid package

* Thu Aug 17 2017 Christoph Junghans <junghans@votca.org> - 20170811-5
- Comments from the review bug #1474958
  - Drop Buildrequires mpi-devel for lammps-openmpi and lammps-mpich
  - Move Requires: mpi to lammps-openmpi and lammps-mpich
  - Install LICENSE for lammps-openmpi and lammps-mpich

* Wed Aug 16 2017 Christoph Junghans <junghans@votca.org> - 20170811-4
- Set cmake linker flags to incl. $MPI_LIB as RUNPATH

* Tue Aug 15 2017 Christoph Junghans <junghans@votca.org> - 20170811-3
- Added python provide
- Added mpi deps

* Tue Aug 15 2017 Christoph Junghans <junghans@votca.org> - 20170811-2
- Fix python3 dep

* Mon Aug 14 2017 Christoph Junghans <junghans@votca.org> - 20170811-1
- Bump version to 20170811, drop 594.patch merged upstream
- Improvment from reveiw bug #1474958
  - split devel package into mpi*-devel and header
  - move python interface into own package and to python3
  - support for epel7

* Fri Jul 21 2017 Christoph Junghans <junghans@votca.org> - 20170706-1
- Initial import

