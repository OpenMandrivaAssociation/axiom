%define axvers	20091101

Summary:	Symbolic Computation Program
Name:		axiom
Version:	3.4
Release:	%mkrel 0.%{axvers}.1
Source0:	%{name}-nov2008-src.tgz
# This is the gcl package, as of 20091123, BUILD dir after rpmbuild -bp
# This allows having an axiom binary that doesn't require
#	echo 0 >/proc/sys/kernel/randomize_va_space
# or equivalent sysctl call
Source1:	gcl-2.6.8pre.tgz
# Fix underlinking - AdamW 2008/07
Patch0:		axiom-july2008-underlink.patch
# Use the new snapshot we forced into the build (see above), and
# disable one patch which won't apply to it - AdamW 2008/08
Patch1:		axiom-nov2008-gcl.patch
License:	BSD
Group:		Sciences/Mathematics
URL:		http://axiom.axiom-developer.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libgmp-devel
BuildRequires:	libncurses-devel
BuildRequires:	libreadline-devel
BuildRequires:	binutils-devel
BuildRequires:	libxau-devel
BuildRequires:	libice-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxdmcp-devel
BuildRequires:	libxext-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxt-devel
BuildRequires:	x11-proto-devel
BuildRequires:	x11-xtrans-devel
BuildRequires:	xpm-static-devel
BuildRequires:	tetex
BuildRequires:	tetex-latex
BuildRequires:	gawk
BuildRequires:	ghostscript
Requires:	xterm

%description
Axiom is a general purpose Computer Algebra system. 
It is useful for research and development of mathematical algorithms. 
It defines a strongly typed, mathematically correct type hierarchy. 
It has a programming language and a built-in compiler. 

%prep
%setup -q -n %{name}
cp -f %{SOURCE1} zips
%patch0 -p1 -b .underlink
%patch1 -p1 -b .gcl

%build
export AXIOM=`pwd`/mnt/linux
export PATH=$AXIOM/bin:$PATH

# parallel build fail
make XLIB=%{_libdir} LDF=-L%{_libdir}

%install
mkdir -p %{buildroot}%{_libdir}/%{name}-%{version}
cp -far mnt/linux/* %{buildroot}%{_libdir}/%{name}-%{version}

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/axiom <<EOF
#!/bin/sh
AXIOM=%{_libdir}/%{name}-%{version}
export AXIOM
PATH=\$AXIOM/bin:\$PATH
export PATH
exec \$AXIOM/bin/AXIOMsys "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/axiom

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license/license.*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*
%{_bindir}/axiom
