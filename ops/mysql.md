# MySQL的编译安装、部署与配置

MySQL是最流行的开源数据库，而PostgreSQL是最先进的开源数据库。虽然我现在自己已经全面投入PostgreSQL的怀抱中了，但是还有许多迷途的羔羊执迷不悟，或者无力抽身，不求上进，满足于MySQL。所以目前来看还有是有MySQL的使用需求的。本文描述了*nix下MySQL的源码安装方法。

# 从源码编译安装MySQL

```bash
tar -zxvf mysql-5.7.9-osx10.10-x86_64.tar.gz
mv mysql-5.7.9-osx10.10-x86_64 /usr/local/mysql
chown -R root:wheel mysql
bin/mysqld --initialize --user=mysql
cd /usr/local
sudo chown -R root:wheel mysql
cd /usr/local/mysql
sudo bin/mysqld --initialize --user=mysql

# Remember the root password
cp support-files/my-default.cnf /etc/my.cnf

# Add Following content to /etc/my.cnf
[client]
default-character-set=utf8
[mysqld]
default-storage-engine=INNODB
character-set-server=utf8
collation-server=utf8_general_ci

# Admin
support-files/mysql.server start
support-files/mysql.server restart
support-files/mysql.server stop
support-files/mysql.server status

# Change Root Password
bin/mysqladmin -u root -p password <newpassword>
$ <Input temp password here>

# login with root
bin/mysql -p

# Create Main User
CREATE USER 'vonng'@'%' IDENTIFIED BY 'xxxx';
grant all privileges on *.* to 'vonng'@'%' with grant option;
create database vonng;
create database test;

# Create server user
CREATE USER 'vonngserver'@'localhost' IDENTIFIED BY 'xxxx';
grant all privileges on vonng.* to 'vonngserver'@'localhost';
grant all privileges on test.* to 'vonngserver'@'localhost';
flush privileges;

# Uninstall
sudo rm -rf /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm -rf /var/db/receipts/com.mysql.*

# Dump:
/path/to/mysql/bin/mysqldump -u<username> -p <databasename> > dumpfile_name
# Example: /usr/local/mysql/bin/mysqldump -uvonng -p cnzzdb > ~/Data/mysql/cnzzdb.sql  

# Recover
mysql -u<username> -p -D <dbname> < dump_file_name
# Example mysql -p -D testdb< ~/Data/mysql/cnzzdb.sql
```

### 在Mac上设置开机自动启动
```bash
sudo vi /Library/LaunchDaemons/com.mysql.mysql.plist

<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">  
<plist version="1.0">  
  <dict>  
    <key>KeepAlive</key>  
    <true/>  
    <key>Label</key>  
    <string>com.mysql.mysqld</string>  
    <key>ProgramArguments</key>  
    <array>  
    <string>/usr/local/mysql/bin/mysqld_safe</string>  
    <string>--user=root</string>  
    </array>    
  </dict>  
</plist> 

sudo launchctl load -w /Library/LaunchDaemons/com.mysql.mysql.plist 
```