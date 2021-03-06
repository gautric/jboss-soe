##
## RPM spec file to generate the jbossas RPM package for the Platform Release 
## This package provides base JBoss Enterprise Application Platform
##
## Author: Juergen Hoffmann <jhoffmann@redhat.com>
##
## Define some utility variables that are used by RPM withing this spec file.
## The tokenized variables with @@ are replaced by ant build script at runtime.
##
%define projectName @RELEASE_NAME@

%define pkg_name @PACKAGE_NAME@
%define pkg_version @PACKAGE_VERSION@
%define pkg_release @PACKAGE_RELEASE@
%define pkg_root @INSTALL_ROOT@
%define pkg_basedir @INSTALL_PREFIX@

#### Define user and group for the installed files.
%define runas_user @RUNAS_USER@
%define runas_group @RUNAS_GROUP@
%define runas_user_uid @RUNAS_USER_UID@
%define runas_group_gid @RUNAS_GROUP_GID@

Name:      %{pkg_name}
Version:   %{pkg_version}
Release:   %{pkg_release}
Epoch:     0
Summary:   Custom JBoss EAP Build
Vendor:    Red Hat
BuildArch: x86_64
Packager:  Juergen Hoffmann <jhoffmann@redhat.com>

Group:     Applications/Internet
License:   GPL v3
URL:       http://support.redhat.com/
Source0:   %{projectName}.tar
BuildRoot: %{_topdir}/buildroot/%{name}-%{version}

## Turn off for safety reasons.
AutoReq: off

#Requires: %{projectName}-tools 
#Requires: %{projectName}-tools >= %{pkg_version}

# Do not provide too much stuff and screw up other dependencies
AutoProv: off
Provides: %{name} = %{version}
Requires: apr

%description
Base JBoss Enterprise Application Platform version %{version} 
Software distribution for the v@PACKAGE_VERSION@ Release

%prep
%setup -n %{projectName}

%install
mkdir -p $RPM_BUILD_ROOT%{pkg_basedir}
cp -r * $RPM_BUILD_ROOT%{pkg_basedir}
%{__rm} -rf %{_tmppath}/jboss-eap-base.filelist
find $RPM_BUILD_ROOT%{pkg_basedir} -type d | sed '{s#'${RPM_BUILD_ROOT}'##;}' | sed '{s#\(^.*$\)#%dir "\1"#g;}' >>%{_tmppath}/jboss-eap-base.filelist
find $RPM_BUILD_ROOT%{pkg_basedir} -type f | sed '{s#'${RPM_BUILD_ROOT}'##;}' | sed '{s#\(^.*$\)#"\1"#g;}' >>%{_tmppath}/jboss-eap-base.filelist

%preun
if [ $1 = 0 ]; then
  rm -rf %{pkg_basedir}
fi


%pre
# Add the "jboss" user
getent group %{runas_group} >/dev/null || groupadd -g %{runas_group_gid} -r %{runas_group}
getent passwd %{runas_user} >/dev/null || \
  /usr/sbin/useradd -r -u %{runas_user_uid} -g %{runas_group} -s /sbin/nologin \
  -d %{pkg_basedir} -c "JBoss System user" %{runas_user}

%post
## This condition is true during first installation of package.
if [ $1 -eq 1 ]; then

  ## Put a profile specific init symlink in /etc/init.d/
  chmod 755 %{pkg_basedir}/bin/standalone.sh
  chmod 755 %{pkg_basedir}/bin/domain.sh
  chown -R %{runas_user}:%{runas_group} %{pkg_basedir}

fi
%clean
# Clean up the RPM build root directory.
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf %{_tmppath}/jboss-eap-base.filelist

#### Files for main jbossas package.
%files -f %{_tmppath}/jboss-eap-base.filelist
%dir %{pkg_basedir}
%defattr(-,%{runas_user},%{runas_group},-)

%changelog
* Thu Nov 08 2012 Juergen Hoffmann <jhoffmann@redhat.com> - 0:5.0.1-2
- initial RPM spec file
