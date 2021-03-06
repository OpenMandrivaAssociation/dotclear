Name:		dotclear
Version:	2.6.3
Release:	2
Summary:	Web-based blog

License:	GPLv2
Group:		System/Servers
URL:		http://www.dotclear.net
Source0:	http://download.dotclear.org/latest/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		php53.patch
Requires:		php-xml 
Requires:		php-iconv
Requires:		php-mbstring
BuildArch:	noarch

%description
dotclear is a multilingual web application developed in php. 
It provides personal blogs and trackbacks to react,
but also can be used in a multi-user mode with several right levels.

%prep
%setup -q -n %{name}
%patch0 -p1

%build

%install
# install files
install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp -aRf * %{buildroot}%{_var}/www/%{name}
for i in CHANGELOG CREDITS LICENSE README; do
	rm -f %{buildroot}%{_var}/www/%{name}/$i
done

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
Alias /dotclear /var/www/dotclear
<Directory /var/www/dotclear>
    Require all granted
</Directory>

<Directory /var/www/dotclear/admin/install>
    Require local granted
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"
</Directory>
EOF

# remove .htaccess files
find %{buildroot}%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

# fix exectuable bit 
find %{buildroot}%{_var}/www/%{name} -type f -exec chmod 644 {} \;
chmod 755 %{buildroot}%{_var}/www/%{name}/inc/dbschema/upgrade-cli.php

cat > README.urpmi <<EOF
Dotclear is a database driven blogging program designed to make it exceedingly
easy to publish an online blog, sometimes also called a weblog or journal.

Once this package is installed, there are a few configuration items which need
to be performed before the blog is usable.  First, you need to install
Mysql or PostgreSQL database and corresponding php modules:

# urpmi mysql php-mysql

or 

# urpmi postgresql php-pgsql

Then, you need to establish a username and password to connect to your
MySQL database as, and make both MySQL/Postgres and Dotclear aware of this.
Let's start by creating the database and the username / password
inside MySQL first:

  # mysql
  mysql> create database dotclear;
  Query OK, 1 row affected (0.00 sec)

  mysql> grant all privileges on dotclear.* to dotclear identified by 'dotclear';
  Query OK, 0 rows affected (0.00 sec)

  mysql> flush privileges;
  Query OK, 0 rows affected (0.00 sec)

  mysql> exit
  Bye
  #

Under certain curcumstances, you may need to run variations of the "grant"
command:
mysql> grant all privileges on dotclear.* to dotclear@localhost identified by 'dotclear';
   OR
mysql> grant all privileges on dotclear.* to dotclear@'%' identified by 'dotclear';

This has created an empty database called 'dotclear', created a user named
'dotclear' with a password of 'dotclear', and given the 'dotclear' user total
permission over the 'dotclear' database.  Obviously, you'll want to select a
different password, and you may want to choose different database and user
names depending on your installation.  The specific values you choose are
not constrained, they simply need to be consistent between the database and the
config file.

Once that's done and the database server and web server have been started, 
 in your favourite web browser, enter following URL :
http://hostname/dotclear/admin/install/wizard.php  and 
follow the instructions given to you on the pages you see to set up the 
database tables and begin publishing your blog.
EOF

%files
%doc README.urpmi CHANGELOG CREDITS LICENSE
%config(noreplace) %{_webappconfdir}/%{name}.conf
%dir %{_var}/www/%{name}
%{_var}/www/%{name}/*.php
%{_var}/www/%{name}/*.md
#%{_var}/www/%{name}/inc/
%{_var}/www/%{name}/admin
#%{_var}/www/%{name}/cache
%{_var}/www/%{name}/db
%{_var}/www/%{name}/locales
%{_var}/www/%{name}/plugins
%{_var}/www/%{name}/public
%{_var}/www/%{name}/themes
%attr(0775,root,apache) %{_var}/www/%{name}/cache
%attr(0775,root,apache) %{_var}/www/%{name}/inc/


