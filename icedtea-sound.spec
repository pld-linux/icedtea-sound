# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# build with tests (use network)

%define	use_jdk	icedtea7

Summary:	Collection of audio SPI implementations for Java
Name:		icedtea-sound
Version:	1.0.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://icedtea.wildebeest.org/download/source/%{name}-%{version}.tar.xz
# Source0-md5:	e4d8013735ae517c015327924dabf3ed
URL:		http://icedtea.classpath.org/wiki/IcedTea-Sound
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_tests:BuildRequires:	java-junit}
BuildRequires:	jpackage-utils
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpm-javaprov
%{?buildrequires_jdk}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IcedTea-Sound contains the PulseAudio provider which was removed from
IcedTea itself from 2.5.0 onwards.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-jdk-home="%{java_home}" \
	--docdir="%{_javadocdir}/%{name}-%{version}" \
	%{!?with_javadoc:--disable-docs}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

rm $RPM_BUILD_ROOT%{_datadir}/%{name}/src.zip

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libicedtea-sound.so.1.0.1
%attr(755,root,root) %{_libdir}/libicedtea-sound.so
%{_datadir}/%{name}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
