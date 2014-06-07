Name:			os-collect-config
Version:		0.1.11
Release:		6%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
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
Requires:		python-eventlet
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

%setup -q -n %{name}-%{version}

%patch0001 -p1

sed -i '/setuptools_git/d' setup.py
sed -i s/REDHATOSCOLLECTCONFIGVERSION/%{version}/ os_collect_config/version.py
sed -i s/REDHATOSCOLLECTCONFIGRELEASE/%{release}/ os_collect_config/version.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf

%post
%systemd_post os-collect-config.service

%preun
%systemd_preun os-collect-config.service

%postun
%systemd_postun_with_restart os-collect-config.service

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-collect-config
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/os-collect-config.conf
%{python_sitelib}/os_collect_config*
%{_unitdir}/os-collect-config.service

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Steven Dake <sdake@redhat.com> - 0.1.11-5
- install a os-collect-config default conf file

* Mon Feb 24 2014 Steven Dake <sdake@redhat.com> - 0.1.11-4
- Make runtime version calculation instead of using python-pbr

* Thu Feb 20 2014 Steven Dake <sdake@redhat.com> - 0.1.11-3
- Added missing dependency python-anyjson
- Added missing build requires python-pbr

* Thu Feb 20 2014 Steven Dake <sdake@redhat.com> - 0.1.11-2
- Fixed missing dependency python-oslo-config
- Added cr after every changelog entry

* Wed Feb 19 2014 Steven Dake <sdake@redhat.com> - 0.1.11-1
- Update to version 0.1.11
- Add python2-devel build requires
- Add systemd for post/preun/postun buildrequires
- Add a systemd postun scriptlet
- Make setup quiet

* Tue Oct 15 2013 Lucas Alvares Gomes <lgomes@redhat.com> - 0.1.2-1
- Update to version 0.1.2

* Fri Sep 6 2013 Lucas Alvares Gomes <lgomes@redhat.com> - 0.0.1-1
- Initial version
