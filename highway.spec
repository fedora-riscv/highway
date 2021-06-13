# static library only
%global debug_package   %nil

# gtest in RHEL does not contain pkgconfig
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^pkgconfig\\(gtest\\)$

%global common_description %{expand:
Highway is a C++ library for SIMD (Single Instruction, Multiple Data), i.e.
applying the same operation to 'lanes'.}

Name:           highway
Version:        0.12.2
Release:        1%{?dist}
Summary:        Efficient and performance-portable SIMD

License:        ASL 2.0
URL:            https://github.com/google/highway
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel

%description
%common_description

%package        devel
Summary:        Development files for Highway
Provides:       highway-static = %{version}-%{release}
Requires:       gtest-devel

%description devel
%{common_description}

Development files for Highway.

%package        doc
Summary:        Documentation for Highway
BuildArch:      noarch

%description doc
%{common_description}

Documentation for Highway.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake -DHWY_SYSTEM_GTEST:BOOL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files devel
%license LICENSE
%{_includedir}/hwy/
%{_libdir}/libhwy.a
%{_libdir}/libhwy_contrib.a
%{_libdir}/pkgconfig/libhwy.pc
%{_libdir}/pkgconfig/libhwy-contrib.pc
%{_libdir}/pkgconfig/libhwy-test.pc

%files doc
%license LICENSE
%doc g3doc hwy/examples

%changelog
* Sun Jun 13 13:15:46 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.2-1
- Update to 0.12.2

* Mon May 31 22:26:28 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-2
- Add workaround for the lack of pkgconfig in RHEL8 gtest

* Sun May 23 19:03:29 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-1
- Update to 0.12.0
- Close: rhbz#1963675

* Mon May 17 18:03:58 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.0-1.20210518git376a400
- Initial RPM
