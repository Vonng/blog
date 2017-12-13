# PostGIS 2.4 源码编译

本例使用PostgreSQL10.1，PostGIS2.4.2，在CentOS7.3上编译通过。



## 编译工具

此类工具一般系统都自带。

* GCC与G++，版本至少为`4.x`。
* GNU Make，CMake， Autotools
*  Git 

CentOS下直接通过`sudo yum install gcc gcc-c++ git autoconf automake libtool m4 `安装。



## 必选依赖

### PostgreSQL

PostgreSQL是PostGIS的宿主平台。这里以10.1为例。



### GEOS

GEOS是Geometry Engine, Open Source的缩写，是一个C++版本的几何库。是PostGIS的核心依赖。

PostGIS 2.4用到了GEOS 3.7的一些新特性。不过截止到现在，GEOS官方发布的最新版本是3.6.2，3.7版本的GEOS可以通过[Nightly snapshot](http://geos.osgeo.org/snapshots/)获取。所以目前如果希望用到所有新特性，需要从源码编译安装GEOS 3.7。

```bash
# 滚动的每日更新，此URL有可能过期，检查这里http://geos.osgeo.org/snapshots/
wget -P ./ http://geos.osgeo.org/snapshots/geos-20171211.tar.bz2
tar -jxf geos-20171211.tar.bz2
cd geos-20171211
./configure
make
sudo make install
cd ..
```

### Proj

为PostGIS提供坐标投影支持，目前最新版本为4.9.3 ：[下载](http://proj4.org/download.html)

```bash
# 此URL有可能过期，检查这里http://proj4.org/download.html
wget -P . http://download.osgeo.org/proj/proj-4.9.3.tar.gz
tar -zxf proj-4.9.3.tar.gz
cd proj-4.9.3
make 
sudo make install
```

### JSON-C

目前用于导入GeoJSON格式的数据，函数`ST_GeomFromGeoJson`用到了这个库。

编译`json-c`需要用到`autoconf, automake, libtool`。

```bash
git clone https://github.com/json-c/json-c
cd json-c
sh autogen.sh

./configure  # --enable-threading
make
make install
```

### LibXML2

目前用于导入GML与KML格式的数据，函数`ST_GeomFromGML`和`ST_GeomFromKML`依赖这个库。

目前可以在这个[FTP](ftp://xmlsoft.org/libxml2/)服务器上搞到，目前使用的版本是`2.9.7`

```bash
tar -zxf libxml2-sources-2.9.7.tar.gz
cd libxml2-sources-2.9.7
./configure
make 
sudo make install
```



### GADL

```bash
wget -P . http://download.osgeo.org/gdal/2.2.3/gdal-2.2.3.tar.gz
```



### SFCGAL

SFCGAL是CGAL的扩展包装，虽说是可选项，但是很多函数都会经常用到，因此这里也需要安装。[下载页面](http://oslandia.github.io/SFCGAL/installation.html)

SFCGAL依赖的东西比较多。包括`CMake, CGAL, Boost, MPFR, GMP`等，其中，`CGAL`在上面手动安装过了。这里还需要手动安装BOOST

```bash
wget -P . https://github.com/Oslandia/SFCGAL/archive/v1.3.0.tar.gz

```



### Boost

Boost是C++的常用库，SFCGAL依赖BOOST，[下载页面](http://www.boost.org)

```bash
wget -P . https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz
tar -zxf boost_1_65_1.tar.gz
cd boost_1_65_1
./bootstrap.sh
./b2
```





## 可选依赖





### Optional - Add protobuf support for vector tiles

To optionally add support for vector tiles, build protobuf dependencies as well:

```
sudo apt-get install autoconf automake libtool curl make g++ unzip
cd ~/git
git clone https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig 

# compile protobuf-c https://github.com/protobuf-c/protobuf-c
cd ~/
curl -OL https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.0/protobuf-c-1.3.0.tar.gz
tar xzf protobuf-c-1.3.0.tar.gz
cd protobuf-c-1.3.0
./configure && make && make install

```

## Build PostGIS

```
wget http://download.osgeo.org/postgis/source/postgis-2.4.1.tar.gz
tar xfz postgis-2.4.1.tar.gz
cd postgis-2.4.1

```

A basic configuration for PostGIS 2.4, with raster and topology support:

```
./configure
make
sudo make install
sudo ldconfig
sudo make comments-install

```

## Spatially enabling a database

Connect to your database using pgAdmin or psql, and use the commands to add the PostgreSQL extensions. To add PostGIS with raster support:

```
CREATE EXTENSION postgis;

```

To add topology support, a second extension can be created on the database:

```
CREATE EXTENSION postgis_topology;

```

## Troubleshooting

If you already had Postgres running before the build, make sure to restart:

```
sudo /etc/init.d/postgresql restart
```