%define		template	varnish
Summary:	Varnish Cache statistics template for Cacti
Name:		cacti-template-%{template}
Version:	0.0.2
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://forums.cacti.net/download.php?id=16163&/varnish-cacti-stats-%{version}.zip
# Source0-md5:	b7a4ff93877cbd395c58525887b52dd9
URL:		http://forums.cacti.net/viewtopic.php?t=31260
Requires:	cacti >= 0.8.6j
Requires:	cacti-add_template
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cactidir		/usr/share/cacti
%define		resourcedir		%{cactidir}/resource
%define		scriptsdir		%{cactidir}/scripts

%description
Template for Cacti - Varnish Cache statistics.

%prep
%setup -q -n varnish-cacti-stats-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{resourcedir},%{scriptsdir}}
cp -a templates/*.xml $RPM_BUILD_ROOT%{resourcedir}
install -p scripts/*.py $RPM_BUILD_ROOT%{scriptsdir}

%post
%{_sbindir}/cacti-add_template \
	%{resourcedir}/cacti_data_template_varnish_statistics.xml \
	%{resourcedir}/cacti_graph_template_varnish_-_cache_hitrate.xml
	%{resourcedir}/cacti_graph_template_varnish_-_number_of_requests.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{scriptsdir}/get_varnish_stats.py
%{resourcedir}/*.xml
