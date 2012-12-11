%define tarversion 2_8_0

%define major 28

%define libname %mklibname xerces-c %major
%define libdev %mklibname xerces-c %major -d 

%define enable_debug 0
%{?_enable_debug: %{expand: %%global enable_debug 1}}

Name: xerces-c%major
Version: 2.8.0
Release: %mkrel 5
Epoch: 1
URL: http://xml.apache.org/xerces-c/
License: Apache
Source0: xerces-c-src_%{tarversion}.tar.gz
Patch0: xerces-c-lib64.patch
# Most of apps 
Patch1: xerces-c-pvtheader.patch
# XQilla patches
Patch2: xercesc_content_type.patch
Patch3: xercesc_regex.patch
Patch4: xerces-c-2.8.x-CVE-2009-1885.diff
Summary:	Xerces-C++ validating XML parser
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: zlib-devel
BuildRequires: libicu-devel

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.


#----------------------------------------------------------------------

%package -n %libname
Group: System/Libraries
Summary: Xerces-c library

%description -n %libname
xerces-c library

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root,-)
%doc LICENSE.txt
%_libdir/libxerces-*.so.*

#----------------------------------------------------------------------

%package -n %libdev
Requires: %libname = %epoch:%version-%release
Group: Development/C
Summary:	Header files for Xerces-C++ validating XML parser
Provides:	xerces-c%major-devel = %epoch:%version-%release
Conflicts:	%{mklibname xerces-c 0 -d}
Conflicts:	%{mklibname xerces-c 3.0 -d}

%description -n %libdev
Header files you can use to develop XML applications with Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%files -n %libdev
%defattr(-,root,root,-)
%_libdir/libxerces-c.so
%_libdir/libxerces-depdom.so
%_includedir/xercesc

#----------------------------------------------------------------------

%prep
%setup -q -n xerces-c-src_%{tarversion}
%if "%{_lib}" != "lib"
%patch0 -p1 -b .orig
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0 -b .CVE-2009-1885

%build
export XERCESCROOT=%_builddir/xerces-c-src_%{tarversion}

cd $XERCESCROOT/src/xercesc
./runConfigure \
	-plinux \
	-cgcc \
	-xg++ \
	-minmem \
	-nsocket \
	-tnative \
	-rpthreads \
%if %{enable_debug}
	-d \
%endif
%if "%{_lib}" != "lib"
    -b "64" \
%else
    -b "32" \
%endif
    -P %_prefix \
	-C --libdir=%_libdir

make

%install
rm -rf %buildroot

export XERCESCROOT=%_builddir/xerces-c-src_%{tarversion}
cd $XERCESCROOT/src/xercesc
%makeinstall_std

%clean
rm -rf %buildroot


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.8.0-5mdv2011.0
+ Revision: 615542
- the mass rebuild of 2010.1 packages

* Sun Aug 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.8.0-4mdv2010.1
+ Revision: 422640
- renamed to xerces-c28
- fix deps
- "fork" this one to prepare for 3.0.1

* Sun Aug 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.8.0-3mdv2010.0
+ Revision: 422544
- P4: security fix for CVE-2009-1885

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1:2.8.0-2mdv2009.0
+ Revision: 266081
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Apr 24 2008 Helio Chissini de Castro <helio@mandriva.com> 1:2.8.0-1mdv2009.0
+ Revision: 197274
- Disable nrproc compilation
- Added debug compiling check turned off by default
- Added xqilla content patches ( needed for xqilla 2.2 )
- New upstream version
- Compile with pthreads
- Fixed devel package name
- fixed proper soname

  + Thierry Vignaud <tv@mandriva.org>
    - fix summary-not-capitalized
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Nov 29 2007 Thierry Vignaud <tv@mandriva.org> 1:2.7.0-7mdv2008.1
+ Revision: 113935
- fix invalid group

* Fri Nov 23 2007 Thierry Vignaud <tv@mandriva.org> 1:2.7.0-6mdv2008.1
+ Revision: 111613
- rebuild for new libicu

* Mon May 07 2007 Helio Chissini de Castro <helio@mandriva.com> 1:2.7.0-5mdv2008.0
+ Revision: 24815
- Obsoletes xerces-c packages with samples binaries. This is not necessary
- Fixed 64 build
- Get rid of nls, use ICU


* Tue Sep 19 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-09-19 14:46:32 (62357)
- Most of packages like pathan or xquery depends on private headers. If we want avoid include an internal copy of xerces-c in every package, we need install base impl headers. This will enable, along with a post 4.2 db, the construction of dbxml and reduce size of many applications with code embedded

* Wed Aug 23 2006 Thierry Vignaud <tvignaud@mandriva.com>
+ 2006-08-23 20:57:52 (57755)
- fix group

* Wed Aug 16 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-16 15:23:43 (56359)
- Fixed x86_64 issues

* Tue Aug 15 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-15 13:18:46 (56183)
- Raise epoch to make proper devel to be installed. Last sonam was wrong named 26, since 26 is major, and minor is 0

* Tue Aug 15 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-15 06:18:36 (56161)
- No distributed compilation

* Tue Aug 15 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-15 06:10:46 (56155)
- import xerces-c-2.7.0-1mdv2007.0

* Mon Dec 13 2004 Warly <warly@mandrakesoft.com> 2.6.0-2mdk
- rebuild without libxerces25 dependencies

* Wed Aug 18 2004 Warly <warly@mandrakesoft.com> 2.5.0-0.20040818.1mdk
- update to latest CVS version

* Fri Jul 23 2004 Warly <warly@mandrakesoft.com> 2.5.0-0.20040723.1mdk
- go to version 20040723104641 for bug 10387

* Tue Jul 20 2004 Warly <warly@mandrakesoft.com> 2.5.0-0.20040720.1mdk
- new version (based on CVS version)

