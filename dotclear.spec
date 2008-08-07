%define	name	dotclear
%define	version	1.2.5
%define	release	%mkrel 5
%define order	71

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Web-based blog
License:	GPL
Group:		System/Servers
URL:		http://www.dotclear.net
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-apache.conf.bz2
Source2:	README.urpmi
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache-mpm >= 2.0.54
Requires:       apache-mod_php php-xml php-mysql
BuildArch:	noarch
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
dotclear is a multilingual web application developed in php. 
It provides personal blogs and trackbacks to react,
but also can be used in a multi-user mode with several right levels.

%prep
%setup -q -n %{name}

%build

%install
rm -rf  $RPM_BUILD_ROOT

# install files
install -d -m 755 $RPM_BUILD_ROOT%{_var}/www/%{name}
install -d -m 755 $RPM_BUILD_ROOT%_defaultdocdir/%{name}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%_defaultdocdir/%{name}
mv CHANGELOG COPYING LISEZMOI.txt VERSION $RPM_BUILD_ROOT%_defaultdocdir/%{name}
cp -aRf * $RPM_BUILD_ROOT%{_var}/www/%{name}
rm -f $RPM_BUILD_ROOT%_defaultdocdir/%{name}/{CHANGELOG,COPYING,LISEZMOI.txt,VERSION}

# apache configuration
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/webapps.d
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/webapps.d/%{order}_%{name}.conf

# remove .htaccess files
find $RPM_BUILD_ROOT%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -e %{_sbindir}/ADVXctl ]; then %{_sbindir}/ADVXctl update;fi
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ -e %{_sbindir}/ADVXctl ]; then %{_sbindir}/ADVXctl update;fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{order}_%{name}.conf
%dir %_defaultdocdir/%{name}
%_defaultdocdir/%{name}/README.urpmi
%dir %{_var}/www/%{name}
%{_var}/www/%{name}/*.php
%attr(0755,apache,apache) %{_var}/www/%{name}/conf
%{_var}/www/%{name}/ecrire
%{_var}/www/%{name}/images
%{_var}/www/%{name}/inc
%{_var}/www/%{name}/install
%{_var}/www/%{name}/l10n
%{_var}/www/%{name}/layout
%{_var}/www/%{name}/share
%{_var}/www/%{name}/themes
