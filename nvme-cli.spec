Summary:	NVMe management command line interface
Summary(pl.UTF-8):	Konsolowy interfejs do zarządzania NVMe
Name:		nvme-cli
Version:	1.12
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/linux-nvme/nvme-cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	94997b72a63b5bc26c2862c7603bb6e3
URL:		https://github.com/linux-nvme/nvme-cli
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dracutdir	/usr/lib/dracut

%description
nvme-cli provides NVM-Express user space tooling for Linux.

%description -l pl.UTF-8
nvme-cli dostarcza narzędzia zarządzania NVM-Express.

%package -n dracut-nvmf
Summary:	nvmf support for Dracut
Summary(pl.UTF-8):	Obsługa nvmf dla Dracut
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	dracut
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n dracut-nvmf
nvmf support for Dracut.

%description -n dracut-nvmf -l pl.UTF-8
Obsługa nvmf dla Dracut.

%package -n bash-completion-nvme-cli
Summary:	bash-completion for nvme-cli
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla nvme-cli
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-nvme-cli
bash-completion for nvme-cli.

%description -n bash-completion-nvme-cli -l pl.UTF-8
Bashowe dopełnianie składni dla nvme-cli.

%package -n zsh-completion-nvme-cli
Summary:	zsh-completion for nvme-cli
Summary(pl.UTF-8):	Dopełnianie składni w zsh dla nvme-cli
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description -n zsh-completion-nvme-cli
zsh-completion for nvme-cli.

%description -n zsh-completion-nvme-cli -l pl.UTF-8
Dopełnianie składni w zsh dla nvme-cli.

%prep
%setup -q

%build

PREFIX=%{_prefix} \
LDFLAGS="${LDFLAGS:-%rpmldflags}" \
CFLAGS="${CFLAGS:-%rpmcflags} -I." \
CXXFLAGS="${CXXFLAGS:-%rpmcxxflags}" \
CPPFLAGS="${CPPFLAGS:-%rpmcppflags}" \
%{?__cc:CC="%{__cc}"} \
%{?__cxx:CXX="%{__cxx}"} \
V=1 \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT \
	DRACUTDIR=%{dracutdir} \
	SYSTEMDDIR=%{systemdunitdir}/..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-nvmf-autoconnect.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/71-nvmf-iopolicy-netapp.rules
%attr(755,root,root) %{_sbindir}/nvme
%{_mandir}/man1/nvme*
%{systemdunitdir}/nvmefc-boot-connections.service
%{systemdunitdir}/nvmf-autoconnect.service
%{systemdunitdir}/nvmf-connect.target
%{systemdunitdir}/nvmf-connect@.service

%files -n dracut-nvmf
%defattr(644,root,root,755)
%{dracutdir}/dracut.conf.d/70-nvmf-autoconnect.conf

%files -n bash-completion-nvme-cli
%defattr(644,root,root,755)
%{bash_compdir}/nvme

%files -n zsh-completion-nvme-cli
%defattr(644,root,root,755)
%{zsh_compdir}/_nvme
