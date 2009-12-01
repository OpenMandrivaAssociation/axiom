%define axvers	20081101
%define AXIOM	%{_libdir}/%{name}-%{version}

Summary:	Symbolic Computation Program
Name:		axiom
Version:	3.4
Release:	%mkrel 0.%{axvers}.1
Source0:	%{name}-nov2008-src.tgz
# This is the gcl package, as of 20091125, BUILD dir after rpmbuild -bp
# This allows having an axiom binary that doesn't require
#	echo 0 >/proc/sys/kernel/randomize_va_space
# or equivalent sysctl call
Source1:	gcl-2.6.8pre.tgz
Source2:	gcl-2.6.8pre.h.linux.defs.patch
Source3:	gcl-2.6.8pre.unixport.makefile.patch
Source4:	gcl-2.6.8pre.unixport.init_gcl.lsp.in.patch
# Fix underlinking - AdamW 2008/07
Patch0:		axiom-july2008-underlink.patch
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
cp -f %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} zips
%patch0 -p1 -b .underlink

%build
export AXIOM=`pwd`/mnt/linux
export PATH=$AXIOM/bin:$PATH

# parallel build fail
make XLIB=%{_libdir} LDF=-L%{_libdir} MAKE=make

%install
mkdir -p %{buildroot}%{_libdir}/%{name}-%{version}
cp -far mnt/linux/* %{buildroot}%{_libdir}/%{name}-%{version}

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/axiom <<EOF
#!/bin/sh
AXIOM=%{AXIOM}
export AXIOM
PATH=\$AXIOM/bin:\$PATH
export PATH
exec \$AXIOM/bin/sman "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/axiom

# correct some %{buildroot} references
perl -pi -e 's|%{buildroot}/axiom/mnt/linux|%{AXIOM}|;'		\
	%{buildroot}%{AXIOM}/bin/index.html			\
	%{buildroot}%{AXIOM}/bin/man/man1/*.1			\
	%{buildroot}%{AXIOM}/bin/lib/pipedocs

# remove executable bit of some text files
chmod -x %{buildroot}%{AXIOM}/lib/{command.list,copyright}	\
	`find %{buildroot}%{AXIOM} -name axiom.sty`

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license/license.*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*
%{_bindir}/axiom
