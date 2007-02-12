Summary:	Bjorb - secure TCP relay software
Summary(pl.UTF-8):   Bjorb - oprogramowanie do bezpiecznego przekazywania TCP
Name:		bjorb
Version:	0.5.5p1
Release:	0.1
License:	see COPYRIGHT, modified is not distributable
Group:		Networking/Daemons
Source0:	http://people.FreeBSD.org/~foxfair/distfiles/%{name}-%{version}.tar.gz
# Source0-md5:	abea77967a1a0fd2dcd1b407d652b3bf
Source1:	%{name}.init
Patch0:		%{name}-fbsd_patches.patch
Patch1:		%{name}-Makefile.in.patch
Patch2:		%{name}-sysconfdir.patch
URL:		http://www.hitachi-ms.co.jp/bjorb/
BuildRequires:	autoconf
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
Bjorb is secure TCP relay software. Bjorb provides you, secure
end-to-end connection over insecure network such as Internet.
Features:
- Encrypt/decrypt any "static port" TCP connection with SSL.
- Restrict access by IP address.
- Server side certification.
- Client side certification.

%description -l pl.UTF-8
Bjorb to oprogramowanie do bezpiecznego przekazywania TCP. Bjorb
udostępnia bezpieczne połączenie końcówek przez niebezpieczną sieć
taką jak Internet. Możliwości:
- Szyfrowanie/odszyfrowywanie dowolnego połączenia TCP na "statycznym
  porcie" przy użyciu SSL
- Ograniczanie dostępu według adresów IP.
- Certyfikacja po stronie serwera.
- Certyfikacja po stronie klienta.

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

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/{bjorb.conf.sample,bjorb.conf}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "Bjorb daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT README doc/sample/bjorb.conf.doc doc/sample/bjorb.conf.sample
%lang(ja) %doc ChangeLog.jp COPYRIGHT.jp README.jp doc/features.jp doc/bjorb.conf.5.jp.txt
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
