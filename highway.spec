%global common_description %{expand:
Highway is a C++ library for SIMD (Single Instruction, Multiple Data), i.e.
applying the same operation to 'lanes'.}

# https://github.com/google/highway/issues/776
%ifarch aarch64
%global toolchain clang
%endif

Name:           highway
Version:        0.17.0
Release:        %autorelease
Summary:        Efficient and performance-portable SIMD

License:        ASL 2.0
URL:            https://github.com/google/highway
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
%ifarch aarch64
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  gtest-devel

%description
%common_description

%package        devel
Summary:        Development files for Highway
Requires:       %{name}%{?_isa} = %{version}-%{release}

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
# https://github.com/google/highway/issues/775
%ifnarch s390x
%ctest
%endif

%files
%license LICENSE
%{_libdir}//libhwy.so.0
%{_libdir}//libhwy.so.%{version}
%{_libdir}//libhwy_contrib.so.0
%{_libdir}//libhwy_contrib.so.%{version}
%{_libdir}//libhwy_test.so.0
%{_libdir}//libhwy_test.so.%{version}

%files devel
%license LICENSE
%{_includedir}/hwy/
%{_libdir}/libhwy.so
%{_libdir}/libhwy_contrib.so
%{_libdir}/libhwy_test.so
%{_libdir}/pkgconfig/libhwy.pc
%{_libdir}/pkgconfig/libhwy-contrib.pc
%{_libdir}/pkgconfig/libhwy-test.pc

%files doc
%license LICENSE
%doc g3doc hwy/examples

%changelog
%autochangelog
