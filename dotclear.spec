%define	name	dotclear
%define	version	2.1.5
%define	release	%mkrel 1
%define order	71

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Web-based blog
License:	GPLv2
Group:		System/Servers
URL:		http://www.dotclear.net
Source0:	http://download.dotclear.org/latest/%{name}-%{version}.tar.gz
Source1:	%{name}-apache.conf.bz2
Source2:	README.urpmi
Requires(pre):  mod_php >= 2.0.54-5mdk    
Requires(pre):  apache >= 2.0.54-5mdk     
Requires(pre):  rpm-helper   
Requires:		php-xml 
Requires:		php-iconv
Requires:		php-mbstring
BuildArch:	noarch

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
dotclear is a multilingual web application developed in php. 
It provides personal blogs and trackbacks to react,
but also can be used in a multi-user mode with several right levels.

%prep
%setup -q -n %{name}

	   
%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# install files
install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%_defaultdocdir/%{name}
install -m 644 %{SOURCE2} %{buildroot}%_defaultdocdir/%{name}
mv CHANGELOG %{buildroot}%_defaultdocdir/%{name}
cp -aRf * %{buildroot}%{_var}/www/%{name}
rm -f %{buildroot}%_defaultdocdir/%{name}/CHANGELOG

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
bzcat %{SOURCE1} > %{buildroot}%{_webappconfdir}/%{order}_%{name}.conf

# remove .htaccess files
find %{buildroot}%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

# fix exectuable bit 
find %{buildroot}%{_var}/www/%{name} -type f -exec chmod 644 {} \;
chmod 755 %{buildroot}%{_var}/www/%{name}/inc/dbschema/upgrade-cli.php

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%config(noreplace) %_webappconfdir/%{order}_%{name}.conf
%dir %_defaultdocdir/%{name}
%_defaultdocdir/%{name}/README.urpmi
%dir %{_var}/www/%{name}
%{_var}/www/%{name}/*.php
%{_var}/www/%{name}/inc/
%{_var}/www/%{name}/admin
%{_var}/www/%{name}/cache
%{_var}/www/%{name}/db
%{_var}/www/%{name}/locales
%{_var}/www/%{name}/plugins
%{_var}/www/%{name}/public
%{_var}/www/%{name}/themes
%dir %attr(0775,root,apache) %{_var}/www/%{name}/cache
%dir %attr(0775,root,apache) %{_var}/www/%{name}/inc/
