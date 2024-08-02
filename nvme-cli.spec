Summary:	NVMe management command line interface
Summary(pl.UTF-8):	Konsolowy interfejs do zarządzania NVMe
Name:		nvme-cli
Version:	2.10
Release:	1
License:	GPL v2+
Group:		Applications
#Source0Download: https://github.com/linux-nvme/nvme-cli/releases
Source0:	https://github.com/linux-nvme/nvme-cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	50aca763b0c931dfb2af79c6762958e5
URL:		https://github.com/linux-nvme/nvme-cli
BuildRequires:	asciidoc
BuildRequires:	json-c-devel >= 0.14
BuildRequires:	linux-libc-headers >= 7:6.6
BuildRequires:	libnvme-devel >= 1.10
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	xmlto
Requires:	json-c >= 0.14
Requires:	libnvme >= 1.10
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
Requires:	bash-completion >= 1:2.0
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

# correct wrong filename, will be fixed in next release
# https://github.com/linux-nvme/nvme-cli/issues/2448
%{__mv} Documentation/nvme-ocp-unsupported-reqs-log{-pages,}.txt
%{__sed} -i -e 's/nvme-ocp-unsupported-reqs-log-pages/nvme-ocp-unsupported-reqs-log/' \
	Documentation/meson.build

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
%dir %{_sysconfdir}/nvme
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nvme/discovery.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/65-persistent-net-nbft.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-nvmf-autoconnect.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/71-nvmf-netapp.rules
%attr(755,root,root) %{_sbindir}/nvme
%{_mandir}/man1/nvme.1*
%{_mandir}/man1/nvme-*.1*
%{systemdunitdir}/nvmefc-boot-connections.service
%{systemdunitdir}/nvmf-autoconnect.service
%{systemdunitdir}/nvmf-connect-nbft.service
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
