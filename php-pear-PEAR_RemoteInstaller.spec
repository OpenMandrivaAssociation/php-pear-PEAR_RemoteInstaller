%define		_class		PEAR
%define		_subclass	Command
%define		upstream_name	%{_class}_RemoteInstaller

Name:		php-pear-%{upstream_name}
Version:	0.3.1
Release:	%mkrel 13
Summary:	PEAR Remote installation plugin through FTP
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PEAR_RemoteInstaller/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
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
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-10mdv2011.0
+ Revision: 667637
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-9mdv2011.0
+ Revision: 607133
- rebuild

* Sat Nov 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.1-8mdv2010.1
+ Revision: 467949
- spec cleanup
- use pear installer
- don't ship tests, even in documentation
- own all directories
- use rpm filetriggers starting from mandriva 2010.1

* Thu Oct 01 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.1-7mdv2010.0
+ Revision: 452039
- fix %%postun

* Sun Sep 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.1-6mdv2010.0
+ Revision: 450269
- use pear installer
- use fedora %%post/%%postun

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.3.1-5mdv2010.0
+ Revision: 426665
- rebuild

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-4mdv2009.1
+ Revision: 321893
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.3.1-3mdv2009.0
+ Revision: 224842
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-2mdv2008.1
+ Revision: 178534
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Apr 20 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-1mdv2008.0
+ Revision: 15547
- 0.3.1


* Sat Nov 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdv2007.0
+ Revision: 81195
- Import php-pear-PEAR_RemoteInstaller

* Sat Apr 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1mdk
- 0.3.0

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdk
- 0.2.0
- new group (Development/PHP)

* Tue Nov 08 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdk
- initial Mandriva package

