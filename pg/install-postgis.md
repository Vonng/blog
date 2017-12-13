# AN ALMOST IDIOT'S GUIDE TO INSTALL PostgreSQL10,PostGIS2.4,PGROUTING2.5.2 WITH YUM

> 参考<http://www.postgresonline.com/journal/archives/362-An-almost-idiots-guide-to-install-PostgreSQL-9.5,-PostGIS-2.2-and-pgRouting-2.1.0-with-Yum.html>

### 1. 安装环境

- CentOS 7
- PostgreSQL10
- PostGIS2.4
- PGROUTING2.5.2



### 2. PostgreSQL10安装

##### 2.1 确定系统环境

```
uname -a

Linux localhost.localdomain 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```

##### 2.2 安装正确的rpm包

```
  rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
```

不同的系统使用不同的rpm源，你可以从 <http://yum.postgresql.org/repopackages.php>获取相应的平台链接。

##### 2.3 查看rpm包是否正确安装

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

##### 2.4 安装PG

```
yum install -y postgresql10 postgresql10-server postgresql10-libs postgresql10-contrib postgresql10-devel
```

你可以根据需要选择安装相应的rpm包。

##### 2.5 启动服务

默认情况下，PG安装目录为`/usr/pgsql-10/`，data目录为`/var/lib/pgsql/`,系统默认创建用户`postgres`

```
passwd postgres # 为系统postgres设置密码
su - postgres 	# 切换到用户postgres
/usr/pgsql-10/bin/initdb -D /var/lib/pgsql/10/data/	# 初始化数据库
/usr/pgsql-10/bin/pg_ctl -D /var/lib/pgsql/10/data/ -l logfile start	# 启动数据库
/usr/pgsql-10/bin/psql postgres postgres	# 登录
```

### 3. PostGIS安装

```
yum install postgis24_10-client postgis24_10
```

> 如果遇到错误如下：
>
> ```
> --> 解决依赖关系完成
> 错误：软件包：postgis24_10-client-2.4.2-1.rhel7.x86_64 (pgdg10)
>           需要：libproj.so.0()(64bit)
> 错误：软件包：postgis24_10-2.4.2-1.rhel7.x86_64 (pgdg10)
>           需要：gdal-libs >= 1.9.0
> ```
> 你可以尝试通过以下命令解决:```yum -y install epel-release```

### 4. fdw安装

```
yum install ogr_fdw10
```

### 5. pgrouting安装

```
yum install pgrouting_10
```

### 6. 验证测试

```
# 登录pg后执行以下命令，无报错则证明成功
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION ogr_fdw;

SELECT postgis_full_version();
```



