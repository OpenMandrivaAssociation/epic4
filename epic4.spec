%define help_version    20050315

Name:           epic4
Version:        2.8
Release:        %mkrel 1
Summary:        (E)nhanced (P)rogrammable (I)RC-II (C)lient
Group:          Networking/IRC
License:        BSD
URL:            http://www.epicsol.org/
Source0:        ftp://ftp.epicsol.org/pub/epic/EPIC4-PRODUCTION/epic4-%{version}.tar.bz2
Source1:        ftp://ftp.epicsol.org/pub/epic/EPIC4-PRODUCTION/epic4-help-%{help_version}.tar.gz
Source2:        epic.wmconfig
Source3:        ircII.servers
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
  --add-category="X-MandrivaLinux-Internet-Chat" \
  --dir %{buildroot}%{_datadir}/applications %{name}.desktop

%post
%{update_menus}
%{update_desktop_database}

%postun
%{clean_menus}
%{clean_desktop_database}

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
