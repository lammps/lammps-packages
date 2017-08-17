Name:           lammps-fedora-repo
Version:        2
Release:        1
Summary:        LAMMPS Fedora Repository Configuration
Packager:       LAMMPS Packages <packages@lammps.org>

Group:          LAMMPS
License:        BSD
URL:            http://packages.lammps.org/rpm/
Source0:        lammps-fedora.repo

BuildArch:      noarch

%description
This package contains the DNF package manager configuration files for the
official LAMMPS repository of precompiled LAMMPS binaries for Fedora
Linux installations

%prep
# no setup

%build
# no build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d/
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/*.repo

%changelog
* Sat Jun 15 2013 Axel Kohlmeyer <akohlmey@gmail.com> - 1-2
- Updated repo file to not include source packages. No need.


* Wed Jun  12 2013 Axel Kohlmeyer <akohlmey@gmail.com> - 1-1
- Initial Fedora style SPEC file


