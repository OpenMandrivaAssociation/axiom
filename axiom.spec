%define axvers	20100719
%define AXIOM	%{_libdir}/%{name}-%{version}

Summary:	Symbolic Computation Program
Name:		axiom
Version:	3.4
Release:	%mkrel 0.%{axvers}.1
Source0:	%{name}-%{axvers}.tar.bz2

# Hint to use the html interface:
# in axiom prompt type:
#	)browse
# in firefox, open localhost:8085/usr/lib64/axiom-3.4/doc/hypertex/topicspage.xhtml
# or in a shell, type:
# firefox -remote 'openURL(localhost:8085/usr/lib64/axiom-3.4/doc/hypertex/topicspage.xhtml)'
# other good starting point is:
# /usr/lib64/axiom-3.4/doc/axbook/book-index.xhtml
# of course, if you don't need axiom evaluating expressions, just use:
# file:///usr/lib64/axiom-3.4/doc/axbook/book-index.xhtml
# The interface is not complete, and there are several missing features

# git clone git://github.com/daly/axiom.git axiom
# cd axiom
# git archive --format=tar --prefix=axiom/ d7b61fa6dea4e97d3d329e7cc418ccf6df22ea3f | bzip2 > axiom-20100719.tar.bz2

# This is the gcl package, as of 20091125, BUILD dir after rpmbuild -bp
# This allows having an axiom binary that doesn't require
#	echo 0 >/proc/sys/kernel/randomize_va_space
# or equivalent sysctl call
# Fix underlinking - AdamW 2008/07
Patch0:		axiom-20091201-underlink.patch
License:	BSD
Group:		Sciences/Mathematics
URL:		http://axiom.axiom-developer.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#BuildRequires:	libgmp-devel
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
