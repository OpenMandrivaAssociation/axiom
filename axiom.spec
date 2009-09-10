%define axvers		20080701

Summary:	Symbolic Computation Program
Name:		axiom
Version:	3.4
Release:	%mkrel 0.%{axvers}.2
Source0:	%{name}-july2008-src.tgz
# Axiom build uses an in-tree gcl 2.6.8 snapshot. There's two, and you
# can switch between them with Makefile changes. Unfortunately, both
# are too old to build on x86-64 - they fail with an "I am not an
# object" error. As I can't find where the hell this was fixed, my ugly
# hack is to simply replace their in-tree snapshot with a newer one.
# This is just a 2008/08/01 snapshot of gcl CVS, tarred up. It's
# inserted into the tree in place of the shipped file of the same name
# in %setup below. - AdamW 2008/08
Source1:	gcl-2.6.8pre2.tgz
# Fix underlinking - AdamW 2008/07
Patch0:		axiom-july2008-underlink.patch
# Use the new snapshot we forced into the build (see above), and
# disable one patch which won't apply to it - AdamW 2008/08
Patch1:		axiom-july2008-gcl.patch
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
cp -f %{SOURCE1} zips/gcl-2.6.8pre2.tgz
%patch0 -p1 -b .underlink
%patch1 -p1 -b .gcl

%build
export AXIOM=`pwd`/mnt/linux
export PATH=$AXIOM/bin:$PATH

# parallel build fail
make XLIB=%{_libdir} LDF=-L%{_libdir}

%install
rm -rf %{buildroot}

# create the directory structure
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/algebra
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/autoload
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/bin
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/lib
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/lib/graph
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/ps
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/boot
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/lib
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/interp
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/algebra
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/input
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/hypertex
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/hypertex/pages
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/hypertex/bitmaps
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/msgs
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/viewports
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/src
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/src/algebra
install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/input

pushd mnt/linux

# create *.VIEW directory structure
# and copy the content
( cd doc/viewports; for i in *.VIEW ; do \
	install -d -m 755 %{buildroot}%{_libdir}/%{name}-%{version}/doc/viewports/$i; \
	install -m 644 $i/{data,graph*,image*} %{buildroot}%{_libdir}/%{name}-%{version}/doc/viewports/$i; \
done; )

install -m644 algebra/*.o %{buildroot}%{_libdir}/%{name}-%{version}/algebra
cp -R algebra/*.daase %{buildroot}%{_libdir}/%{name}-%{version}/algebra
install -m644 autoload/*.o %{buildroot}%{_libdir}/%{name}-%{version}/autoload
install -m755 lib/{command.list,copyright,ex2ht,hthits,htsearch,presea,session,spadbuf,spadclient,summary,view2d,view3d,viewman} %{buildroot}%{_libdir}/%{name}-%{version}/lib
install -m644 lib/graph/*.ps %{buildroot}%{_libdir}/%{name}-%{version}/lib/graph

# -0777 is here to tell perl to stop the substiution at the fist match
perl -pi -0777 -e "s|AXIOM=.*|AXIOM=%{_libdir}/%{name}-%{version}\nexport AXIOM|" bin/axiom

install -m755 bin/axiom %{buildroot}%{_bindir}
install -m755 bin/{AXIOMsys,asq,clef,viewalone,sman,booklet,boxhead,boxtail,boxup,document,htadd,hypertex} %{buildroot}%{_libdir}/%{name}-%{version}/bin

install -m644 doc/ps/{*.ps,*.epsi,*.eps} %{buildroot}%{_libdir}/%{name}-%{version}/doc/ps
install -m644 doc/*.dvi  %{buildroot}%{_libdir}/%{name}-%{version}/doc/
install -m644 doc/hypertex/pages/{*.ht,*.pht,*.db}  %{buildroot}%{_libdir}/%{name}-%{version}/doc/hypertex/pages
install -m644 doc/hypertex/bitmaps/{*.bitmap,*.xbm} %{buildroot}%{_libdir}/%{name}-%{version}/doc/hypertex/bitmaps
install -m644 doc/msgs/s2-us.msgs %{buildroot}%{_libdir}/%{name}-%{version}/doc/msgs
install -m644 doc/src/algebra/*.dvi %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/algebra
install -m644 doc/src/boot/* %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/boot
install -m644 doc/src/input/*.dvi %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/input
install -m644 doc/src/interp/*.dvi %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/interp
install -m644 doc/src/lib/*.dvi %{buildroot}%{_libdir}/%{name}-%{version}/doc/src/lib
install -m644 input/{*.input,*.as} %{buildroot}%{_libdir}/%{name}-%{version}/input
popd

cat > %{buildroot}%{_bindir}/AXIOMsys <<EOF
#!/bin/sh
AXIOM=%{_libdir}/%{name}-%{version}
export AXIOM
PATH=\$AXIOM/bin:\$PATH
export PATH
exec \$AXIOM/bin/AXIOMsys "\$@"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license/license.*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*
%attr(755,root,root) %{_bindir}/AXIOMsys
%{_bindir}/axiom

