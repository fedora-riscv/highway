# static library only
%global debug_package   %nil
%undefine __cmake3_in_source_build

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

BuildRequires:  cmake3
BuildRequires:  gcc-c++

# EPEL7 GCC 8
BuildRequires:  devtoolset-8-toolchain
BuildRequires:  scl-utils

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
do_build () {
%cmake3 -DBUILD_TESTING:BOOL=OFF
%cmake3_build
}

export -f do_build
scl enable devtoolset-8 do_build

%install
%cmake3_install

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
* Sun Jun 13 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.2-1
- Update to 0.12.2

* Mon May 31 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-2
- Add workaround for the lack of pkgconfig in RHEL8 gtest

* Sun May 23 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.1-1
- Update to 0.12.1
- Close: rhbz#1963675

* Mon May 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.0-1.20210518git376a400
- Initial RPM
