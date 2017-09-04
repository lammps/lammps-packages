Name:           lammps-fedora-repo
Version:        2
Release:        2
Summary:        LAMMPS Fedora Repository Configuration

Group:          LAMMPS
License:        BSD
URL:            http://packages.lammps.org/rpm/
Source0:        lammps-fedora.repo
Source1:        RPM-GPG-KEY-lammps-2017.1

BuildArch:      noarch

%description
This package contains the DNF (or Yum) package manager configuration
files for the official LAMMPS repository of precompiled LAMMPS binaries
for Fedora Linux installations.

%prep
exit 0

%setup -q

%build
cat > README <<EOF
This is the repository package for RPM binary packages built
by the LAMMPS developers and distributed through http://packages.lammps.org
EOF
exit 0

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/pki/rpm-gpg/
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/rpm-gpg/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%config(noreplace) %{_sysconfdir}/yum.repos.d/*.repo
%config(noreplace) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-*

%changelog
* Mon Sep  4 2017 Axel Kohlmeyer <akohlmey@gmail.com> - 2-2
- update spec and repo file to refer to public package key

* Thu Aug 17 2017 Axel Kohlmeyer <akohlmey@gmail.com> - 2-2
- update repo file with metadata timeouts

* Thu Aug 17 2017 Axel Kohlmeyer <akohlmey@gmail.com> - 2-1
- Update spec file for restarted automated RPM build

* Sat Jun 15 2013 Axel Kohlmeyer <akohlmey@gmail.com> - 1-2
- Updated repo file to not include source packages. No need.

* Wed Jun  12 2013 Axel Kohlmeyer <akohlmey@gmail.com> - 1-1
- Initial Fedora style SPEC file
