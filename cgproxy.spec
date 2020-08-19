%global __provides_exclude_from ^%{_libdir}/%{name}/.*\\.so$

Name:       cgproxy
Version:    0.19
Release:    1%{?dist}
Summary:    A transparent proxy program powered by cgroup2 and tproxy
License:		GPLv2

URL:        https://github.com/springzfx/%{name}
Source0:    %{URL}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Patch1:     0001-Always-install-systemd-unit-files-in-right-place.patch
# Patch2:     0002-Don-t-hardcode-paths.patch

# for build
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    cmake >= 3.14
BuildRequires:    libbpf-devel
BuildRequires:    json-devel
%if 0%{?fedora} >= 30
BuildRequires:    systemd-rpm-macros
%else
BuildRequires:    systemd
%endif


%description
cgproxy will transparent proxy anything running in specific cgroup. 
It resembles with proxychains and tsocks in default setting.



%prep
%autosetup

%build
%cmake  -Dbuild_execsnoop_dl=ON \
        -Dbuild_static=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.json

%{_bindir}/cgnoproxy
%{_bindir}/%{name}
%{_bindir}/cgproxyd

%dir %{_unitdir}
%{_unitdir}/%{name}.service

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libexecsnoop.so

%{_datadir}/%{name}

%dir %{_pkgdocdir}
%{_mandir}/man1/*.1.*
%{_pkgdocdir}/*


%changelog
* Wed Aug 05 11:31:07 GMT 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 0.18-2
- fix license
