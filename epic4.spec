%define help_version    20050315

Name:           epic4
Version:        2.10.1
Release:        1
Summary:        (E)nhanced (P)rogrammable (I)RC-II (C)lient
Group:          Networking/IRC
License:        BSD
URL:            http://www.epicsol.org/
Source0:        ftp://ftp.epicsol.org/pub/epic/EPIC4-PRODUCTION/epic4-%{version}.tar.bz2
Source1:        ftp://ftp.epicsol.org/pub/epic/EPIC4-PRODUCTION/epic4-help-%{help_version}.tar.gz
Source2:        epic.wmconfig
Source3:        ircII.servers
# Don't include term.h, it conflicts with termcap.h - AdamW 2008/12
Patch0:		epic4-2.10-include.patch
Obsoletes:      ircii-EPIC4 < %{version}-%{release}
Provides:       ircii-EPIC4 = %{version}-%{release}
Obsoletes:      epic < %{version}-%{release}
Provides:       epic = %{version}-%{release}
Obsoletes:      epic-help < %{help_version}
Provides:       epic-help = %{help_version}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:  desktop-file-utils
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  tcl-devel
BuildRequires:  perl-devel

%description
EPIC is the (E)nhanced (P)rogrammable (I)RC-II (C)lient.  It
is a program used to connect to IRC servers around the globe
so that the user can ``chat'' with others.

%prep 
%setup -q -a 1 -T -b 0
%patch0 -p1 -b .include
%{__rm} -r `%{_bindir}/find -type d -name CVS`

%build
%{configure2_5x} --with-ipv6 \
                 --with-perl \
                 --with-ssl \
                 --without-socks \
                 --without-socks5 \
                 --with-tcl

%{make} wserv_exe="%{_libexecdir}"

%install
%{__rm} -rf %{buildroot}
%{makeinstall} installhelp sharedir=%{buildroot}%{_datadir} libexecdir=%{buildroot}%{_libexecdir}
%{__install} -m644 %{SOURCE3} %{buildroot}%{_datadir}/epic
%{__chmod} 755 %{buildroot}%{_datadir}/epic/script/epic-crypt-gpg{,-aa}

%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Epic
Comment=EPIC is the (E)nhanced (P)rogrammable (I)RC-II (C)lient.
Exec=%{_bindir}/%{name} 
Icon=irc_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-Chat;Network;IRCClient;
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{_bindir}/desktop-file-install --vendor="mandriva" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{name}.desktop

# Empty docs make rpmlint go crazy
find %buildroot -size 0 |xargs rm -f

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc INSTALL UPDATES KNOWNBUGS BUG_FORM doc/*
%{_bindir}/*
%{_libexecdir}/*
%dir %{_datadir}/epic
%config(noreplace) %{_datadir}/epic/ircII.servers
%{_datadir}/epic/script/
%{_datadir}/epic/help/
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.10-4mdv2011.0
+ Revision: 610380
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 2.10-3mdv2010.1
+ Revision: 537455
- rebuild

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 2.10-2mdv2010.0
+ Revision: 437468
- rebuild

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 2.10-1mdv2009.1
+ Revision: 311087
- remove mdv menu category
- add include.patch (fix build by dropping an include that introduces conflicts)
- new release 2.10

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.8-3mdv2009.0
+ Revision: 244928
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Nov 10 2007 David Walluck <walluck@mandriva.org> 2.8-1mdv2008.1
+ Revision: 107317
- 2.8

* Mon Sep 10 2007 David Walluck <walluck@mandriva.org> 2.6-2mdv2008.0
+ Revision: 83959
- rebuild
- update BuildRequires
- don't force removal of CVS dirs
- use %%{_libexecdir} macro
- kill the old Debian menu


* Sun Feb 04 2007 David Walluck <walluck@mandriva.org> 2.6-1mdv2007.0
+ Revision: 116127
- 2.6
- Import epic4

* Wed Sep 06 2006 Nicolas L�cureuil <neoclust@mandriva.org> 2.2-3mdv2007.0
- XDG

* Mon Jan 09 2006 Marcel Pol <mpol@mandriva.org> 2.2-2mdk
- rebuild for new openssl

* Mon Jun 13 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.2-1mdk
- 2.2

* Fri May 06 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.1.1-2mdk
- lib64 fix
- fix menu section
- %%mkrel

* Thu Nov 11 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.1.1-1mdk
- 2.1.1
- drop P1 & P2 (fixed upstream)

* Fri May 07 2004 Michael Scherer <misc@mandrake.org> 1.0.1-7mdk 
- change Group

* Wed Apr 28 2004 Michael Scherer <misc@mandrake.org> 1.0.1-6mdk 
- [DIRM]
- removed useless messages ( ftp no longer valid )
- rpmbuildupdate aware
- correct rpmlint warnings

