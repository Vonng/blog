---
title: "PgAdmin Installation and Configuration"
date: 2018-04-14
author: "vonng"
summary: "PgAdmin is a GUI program for managing PostgreSQL, written in Python, but it's quite dated and requires some additional configuration."
tags: [PostgreSQL, "PG Administration", Tools]
---

## PgAdmin4 Installation and Configuration

PgAdmin is a GUI designed specifically for PostgreSQL. It works very well. It can run as either a local GUI program or a web service. Since PgAdmin's GUI components have display issues on Retina screens, this guide primarily covers how to configure and run PgAdmin4 as a web service (Python Flask).

### Download

PgAdmin can be downloaded from the official FTP.

[PostgreSQL website FTP directory](https://ftp.postgresql.org/pub/pgadmin3/pgadmin4)

```bash
wget https://ftp.postgresql.org/pub/pgadmin3/pgadmin4/v1.1/source/pgadmin4-1.1.tar.gz
tar -xf pgadmin4-1.1.tar.gz && cd pgadmin4-1.1/
```

You can also download from the official [Git Repo](git://git.postgresql.org/git/pgadmin4.git):

```bash
git clone git://git.postgresql.org/git/pgadmin4.git
cd pgadmin4
```

### Install Dependencies

First, you need to install Python - either version 2 or 3 will work. Here we'll use administrator privileges to install the Anaconda3 distribution as an example.

First create a virtual environment (though using the physical environment directly is also fine):

```bash
conda create -n pgadmin python=3 anaconda
```

Based on your Python version, install dependencies according to the corresponding requirements file.

```bash
sudo pip install -r requirements_py3.txt
```

### Configuration Options

First run the initialization script to create the PgAdmin administrator user.

```bash
python web/setup.py
```

Follow the prompts to enter email and password.

Edit `web/config.py` to modify default configuration, mainly changing the listen address and port.

```python
DEFAULT_SERVER = 'localhost'
DEFAULT_SERVER_PORT = 5050
```

Change the listen address to `0.0.0.0` to allow access from any IP.
Modify the port as needed.