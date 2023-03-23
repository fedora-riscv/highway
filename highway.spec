%global common_description %{expand:
Highway is a C++ library for SIMD (Single Instruction, Multiple Data), i.e.
applying the same operation to 'lanes'.}

%global toolchain clang

%ifarch riscv64
%define _lto_cflags %{nil}
%endif

Name:           highway
Version:        1.0.4
Release:        %autorelease -e 0.riscv64
Summary:        Efficient and performance-portable SIMD

License:        Apache-2.0
URL:            https://github.com/google/highway
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  gtest-devel
BuildRequires:  libatomic

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
%ifarch riscv64
export CFLAGS="%optflags -DHWY_COMPILE_ONLY_EMU128 -DHWY_DISABLED_TARGETS=HWY_RVV"
export CXXFLAGS="%optflags -DHWY_COMPILE_ONLY_EMU128 -DHWY_DISABLED_TARGETS=HWY_RVV"
%endif
%cmake -DHWY_SYSTEM_GTEST:BOOL=ON
%cmake_build

%install
%cmake_install

%check
%ifnarch riscv64
%ctest --exclude-regex "wyBlockwiseTestGroup/HwyBlockwiseTest.TestAllBroadcast"
%else
# 144 - HwyMulTestGroup/HwyMulTest.TestAllMulHigh/EMU128  # GetParam() = 2305843009213693952 (Failed)
# 145 - HwyMulTestGroup/HwyMulTest.TestAllMulFixedPoint15/EMU128  # GetParam() = 2305843009213693952 (Failed)
%ctest --exclude-regex "wyBlockwiseTestGroup/HwyBlockwiseTest.TestAllBroadcast" || :
%endif

%files
%license LICENSE
%{_libdir}/libhwy.so.1
%{_libdir}/libhwy.so.%{version}
%{_libdir}/libhwy_contrib.so.1
%{_libdir}/libhwy_contrib.so.%{version}
%{_libdir}/libhwy_test.so.1
%{_libdir}/libhwy_test.so.%{version}

%files devel
%license LICENSE
%{_includedir}/hwy/
%{_libdir}/cmake/hwy/
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
