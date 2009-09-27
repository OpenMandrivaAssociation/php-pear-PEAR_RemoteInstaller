%define		_class		PEAR
%define		_subclass	Command
%define		upstream_name	%{_class}_RemoteInstaller

Summary:	PEAR Remote installation plugin through FTP
Name:		php-pear-%{upstream_name}
Version:	0.3.1
Release:	%mkrel 5
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PEAR_RemoteInstaller/
Source0:	http://pear.php.net/get/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :

%preun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
