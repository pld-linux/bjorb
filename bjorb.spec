# TODO: initscript
Summary:	Bjorb - secure TCP relay software.
Name:		bjorb
Version:	0.5.5p1
Release:	0.1
License:	see COPYRIGHT
Group:		Networking/Daemons
Source0:	http://people.FreeBSD.org/~foxfair/distfiles/%{name}-%{version}.tar.gz
# Source0-md5:	abea77967a1a0fd2dcd1b407d652b3bf
# http://www.freebsd.org/cgi/cvsweb.cgi/ports/security/bjorb/files/
Patch0:		%{name}-fbsd_patches.patch
Patch1:		%{name}-Makefile.in.patch
Patch2:		%{name}-sysconfdir.patch
URL:		http://www.hitachi-ms.co.jp/bjorb/
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	openssl-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bjorb is secure TCP relay software. Bjorb provides you, secure
end-to-end connection over insecure network such as Internet.
Features:
 1. Encrypt/decrypt any "static port" TCP connection with SSL.
 2. Restrcit access by IP address.
 3. Server side certification.
 4. Client side certification.

%define _sysconfdir /etc/%{name}	

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__autoconf}
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd src
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/{bjorb.conf.sample,bjorb.conf}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT README doc/sample/bjorb.conf.doc doc/sample/bjorb.conf.sample
%lang(ja) %doc ChangeLog.jp COPYRIGHT.jp README.jp doc/features.jp doc/bjorb.conf.5.jp.txt
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
