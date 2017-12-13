# PostgreSQL安装手册
[author]: # "Vonng (fengruohang@outlook.com)"
[tags]: # "PostgreSQL"
[mtime]: #	"2017-01-28"

Linux与Mac下编译安装PostgreSQL的过程。
----

安装详细细节，或者其他需求请参考官方文档安装说明：
[Install From Source Code](https://www.postgresql.org/docs/9.6/static/installation.html)

## 处理依赖
PostgreSQL的依赖都比较常见，一般系统中均已自带：
`GNU Make 3.8+，ISO/ANSI C compiler，tar, zlib, GNU Readline Lib 6`
如果需要使用`plpython`,还需要配置Python解释器。


### Readline与Zlib
主要是`zlib`和`readline`可能出问题。
`configure --without-readline --without-zlib`可以不用。

Ret Hat和CentOS，直接使用Yum安装`devel`版本。
```bash
sudo yum install readline-devel
sudo yum install zlib-devel
```

Mac直接使用`homebrew`：

```bash
brew install readline zlib
```

### Python的配置

这里以Anaconda为例，假设安装在`/Users/vonng/anaconda`目录下，

```bash
export PATH="/Users/vonng/anaconda/bin/:$PATH"
export C_INCLUDE_PATH="/Users/vonng/include/:$C_INCLUDE_PATH"
export LIBRARY_PATH="/Users/vonng/anaconda/lib/:$LIBRARY_PATH"
export LD_LIBRARY_PATH="/Users/vonng/anaconda/lib/:$LD_LIBRARY_PATH"
```
Pg运行后，需要用到`plpython3.so`或`libpython3.6m.dylib`，在`LD_LIBRARY_PATH`中能找到这两个库即可。


## 	2. PostgreSQL的安装
```bash
./configure PYTHON=/Users/vonng/anaconda/bin/python --with-python 
sudo make install-world -j8
```

## 开机自动启动


## 	3. 数据库的初始化与启动
```bash
＃ 创建一个用户,postgres主进程应当由一个独立的用户持有。
$ adduser postgres
＃ 创建一个数据目录，并指定上面创建的用户所有
$ mkdir /usr/local/pgsql/data
$ chown postgres /usr/local/pgsql/data
$ su - postgres
# 初始化数据目录
$ /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
$ 启动数据库
/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >logfile 2>&1 &

# 另一种启动数据库的方式是使用pg_ctl，推荐这种方式：
$ /usr/local/pgsql/bin/pg_ctl init -D /usr/local/pgsql/data -l /usr/local/pgsql/data/logfile
# 最后通过pg_ctl启动数据库
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
```

## 4. 配置PostgreSQL

### 创建数据库、角色、授权
PostgreSQL安装完成后会自带一个postgres数据库，用户postgres可直接使用psql连接。
每个操作系统用户可以直接连接自己同名的数据库。psql  [-U<username>] [database]

```
$ psql
# 创建数据库
$ create database vonng;
# 创建角色：
$ CREATE USER vonng LOGIN SUPERUSER PASSWORD 'xxxxxxx';
# 授予权限：
$ GRANT ALL PRIVILEGES ON DATABASE vonng to vonng;
```

### 允许从外部主机访问PostgreSQL

```
# Pg默认只接受本机的连接。需要配置HBA允许外部链接，具体细节参见文档。
# 这里假设我们希望在10.0.0.0-10.255.255.255的A类局域网段内允许任何用户连接任何数据库。
# 打开数据文件夹中的pg_hba.conf文件.
$ vi /usr/local/pgsql/data/pg_hba.conf
# 在最下方添加一行
host    all     all     10.0.0.0/8      trust
# 打开数据文件夹中的postgresql.conf
# 找到 #listen_addresses = 'localhost',修改为 listen_addresses="*"
# 重启PostgreSQL:
$ pg_ctl stop -D /usr/local/pgsql/data
$ pg_ctl start -D /usr/local/pgsql/data -l logfile
# 在另一台机器上测试 $ psql -h<Your Pgserver host> -U<Your Pgserver username>。
```

## 5. PostgreSQL的常用运维命令

```bash
#备份一个数据库
$ pg_dump [connection-option...] [option...] [dbname]
#恢复一个数据库
$ psql [connectino-option] < dumpfile.sql
```

## 一些附件的安装

### Multicorn
```
export C_INCLUDE_PATH="/usr/local/anaconda/include/python2.7:$C_INCLUDE_PATH"
make && sudo make install
```

### Redis FDW
```
# 先安装hiredis
git clone https://github.com/redis/hiredis
cd hiredis
make -j8
sudo make install

# 再安装redis_fdw
git clone https://github.com/pg-redis-fdw/redis_fdw
cd redis_fdw
PGSQL_BIN="/usr/local/pgsql/bin/"
git checkout REL9_5_STABLE
PATH="$PGSQL_BIN:$PATH" make USE_PGXS=1
sudo PATH="$PGSQL_BIN:$PATH" make USE_PGXS=1 install
```

### Psycopg2
对于一些依赖libpq的程序。需要将libpq放到动态链接目录中。
```bash
sudo rm -rf /usr/local/lib/libpq.* /usr/lib/libpq.* /lib/libpq.*  /usr/local/lib64/libpq.* /usr/lib64/libpq.* /lib64/libpq.* ;
sudo ln -s /usr/local/pgsql/lib/libpq.* /lib64/
```

