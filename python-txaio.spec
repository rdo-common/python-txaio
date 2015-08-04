%global pypi_name txaio

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        4%{?dist}
Summary:        Compatibility API between asyncio/Twisted/Trollius

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.zip
# Release on pypi is missing a util file which is needed to launch tests
# See: https://github.com/tavendo/txaio/issues/3
Source1:        https://raw.githubusercontent.com/tavendo/txaio/v1.0.0/test/util.py
Patch0:         python-txaio-1.0.0-sphinx-config_find-theme.patch

BuildArch: noarch

BuildRequires:  python2-devel
BuildRequires:  pytest
BuildRequires:  python-pytest-cov
BuildRequires:  python-mock
BuildRequires:  python-pep8
BuildRequires:  python-sphinx
BuildRequires:  python2-sphinx-theme-alabaster
BuildRequires:  python-six
BuildRequires:  python-twisted
Requires:       python-twisted
Requires:       python-six
Provides:       python2-%{pypi_name} = %{version}-%{release}

%description
Helper library for writing code that runs unmodified on both Twisted and
asyncio.


%package -n     python3-%{pypi_name}
Summary:        Compatibility API between asyncio/Twisted/Trollius
BuildArch: noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-mock
BuildRequires:  python3-pep8
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-theme-alabaster
BuildRequires:  python3-six
Requires:       python3-six

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

cp %{SOURCE1} test/


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

# Build documentation
cd doc && make html

# Remove buildinfo
rm -rf _build/html/.buildinfo

# Unbundle jquery
rm -f  _build/html/_static/jquery.js
ln -s /usr/share/javascript/jquery/latest/jquery.min.js _build/html/_static/jquery.js


%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%{__python2} setup.py install --skip-build --root %{buildroot}


%check
PYTHONPATH=$PYTHONPATH:. coverage3 run -p --source=txaio /usr/bin/py.test-%{python3_version} -s

PYTHONPATH=$PYTHONPATH:. coverage2 run -p --source=txaio /usr/bin/py.test-%{python2_version} -s


%files
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
%doc doc/_build/html


%changelog
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
