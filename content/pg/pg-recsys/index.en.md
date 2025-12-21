---
title: Building an ItemCF Recommender in Pure SQL
date: 2017-04-05
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Five minutes, PostgreSQL, and the MovieLens dataset—that’s all you need to implement a classic item-based collaborative filtering recommender.
tags: [PostgreSQL,PG开发,推荐系统]
---

Everyone knows “item-based collaborative filtering” (ItemCF): Amazon recommendations, YouTube watch-next, etc. Here’s how to implement it in PostgreSQL using the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. No Python, just SQL.

## Theory in one minute

ItemCF recommends items **similar** to what a user already **likes**. You need:

1. A user–item rating log (`user_id`, `item_id`, `rating`). Behavior logs (view, click, favorite, purchase) can be weighted into pseudo-ratings.
2. An item–item similarity matrix. For items *i* and *j*:

\[
w_{ij} = \frac{|N(i) \cap N(j)|}{\sqrt{|N(i)|\,|N(j)|}}
\]

where \(N(i)\) is the set of users who liked *i*. If many users like both, the items are similar. Represent the matrix as a table of triples `(i, j, similarity)`.

To predict user *u*’s preference for item *j*:

\[
p_{uj} = \sum_{i \in N(u)} w_{ji} r_{ui}
\]

In practice we limit the sum to the top-K similar items per item.

## Step 1: load ratings

```sql
CREATE TABLE mls_ratings (
  user_id   INT,
  movie_id  INT,
  rating    INT,
  rated_at  timestamptz,
  PRIMARY KEY (user_id, movie_id)
);

COPY mls_ratings FROM '/path/ratings.csv' CSV HEADER;
ALTER TABLE mls_ratings
  ALTER COLUMN rating SET DATA TYPE INT USING (rating::numeric * 2)::INT,
  ALTER COLUMN rated_at SET DATA TYPE timestamptz USING to_timestamp(rated_at::float);
```

## Step 2: compute item similarities

```sql
CREATE TABLE mls_similarity (
  i INT,
  j INT,
  sim FLOAT,
  PRIMARY KEY (i, j)
);

WITH occur AS (
  SELECT movie_id, count(*) AS n
  FROM mls_ratings
  GROUP BY movie_id
),
common AS (
  SELECT a.movie_id AS i, b.movie_id AS j, count(*) AS n
  FROM mls_ratings a JOIN mls_ratings b USING (user_id)
  GROUP BY i, j
)
INSERT INTO mls_similarity
SELECT i, j, n / sqrt(n1.n * n2.n)
FROM common
JOIN occur AS n1 ON n1.movie_id = i
JOIN occur AS n2 ON n2.movie_id = j;
```

This computes \(w_{ij}\) for every item pair using pure SQL. For production you’d prune very low scores to keep the table manageable.

## Step 3: recommend

Recommend 10 unseen movies to user 10:

```sql
WITH watched AS (
  SELECT movie_id, rating
  FROM mls_ratings
  WHERE user_id = 10
),
scored AS (
  SELECT s.j AS movie_id,
         sum(w.rating * s.sim) AS score
  FROM watched w
  JOIN mls_similarity s ON s.i = w.movie_id
  GROUP BY s.j
)
SELECT m.movie_id, score
FROM scored m
WHERE NOT EXISTS (
  SELECT 1 FROM watched w WHERE w.movie_id = m.movie_id
)
ORDER BY score DESC
LIMIT 10;
```

That’s it: a basic ItemCF pipeline entirely inside PostgreSQL. From here you can add time decay, normalize ratings, or materialize similarity tables per business need, but the foundation is just a handful of SQL statements.
