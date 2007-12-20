%define name		axiom
%define axvers		20050901
%define release		 %mkrel 0.%axvers.1
%define x11shlibdir	%{_prefix}/X11R6/%{_lib}

Summary: Symbolic Computation Program
Name: %{name}
Version: 3.4
Release: %{release}
Source0: %{name}-Sept2005-src.tar.bz2
License: BSD/GPL
Group: Sciences/Mathematics
Url: http://axiom.axiom-developer.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgmp-devel
BuildRequires: libncurses-devel
BuildRequires: libreadline-devel
BuildRequires: binutils-devel
BuildRequires: X11-devel xpm-static-devel
BuildRequires: tetex tetex-latex
BuildRequires: gawk
BuildRequires: ghostscript
Requires:      xterm

%description
Axiom is a general purpose Computer Algebra system. 
It is useful for research and development of mathematical algorithms. 
It defines a strongly typed, mathematically correct type hierarchy. 
It has a programming language and a built-in compiler. 

%prep
%setup -q -n %{name}

%build
export AXIOM=`pwd`/mnt/linux
export PATH=$AXIOM/bin:$PATH

# parallel build fail
make XLIB=%{x11shlibdir} LDF=-L%{x11shlibdir}

%install
rm -rf $RPM_BUILD_ROOT

# create the directory structure
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/algebra
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/autoload
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/bin
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/graph
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/ps
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/boot
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/lib
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/interp
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/algebra
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/input
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/graph
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/hypertex
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/hypertex/pages
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/hypertex/bitmaps
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/msgs
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/viewports
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/src
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/src/algebra
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/input

pushd mnt/linux

# create *.VIEW directory structure
# and copy the content
( cd doc/viewports; for i in *.VIEW ; do \
	install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/viewports/$i; \
	install -m 644 $i/{data,graph*,image*} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/viewports/$i; \
done; )

install -m644 algebra/*.o $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/algebra
install -m644 algebra/*.daase $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/algebra
install -m644 autoload/*.o $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/autoload
install -m755 lib/{command.list,copyright,ex2ht,hthits,htsearch,presea,session,spadbuf,spadclient,summary,view2D,view3D,viewman} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib
install -m644 lib/graph/*.ps $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/lib/graph

# -0777 is here to tell perl to stop the substiution at the fist match
perl -pi -0777 -e "s|AXIOM=.*|AXIOM=%{_libdir}/%{name}-%{version}\nexport AXIOM|" bin/axiom

install -m755 bin/axiom $RPM_BUILD_ROOT%{_bindir}
install -m755 bin/{AXIOMsys,asq,clef,viewAlone,sman,booklet,boxhead,boxtail,boxup,document,htadd,htsearch,hypertex} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/bin

install -m644 doc/ps/{*.ps,*.epsi,*.eps} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/ps
install -m644 doc/*.dvi  $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/
install -m644 doc/hypertex/pages/{*.ht,*.pht,*.db}  $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/hypertex/pages
install -m644 doc/hypertex/bitmaps/{*.bitmap,*.xbm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/hypertex/bitmaps
install -m644 doc/msgs/s2-us.msgs $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/msgs
install -m644 doc/src/algebra/*.dvi $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/algebra
install -m644 doc/src/boot/* $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/boot
install -m644 doc/src/graph/{*.dvi,*.sty} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/graph
install -m644 doc/src/input/{*.dvi,*.sty} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/input
install -m644 doc/src/interp/{*.dvi,*.sty} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/doc/src/interp

install -m644 input/{*.input,*.as} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/input
popd

cat > $RPM_BUILD_ROOT%{_bindir}/AXIOMsys <<EOF
#!/bin/sh
AXIOM=%{_libdir}/%{name}-%{version}
export AXIOM
PATH=\$AXIOM/bin:\$PATH
export PATH
exec \$AXIOM/bin/AXIOMsys "\$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc license/LICENSE.*
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*
%attr(755,root,root) %{_bindir}/AXIOMsys
%{_bindir}/axiom

