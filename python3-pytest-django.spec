#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some db setup required?)

Summary:	Django plugin for pytest
Summary(pl.UTF-8):	Wtyczka Django dla pytesta
Name:		python3-pytest-django
Version:	4.5.2
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-django/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-django/pytest-django-%{version}.tar.gz
# Source0-md5:	5d7e84c0ebf467ba40ea0508ba7b6894
URL:		https://pypi.org/project/pytest-django/
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.11.1
%if %{with tests}
BuildRequires:	python3-django >= 2.2
BuildRequires:	python3-django-configurations >= 2.0
BuildRequires:	python3-pytest >= 5.4
BuildRequires:	python3-pytest-xdist
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pytest-django allows you to test your Django project/applications with
the pytest testing tool.

%description -l pl.UTF-8
pytest-django pozwala testować projekty/aplikacje Django przy użyciu
narzędzia testującego pytest.

%package apidocs
Summary:	API documentation for Python pytest-django module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-django
Group:		Documentation

%description apidocs
API documentation for Python pytest-django module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-django.

%prep
%setup -q -n pytest-django-%{version}

%build
%py3_build

%if %{with tests}
DJANGO_SETTINGS_MODULE=pytest_django_test.settings_sqlite \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_django.plugin,xdist.plugin" \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%{py3_sitescriptdir}/pytest_django
%{py3_sitescriptdir}/pytest_django-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
