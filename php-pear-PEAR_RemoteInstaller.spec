%define		_class		PEAR
%define		_subclass	Command
%define		_status		alpha
%define		_pearname	%{_class}_RemoteInstaller

Summary:	%{_pearname} - PEAR Remote installation plugin through FTP
Name:		php-pear-%{_pearname}
Version:	0.3.1
Release:	%mkrel 1
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/PEAR_RemoteInstaller/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix

%description
Originally part of the 1.4.0 new features, remote installation
through FTP is now its own package. This package adds the commands
"remote-install" "remote-upgrade" "remote-uninstall" and 
"remote-upgrade-all" to the PEAR core.
    
To take advantage, you must have a config file on the remote ftp
server and full access to the server to create and remove files.
The config-create command can be used to get started, and the
remote_config configuration variable is set to the full URL as
in "ftp://ftp.example.com/path/to/pear.ini"
 
After this is done, install/upgrade as normal using the remote*
commands as if they were local.

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install -m0644 %{_pearname}-%{version}/%{_class}/*.php %{buildroot}%{_datadir}/pear/%{_class}
install -m0644 %{_pearname}-%{version}/%{_class}/%{_subclass}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/*.php
%{_datadir}/pear/packages/%{_pearname}.xml
