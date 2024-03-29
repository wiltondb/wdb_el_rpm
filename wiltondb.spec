Name: wiltondb
%global version_postgres_epoch 1
%global version_postgres_major 15
%global version_postgres_minor 4
%global version_wiltondb 3.3
%global version_wiltondb_pg_release 5
%global version_wiltondb_bbf_release 10
%global version_orig_tarball_package 1
%global version_postgres %{version_postgres_epoch}:%{version_postgres_major}.%{version_postgres_minor}.wiltondb%{version_wiltondb}_%{version_wiltondb_pg_release}
Version: %{version_wiltondb}_%{version_wiltondb_pg_release}_%{version_wiltondb_bbf_release}
Release: 1%{?dist}

Summary: Wilton DB build of Babelfish extensions for PostgreSQL
License: PostgreSQL
Url: https://wiltondb.com/

%global source0_filename wiltondb_%{version_wiltondb}-%{version_wiltondb_pg_release}-%{version_wiltondb_bbf_release}.orig.tar.xz
%global source0_dirname wiltondb-%{version_wiltondb}-%{version_wiltondb_pg_release}-%{version_wiltondb_bbf_release}
%global source0_sha512 26c270ac478ca3136d8696c07d2d8e8a6f5a569622ec018333295dde54177017134e0d2eba1731cfdeb8c98a700f3e958c1735759efebfbf104084baa3ed2ac4
%global source0_package %{version_wiltondb}-%{version_wiltondb_pg_release}-%{version_wiltondb_bbf_release}-%{version_orig_tarball_package}~focal
%global source0_url https://launchpad.net/~wiltondb/+archive/ubuntu/wiltondb/+sourcefiles/wiltondb/%{source0_package}/%{source0_filename}
Source0: %{source0_filename}
Source1: wiltondb-setup
	
BuildRequires: antlr4-cpp-runtime-devel
BuildRequires: bison
BuildRequires: cmake%{?el7:3}
BuildRequires: flex
BuildRequires: freetds-devel
BuildRequires: %{?el7:devtoolset-8-}gcc
BuildRequires: %{?el7:devtoolset-8-}gcc-c++
BuildRequires: java
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: perl-libs
%if 0%{?el9}
BuildRequires: perl-lib
%endif
BuildRequires: perl(FindBin)
BuildRequires: utf8cpp-devel
BuildRequires: wget

BuildRequires: postgresql-private-devel = %{version_postgres}
BuildRequires: postgresql-server-devel = %{version_postgres}

Requires: babelfishpg-money%{?_isa} = %{version}-%{release}
Requires: babelfishpg-common%{?_isa} = %{version}-%{release}
Requires: babelfishpg-tds%{?_isa} = %{version}-%{release}
Requires: babelfishpg-tsql%{?_isa} = %{version}-%{release}
Requires: wiltondb-pg-hint-plan%{?_isa} = %{version}-%{release}
Requires: wiltondb-tds-fdw%{?_isa} = %{version}-%{release}
Requires: openssl
 
%description
WiltonDB a set of Babelfish extensions to provide the capability for PostgreSQL to understand queries from applications written for Microsoft SQL Server. WiltonDB understands the SQL Server wire-protocol and T-SQL, the Microsoft SQL Server query language.

%package -n babelfishpg-money
Summary: Supports the money type in MSSQL
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
%description -n babelfishpg-money
This is a variation of the opensource fixeddecimal extension. FixedDecimal is a fixed precision decimal type which provides a subset of the features of PostgreSQL's builtin NUMERIC type, but with vastly increased performance. Fixeddecimal is targeted to cases where performance and disk space are a critical.

%package -n babelfishpg-common
Summary: Supports the various datatypes in MSSQL
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
Requires: babelfishpg-money%{?_isa} = %{version}-%{release}
%description -n babelfishpg-common
Supports NUMERIC, VARBINARY and other datatypes.

%package -n babelfishpg-tds
Summary: Supports the TDS connection
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
%description -n babelfishpg-tds
Supports Tabular Data Stream (TDS) protocol.

%package -n babelfishpg-tsql
Summary: Supports the T-SQL language
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
Requires: babelfishpg-common%{?_isa} = %{version}-%{release}
%description -n babelfishpg-tsql
Supports Transact-SQL (T-SQL) language.

%package -n wiltondb-pg-hint-plan
Summary: Makes it possible to tweak PostgreSQL execution plans
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
%description -n wiltondb-pg-hint-plan
Makes it possible to tweak PostgreSQL execution plans using so-called "hints" in SQL comments.

%package -n wiltondb-tds-fdw
Summary: Foreign data wrapper that can connect to databases that use the TDS protocol
Requires: postgresql-server%{?_isa} = %{version_postgres}
Requires: postgresql-contrib%{?_isa} = %{version_postgres}
%description -n wiltondb-tds-fdw
Foreign data wrapper that can connect to databases that use the Tabular Data Stream (TDS) protocol, such as Sybase databases and Microsoft SQL server.

%prep
pushd %{_sourcedir}
if [ ! -s %{SOURCE0} ] ; then
	rm %{SOURCE0}
	wget -nv %{source0_url} -O $(basename %{SOURCE0})
fi
echo "%{source0_sha512}  $(basename %{SOURCE0})" | sha512sum -c
popd

%setup -q -n %{source0_dirname}

%build
%if 0%{?el7}
. /opt/rh/devtoolset-8/enable
mkdir el7bin
ln -s /usr/bin/cmake3 ./el7bin/cmake
export PATH=$PATH:`pwd`/el7bin/
%endif

export PG_CONFIG=/usr/bin/pg_config
export PG_SRC=`pwd`/postgresql_modified_for_babelfish
export ANTLR4_JAVA_BIN=/usr/bin/java

# money
pushd ./contrib/babelfishpg_money/
make %{?_smp_mflags}
popd

# common
pushd ./contrib/babelfishpg_common/
make %{?_smp_mflags}
popd

# tds
pushd ./contrib/babelfishpg_tds/
make %{?_smp_mflags}
popd

# tsql
pushd ./contrib/babelfishpg_tsql/
make #%{?_smp_mflags}
popd

# pg_hint_plan
pushd ./extensions/pg_hint_plan/
make #%{?_smp_mflags}
popd

# tds_fdw
pushd ./extensions/tds_fdw/
make #%{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/pgsql
mkdir -p %{buildroot}%{_datadir}/pgsql/extension

cp -p %{SOURCE1} %{buildroot}%{_bindir}/

# money
cp -p ./contrib/babelfishpg_money/babelfishpg_money.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_money/babelfishpg_money--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_money/babelfishpg_money.control %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_money/fixeddecimal--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/

# common
cp -p ./contrib/babelfishpg_common/babelfishpg_common.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.1.0--1.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.0--1.2.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--1.2.1--2.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.0.0--2.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.1.0--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.2.0--2.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.3.0--2.4.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.3.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.4.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--2.5.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.0.0--3.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.1.0--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.1.0--3.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.3.0--3.3.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/sql/babelfishpg_common--3.3.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_common/babelfishpg_common.control %{buildroot}%{_datadir}/pgsql/extension/

# tds
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tds/babelfishpg_tds.control %{buildroot}%{_datadir}/pgsql/extension/

# tsql
cp -p ./contrib/babelfishpg_tsql/babelfishpg_tsql.so %{buildroot}%{_libdir}/pgsql/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.0.0--1.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.1.0--1.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.2.0--1.2.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--1.2.1--2.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.0.0--2.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.1.0--2.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.2.0--2.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.3.0--2.4.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.3.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.4.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.5.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--2.6.0--3.0.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.0.0--3.1.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.1.0--3.2.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.2.0--3.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.3.0--3.3.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/sql/babelfishpg_tsql--3.3.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./contrib/babelfishpg_tsql/babelfishpg_tsql.control %{buildroot}%{_datadir}/pgsql/extension/

# pg_hint_plan
cp -p ./extensions/pg_hint_plan/pg_hint_plan.so %{buildroot}%{_libdir}/pgsql/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.0.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.0--1.3.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.1--1.3.2.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.2--1.3.3.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.3--1.3.4.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.5--1.3.6.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.4--1.3.5.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.6--1.3.7.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.7--1.3.8.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.8--1.3.9.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.3.9--1.4.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.4--1.4.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.4.1--1.4.2.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.4.2--1.5.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan--1.5--1.5.1.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/pg_hint_plan/pg_hint_plan.control %{buildroot}%{_datadir}/pgsql/extension/

# tds_fdw
cp -p ./extensions/tds_fdw/tds_fdw.so %{buildroot}%{_libdir}/pgsql/
cp -p ./extensions/tds_fdw/sql/tds_fdw--2.0.3.sql %{buildroot}%{_datadir}/pgsql/extension/
cp -p ./extensions/tds_fdw/tds_fdw.control %{buildroot}%{_datadir}/pgsql/extension/

%files
%{_bindir}/wiltondb-setup
%doc README.md
%license LICENSE.PostgreSQL
 
%files -n babelfishpg-money
%{_libdir}/pgsql/babelfishpg_money.so
%{_datadir}/pgsql/extension/babelfishpg_money--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_money.control
%{_datadir}/pgsql/extension/fixeddecimal--1.0.0--1.1.0.sql

%files -n babelfishpg-common
%{_libdir}/pgsql/babelfishpg_common.so
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.0.0--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.1.0--1.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.0--1.2.1.sql
%{_datadir}/pgsql/extension/babelfishpg_common--1.2.1--2.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.0.0--2.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.1.0--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.2.0--2.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.3.0--2.4.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.3.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.4.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--2.5.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.0.0--3.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.1.0--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.1.0--3.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.3.0--3.3.1.sql
%{_datadir}/pgsql/extension/babelfishpg_common--3.3.1.sql
%{_datadir}/pgsql/extension/babelfishpg_common.control

%files -n babelfishpg-tds
%{_libdir}/pgsql/babelfishpg_tds.so
%{_datadir}/pgsql/extension/babelfishpg_tds--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tds.control

%files -n babelfishpg-tsql
%{_libdir}/pgsql/babelfishpg_tsql.so
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.0.0--1.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.1.0--1.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.2.0--1.2.1.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--1.2.1--2.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.0.0--2.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.1.0--2.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.2.0--2.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.3.0--2.4.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.3.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.4.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.5.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--2.6.0--3.0.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.0.0--3.1.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.1.0--3.2.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.2.0--3.3.0.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.3.0--3.3.1.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql--3.3.1.sql
%{_datadir}/pgsql/extension/babelfishpg_tsql.control

%files -n wiltondb-pg-hint-plan
%{_libdir}/pgsql/pg_hint_plan.so
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.0.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.0--1.3.1.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.1--1.3.2.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.2--1.3.3.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.3--1.3.4.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.5--1.3.6.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.4--1.3.5.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.6--1.3.7.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.7--1.3.8.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.8--1.3.9.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.3.9--1.4.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.4--1.4.1.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.4.1--1.4.2.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.4.2--1.5.sql
%{_datadir}/pgsql/extension/pg_hint_plan--1.5--1.5.1.sql
%{_datadir}/pgsql/extension/pg_hint_plan.control

%files -n wiltondb-tds-fdw
%{_libdir}/pgsql/tds_fdw.so
%{_datadir}/pgsql/extension/tds_fdw--2.0.3.sql
%{_datadir}/pgsql/extension/tds_fdw.control

%changelog
* Sun Mar 17 2024 WiltonDB Software <info@wiltondb.com> - 3.3_5_10-1
- Update to wiltondb3.3-5-10

* Sat Mar  2 2024 WiltonDB Software <info@wiltondb.com> - 3.3_4_9-1
- Update to wiltondb3.3-4-9

* Mon Feb 12 2024 WiltonDB Software <info@wiltondb.com> - 3.3_4_6-1
- Update to wiltondb3.3-4-6

* Sun Dec 31 2023 WiltonDB Software <info@wiltondb.com> - 3.3_3_5-1
- Update to wiltondb3.3-3-5

* Sun Oct 22 2023 WiltonDB Software <info@wiltondb.com> - 3.3_2_4-1
- Update to wiltondb3.3-2-4

* Wed Oct 18 2023 WiltonDB Software <info@wiltondb.com> - 3.3_2_3-3
- Setup script added

* Tue Oct 17 2023 WiltonDB Software <info@wiltondb.com> - 3.3_2_3-2
- EL7 build fix

* Tue Oct 17 2023 WiltonDB Software <info@wiltondb.com> - 3.3_2_3-1
- Wiltondb3.3 initial build

* Fri Jun 30 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_2-1
- Update to BABEL_3_2_STABLE (c96f3c8)

* Mon May  9 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_1-2
- UTF8-CPP usage fix with ANTLR

* Mon May  8 2023 Alex Kasko <alex@staticlibs.net> - BABEL_3_1-1
- Update to BABEL_3_1_STABLE (28aa208)

* Tue Mar  7 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-3
- SQL patches for JDBC introspection, clean extension install only

* Wed Feb 15 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-2
- Update to the same upstream tag that was re-created on different commit

* Tue Jan 31 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_3_0-1
- Update to BABEL_2_3_0

* Sat Jan  7 2023 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_1-1
- Update to BABEL_2_2_1

* Fri Dec 23 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-6
- EL 9 perl fix

* Fri Dec 23 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-5
- Use macros to have the same spec for el 7, 8 and 9

* Wed Dec 21 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-4
- Use utf8cpp instead of codecvt with antlr C++ runtime

* Tue Dec 20 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-3
- Use cmake directly when building TSQL module

* Sat Dec 17 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-2
- Full working build
	
* Thu Dec 8 2022 Alex Kasko <alex@staticlibs.net> - BABEL_2_2_0-1
- Initial packaging of BABEL_2_2_0
