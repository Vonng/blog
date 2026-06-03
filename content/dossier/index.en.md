---
title: "Ruohang Feng - PostgreSQL Contributor Dossier"
summary: "Nomination dossier for PostgreSQL Recognized Contributor: code, packaging, translation, education, and advocacy contributions by Ruohang Feng."
description: "Ruohang Feng's PostgreSQL Contributor Dossier, updated from the May 2026 DOCX source and presented as a static HTML page."
date: 2026-05-01
layout: dossier
showDate: false
showAuthor: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showComments: false
---

<article class="dossier" aria-labelledby="dossier-title">
  <section class="dossier-sheet dossier-sheet-primary" aria-label="Contributor dossier page 1">
    <div class="dossier-topline">
      <span>May 2026</span>
      <span>Ruohang Feng - PostgreSQL Contributor Dossier</span>
    </div>

    <header class="dossier-hero">
      <div>
        <h1 id="dossier-title">Ruohang Feng (Vonng)</h1>
        <p>Nomination Dossier - PostgreSQL Recognized Contributor</p>
      </div>
      <aside aria-label="Prepared for">
        <span>Prepared for</span>
        <strong>Contributors Committee</strong>
        <a href="mailto:contributors@postgresql.org">contributors@postgresql.org</a>
        <time datetime="2026-05">May 2026</time>
      </aside>
    </header>

    <dl class="dossier-meta">
      <div class="dossier-meta-name">
        <dt>Name</dt>
        <dd>Ruohang Feng / 冯若航 / Vonng</dd>
      </div>
      <div class="dossier-meta-identity">
        <dt>Primary Identity</dt>
        <dd><a href="https://github.com/pgsty/pigsty">Pigsty</a> Author &amp; Founder</dd>
      </div>
      <div class="dossier-meta-based">
        <dt>Based in</dt>
        <dd>Shanghai, China · Singapore</dd>
      </div>
      <div class="dossier-meta-active">
        <dt>Active on Postgres since</dt>
        <dd>2015 - 11 years, independent</dd>
      </div>
      <div class="dossier-meta-links">
        <dt>Links</dt>
        <dd>
          <a href="https://github.com/Vonng">Github</a>
          <a href="https://vonng.com/en">Website</a>
          <a href="https://www.linkedin.com/in/vonng">LinkedIn</a>
          <a href="https://x.com/RonVonng">Twitter</a>
          <a href="mailto:rh@vonng.com">Email</a>
        </dd>
      </div>
    </dl>

    <p class="dossier-lede">
      Sustained contributions to the PostgreSQL ecosystem across <em>closely-related code, packaging, documentation translation, and community education</em> - the categories enumerated in the <a href="https://www.postgresql.org/about/policies/contributors/">Recognized Contributors Policy</a>. Produced independently since 2015, with focus on the cross-distribution extension supply chain, Chinese-language access to official Postgres material, and vendor-neutral advocacy from within the Chinese Postgres community.
    </p>

    <section class="dossier-section" aria-labelledby="code">
      <h2 id="code"><span>I. Code</span><em>closely related external projects</em></h2>

      <div class="dossier-entry">
        <h3>Pigsty - PostgreSQL distribution</h3>
        <p><a href="https://github.com/pgsty/pigsty">Pigsty</a> (5,131 GitHub stars, current release v4.3.0) is a battery-included open-source PostgreSQL distribution integrating HA (Patroni), PITR (pgBackRest), pooling (PgBouncer), observability (pg_exporter + Grafana), and the extension ecosystem described below. It runs directly on bare Linux across 16 distributions and has gained visible community adoption among Postgres distributions. The documentation site <a href="https://pigsty.io/">pigsty.io</a> currently serves approximately <strong>10,000 developers</strong> and <strong>1M package downloads per month</strong>.</p>
      </div>

      <div class="dossier-entry">
        <h3>pg_exporter - Prometheus exporter for PostgreSQL</h3>
        <p><a href="https://github.com/pgsty/pg_exporter">pg_exporter</a> is a Go implementation exposing 600+ PostgreSQL metrics via declarative YAML configuration, with dynamic query planning, multi-version compatibility, and per-cluster customization. It powers the Pigsty monitoring stack and is also used independently by operators who do not run Pigsty.</p>
      </div>
    </section>

    <section class="dossier-section" aria-labelledby="packaging">
      <h2 id="packaging"><span>II. Packaging</span><em>Packagers</em></h2>

      <div class="dossier-stats" aria-label="Packaging metrics">
        <div><strong>1,617</strong><span>Extension catalog entries</span></div>
        <div><strong>511</strong><span>PG extensions available with PGDG</span></div>
        <div><strong>16</strong><span>Linux distributions</span></div>
        <div><strong>14</strong><span>PG kernel forks</span></div>
        <div><strong>100k+</strong><span>Packages in repository</span></div>
      </div>

      <p>Two complementary packaging efforts, both fully compatible with the upstream PGDG YUM and APT archives:</p>

      <div class="dossier-entry">
        <h3>PGEXT.CLOUD - global extension binary repository</h3>
        <p><a href="https://pgext.cloud/">PGEXT.CLOUD</a> catalogs metadata for <strong>1,617 extensions</strong> in the broader Postgres ecosystem and, when used together with PGDG, provides installable RPM and DEB packages for <strong>511 PostgreSQL extensions</strong> across 16 Linux distributions (EL 8/9/10, Debian 11/12/13, Ubuntu 22.04/24.04/26.04, and derivatives) and 5 PostgreSQL major versions (14-18). It remains interoperable with the upstream PGDG repos maintained by Devrim Gündüz and Christoph Berg. The registry focuses on extensions that fall outside the upstream PGDG build matrix and on unifying EL-family and Debian-family coverage under a single metadata schema. The repository currently holds 100k+ packages and is globally CDN-accessible.</p>
      </div>

      <div class="dossier-entry">
        <h3>PGDG mirror for mainland China</h3>
        <p>Also operates a <a href="https://pigsty.io/docs/repo/pgdg/#mirror"><strong>hosted mirror of the official PGDG YUM and APT repositories for the mainland-China region</strong></a>, addressing network-access problems that have historically blocked Chinese users from installing official Postgres builds reliably. The mirror tracks upstream and preserves full compatibility with the canonical PGDG layout.</p>
      </div>

      <div class="dossier-entry">
        <h3>PIG - extension package manager &amp; CLI</h3>
        <p><a href="https://pigsty.io/docs/pig">PIG</a> is a standalone Go CLI serving as both a PostgreSQL extension package manager and a general-purpose Postgres package-management tool. It resolves extension dependencies, detects the running kernel, and pulls binaries from PGEXT.CLOUD or the upstream PGDG repositories. PIG v1.0 was announced on <a href="https://www.postgresql.org/about/news/">postgresql.org News</a>.</p>
      </div>
    </section>

    <section class="dossier-section" aria-labelledby="translation">
      <h2 id="translation"><span>III. Translation</span><em>user-facing documentation</em></h2>
      <p>An independent, actively maintained Chinese translation track covering the full official Postgres documentation set and the surrounding ecosystem:</p>
      <ul>
        <li><strong>PostgreSQL 14-18 official documentation</strong> - Simplified Chinese translation, published at <a href="https://pg.center/docs/">pg.center/docs/</a>, maintained across releases rather than pinned to a single version.</li>
        <li><strong>Core companion projects</strong> - full documentation translations for <em>PgBouncer</em>, <em>Patroni</em>, and <em>pgBackRest</em>.</li>
        <li><strong>Extension documentation</strong> - Chinese translations for the documentation of approximately <strong>500 Postgres extensions</strong> in the PGEXT.CLOUD catalog, substantially lowering the barrier for Chinese-speaking users to discover and adopt extensions.</li>
      </ul>
      <blockquote>This is an independent, newly-built translation track maintained actively against current upstream releases.</blockquote>
    </section>

    <footer class="dossier-page-footer">
      <span>Ruohang Feng - Contributor Dossier</span>
      <span>Page 1 / 2</span>
    </footer>
  </section>

  <section class="dossier-sheet" aria-label="Contributor dossier page 2">
    <div class="dossier-topline">
      <span>May 2026</span>
      <span>Ruohang Feng - PostgreSQL Contributor Dossier</span>
    </div>

    <header class="dossier-continuation">
      <div>
        <h2>Ruohang Feng (Vonng)</h2>
        <p>Nomination Dossier - continued</p>
      </div>
      <a href="mailto:contributors@postgresql.org">contributors@postgresql.org</a>
    </header>

    <section class="dossier-section" aria-labelledby="education">
      <h2 id="education"><span>IV. Open Education</span><em>blogs, articles, reference material</em></h2>

      <div class="dossier-entry">
        <h3>pg.center - Chinese mirror of postgresql.org</h3>
        <p><a href="https://pg.center/docs/">pg.center</a> is a Chinese-language mirror of postgresql.org: the official site content, the documentation set for PG 14-18, and companion project and extension documentation are translated and served together as a single reference surface for Chinese-speaking operators and developers. It is the primary Chinese entry point to official Postgres material currently maintained against live releases.</p>
      </div>

      <div class="dossier-entry">
        <h3>Postgres writing in Chinese (2016-present)</h3>
        <p>Has published continuously on Postgres in Chinese for ~10 years through the personal column <em>PostgreSQL, Database and Cloud</em> and the WeChat channel <em>Lao Feng Yun Shu</em> (老冯云数). The WeChat channel itself has <strong>~60,000 subscribers</strong>, with a combined cross-platform readership of approximately <strong>100,000 followers</strong> - an audience that establishes the author as one of the leading independent KOL voices on databases and cloud infrastructure in the Chinese-speaking technical community. Coverage spans Postgres ecosystem, extensions, application development, operations, administration, and kernel-level discussion.</p>
      </div>

      <div class="dossier-entry">
        <h3>&ldquo;Postgres is Eating the Database World&rdquo; (2024)</h3>
        <p>English essay at <a href="https://vonng.com/en/pg/pg-eat-db-world/">vonng.com</a>, which <a href="https://news.ycombinator.com/item?id=39711863">reached the Hacker News front page</a> and subsequently circulated widely in Postgres ecosystem discourse around extensibility.</p>
      </div>
    </section>

    <section class="dossier-section" aria-labelledby="community">
      <h2 id="community"><span>V. Community &amp; Advocacy</span></h2>
      <ul>
        <li>Former member of the <strong>Technical Committee of the PostgreSQL Chinese Community</strong>.</li>
        <li>Regular speaker and attendee at <strong>PGConf.Asia</strong> and <strong>PGConf.Dev</strong> for multiple consecutive years.</li>
        <li>Operates as a <strong>one-person independent developer</strong> (OPC) - not a vendor employee and not an organizational affiliate - providing a rare vendor-neutral voice from within the Chinese Postgres community in a landscape dominated by large-platform and state-backed actors.</li>
      </ul>

      <div class="dossier-entry">
        <h3>Recent conference participation</h3>
        <div class="dossier-table-wrap">
          <table class="dossier-events">
            <thead>
              <tr>
                <th>Event</th>
                <th>Role</th>
                <th>Topic</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td data-label="Event">PGConf.Dev 2026</td>
                <td data-label="Role">Speech</td>
                <td data-label="Topic">Extensions for Everyone</td>
              </tr>
              <tr>
                <td data-label="Event">HOW / PGConf.Asia 2026</td>
                <td data-label="Role">Speech</td>
                <td data-label="Topic">DBA Agent and Runtime</td>
              </tr>
              <tr>
                <td data-label="Event">HOW / PGConf.Asia 2025</td>
                <td data-label="Role">Speech</td>
                <td data-label="Topic">Let your elephant run</td>
              </tr>
              <tr>
                <td data-label="Event">PGEXT.Day 2025</td>
                <td data-label="Role">Speech</td>
                <td data-label="Topic">The Missing Package Manager and Extension Repo for PostgreSQL Ecosystem</td>
              </tr>
              <tr>
                <td data-label="Event">PGConf.Dev 2025</td>
                <td data-label="Role">Lightning Talk</td>
                <td data-label="Topic">Extension Delivery: Make your PGEXT accessible to users</td>
              </tr>
              <tr>
                <td data-label="Event">PGConf.Dev 2024</td>
                <td data-label="Role">Attendee</td>
                <td data-label="Topic">-</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="dossier-section dossier-assessment" aria-labelledby="assessment">
      <h2 id="assessment"><span>Honest Assessment</span></h2>
      <p>The recognition being sought is <strong>Significant Contributor</strong>, on the basis of sustained packaging, closely-related code, documentation translation, and community education. To be explicit about what this case is <em>not</em>:</p>
      <ul>
        <li><strong>Not a kernel developer or core committer.</strong> The author makes no claim to core-developer or committer standing within the PostgreSQL project.</li>
        <li><strong>No track record of committed patches</strong> to the core Postgres repository, and participation on pgsql-hackers has been occasional rather than sustained - a fact plainly visible in the list archives.</li>
      </ul>
    </section>

    <section class="dossier-section dossier-verification" aria-labelledby="verification">
      <h2 id="verification"><span>Verification</span></h2>
      <ul>
        <li><strong>Code &amp; packaging:</strong> <a href="https://github.com/pgsty/pigsty">github.com/pgsty/pigsty</a> · <a href="https://github.com/pgsty/pg_exporter">github.com/pgsty/pg_exporter</a> · <a href="https://pgext.cloud/">pgext.cloud</a> · <a href="https://pigsty.io/docs/pig">pigsty.io/docs/pig</a></li>
        <li><strong>Translation &amp; writing:</strong> <a href="https://pg.center/docs/">pg.center/docs/</a> · <a href="https://vonng.com/en">vonng.com/en</a> (English) · &ldquo;老冯云数&rdquo; on WeChat (Chinese) · <a href="https://www.postgresql.org/about/news/">postgresql.org News archive</a></li>
      </ul>
    </section>

    <footer class="dossier-page-footer">
      <span>Ruohang Feng - <a href="mailto:rh@vonng.com">rh@vonng.com</a> - <a href="https://vonng.com/">https://vonng.com</a></span>
      <span>Page 2 / 2</span>
    </footer>
  </section>
</article>
