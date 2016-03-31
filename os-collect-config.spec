
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:			os-collect-config
Version:		0.1.37
Release:		1%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		http://tarballs.openstack.org/%{name}/%{name}-%{version}%{?milestone}.tar.gz
Source1:		os-collect-config.service
Source2:		os-collect-config.conf

Patch0001: 0001-Remove-pbr-runtime-dependency-and-replace-with-build.patch

BuildArch:		noarch
BuildRequires:		python-setuptools
BuildRequires:		python2-devel
BuildRequires:		systemd
BuildRequires:		python-pbr

Requires:		python-setuptools
Requires:		python-argparse
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python-eventlet
Requires:		python-heatclient
Requires:		python-keystoneclient
Requires:		python-requests
Requires:		python-iso8601
Requires:		python-lxml
Requires:		python-six
Requires:		python-oslo-config
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%patch0001 -p1

#
# patches_base: 0.1.11
#

sed -i '/setuptools_git/d' setup.py
sed -i s/REDHATOSCOLLECTCONFIGVERSION/%{version}/ os_collect_config/version.py
sed -i s/REDHATOSCOLLECTCONFIGRELEASE/%{release}/ os_collect_config/version.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/os_collect_config/tests

%post
%systemd_post os-collect-config.service

%preun
%systemd_preun os-collect-config.service

%postun
%systemd_postun os-collect-config.service

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-collect-config
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/os-collect-config.conf
%{python_sitelib}/os_collect_config*
%{_unitdir}/os-collect-config.service

%changelog
* Thu Mar 31 2016 RDO <rdo-list@redhat.com> 0.1.37-1
- RC1 Rebuild for Mitaka RC1 0.1.37
