Summary:	NVMe management command line interface
Summary(pl.UTF-8):	Konsolowy interfejs do zarządzania NVMe
Name:		nvme-cli
Version:	2.2.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/linux-nvme/nvme-cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	00e9e1e0ed803db7f458824ccbdf2a5c
URL:		https://github.com/linux-nvme/nvme-cli
BuildRequires:	asciidoc
BuildRequires:	json-c-devel >= 0.14
BuildRequires:	libnvme-devel >= 1.2
BuildRequires:	meson >= 0.48.0
BuildRequires:	ninja
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	xmlto
BuildRequires:	zlib-devel
Requires:	json-c >= 0.14
Requires:	libnvme >= 1.2
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
BuildArch:	noarch

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
%meson build \
	-Dsystemddir=%{systemdunitdir} \
	-Dudevrulesdir=%{_sysconfdir}/udev/rules.d \
	-Ddocs=man \
	-Ddocs-build=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
