%define		template	varnish
Summary:	Varnish Cache statistics template for Cacti
Name:		cacti-template-%{template}
Version:	0.0.3
Release:	0.6
License:	GPL v2
Group:		Applications/WWW
Source1:	get_varnish_stats.py
Source2:	cacti_host_template_varnish.xml
URL:		http://forums.cacti.net/viewtopic.php?p=182152
BuildRequires:	rpmbuild(macros) >= 1.554
Requires:	cacti >= 0.8.7e-8
Conflicts:	cacti-spine < 0.8.7e-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cactidir		/usr/share/cacti
%define		resourcedir		%{cactidir}/resource
%define		scriptsdir		%{cactidir}/scripts

%description
Template for Cacti - Varnish Cache statistics.

%prep
%setup -qcT

cat > README <<'EOF'
Uses advanced template from:
<http://forums.cacti.net/viewtopic.php?p=182152>

Combines script to pull data via Varnish admin port from
<http://forums.cacti.net/viewtopic.php?t=31260>

How to install
==============

1 - Import cacti_host_template_varnish.xml to Cacti (tested with 0.8.7e)
2 - Copy get_varnish_stats.py to "scripts"

###############################################################################
IMPORTANT: You need to recompile spine with "./configure --with-results-buffer=2048"
###############################################################################

EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{resourcedir},%{scriptsdir}}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{scriptsdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{resourcedir}

%post
%cacti_import_template %{resourcedir}/cacti_host_template_varnish.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{scriptsdir}/get_varnish_stats.py
%{resourcedir}/*.xml
