#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some db setup required?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Django plugin for pytest
Summary(pl.UTF-8):	Wtyczka Django dla pytesta
Name:		python-pytest-django
# keep 3.x here for python2 support
Version:	3.10.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-django/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-django/pytest-django-%{version}.tar.gz
# Source0-md5:	08df95a09382bdc15a9428b072fe15a8
URL:		https://pypi.org/project/pytest-django/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.11.1
%if %{with tests}
BuildRequires:	python-django >= 1.8
BuildRequires:	python-django < 2
BuildRequires:	python-django-configurations >= 2.0
BuildRequires:	python-pathlib2
BuildRequires:	python-pytest >= 3.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.11.1
%if %{with tests}
BuildRequires:	python3-django >= 1.8
BuildRequires:	python3-django-configurations >= 2.0
BuildRequires:	python3-pytest >= 3.6
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pytest-django allows you to test your Django project/applications with
the pytest testing tool.

%description -l pl.UTF-8
pytest-django pozwala testować projekty/aplikacje Django przy użyciu
narzędzia testującego pytest.

%package -n python3-pytest-django
Summary:	Django plugin for pytest
Summary(pl.UTF-8):	Wtyczka Django dla pytesta
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pytest-django
pytest-django allows you to test your Django project/applications with
the pytest testing tool.

%description -n python3-pytest-django -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
DJANGO_SETTINGS_MODULE=pytest_django_test.settings_sqlite \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_django.plugin \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
DJANGO_SETTINGS_MODULE=pytest_django_test.settings_sqlite \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_django.plugin \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%{py_sitescriptdir}/pytest_django
%{py_sitescriptdir}/pytest_django-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-django
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%{py3_sitescriptdir}/pytest_django
%{py3_sitescriptdir}/pytest_django-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
