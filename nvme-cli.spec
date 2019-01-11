Summary:	NVMe management command line interface
Summary(pl.UTF-8):	Konsolowy interfejs do zarządzania NVMe
Name:		nvme-cli
Version:	1.7
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/linux-nvme/nvme-cli/archive/v%{version}.tar.gz
# Source0-md5:	ec64bc935957f6bc52109bde704a5a42
URL:		https://github.com/linux-nvme/nvme-cli
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nvme-cli provides NVM-Express user space tooling for Linux.

%description -l pl.UTF-8
nvme-cli dostarcza narzędzia zarządzania NVM-Express.

%package -n bash-completion-nvme-cli
Summary:	bash-completion for nvme-cli
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla nvme-cli
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-nvme-cli
bash-completion for nvme-cli.

%description -n bash-completion-nvme-cli -l pl.UTF-8
Bashowe dopełnianie składni dla nvme-cli.

%package -n zsh-completion-nvme-cli
Summary:	zsh-completion for nvme-cli
Summary(pl.UTF-8):	Dopełnianie składni w zsh dla nvme-cli
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_sbindir}/nvme
%{_mandir}/man1/nvme*

%files -n bash-completion-nvme-cli
%defattr(644,root,root,755)
%{bash_compdir}/nvme

%files -n zsh-completion-nvme-cli
%defattr(644,root,root,755)
%{zsh_compdir}/_nvme
