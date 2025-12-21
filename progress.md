# Blog Front Matter 梳理进度

## 统计
- db: 56 篇中文，54 篇英文 ✅ 已完成
- cloud: 45 篇 ✅ 已完成
- pg: 103 篇 ✅ 已完成

## 处理规则
1. YAML 字段顺序: title, linkTitle, date, author, summary, series, tags
2. 中文标题使用全角引号 ""
3. linkTitle 若与 title 相同则删除
4. 英文版 title 和 linkTitle 用双引号括起来
5. summary 使用 `>` 式 here document，从第二行开始
6. summary 长度控制在 50-100 字左右
7. 每篇文章 1-5 个标签
8. 中文用中文标签，英文用英文标签
9. 记录非老冯作者

## 非老冯作者记录

### db 目录发现的非老冯作者：

| 文章 | 作者 | 原文链接 |
|------|------|----------|
| 7-week-7-db | Matt Blewitt | https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/ |
| bio-core-cpu-core | DHH | https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f |
| can-mysql-catchup | Peter Zaitsev | https://www.percona.com/blog/can-mysql-catch-up-with-postgresql/ |
| can-oracle-save-mysql | Peter Zaitsev | https://www.percona.com/blog/can-oracle-save-mysql/ |
| future-hardware | Alex Miller | https://transactional.blog/blog/2024-modern-database-hardware |
| goodbye-gpl | Martin Kleppmann | https://martin.kleppmann.com/2021/04/14/goodbye-gpl.html |
| microservice-bad-idea | DHH | https://world.hey.com/dhh/microservices-are-a-bad-idea-7a8dbddc |
| mongo-powered-by-pg | John De Goes | https://www.linkedin.com/pulse/mongodb-32-now-powered-postgresql-john-de-goes |
| open-data-standard | Paul Copplestone | https://supabase.com/blog/open-data-standards-postgres-otel-iceberg |
| openai-pg | Bohan Zhang | PGConf.Dev 2025 演讲 |
| oracle-kill-mysql | Peter Zaitsev | https://www.percona.com/blog/is-oracle-finally-killing-mysql/ |
| oracle-pg-xact | Laurenz Albe | https://www.cybertec-postgresql.com/en/comparison-of-the-transaction-systems-of-oracle-and-postgresql/ |
| oss-gov | Steven Vaughan-Nichols | https://www.zdnet.com/article/switzerland-now-requires-all-government-software-to-be-open-source/ |
| sakila-where-are-you-going | Marco Tusa | https://www.percona.com/blog/sakila-where-are-you-going/ |
| smalldata-decade | Hannes Mühleisen | https://duckdb.org/2025/05/19/the-lost-decade-of-small-data.html |

---

## db 目录进度 ✅ 已完成

所有 56 篇 db 目录文章 Front Matter 已处理完成。

---

## cloud 目录进度 ✅ 已完成

所有 45 篇 cloud 目录文章 Front Matter 已处理完成。

### cloud 目录发现的非老冯作者：

| 文章 | 作者 | 原文链接 |
|------|------|----------|
| ahrefs-saving | Efim Mirochnik | https://tech.ahrefs.com/how-ahrefs-saved-us-400m-in-3-years-by-not-going-to-the-cloud-8939dd930af8 |
| cloud-exit-faq | DHH | https://world.hey.com/dhh/cloud-exit-faq-5c3b15e8 |
| odyssey | DHH | https://world.hey.com/dhh |
| odyssey-done | DHH | https://world.hey.com/dhh/our-cloud-exit-savings-will-now-top-ten-million-over-five-years-c7d9b5bd |
| s3-scam | Maciej Pocwierz | https://medium.com/@maciej.pocwierz/how-an-empty-s3-bucket-can-make-your-aws-bill-explode-934a383cb8b1 |
| uptime | DHH | https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67 |

---

## pg 目录进度 ✅ 已完成

所有 103 篇 pg 目录文章 Front Matter 已处理完成。

### pg 目录发现的非老冯作者：

| 文章 | 作者 | 原文链接 |
|------|------|----------|
| pg-for-everything | Ajay Kulkarni | https://www.timescale.com/blog/postgres-for-everything/ |
| pg-in-2024 | Jonathan Katz | https://jkatz05.com/post/postgres/postgresql-2024/ |
| pg-license | Jonathan Katz | https://jkatz05.com/post/postgres/postgres-license-2024/ |
| vector-json-pg | Jonathan Katz | https://jkatz05.com/post/postgres/vectors-json-postgresql/ |
