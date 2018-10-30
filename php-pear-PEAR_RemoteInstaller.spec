%define	_class	PEAR
%define	_subclass	Command
%define	modname	%{_class}_RemoteInstaller

Summary:	PEAR Remote installation plugin through FTP
Name:		php-pear-%{modname}
Version:	0.3.2
Release:	11
License:	PHP License
Group:		Development/PHP
Url:		http://pear.php.net/package/PEAR_RemoteInstaller/
Source0:	http://download.pear.php.net/package/PEAR_RemoteInstaller-%{version}.tgz
BuildArch:	noarch
BuildRequires:	php-pear
Requires(post,preun):	php-pear
Requires:	php-pear

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
%setup -qc
mv package.xml %{modname}-%{version}/%{modname}.xml

%install
cd %{modname}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{modname}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{modname}.xml %{buildroot}%{_datadir}/pear/packages

%files
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{modname}.xml

