---
title: "Pigsty v0.5: Declarative DB Templates"
linkTitle: "Pigsty v0.5 Release Notes"
date: 2020-12-26
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.5.0)）
summary: >
  Pigsty v0.5 introduces declarative database templates so roles, schemas, extensions, and ACLs can be described entirely in YAML.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.5.0

## v0.5.0

### Outline

- The official docs site (http://pigsty.cc/) is live.
- Database templating becomes fully declarative: define users, roles, databases, ACLs, extensions, and schemas in config.
- The default [access model](https://pigsty.cc/docs/setup/security) is refined and HBA management now comes straight from Pigsty instead of Patroni.
- Grafana provisioning switched from shoving a sqlite file to JSON provisioning via API.
- Added the `pg-cluster-replication` dashboard to the open bundle.
- CentOS 7.8 offline bundle: `pkg.tgz`.

### Declarative Database Layouts

Multi-tenant headaches go away once everything is described as code. The new templates let you declare users, passwords, role hierarchies, DB defaults, extensions, schemas, and default privileges in YAML so a single config file replaces piles of runbooks. A stripped example:

```yaml
# per-cluster settings
pg_users:
  - username: test
    password: test
    comment: default test user
    groups: [ dbrole_readwrite ]
pg_databases:
  - name: test
    extensions: [{name: postgis}]
    parameters:
      search_path: public,monitor

# environment-wide system roles
pg_replication_username: replicator
pg_replication_password: DBUser.Replicator
pg_monitor_username: dbuser_monitor
pg_monitor_password: DBUser.Monitor
pg_admin_username: dbuser_admin
pg_admin_password: DBUser.Admin

# default roles
pg_default_roles:
  - username: dbrole_readonly
    options: NOLOGIN
    comment: role for readonly access

  - username: dbrole_readwrite
    options: NOLOGIN
    comment: role for read-write access
    groups: [ dbrole_readonly ]

  - username: dbrole_admin
    options: NOLOGIN BYPASSRLS
    comment: role for object creation
    groups: [dbrole_readwrite,pg_monitor,pg_signal_backend]

  - username: postgres
    options: SUPERUSER LOGIN
    comment: system superuser

  - username: replicator
    options: REPLICATION LOGIN
    groups: [pg_monitor, dbrole_readonly]
    comment: system replicator

  - username: dbuser_monitor
    options: LOGIN CONNECTION LIMIT 10
    comment: system monitor user
    groups: [pg_monitor, dbrole_readonly]

  - username: dbuser_admin
    options: LOGIN BYPASSRLS
    comment: system admin user
    groups: [dbrole_admin]

  - username: dbuser_stats
    password: DBUser.Stats
    options: LOGIN
    comment: business read-only user for statistics
    groups: [dbrole_readonly]

# default privileges applied to dbsu/admin objects
pg_default_privilegs:
  - GRANT USAGE                         ON SCHEMAS   TO dbrole_readonly
  - GRANT SELECT                        ON TABLES    TO dbrole_readonly
  - GRANT SELECT                        ON SEQUENCES TO dbrole_readonly
  - GRANT EXECUTE                       ON FUNCTIONS TO dbrole_readonly
  - GRANT INSERT, UPDATE, DELETE        ON TABLES    TO dbrole_readwrite
  - GRANT USAGE,  UPDATE                ON SEQUENCES TO dbrole_readwrite
  - GRANT TRUNCATE, REFERENCES, TRIGGER ON TABLES    TO dbrole_admin
  - GRANT CREATE                        ON SCHEMAS   TO dbrole_admin
  - GRANT USAGE                         ON TYPES     TO dbrole_admin

pg_default_schemas: [monitor]

pg_default_extensions:
  - { name: 'pg_stat_statements',  schema: 'monitor' }
  - { name: 'pgstattuple',         schema: 'monitor' }
  - { name: 'pg_qualstats',        schema: 'monitor' }
  - { name: 'pg_buffercache',      schema: 'monitor' }
  - { name: 'pageinspect',         schema: 'monitor' }
  - { name: 'pg_prewarm',          schema: 'monitor' }
  - { name: 'pg_visibility',       schema: 'monitor' }
  - { name: 'pg_freespacemap',     schema: 'monitor' }
  - { name: 'pg_repack',           schema: 'monitor' }
  - name: postgres_fdw
  - name: file_fdw
  - name: btree_gist
  - name: btree_gin
  - name: pg_trgm
  - name: intagg
  - name: intarray

pg_hba_rules:
  - title: allow meta node password access
    role: common
    rules:
      - host    all     all                         10.10.10.10/32      md5

  - title: allow intranet admin password access
    role: common
    rules:
      - host    all     +dbrole_admin               10.0.0.0/8          md5
      - host    all     +dbrole_admin               172.16.0.0/12       md5
      - host    all     +dbrole_admin               192.168.0.0/16      md5

  - title: allow intranet password access
    role: common
    rules:
      - host    all             all                 10.0.0.0/8          md5
      - host    all             all                 172.16.0.0/12       md5
      - host    all             all                 192.168.0.0/16      md5

  - title: allow local read-write access
    role: common
    rules:
      - local   all     +dbrole_readwrite                               md5
      - host    all     +dbrole_readwrite           127.0.0.1/32        md5

  - title: allow read-only access
    role: replica
    rules:
      - local   all     +dbrole_readonly                               md5
      - host    all     +dbrole_readonly           127.0.0.1/32        md5
pg_hba_rules_extra: []

pgbouncer_hba_rules:
  - title: local password access
    role: common
    rules:
      - local  all          all                                     md5
      - host   all          all                     127.0.0.1/32    md5

  - title: intranet password access
    role: common
    rules:
      - host   all          all                     10.0.0.0/8      md5
      - host   all          all                     172.16.0.0/12   md5
      - host   all          all                     192.168.0.0/16  md5
pgbouncer_hba_rules_extra: []
```

### Templates and Permissions

Two SQL templates (`pg-init-template.sql` for template1 and `pg-init-business.sql` for business databases) now give you hooks to seed any custom logic. The default ACL layout was tightened for multi-tenant instances: regular users no longer get implicit CONNECT on foreign databases, CREATE on their own DB, or CREATE inside `public`.

## Provisioning Updates

Grafana provisioning now happens through the API, so you can feed dashboards into an existing Grafana by simply pointing `grafana_url` at a username/password endpoint. Pigsty generates HBAs on its own so Patroni stays focused on HA, and the supply chain is cleaner.
