Name:			os-collect-config
Version:		0.1.11
Release:		3%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
Source1:		os-collect-config.service

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

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service

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
%{python_sitelib}/os_collect_config*
%{_unitdir}/os-collect-config.service

%changelog
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
