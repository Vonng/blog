---
title: "Batch Configure SSH Passwordless Login"
date: 2018-01-07
author: "vonng"
summary: >
  Quick configuration for passwordless login to all machines
tags: [PostgreSQL, PG Management]
---

Configuring SSH is fundamental operations work - sometimes the basics need revisiting.

---------------------

## Generate Public-Private Key Pairs

Ideally, everything should use public-private key authentication for passwordless direct connection from local to all database machines. Password authentication should be avoided.

First, use `ssh-keygen` to generate public-private key pairs:

```bash
ssh-keygen -t rsa
```

Pay attention to permissions: SSH files should have permissions set to `0600`, and `.ssh` directory permissions should be set to `0700`. Incorrect settings will prevent passwordless login from working.

---------------------

## Configure ssh config to traverse jumphost

Replace `User` with your own name. Put in `.ssh/config`. Here's how to configure direct passwordless connection to production database in a jumphost environment:

```bash
# Vonng's ssh config

# SpringBoard IP
Host <BastionIP>
	Hostname <your_ip_address>
	IdentityFile ~/.ssh/id_rsa

# Target Machine Wildcard (Proxy via Bastion)
Host 10.xxx.xxx.*
	ProxyCommand ssh <BastionIP> exec nc %h %p 2>/dev/null
	IdentityFile ~/.ssh/id_rsa

# Common Settings
Host *
	User xxxxxxxxxxxxxx
	PreferredAuthentications publickey,password
	Compression yes
	ServerAliveInterval 30
	ControlMaster auto
	ControlPath ~/.ssh/ssh-%r@%h:%p
	ControlPersist yes
	StrictHostKeyChecking no
```

---------------------

## Copy Public Key to Target Machines

Then copy the public key to jumphost, DBA workstation, and all database machines.

```bash
ssh-copy-id <target_ip>
```

Each execution of this command requires password input, which is tedious and boring. It can be automated through expect scripts or using `sshpass`.

---------------------

## Use expect for Automation

Replace `<your password>` in the following script with your actual password. If the server IP list changes, modify the list accordingly.

```bash
#!/usr/bin/expect
foreach id { 
     10.xxx.xxx.xxx
     10.xxx.xxx.xxx
     10.xxx.xxx.xxx
} {
    spawn ssh-copy-id $id
    expect {
    	"*(yes/no)?*"
    	{
            send "yes\n"
            expect "*assword:" { send "<your password>\n"}
    	}
     	"*assword*" { send "<your password>\n"}
    }
}

exit
```

---------------------

## More Elegant Solution: `sshpass`

```bash
sshpass -p <your password> ssh-copy-id <target address>
```

The downside is that passwords are likely to appear in bash history - clean up traces promptly after execution.