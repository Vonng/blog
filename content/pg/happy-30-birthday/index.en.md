---
title: "Happy 30th Birthday, PostgreSQL"
linkTitle: "PG Turns 30"
date: 2026-07-08
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  On July 8, 1996, the PostgreSQL community picked up the flame from Postgres95. Thirty years later, it has grown from a Berkeley research project into a default foundation of the global database ecosystem.
tags: [PostgreSQL,PG-Ecosystem]
---

Today, July 8, 2026, is PostgreSQL's 30th birthday.

Thirty years ago, Marc Fournier made a commit named "Postgres95 1.01 Distribution - Virgin Sources" into a newly created CVS repository.
It was the first commit in the PostgreSQL codebase ([`d31084e`](https://github.com/postgres/postgres/commit/d31084e9d1118b25fd16580d9d8c2924b5740dff)), and it still sits at the very bottom of the Git history.

[![commit.webp](commit.webp)](https://github.com/postgres/postgres/commit/d31084e9d1118b25fd16580d9d8c2924b5740dff)



## Why July 8?

Every July 8, the PostgreSQL community says "Happy Birthday" to the project. 
The date comes from July 8, 1996, when Marc Fournier set up the first public CVS server on Hub.org.
From that point on, the global community formally took over the code of a ten-year-old academic project from Berkeley. 
The "Initial release" date on Wikipedia is also marked as this day.

Of course, if you trace the lineage, PostgreSQL is older than thirty. 
In 1986, Michael Stonebraker started the POSTGRES project at the University of California, Berkeley,
as the successor to his earlier work Ingres. "Post-Ingres" is where the name came from.

![Early figures behind Postgres and Postgres95](lineage.webp)

Ingres itself goes back to the mid-1970s. In 1994, two Berkeley graduate students, Andrew Yu and Jolly Chen, replaced POSTGRES's original POSTQUEL language with SQL, then released the project as open source the next year under the name Postgres95.

By 1996, the Berkeley academic project had reached its end. What would happen to the code?
The answer was that CVS server. From that day on, the project no longer belonged to a university or a company.
It belonged to a self-organizing global community.

The project was renamed PostgreSQL in the same year, then restarted as version 6.0 in January 1997.
Stonebraker himself received the Turing Award in 2014, with POSTGRES as one of his signature works.


---------

## Birthday Details: July 8 or July 9?

Careful readers may notice a small puzzle: the timestamp of the "Virgin Sources" commit is actually 1996-07-09 06:22:35 UTC. So should the birthday be July 8 or July 9?

In the historical record, July 8 is the day the CVS server went live. That is a date, not a second-precision timestamp.
The only moment in this story that is precise to the second is the first commit at 1996-07-09 06:22:35 UTC.

Now convert that timestamp to California time, where Postgres95 was born. Berkeley was on Pacific Daylight Time, UTC-7. 
That makes the first commit 1996-07-08 23:22:35, only 37 minutes and 25 seconds before midnight.

So the community birthday, the day the server opened, and the first moment the code landed are separate facts. 
But in California time, they fall on the same late night. Move east to UTC, and the calendar has just flipped to July 9. 
The "one-day difference" is just those 37 minutes straddling midnight. 

From the place of birth, PostgreSQL was indeed born on July 8.


---------

## Thirty Years In

The milestones of these thirty years are easy to list: 6.5 introduced MVCC, 7.1 brought WAL, 8.0 added native Windows support, 
9.0 delivered streaming replication, 9.4 answered the NoSQL wave with JSONB, and 10 added logical replication and declarative partitioning. 
Today, PostgreSQL 18 is the stable major release, and 19 is already on the road.

But more important than any single feature is the seed Stonebraker planted forty years ago: **extensibility**.

Thirty years later, that is what turned PostgreSQL from a database into an ecosystem. 
PostGIS made it the de facto standard for geospatial data. TimescaleDB made it handle time series. 
Citus gave it horizontal scale. pgvector let it serve as a vector database in the AI wave. 
Hundreds of extensions mean PostgreSQL is no longer just a database. It is a database platform.

For years, PostgreSQL has stayed near the top of Stack Overflow's "most popular database" rankings. 
It has become the default choice. Or, in in other words: [**PostgreSQL is eating the database world**](/pg/pg-eat-db-world/).


---------

## The Next Thirty Years

Standing at the 30-year mark, we can already see a quiet change in who uses databases. More and more SQL is no longer written by humans. 
It is written by AI and agents. When agents become first-class database users, PostgreSQL's openness, extensibility, and rock-solid reliability are exactly the qualities this new era needs most.

![PostgreSQL's 30th birthday](featured.webp)

A database born in academia, raised by a community, and controlled by no single company is especially valuable today, as data sovereignty and AI infrastructure become more important.

On that late California night thirty years ago, Marc Fournier probably did not expect that the codebase he had just committed would,
thirty years later, be running in every corner of the planet: from Raspberry Pi boards to mainframes, 
from the first line of code at a startup to the core systems of banks and telecoms, and now to the memory layer of AI agents.

Happy birthday, PostgreSQL. May your next thirty years remain free, open, and rock solid.

![bruce.webp](bruce.webp)

## References

- [The first PostgreSQL Git commit: `d31084e`](https://github.com/postgres/postgres/commit/d31084e9d1118b25fd16580d9d8c2924b5740dff)
- [PostgreSQL History: PostgreSQL Documentation](https://www.postgresql.org/docs/current/history.html)
- [PostgreSQL: Wikipedia](https://en.wikipedia.org/wiki/PostgreSQL)
- [PostgreSQL is eating the database world](/pg/pg-eat-db-world/)
- [Stack Overflow 2025: PostgreSQL Has Dominated the Database World](/pg/so2025-pg/)
