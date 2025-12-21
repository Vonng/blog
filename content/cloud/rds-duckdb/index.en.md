---
title: "Alicloud’s rds_duckdb: Tribute or Rip-Off?"
summary: >
  Does bolting DuckDB onto RDS suddenly make open-source Postgres ‘trash’? Business and open source should be symbiotic. If a vendor only extracts without giving back, the community will spit it out."
date: 2025-03-06
tags: [PostgreSQL,PG生态]
categories: [Blog]
---

A viral post titled “[Heavenly ‘PostgreSQL’ Calls Earthly Postgres ‘Little Trash’](https://mp.weixin.qq.com/s/fFTTRioeTvCmjKip0lx3Cg)” hyped up Alicloud RDS’s new `rds_duckdb` plugin for OLAP and declared that managed RDS PG is noble while open-source Postgres is garbage. That take is ridiculous.

I know DuckDB and the derivative `pg_duckdb` extension inside out. I’m happy when cloud vendors integrate open source legally and respectfully. But if you disparage the upstream while riding on its work, someone has to push back.

-------

## PG + DuckDB, the background

DuckDB is a fast embedded OLAP database I’ve followed for years. In “[PostgreSQL Is Eating the Database World](/en/pg/pg-eat-db-world/)” I talked about welding DuckDB onto PG to build true HTAP, and that article [sparked a worldwide trend](/en/db/pg-kiss-duckdb/). 2024 saw multiple PG extensions that embed DuckDB; it was one of the year’s signature moves.

Among those experiments, `pg_duckdb`—co-developed by MotherDuck and Hydras’ OLAP startup—is the most promising. I packaged it for EL8/9, Debian 12, Ubuntu 22/24, both x86 and ARM, and spent countless hours testing it.

Out of the 200+ PG extensions I maintain, the four DuckDB-related ones (including `pg_mooncake`, built atop `pg_duckdb`) are both the most painful and the most exciting: huge dependencies, gnarly build chains, multiple `libduckdb` versions, cross-platform PG support. But OLTP + OLAP fusion is worth the pain.

-------

## Tribute or plagiarism?

When Alicloud launched `rds_duckdb` last October, my first reaction was “cool, adoption!” Two months after `pg_duckdb` went public, a cloud vendor followed suit—that helps the industry.

But `rds_duckdb` isn’t open source, so we can’t inspect its code. We can only observe behavior, and the surface looks… familiar. Early `pg_duckdb` exposed a single switch: `SET pg_duckdb.execution = on;` and boom, DuckDB queries over PG tables. `rds_duckdb`’s centerpiece? `SET rds_duckdb.execution = on;`. Same flow, different prefix.

Given the timing (two months gap) and the identical UX, it’s reasonable to assume heavy inspiration at minimum. Maybe the code is different—we can’t tell because it’s closed. They added some extra functions (copy data, show sizes, PG 12/13 support), but nothing groundbreaking. Honestly it looks like a prototype compared to later `pg_duckdb` builds or `pg_mooncake`. If you’re going to plagiarize, at least do it well.

And if it’s a “tribute,” where’s the attribution? No credits to `pg_duckdb` or even DuckDB anywhere.

-------

## Obligations under MIT

Both DuckDB and `pg_duckdb` are MIT licensed. The requirements are simple: **keep the copyright notice and include the MIT license text**. It’s literally “use the code for free, just don’t erase our names.”

I scoured Alicloud’s RDS docs and couldn’t find DuckDB’s copyright notice or license anywhere. If `rds_duckdb` doesn’t reuse code, fine. But if it does, omitting attribution violates MIT before we even talk about morals.

-------

## Attacking open source

I don’t know whether that WeChat account coordinates with Alicloud, but their anti-open-source streak is obvious. Recent posts include calling Postgres “little trash,” saying “[cloud-native DBs destroyed Kubernetes self-managed databases](https://mp.weixin.qq.com/s/YCUBDWzPGs2meubY2uYqXQ),” and “[open source is a scam](https://mp.weixin.qq.com/s/iTow4Pu8DjDNJl3CnuiLBA).”

This bias is absurd. Open source is why foundational software exists at all. DeepSeek’s breakthrough? Standing on open shoulders. Postgres’s rise? Same story. Most “cloud databases” are just open-source engines with proprietary duct tape. Without OSS, their products wouldn’t exist.

Yet hyperscalers rake in profits and rarely give back, igniting debates about “[clouds freeloading on open source](https://mp.weixin.qq.com/s/W5kOLxeJCIHjnWbIHc1Pzw)” and [the tensions keep rising](https://mp.weixin.qq.com/s/jgYDHdCqWDRDfoFkfs7W8Q). Some vendors do contribute—AWS helped make `pgvector` the de facto standard and released log_fdw, pgcollection, pgtle, etc.

Alicloud, however, seems stuck in “eat from the OSS/Startup bowl” mode. The manners are rough, the product quality is [embarrassing](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA), and customers end up thinking the whole thing is a clown show. Users aren’t mad that clouds *use* open source; they’re mad when a giant ships a half-baked clone, sneers at the upstream, and calls it innovation.

-------

## Further reading

[Grassroots Circus: Alicloud RDS Crashed Again](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA)

[Is Cloud Storage a Pig-Butchering Scam?](https://mp.weixin.qq.com/s/UxjiUBTpb1pRUfGtR9V3ag)

[Is a Cloud Database Just a Tax on IQ?](https://mp.weixin.qq.com/s/LefEAXTcBH-KBJNhXNoc7A)

[Alicloud’s High-Availability Myth Shattered](https://mp.weixin.qq.com/s/rXwEayprvDKCgba4m-naoQ)

[From Cost Cutting to Actual Efficiency Gains](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg)

[Lessons From Alicloud’s Epic Failure](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ)

[Alipay Down Again During Double-11](https://mp.weixin.qq.com/s/D2XmL2YYN2kqHtwFN4FVGQ)

[Alicloud DCDN Racked Up ¥1,600 in 32 Seconds](https://mp.weixin.qq.com/s/0Wnv1B80Tk4J03X3uAm4Ww)

[Forecast: This Alicloud Incident Will Last 20 Years](https://mp.weixin.qq.com/s/G41IN2y8DrC002FQ_BXtXw)

[Alicloud Singapore AZ-C Fire](https://mp.weixin.qq.com/s/EDRmP7ninfSx-CgNDb8mpg)

[Another Alicloud Outage—Was It a Fiber Cut?](https://mp.weixin.qq.com/s/cb2Lh56uINxacM2uUaB6Vw)

[Cloud Computing: Mediocrity Is Original Sin](https://mp.weixin.qq.com/s/jYIqj94B07oTu9KC85bjtQ)

[taobao.com Certificate Expired](https://mp.weixin.qq.com/s/-ntsNfdEq3b4qs5tKP7tfQ)

[Stop Worshipping Toothpaste Clouds](https://mp.weixin.qq.com/s/XZqe4tbJ9lgf8a6PWj7vjw)

[Luo Yonghao Can’t Save Toothpaste Cloud](https://mp.weixin.qq.com/s/s_MCdaCByDBuocXkY1tvKw)

[Young People Lost Inside Alicloud](https://mp.weixin.qq.com/s/w7YzdxSrAsIqk2gXBks9CA)

[Does Alicloud’s Price Cut Actually Cut Costs?](https://mp.weixin.qq.com/s/rp8Dtvyo9cItBJSsvfrKjw)

[Alicloud Weekly: Database Control Plane Down Again](https://mp.weixin.qq.com/s/3F1ud-tWB3eymu1-dxSHMA)

[Alicloud’s Epic Crash, Again](https://mp.weixin.qq.com/s/cTge3xOlIQCALQc8Mi-P8w)

[How Cloud Vendors See Customers: Broke, Idle, Needy](https://mp.weixin.qq.com/s/y9IradwxTxOsUGcOHia1XQ)
