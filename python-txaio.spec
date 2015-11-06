%global pypi_name txaio

Name:           python-%{pypi_name}
Version:        2.0.4
Release:        2%{?dist}
Summary:        Compatibility API between asyncio/Twisted/Trollius

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         python-txaio-%{version}-sphinx-config_find-theme.patch
Patch1:         python-txaio-%{version}-tests.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  pytest
BuildRequires:  python-pytest-cov
BuildRequires:  python-mock
BuildRequires:  python-pep8
BuildRequires:  python-sphinx
BuildRequires:  python2-sphinx-theme-alabaster
BuildRequires:  python-six
BuildRequires:  python-twisted

%description
Helper library for writing code that runs unmodified on both Twisted and
asyncio.


%package -n     python2-%{pypi_name}
Summary:        Compatibility API between asyncio/Twisted/Trollius
BuildArch:      noarch
Requires:       python-twisted
Requires:       python-six
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
BuildRequires:  python3-sphinx-theme-alabaster
BuildRequires:  python3-six
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
%patch1

# Remove upstream's egg-info
rm -rf %{pypi_name}.egg-info

# README is just a symlink to index.rst. Using this file as README
rm README.rst
cp -a docs/index.rst README.rst


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
PYTHONPATH=$PYTHONPATH:. coverage3 run -p --source=txaio /usr/bin/py.test-%{python3_version} -s

PYTHONPATH=$PYTHONPATH:. coverage2 run -p --source=txaio /usr/bin/py.test-%{python2_version} -s


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
