
## 下载依赖

从源代码编译安装Nginx需要处理一些依赖，最主要的是PCRE，Zlib和OpenSSL。
* [Nginx官网](http://nginx.org/)
* [PCRE官网](http://www.pcre.org/)
* [ZLib官网](http://www.zlib.net/)
* [OpenSSL官网](https://www.openssl.org/source/)

从官网下载最新稳定版本后解压至同一根目录下。
我下载的版本是：
* nginx-1.10.1
* openssl-1.0.2h
* pcre-8.39
* zlib-1.2.8


## 编译

假设根目录为nginx, 下面有四个解压好的目录。在根目录执行以下脚本即可安装(Linux)。
Mac如果出现编译错误，请参考下一节进行手动修正处理。

```bash
#!/bin/bash

NGINX_TARBALL_VERSION=nginx-1.10.1
OPENSSL_TARBALL_VERSION=openssl-1.0.2h
PCRE_TARBALL_VERSION=pcre-8.39
ZLIB_TARBALL_VERSION=zlib-1.2.8

tar -zxf "${NGINX_TARBALL_VERSION}.tar.gz"
tar -zxf "${OPENSSL_TARBALL_VERSION}.tar.gz"
tar -zxf "${PCRE_TARBALL_VERSION}.tar.gz"
tar -zxf "${ZLIB_TARBALL_VERSION}.tar.gz"

cd $NGINX_TARBALL_VERSION

./configure\
    --sbin-path=/usr/local/nginx/nginx\
    --conf-path=/usr/local/nginx/nginx.conf\
    --pid-path=/usr/local/nginx/nginx.pid\
    --with-http_ssl_module\
    --with-pcre="../${PCRE_TARBALL_VERSION}"\
    --with-zlib="../${ZLIB_TARBALL_VERSION}"\
    --with-openssl="../${OPENSSL_TARBALL_VERSION}"

make -j24;
sudo make install;

```

## Mac下编译的额外注意事项。
在Linux下进行完Configure后可以直接开始编译了。但Mac下Ningx对OpenSSL的配置有问题。需要手动修改
环境 OS X EI Capitan 10.11.6 。如果报了错误
```bash
ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make[1]: *** [objs/nginx] Error 1
make: *** [build] Error 2
```
说明nginx 在调用openssl 的源码编译时, 调错了configure, 最终没能正确编译出需要的openssl x86_64库文件。
```bash
# 在当前 nginx 源码目录
cd objs
vi Makefile

# 找到`&& ./config`所在这一行，我的在1196行。
&& ./config --prefix=/Users/vonng/Downloads/nginx/nginx-1.10.1/../openssl-1.0.2h/.openssl no-shared  \

# 将其修改为：
&& ./Configure darwin64-x86_64-cc --prefix=/Users/vonng/Downloads/nginx/nginx-1.10.1/../openssl-1.0.2h/.openssl no-shared  \

# 即将 config 换为 ./Configure darwin64-x86_64-cc
# 保存并返回上级目录，继续进行后续make操作，问题解决！
```



