# TODO
# - create .jar instead of using two trees of .classes
# - external dep for lib/* classes
%define		ver	%(echo %{version} | tr . _)
Summary:	Pixy: XSS and SQLI Scanner for PHP Programs
Name:		pixy
Version:	3.02
Release:	0.5
License:	Gentleperson's Agreement
Group:		Development/Languages/Java
Source0:	http://pixybox.seclab.tuwien.ac.at/pixy/dist/%{name}_%{ver}.zip
# Source0-md5:	037873e8cdfc0d616697798837d76706
URL:		http://pixybox.seclab.tuwien.ac.at/pixy/index.php
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	jre
Requires:	junit
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}

%description
Cross-site scripting (XSS) and SQL injection (SQLI) vulnerabilities
are present in many modern web applications, and are reported
continuously on pages such as BugTraq. In the past, finding such
vulnerabilities usually involved manual source code audits.
Unfortunately, this manual vulnerability search is a very tiresome and
error-prone task.

%prep
%setup -q -n Pixy

rm -f lib/junit.jar
# create startup script in shell
cat > pixy.sh <<'EOF'
#!/bin/sh
# minimum and maximum memory that you want Pixy to use
mem_min=256m
mem_max=1024m

# setup pixy_home, maybe overridden by env var
PIXY_HOME="${PIXY_HOME:-$HOME/.pixy}"
if [ ! -d "$PIXY_HOME" ]; THEN
	echo >&2 "Setting up $PIXY_HOME"
	mkdir -m700 "$PIXY_HOME"
	mkdir -m700 "$PIXY_HOME/config"
	cp -a %{_appdir}/config/* "$PIXY_HOME/config"
fi

CLASSPATH="%{_appdir}/lib:%{_appdir}/class:$(find-jar junit)"
exec java -Xms$mem_min -Xmx$mem_max -Dpixy.home="$PIXY_HOME" -classpath "$CLASSPATH" at.ac.tuwien.infosys.www.pixy.Checker -a -y xss:sql ${1:+"$@"}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir}}
# classes. TODO: include into jar, both of these
cp -a lib build/class $RPM_BUILD_ROOT%{_appdir}
# sample config
cp -a config $RPM_BUILD_ROOT%{_appdir}
install pixy.sh $RPM_BUILD_ROOT%{_bindir}/pixy

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pixy
%{_appdir}
