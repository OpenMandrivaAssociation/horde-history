%define prj    Horde_History

%define xmldir  %{_var}/lib/pear
%define peardir %(pear config-get php_dir 2> /dev/null)

Name:          horde-history
Version:       0.0.2
Release:       %mkrel 1
Summary:       API for tracking the history of an object.
License:       LGPL
Group:         Networking/Mail
Url:           http://pear.horde.org/index.php?package=%{prj}
Source0:       %{prj}-%{version}.tgz
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Requires(pre): %{_bindir}/pear
Requires:      php-pear-channel-horde
BuildRequires: horde-framework
BuildRequires: php-pear
BuildRequires: php-pear-channel-horde

%description
This API provides a way to track changes on arbitrary pieces of data
in Horde applications.


%prep
%setup -q -n %{prj}-%{version}

%build
%__mv ../package.xml .

%install
pear install --packagingroot %{buildroot} --nodeps package.xml

%__rm -rf %{buildroot}/%{peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

%__mkdir_p %{buildroot}%{xmldir}
%__cp package.xml %{buildroot}%{xmldir}/%{prj}.xml

%clean
%__rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/%{prj}.xml

%postun
if [ "$1" -eq "0" ]; then
  pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/%{prj}
fi

%files
%defattr(-, root, root)
%{xmldir}/%{prj}.xml
%{peardir}/Horde/History.php
