---
title: "PostgreSQL MongoFDW Installation and Deployment"
linkTitle: "MongoFDW Installation and Deployment"
date: 2016-05-28
author: "vonng"
summary: "Recently had business requirements to access MongoDB through PostgreSQL FDW, but compiling MongoDB FDW is really a nightmare."
tags: ["PostgreSQL","PG Management","Extension"]
---

> Update: Recently MongoFDW has been taken over by Cybertech for maintenance, so maybe it's not as bad anymore.

Recently had business requirements to access MongoDB through PostgreSQL FDW. Initially I thought this was a pretty easy task. But what happened next was absolutely disgusting. Compiling MongoDB FDW is really a nightmare: chaotic dependencies, temporary downloads and hotpatches, wrong compilation parameters, and worst of all, incorrect documentation. Finally, I successfully compiled it in both production environment (Linux RHEL7u2) and development environment (Mac OS X 10.11.5). Let me record this quickly to save myself the pain next time.

----------

## Environment Overview

Theoretically, to compile this suite of tools, GCC version should be at least 4.1.
Production environment (RHEL7.2 + PostgreSQL9.5.3 + GCC 4.8.5)
Local environment (Mac OS X 10.11.5 + PostgreSQL9.5.3 + clang-703.0.31)

----------

## Dependencies of `mongo_fdw`

Generally speaking, problems that can be solved with package management should be solved with package management.
[mongo_fdw](https://github.com/EnterpriseDB/mongo_fdw "mongo_fdw") is the package we ultimately want to install
It has three direct dependencies:
* [json-c 0.12](https://github.com/json-c/json-c/tree/json-c-0.12 "json-c 0.12")
* [libmongoc-1.3.1](https://github.com/mongodb/mongo-c-driver/tree/r1.3 "libmongoc-1.3.1")
* [libbson-1.3.1](https://github.com/mongodb/libbson/tree/r1.3 "libbson-1.3.1")

Overall, mongo_fdw uses the C driver provided by mongo to accomplish its functionality. So we need to install libbson and libmongoc. Among them, libmongoc is MongoDB's C language driver library, which depends on libbson.
So the final installation order is:
`libbson` → `libmongoc` → `json-c` → `mongo_fdw`

----------

## Indirect Dependencies

The documentation won't tell you about the default dependencies on the GNU Build toolchain. Below are some relatively simple dependencies that can be resolved through package management. Please install `GNU Autotools` in the following order:

`m4-1.4.17` → `autoconf-2.69` → `automake-1.15` → `libtool-2.4.6` → `pkg-config-0.29.1`.

Anyway, whether it's yum, apt, or homebrew, these are all things that can be solved with a single command. There's also one dependency that libmongoc depends on: `openssl-devel`, don't forget to install it.

----------

### Installing `libbson-1.3.1`

```bash
git clone -b r1.3 https://github.com/mongodb/libbson;
cd libbson;
git checkout 1.3.1;
./autogen.sh;
make && sudo make install;
make test;
```

----------

### Installing `libmongoc-1.3.1`

```bash
git clone -b r1.3 https://github.com/mongodb/mongo-c-driver
cd mongo-c-driver;
git checkout 1.3.1;
./autogen.sh;
# The next step is very important, must use the system libbson we just installed.
./configure --with-libbson=system;
make && sudo make install;
```

Why must we use version 1.3.1? There's a reason for this. Because mongo_fdw uses version 1.3.1 of mongo-c-driver by default. But it says in the documentation that any version 1.0.0+ will work, which is complete bullshit. The mongo-c-driver and libbson versions correspond one-to-one. The 1.0.0 version of libbson was brain-damaged and used features beyond C99, like complex number types. Using the default version would be stupid.

----------

#### Installing `json-c`

First, let's solve the json-c problem

```bash
git clone https://github.com/json-c/json-c;
cd json-c
git checkout json-c-0.12
```

- Don't rush to make after `./configure`, this version of json-c has compilation parameter issues.
- Open Makefile, find `CFLAGS`, add `-fPIC` after the compilation parameters
- This way GCC will generate position-independent code, otherwise mongo_fdw linking will fail.

----------

### Installing `mongo_fdw`

Here comes the really disgusting part.

```bash
git clone https://github.com/EnterpriseDB/mongo_fdw;
```

Now, if you naively run `./autogen.sh --with-master`, it will re-download all the packages above..., and all from Amazon cloud hosts outside the firewall. The reliable method is to manually execute the commands in autogen one by one.

First copy the json-c directory above to the mongo_fdw root directory. Then add the include paths for libbson and libmongoc.

```bash
export C_INCLUDE_PATH="/usr/local/include/libbson-1.0/:/usr/local/include/libmongoc-1.0:$C_INCLUDE_PATH"
```

Looking at `autogen.sh`, we find that it has different operations based on different options `--with-legacy` and `--with-master`. Specifically, when the `--with-master` option is specified, it creates a config.h that defines a META_DRIVER macro variable. When this macro variable exists, mongo_fdw will use the mongoc.h header file, which is the so-called "master", the new version of the mongo driver. When it doesn't exist, it will use the "mongo.h" header file, which is the old version of the mongo driver. Here, we directly `vi config.h` and add a line:

```bash
#define META_DRIVER
```

At this point, we can basically say everything is ready. Before the final build, don't forget to execute: `ldconfig`

```bash
sudo ldconfig
```

Go back to the mongo_fdw root directory and `make`. If all goes well, the `mongo_fdw.so` will be generated.

----------

### Let's try it?

```bash
sudo make install;
psql
admin=# CREATE EXTENSION mongo_fdw;
```

If it says it can't find `libmongoc.so` and `libbson.so`, just throw them into pgsql's lib directory.

```bash
sudo cp /usr/local/lib/libbson* /usr/local/pgsql/lib/
sudo cp /usr/local/lib/libmongoc* /usr/local/pgsql/lib/
```