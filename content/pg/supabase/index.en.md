---
title: Self-Hosting Supabase on PostgreSQL
linkTitle: "Self-Hosting Supabase"
date: 2024-11-25
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: Supabase is great, own your own Supabase is even better. A tutorial for self-hosting production-grade supabase on local/cloud/ VM/BMs.
tags: [Database,Supabase]
---



Supabase is great, but having your own Supabase is even better.
Pigsty helps you build enterprise-grade Supabase on your own servers (physical/virtual machines/cloud servers) with one-click deployment —
[more extensions](https://pgext.cloud), better performance, deeper control, and much more cost-effective.

> Pigsty is one of the three 3rd party self-hosting tutorials listed in the [official Supabase docs](https://supabase.com/docs/guides/self-hosting#third-party-guides)


--------

## Quick Start [#short-version]

[Prepare](https://doc.pgsty.com/prepare) a [Linux](https://doc.pgsty.com/prepare/linux) server, follow the Pigsty [standard installation](https://doc.pgsty.com/install/) process, select the `supabase` configuration template, and execute the following commands:

```bash
curl -fsSL https://repo.pigsty.io/get | bash; cd ~/pigsty
./configure -c supabase    # Use supabase configuration (please change credentials in pigsty.yml)
vi pigsty.yml              # Edit domain, passwords, keys...
./install.yml              # Install pigsty
./docker.yml               # Install docker compose components
./app.yml                  # Start supabase stateless components with docker (may be slow)
```

After installation, visit port `8000` in your browser to access Supa Studio, username `supabase`, password `pigsty`.

![](https://doc.pgsty.com/img/docs/supabase-login.png)

------

## Table of Contents

- [What is Supabase?](#what-is-supabase)
- [Why Self-Host?](#why-self-host-supabase)
- [Single Node Quick Start](#single-node-quick-start)
- [Advanced Topic: Security Hardening](#advanced-topic-security-hardening)
- [Advanced Topic: Domain Integration](#advanced-topic-domain-integration)
- [Advanced Topic: External Object Storage](#advanced-topic-external-object-storage)
- [Advanced Topic: Using SMTP](#advanced-topic-using-smtp)
- [Advanced Topic: True High Availability](#advanced-topic-true-high-availability)

------

## What is Supabase?

[Supabase](https://supabase.com/) is a BaaS (Backend as Service), an open-source Firebase alternative, and the most popular database + backend solution in the AI Agent era.
Supabase wraps PostgreSQL and provides authentication, messaging, edge functions, object storage, and automatically generates REST API and GraphQL API based on PostgreSQL database schemas.

Supabase aims to provide developers with a one-stop backend solution, reducing the complexity of developing and maintaining backend infrastructure.
It allows developers to eliminate most backend development work — **developers only need to understand database design and frontend to quickly deliver applications!**
Developers can quickly complete a full application with just frontend development and database schema design using Vibe Coding.

Currently, Supabase is the most popular open-source project in the [PostgreSQL open-source ecosystem](https://ossrank.com/cat/368-postgresql-ecosystem), with [80,000](https://github.com/supabase/supabase/) stars on GitHub.
Supabase also provides "generous" free cloud service quotas for small entrepreneurs — 500 MB of free space, which is sufficient for storing user tables, view counts, and similar data.

------

## Why Self-Host?

Since Supabase cloud service is so attractive, why self-host?

The most intuitive reason is what we mentioned in "[Are Cloud Databases an Intelligence Tax?](https://blog.vonng.com/cloud/rds/)": when your data/computing scale exceeds the cloud computing applicable spectrum (Supabase: 4C/8G/500MB free storage), costs can easily explode.
Moreover, currently, sufficiently reliable [local enterprise-grade NVMe SSDs](https://blog.vonng.com/cloud/bonus/) have a three to four order of magnitude advantage in cost-effectiveness compared to [cloud storage](https://blog.vonng.com/cloud/ebs/), and self-hosting can better leverage this advantage.

Another important reason is **functionality** — Supabase cloud service functionality is limited. Many powerful PostgreSQL extensions cannot be provided as cloud services due to multi-tenant security challenges and licensing issues.
Therefore, although [extensions are PostgreSQL's core feature](https://blog.vonng.com/pg/pg-eat-db-world), only **64** extensions are available on Supabase cloud service.
Self-built Supabase with Pigsty provides up to [**440**](https://pgext.cloud/list) ready-to-use PostgreSQL extensions.

Additionally, autonomy and avoiding vendor lock-in are important reasons for self-hosting — although Supabase aims to provide an open-source alternative to Google Firebase without vendor lock-in, the threshold for self-building enterprise-grade Supabase to high standards is actually quite high.
Supabase includes a series of PostgreSQL extension plugins developed and maintained by them, and plans to replace the native PostgreSQL kernel with the acquired [OrioleDB](https://doc.pgsty.com/pgsql/kernel/orioledb), but these kernels and extensions are not provided in the official PGDG repository.

This is actually a form of implicit vendor lock-in, preventing users from self-building using methods other than the supabase/postgres Docker image. Pigsty provides an open-source, transparent, and universal solution to solve this problem.
We package all 10 missing extensions developed and used by Supabase into ready-to-use RPM/DEB packages, ensuring they are available on all [mainstream Linux operating system distributions](https://doc.pgsty.com/prepare/linux):

| Extension                                                 | Description                                                                                                      |
|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [`pg_graphql`](https://pgext.cloud/e/pg_graphql/)       | Provides GraphQL support within PostgreSQL (RUST), Rust extension, provided by PIGSTY                            |
| [`pg_jsonschema`](https://pgext.cloud/e/pg_jsonschema/) | Provides JSON Schema validation capability, Rust extension, provided by PIGSTY                                   |
| [`wrappers`](https://pgext.cloud/e/wrappers/)           | Supabase's external data source wrapper bundle, Rust extension, provided by PIGSTY                               |
| [`index_advisor`](https://pgext.cloud/e/index_advisor/) | Query index advisor, SQL extension, provided by PIGSTY                                                           |
| [`pg_net`](https://pgext.cloud/e/pg_net/)               | Extension for asynchronous non-blocking HTTP/HTTPS requests with SQL (supabase), C extension, provided by PIGSTY |
| [`vault`](https://pgext.cloud/e/supabase_vault/)        | Extension for storing encrypted credentials in Vault (supabase), C extension, provided by PIGSTY                 |
| [`pgjwt`](https://pgext.cloud/e/pgjwt/)                 | PostgreSQL implementation of JSON Web Token API (supabase), SQL extension, provided by PIGSTY                    |
| [`pgsodium`](https://pgext.cloud/e/pgsodium/)           | Table data encryption storage TDE, extension, provided by PIGSTY                                                 |
| [`supautils`](https://pgext.cloud/e/supautils/)         | Used to ensure database cluster security in cloud environments, C extension, provided by PIGSTY                  |
| [`pg_plan_filter`](https://pgext.cloud/e/plan_filter/)  | Filter and block specific query statements using execution plan costs, C extension, provided by PIGSTY           |

Meanwhile, we [install](https://doc.pgsty.com/pgsql/extension/install) most extensions by default in Supabase self-hosting deployment. You can refer to the available extension list to [enable](https://doc.pgsty.com/pgsql/extension/create) them as needed.

Additionally, Pigsty handles the automatic setup of underlying [high availability](https://doc.pgsty.com/feat/ha/) [PostgreSQL](https://doc.pgsty.com/pgsql/) database clusters, high availability [MinIO](https://doc.pgsty.com/minio/) object storage clusters, and even [Docker](https://doc.pgsty.com/docker/) container infrastructure deployment and [Nginx](https://doc.pgsty.com/admin/portal) reverse proxy, [domain configuration](https://doc.pgsty.com/admin/domain) and [HTTPS certificate issuance](https://doc.pgsty.com/admin/cert). You can deploy any number of stateless Supabase container clusters using Docker Compose and store state in external Pigsty self-hosted database services.

In this self-hosting deployment architecture, you gain the freedom to use different kernels (PostgreSQL 15-17, OrioleDB), the freedom to install [**440**](https://pgext.cloud/list/) extensions, the freedom to scale Supabase/Postgres/MinIO,
the freedom from database operational chores, and the freedom from vendor lock-in to run locally indefinitely. Compared to the cost of using cloud services, the price is just preparing servers and typing a few more commands.


------

## Single Node Quick Start

Let's start with single-node Supabase deployment. We'll introduce multi-node high availability deployment methods later.

[Prepare](https://doc.pgsty.com/prepare) a fresh [Linux server](https://doc.pgsty.com/prepare/linux), use the [`supabase`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml) configuration template provided by Pigsty to execute the [standard installation](https://doc.pgsty.com/install/start) process,
then additionally run [`docker.yml`](https://doc.pgsty.com/docker/playbook#dockeryml) and [`app.yml`](https://doc.pgsty.com/app/playbook) to deploy the stateless Supabase containers (default ports `8000`/`8433`).

```bash
curl -fsSL https://repo.pigsty.io/get | bash; cd ~/pigsty
./configure -c supabase    # Use supabase configuration (please change credentials in pigsty.yml)
vi pigsty.yml              # Edit domain, passwords, keys...
./install.yml              # Install pigsty
./docker.yml               # Install docker compose components
./app.yml                  # Start supabase stateless components with docker
```

Before deploying Supabase, please modify the parameters (domain and passwords) in the automatically generated `pigsty.yml` configuration file according to your actual situation.
If it's just local development testing, you can skip this for now. We'll introduce how to further customize through configuration file modifications later.

[![asciicast](https://doc.pgsty.com/img/asciinema/supabase.svg)](https://asciinema.org/a/731206)

If configured correctly, after about ten minutes, you can access the Supabase Studio graphical management interface locally via `http://<your_ip_address>:8000`.
The default username and password are: `supabase` and `pigsty`.

![](https://doc.pgsty.com/img/docs/supabase-home.png)

<Callout title="DockerHub blocked in mainland China" type="warning">

    In mainland China, Pigsty uses DockerHub mirror sites provided by 1Panel and 1ms to download Supabase-related images by default, which may be slow.
    You can also configure [proxy](https://doc.pgsty.com/docker/config#proxy) and [mirror sites](https://doc.pgsty.com/docker/config#registry) yourself, or manually pull images with `cd /opt/supabase; docker compose pull`.
    We also provide [Supabase self-hosting expert consulting services](https://doc.pgsty.com/service) including complete offline installation solutions.

</Callout>

<Callout title="Using Supabase object storage requires HTTPS/domain" type="warning">

    If you need to use object storage functionality, you need to access Supabase via domain and HTTPS, otherwise errors will occur.

</Callout>


<Callout title="Please change passwords for production deployment!" type="warning">

    For serious production deployments, **must** change all default passwords!

</Callout>




------

## Key Technical Decisions for Self-Hosting

Here are some key technical decisions involved in self-hosting Supabase for your reference:

Using the default **single-node deployment**, Supabase cannot enjoy PostgreSQL/MinIO high availability capabilities.
Nevertheless, single-node deployment still has significant advantages compared to the official pure Docker Compose solution: for example, out-of-the-box monitoring systems, the ability to freely install extensions, component scaling capabilities, and providing fallback database point-in-time recovery capabilities.

If you only have one server or choose to self-host on cloud servers, Pigsty recommends using external S3 instead of local MinIO as object storage to store PostgreSQL backups and support Supabase Storage services.
Such deployment can provide a fallback-level RTO (hour-level recovery time)/RPO (MB-level data loss) disaster recovery level under single-machine deployment conditions during failures.

In serious production deployments, Pigsty recommends using at least 3-4 node deployment strategies to ensure both MinIO and PostgreSQL use multi-node deployments that meet enterprise-grade high availability requirements. In this case, you need to prepare more nodes and disks accordingly and adjust cluster configurations in the `pigsty.yml` configuration manifest, as well as access information in supabase cluster configuration to use high availability access points.

Some Supabase functionality requires sending emails, so SMTP services are needed. Unless purely for internal networks, for serious production deployments, using SMTP cloud services is recommended. Self-built email servers easily have their emails marked as spam and rejected.

If your service is directly exposed to the public network, we strongly recommend using real domains and HTTPS certificates and accessing through [Nginx Portal](https://doc.pgsty.com/admin/portal).

Next, we'll discuss some advanced topics in sequence: how to further improve Supabase security, availability, and performance based on single-node deployment.


------

## Advanced Topic: Security Hardening

**Pigsty Base Components**

For serious production deployments, we strongly recommend changing [Pigsty default passwords](https://doc.pgsty.com/config/security#passwords).
Because these default values are public and well-known, going to production without changing passwords is like streaking:

- [`grafana_admin_password`](https://doc.pgsty.com/infra/param/#grafana_admin_password): `pigsty`, Grafana admin password
- [`pg_admin_password`](https://doc.pgsty.com/pgsql/param/#pg_admin_password): `DBUser.DBA`, PostgreSQL superuser password
- [`pg_monitor_password`](https://doc.pgsty.com/pgsql/param/#pg_monitor_password): `DBUser.Monitor`, PostgreSQL monitoring user password
- [`pg_replication_password`](https://doc.pgsty.com/pgsql/param/#pg_replication_password): `DBUser.Replicator`, PostgreSQL replication user password
- [`patroni_password`](https://doc.pgsty.com/pgsql/param/#patroni_password): `Patroni.API`, Patroni high availability component password
- [`haproxy_admin_password`](https://doc.pgsty.com/node/param/#haproxy_admin_password): `pigsty`, load balancer management password
- [`minio_secret_key`](https://doc.pgsty.com/minio/param/#minio_secret_key): `minioadmin`, MinIO root user key
- Additionally, we strongly recommend changing the [PostgreSQL business user](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L68) password used by Supabase, default is `DBUser.Supa`

The above passwords are for Pigsty component modules and are strongly recommended to be set before installation and deployment.

**Supabase Keys**

In addition to Pigsty component passwords, you also need to [modify Supabase keys](https://supabase.com/docs/guides/self-hosting/docker#securing-your-services), including:

- [`JWT_SECRET`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#130)
- [`ANON_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L131)
- [`SERVICE_ROLE_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L132)
- [`DASHBOARD_USERNAME`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L133): Supabase Studio Web interface default username, default is `supabase`
- [`DASHBOARD_PASSWORD`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L134): Supabase Studio Web interface default password, default is `pigsty`

Please refer to the [Supabase tutorial: Securing your services](https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys) instructions:

- Generate a `JWT_SECRET` longer than 40 characters and use the tools in the tutorial to sign `ANON_KEY` and `SERVICE_ROLE_KEY` JWTs.
- Use the tools provided in the tutorial to generate an `ANON_KEY` JWT based on `JWT_SECRET` and expiration time attributes. This is the credential for anonymous users.
- Use the tools provided in the tutorial to generate a `SERVICE_ROLE_KEY` based on `JWT_SECRET` and expiration time attributes. This is the credential for higher-privilege service roles.
- If your PostgreSQL business user uses a password different from the default, please modify the [`POSTGRES_PASSWORD`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L144) value accordingly
- If your object storage uses a password different from the default, please modify the [`S3_ACCESS_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L154) and [`S3_SECRET_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L155) values accordingly

After modifying Supabase credentials, you can restart Docker Compose containers to apply the new configuration:

```bash tab="Playbook"
./app.yml -t app_config,app_launch
```
```bash tab="Manual"
cd /opt/supabase; make up
```


------

## Advanced Topic: Domain Integration

If you're using Supabase on localhost or within a LAN, you can choose IP:Port direct connection to Kong's exposed HTTP port 8000 to access Supabase.

You can use an internal static DNS domain, but for serious production deployments, we recommend using real domain + HTTPS to access Supabase.
In this case, your server should have a public IP address, you should own a domain, use DNS resolution services provided by cloud/DNS/CDN providers to point it to the installation node's public IP (optional fallback: local `/etc/hosts` static resolution).

A simple approach is to batch replace the placeholder domain (`supa.pigsty`) with your actual domain, say `supa.pigsty.cc`:

```bash
sed -ie 's/supa.pigsty.cc/supa.pigsty/g' ~/pigsty/pigsty.yml
```

If you haven't configured it beforehand, reload Nginx and Supabase configurations:

```bash
make nginx      # Reload nginx configuration
make cert       # Apply for free HTTPS certificate with certbot
./app.yml       # Reload Supabase configuration
```

The modified configuration should look like the following snippet:

```yaml
all:
  vars:
    infra_portal:
      supa :
        domain: supa.pigsty.cc        # Replace with your domain!
        endpoint: "10.10.10.10:8000"
        websocket: true
        certbot: supa.pigsty.cc       # Certificate name, usually same as domain

  children:
    supabase:
      vars:
          supabase:                                       # the definition of supabase app
            conf:                                         # override /opt/supabase/.env
              SITE_URL: https://supa.pigsty                # <------- Change This to your external domain name
              API_EXTERNAL_URL: https://supa.pigsty        # <------- Otherwise the storage api may not work!
              SUPABASE_PUBLIC_URL: https://supa.pigsty     # <------- DO NOT FORGET TO PUT IT IN infra_portal!
```

Complete domain/HTTPS configuration can refer to the [Certificate Management](https://doc.pgsty.com/admin/cert) tutorial. You can also use Pigsty's built-in local static resolution and self-signed HTTPS certificates as fallback.

[![asciicast](https://doc.pgsty.com/img/asciinema/supa-domain.svg)](https://asciinema.org/a/731211)



------

## Advanced Topic: External Object Storage

You can use S3 or S3-compatible services as object storage for PostgreSQL backups and Supabase usage. Here we use Alibaba-Cloud OSS object storage as an example.

> Pigsty provides a [`terraform/spec/aliyun-meta-s3.tf`](https://github.com/pgsty/pigsty/blob/main/terraform/spec/aliyun-meta-s3.tf) template
> that can be used to deploy a server and an OSS bucket on Alibaba-Cloud.

First, modify the S3-related configuration in `all.children.supa.vars.apps.[supabase].conf`, pointing it to the Alibaba-Cloud OSS bucket:

```yaml
# if using s3/minio as file storage
S3_BUCKET: data                       # Replace with S3-compatible service connection information
S3_ENDPOINT: https://sss.pigsty:9000  # Replace with S3-compatible service connection information
S3_ACCESS_KEY: s3user_data            # Replace with S3-compatible service connection information
S3_SECRET_KEY: S3User.Data            # Replace with S3-compatible service connection information
S3_FORCE_PATH_STYLE: true             # Replace with S3-compatible service connection information
S3_REGION: stub                       # Replace with S3-compatible service connection information
S3_PROTOCOL: https                    # Replace with S3-compatible service connection information
```

Reload Supabase configuration with the following command:

```bash
./app.yml -t app_config,app_launch
```

You can also use S3 as PostgreSQL backup repository by adding an `aliyun` backup repository definition in `all.vars.pgbackrest_repo`:

```yaml
all:
  vars:
    pgbackrest_method: aliyun          # pgbackrest backup method: local,minio,[other user-defined repositories...], in this example backup is stored to MinIO
    pgbackrest_repo:                   # pgbackrest backup repository: https://pgbackrest.org/configuration.html#section-repository
      aliyun:                          # Define a new backup repository aliyun
        type: s3                       # Alibaba-Cloud OSS is S3-compatible object storage
        s3_endpoint: oss-cn-beijing-internal.aliyuncs.com
        s3_region: oss-cn-beijing
        s3_bucket: pigsty-oss
        s3_key: xxxxxxxxxxxxxx
        s3_key_secret: xxxxxxxx
        s3_uri_style: host
        path: /pgbackrest
        bundle: y                         # bundle small files into a single file
        bundle_limit: 20MiB               # Limit for file bundles, 20MiB for object storage
        bundle_size: 128MiB               # Target size for file bundles, 128MiB for object storage
        cipher_type: aes-256-cbc          # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest.MyPass    # Set an encryption password, pgBackrest backup repository encryption password
        retention_full_type: time         # retention full backup by time on minio repo
        retention_full: 14                # keep full backup for the last 14 days
```

Then specify using the `aliyun` backup repository in `all.vars.pgbackrest_method` and reset pgBackrest backup:

```bash
./pgsql.yml -t pgbackrest
```

Pigsty will switch the backup repository to external object storage. More backup configurations can refer to [PostgreSQL Backup](https://doc.pgsty.com/pgsql/backup) documentation.



------

## Advanced Topic: Using SMTP

You can use SMTP to send emails by modifying the supabase application configuration and adding SMTP information:

```yaml
all:
  children:
    supabase:        # supa group
      vars:          # supa group vars
        apps:        # supa group app list
          supabase:  # the supabase app
            conf:    # the supabase app conf entries
              SMTP_HOST: smtpdm.aliyun.com:80
              SMTP_PORT: 80
              SMTP_USER: no_reply@mail.your.domain.com
              SMTP_PASS: your_email_user_password
              SMTP_SENDER_NAME: MySupabase
              SMTP_ADMIN_EMAIL: adminxxx@mail.your.domain.com
              ENABLE_ANONYMOUS_USERS: false
```

Don't forget to use `app.yml` to reload the configuration


------

## Advanced Topic: True High Availability

After these configurations, you have an enterprise-grade Supabase (basic single-machine version) with public domain, HTTPS certificate, SMTP, PITR backup, monitoring, IaC, and 400+ extensions.
For high availability configuration, please refer to other parts of Pigsty documentation. If you're too lazy to read and learn, we provide hands-on Supabase self-hosting expert consulting services — ¥2000 to save you from the hassle of tinkering and downloading.

Single-node RTO/RPO relies on external object storage services for fallback. If your node fails, backups are retained in external S3 storage, and you can redeploy Supabase on a new node and restore from backup.
Such deployment can provide a minimum standard RTO (hour-level recovery time)/RPO (MB-level data loss) [fallback disaster recovery level](https://doc.pgsty.com/pgsql/backup) during failures.

To achieve RTO < 30s with zero data loss failover, you need to use [multi-node](https://doc.pgsty.com/install/multinode) high availability deployment, which involves:

- [ETCD](https://doc.pgsty.com/etcd/): DCS needs three or more nodes to tolerate one node failure.
- [PGSQL](https://doc.pgsty.com/pgsql/): PostgreSQL synchronous commit mode without data loss, recommend using at least three nodes.
- [INFRA](https://doc.pgsty.com/infra/): Monitoring infrastructure failure has less impact, recommend using dual replicas in production
- Supabase stateless containers themselves can also be multi-node replicas to achieve high availability.

In this case, you also need to modify PostgreSQL and MinIO access points to use DNS/L2 VIP/HAProxy and other [high availability access points](https://doc.pgsty.com/pgsql/service#access)
For these parts, you only need to refer to the documentation of each module in Pigsty for configuration and deployment.
We recommend referring to the configurations in [`conf/ha/trio.yml`](https://github.com/pgsty/pigsty/blob/main/conf/ha/trio.yml) and [`conf/ha/safe.yml`](https://github.com/pgsty/pigsty/blob/main/conf/ha/trio.yml) to upgrade cluster scale to three nodes or more.
