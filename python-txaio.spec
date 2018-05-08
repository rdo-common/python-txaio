%global pypi_name txaio

Name:           python-%{pypi_name}
Version:        2.10.0
Release:        2%{?dist}
Summary:        Compatibility API between asyncio/Twisted/Trollius

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/b8/87/efcae4040c2a0af9c871116a6dbf02ee582b396e6de3797fb30cdcc4a7e4/txaio-2.10.0.tar.gz
Patch0:         python-txaio-skip-packaging-tests.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-pytest >= 2.6.4
BuildRequires:  python2-pytest-cov >= 1.8.1
BuildRequires:  python2-mock >= 1.3.0
BuildRequires:  python2-pep8 >= 1.6.2
BuildRequires:  python2-sphinx >= 1.2.3
BuildRequires:  python2-sphinx_rtd_theme
BuildRequires:  python2-six
BuildRequires:  python2-twisted >= 12.1.0
BuildRequires:  python2-zope-interface >= 3.6
BuildRequires:  python2-trollius >= 2.0
BuildRequires:  python2-futures >= 3.0.3
BuildRequires:  python2-enchant >= 1.6.6


%description
Helper library for writing code that runs unmodified on both Twisted and
asyncio.


%package -n     python2-%{pypi_name}
Summary:        Compatibility API between asyncio/Twisted/Trollius
BuildArch:      noarch
Requires:       python2-twisted >= 12.1.0
Requires:       python2-zope-interface >= 3.6
Requires:       python2-trollius >= 2.0
Requires:       python2-futures >= 3.0.3
Requires:       python2-six
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Helper library for writing code that runs unmodified on both Twisted and
asyncio.


%package -n     python3-%{pypi_name}
Summary:        Compatibility API between asyncio/Twisted/Trollius
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-mock
BuildRequires:  python3-pep8
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-six
BuildRequires:  python3-enchant >= 1.6.6
Requires:       python3-six
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Helper library for writing code that runs unmodified on both Twisted and
asyncio.


%package doc
Summary: Documentation for txaio
Requires: js-jquery

%description doc
Helper library for writing code that runs unmodified on both Twisted and
asyncio. Documentation in html format.


%prep
%setup -qn %{pypi_name}-%{version}
%patch0

# Remove upstream's egg-info
rm -rf %{pypi_name}.egg-info

# README is just a symlink to index.rst. Using this file as README
rm docs/index.rst
cp -a README.rst docs/index.rst


%build
%py2_build
%py3_build

# Build documentation
cd docs && make html

# Remove buildinfo
rm -rf _build/html/.buildinfo

# Unbundle jquery
rm -f  _build/html/_static/jquery.js
ln -s /usr/share/javascript/jquery/latest/jquery.min.js _build/html/_static/jquery.js


%install
%py2_install
%py3_install


%check
PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/test coverage3 run -p --source=txaio /usr/bin/py.test-%{python3_version} -s
PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/test coverage2 run -p --source=txaio /usr/bin/py.test-%{python2_version} -s


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info/
%{python2_sitelib}/%{pypi_name}/

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/


%files doc
%license LICENSE
%doc docs/_build/html


%changelog
* Tue May 08 2018 Miro Hrončok <mhroncok@redhat.com> - 2.10.0-2
- Remove unused build dependency on tox

* Sun Apr 15 2018 Julien Enselme <jujens@jujens.eu> - 2.10.0-1
- Update to 2.10.0

* Tue Mar 06 2018 Julien Enselme <jujens@jujens.eu> - 2.9.0-1
- Update to 2.9.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.8.2-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Sep 06 2017 Julien Enselme <jujens@jujens.eu> - 2.8.2-1
- Update to 2.8.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Julien Enselme <jujens@jujens.eu> - 2.8.1-1
- Update to 2.8.1

* Sat Jun 10 2017 Julien Enselme <jujens@jujens.eu> - 2.8.0-1
- Update to 2.8.0

* Sun May 07 2017 Julien Enselme <jujens@jujens.eu> - 2.7.1-1
- Update to 2.7.1

* Tue Apr 18 2017 Julien Enselme <jujens@jujens.eu> - 2.7.0-1
- Update to 2.7.0

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 2.6.2-1
- Update to 2.6.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 26 2016 Julien Enselme <jujens@jujens.eu> - 2.5.2-1
- Update to 2.5.2
- Skip failing tests on Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-3
- Rebuild for Python 3.6

* Sat Oct 01 2016 Julien Enselme <jujens@jujens.eu> - 2.5.1-2
- Fix tests for pytest3
- Correct build of documentation with sphinx 1.4.8

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 16 2016 Julien Enselme <jujens@jujens.eu> - 2.5.1-1
- Update to 2.5.1

* Sat Feb 27 2016 Julien Enselme <jujens@jujens.eu> - 2.2.1-1
- Update to 2.2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 6 2015 Julien Enselme <jujens@jujens.eu> - 2.0.4-2
- Rebuilt for python 3.5

* Sat Oct 17 2015 Julien Enselme <jujens@jujens.eu> - 2.0.4-1
- Update 2.0.4

* Mon Sep 28 2015 Julien Enselme <jujens@jujens.eu> - 2.0.2-1
- Update to 2.0.2

* Sat Aug 15 2015 Julien Enselme <jujens@jujens.eu> - 1.0.3-2
- Move python2 package in its own subpackage

* Sat Aug 15 2015 Julien Enselme <jujens@jujens.eu> - 1.0.3-1
- Update to 1.0.3

* Sat Aug 8 2015 Julien Enselme <jujens@jujens.eu> - 1.0.2-1
- Update to 1.0.2
- Use %%py2_build, %%py3_build, %%py2_install and %%py2_install

* Tue Aug 4 2015 Julien Enselme <jujens@jujens.eu> - 1.0.0-4
- Correct sphinx theme name in BuildRequires

* Thu Jul 30 2015 Julien Enselme <jujens@jujens.eu> - 1.0.0-3
- Add provides for python2-txaio
- Remove usage of python2 and python3 dirs
- Unbundle jquery
- Don't remove _sources of documentation

* Fri Jul 24 2015 Julien Enselme <jujens@jujens.eu> - 1.0.0-2
- Remove %%py3dir macro
- Add CFLAGS in %%build

* Sat Jul 18 2015 Julien Enselme <jujens@jujens.eu> - 1.0.0-1
- Initial packaging
