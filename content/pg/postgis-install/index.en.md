---
title: "Installing PostGIS from Source"
date: 2017-09-07
author: "vonng"
summary: "PostGIS is PostgreSQL's killer extension, but compiling and installing it isn't easy."
tags: [PostgreSQL, "PG Administration", Extensions]
---

----------
Strongly recommend using yum / apt commands to install PostGIS from official PostgreSQL binary repositories.

> Reference: <http://www.postgresonline.com/journal/archives/362-An-almost-idiots-guide-to-install-PostgreSQL-9.5,-PostGIS-2.2-and-pgRouting-2.1.0-with-Yum.html>

----------

### 1. Installation Environment

- CentOS 7
- PostgreSQL10
- PostGIS2.4
- PGROUTING2.5.2

----------

### 2. PostgreSQL10 Installation

##### 2.1 Determine System Environment

```bash
$ uname -a

Linux localhost.localdomain 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```

##### 2.2 Install Correct RPM Package

```
rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
```

Different systems use different RPM sources. You can get the appropriate platform links from http://yum.postgresql.org/repopackages.php.

##### 2.3 Check if RPM Package is Correctly Installed

```
yum list | grep pgdg

pgdg-centos10.noarch                        10-2                       installed
CGAL.x86_64                                 4.7-1.rhel7                pgdg10
CGAL-debuginfo.x86_64                       4.7-1.rhel7                pgdg10
CGAL-demos-source.x86_64                    4.7-1.rhel7                pgdg10
CGAL-devel.x86_64                           4.7-1.rhel7                pgdg10
MigrationWizard.noarch                      1.1-3.rhel7                pgdg10
...
```

##### 2.4 Install PostgreSQL

```
yum install -y postgresql10 postgresql10-server postgresql10-libs postgresql10-contrib postgresql10-devel
```

You can choose to install the appropriate RPM packages based on your needs.

##### 2.5 Start Service

By default, PostgreSQL installation directory is `/usr/pgsql-10/`, data directory is `/var/lib/pgsql/`, and the system creates a default user `postgres`.

```
passwd postgres # Set password for system postgres user
su - postgres   # Switch to postgres user
/usr/pgsql-10/bin/initdb -D /var/lib/pgsql/10/data/	# Initialize database
/usr/pgsql-10/bin/pg_ctl -D /var/lib/pgsql/10/data/ -l logfile start	# Start database
/usr/pgsql-10/bin/psql postgres postgres	# Login
```

### 3. PostGIS Installation

```
yum install postgis24_10-client postgis24_10
```

> If you encounter errors like:
>
> ```
> --> Finished Dependency Resolution
> Error: Package: postgis24_10-client-2.4.2-1.rhel7.x86_64 (pgdg10)
>           Requires: libproj.so.0()(64bit)
> Error: Package: postgis24_10-2.4.2-1.rhel7.x86_64 (pgdg10)
>           Requires: gdal-libs >= 1.9.0
> ```
> You can try to resolve it with: `yum -y install epel-release`

### 4. FDW Installation

```
yum install ogr_fdw10
```

### 5. pgRouting Installation

```
yum install pgrouting_10
```

### 6. Verification Testing

```
# After logging into PostgreSQL, execute the following commands. Success if no errors:
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION ogr_fdw;

SELECT postgis_full_version();
```

----------

## Compilation Tools

These tools are generally included with the system.

* GCC and G++, version at least `4.x`.
* GNU Make, CMake, Autotools
* Git 

On CentOS, install directly with `sudo yum install gcc gcc-c++ git autoconf automake libtool m4`.

----------

## Required Dependencies

### PostgreSQL

PostgreSQL is the host platform for PostGIS. Here we use 10.1 as an example.

### GEOS

GEOS is the abbreviation for Geometry Engine, Open Source, a C++ version of the geometry library and PostGIS's core dependency.

PostGIS 2.4 uses some new features from GEOS 3.7. However, as of now, the latest version officially released by GEOS is 3.6.2. GEOS version 3.7 can be obtained through [Nightly snapshot](http://geos.osgeo.org/snapshots/). So currently, if you want to use all new features, you need to compile and install GEOS 3.7 from source.

```bash
# Rolling daily updates, this URL may expire, check here http://geos.osgeo.org/snapshots/
wget -P ./ http://geos.osgeo.org/snapshots/geos-20171211.tar.bz2
tar -jxf geos-20171211.tar.bz2
cd geos-20171211
./configure
make
sudo make install
cd ..
```

### Proj

Provides coordinate projection support for PostGIS. Current latest version is 4.9.3: [Download](http://proj4.org/download.html)

```bash
# This URL may expire, check here http://proj4.org/download.html
wget -P . http://download.osgeo.org/proj/proj-4.9.3.tar.gz
tar -zxf proj-4.9.3.tar.gz
cd proj-4.9.3
make 
sudo make install
```

### JSON-C

Currently used for importing GeoJSON format data. The `ST_GeomFromGeoJson` function uses this library.

Compiling `json-c` requires `autoconf, automake, libtool`.

```bash
git clone https://github.com/json-c/json-c
cd json-c
sh autogen.sh

./configure  # --enable-threading
make
make install
```

### LibXML2

Currently used for importing GML and KML format data. Functions `ST_GeomFromGML` and `ST_GeomFromKML` depend on this library.

Currently available on this [FTP](ftp://xmlsoft.org/libxml2/) server. Current version used is `2.9.7`.

```bash
tar -zxf libxml2-sources-2.9.7.tar.gz
cd libxml2-sources-2.9.7
./configure
make 
sudo make install
```

### GDAL

```bash
wget -P . http://download.osgeo.org/gdal/2.2.3/gdal-2.2.3.tar.gz
```

### SFCGAL

SFCGAL is an extended wrapper for CGAL. Although it's optional, many functions are commonly used, so installation is needed here. [Download page](http://oslandia.github.io/SFCGAL/installation.html)

SFCGAL has many dependencies, including `CMake, CGAL, Boost, MPFR, GMP`, etc. Among these, `CGAL` was manually installed above. Here we still need to manually install BOOST.

```bash
wget -P . https://github.com/Oslandia/SFCGAL/archive/v1.3.0.tar.gz
```

### Boost

Boost is a common C++ library that SFCGAL depends on. [Download page](http://www.boost.org)

```bash
wget -P . https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz
tar -zxf boost_1_65_1.tar.gz
cd boost_1_65_1
./bootstrap.sh
./b2
```