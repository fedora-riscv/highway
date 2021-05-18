# static library only
%global debug_package   %nil
%undefine __cmake3_in_source_build

%global commit          376a400463f7e79e2e79e34ad67225e9397df54f
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20210518
%global prerelease      1

%global common_description %{expand:
Highway is a C++ library for SIMD (Single Instruction, Multiple Data), i.e.
applying the same operation to 'lanes'.}

Name:           highway
Version:        0.12.0
Release:        1%{?prerelease:.%{snapshotdate}git%{shortcommit}}%{?dist}
Summary:        Efficient and performance-portable SIMD

License:        ASL 2.0
URL:            https://github.com/google/highway
Source0:        %url/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

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
%autosetup -p1 -n %{name}-%{commit}

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
* Mon May 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.12.0-1.20210518git376a400
- Initial RPM
