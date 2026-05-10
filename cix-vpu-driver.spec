%global debug_package %{nil}
%global dkms_name     cix-vpu-driver
%global dkms_ver      %{version}-%{release}

Name:           %{dkms_name}
Version:        1.0.1
Release:        1%{?dist}
Summary:        CIX Orion O6 VPU driver (amvx) with DKMS
License:        GPL-2.0-or-later
URL:            https://github.com/cixtech/cix_opensource__vpu_driver
BuildArch:      noarch

Requires:       dkms >= 3.0.0
Requires(post): dkms >= 3.0.0
Requires(preun): dkms >= 3.0.0
Requires:       gcc, make, kernel-devel

%description
This DKMS package provides the CIX VPU kernel module (amvx.ko)
for Orion O6 on Fedora. The module is automatically rebuilt
when the kernel is updated.

%prep
%setup -q -n %{name}-%{version}
sed -i 's/#MODULE_VERSION#/%{dkms_ver}/g' dkms.conf

%build
# DKMS 不在此处编译 -- 编译在目标机器安装时进行

%install
rm -rf %{buildroot}

# 1. 安装内核模块源码到 /usr/src/
SRC_DIR=%{buildroot}/usr/src/%{dkms_name}-%{dkms_ver}
mkdir -p ${SRC_DIR}
cp -a driver/* ${SRC_DIR}/
cp Makefile ${SRC_DIR}/
install -m 644 dkms.conf ${SRC_DIR}/

# 2. 安装固件
mkdir -p %{buildroot}/usr/lib/firmware
if [ -d firmware-binaries ]; then
    cp -a firmware-binaries/* %{buildroot}/usr/lib/firmware/
fi

%post
dkms add -m %{dkms_name} -v %{dkms_ver} || :
dkms build -m %{dkms_name} -v %{dkms_ver} || :
dkms install -m %{dkms_name} -v %{dkms_ver} || :
echo "CIX VPU driver installed. Check: dkms status"

%preun
if [ $1 -eq 0 ]; then
    dkms remove -m %{dkms_name} -v %{dkms_ver} --all || :
fi

%files
/usr/src/%{dkms_name}-%{dkms_ver}/
/usr/lib/firmware/*

%changelog
* Sun May 10 2026 houge - 1.0.1-1
- Initial DKMS package for Orion O6 VPU driver (Fedora 44)
