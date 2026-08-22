# Vonng's Blog

[![Website: Blog](https://img.shields.io/badge/Website-vonng.com-slategray?style=flat)](https://vonng.com)

This is **Ruohang Feng** / [Vonng](https://github.com/Vonng)'s blog, about PostgreSQL, Database, Cloud-Exit, and other tech topics.

- The Main Site: https://vonng.com
- The English Blog: https://vonng.com/en/
- GitHub Pages: https://blog.vonng.com

--------

## Build

Requires **Hugo Extended 0.160.1+** and Go (Hugo Modules pull the theme).

```bash
make dev     # hugo server on :1313
make build   # production build into public/
make sync    # build, sanity-check, and rsync to the server
```

The theme is the [OINK](https://oink.pgsty.com/) Hugo Module, pinned in `go.mod`.
Upgrade it with `hugo mod get github.com/pgsty/oink@vX.Y.Z && hugo mod tidy`.

## Layout

```
hugo.yaml            # the whole site configuration: params, languages, menus
content/<column>/    # one top-level directory per blog column (type: blog)
content/authors/     # author profile pages — the `authors` taxonomy
data/home/*.yaml     # the landing page's sections, one file per language
data/footer/*.yaml   # the fat footer's link grid, one file per language
assets/scss/         # _variables_project.scss and _styles_project.scss
layouts/             # only what the theme does not already provide
```

--------

## License

This blog is licensed under **CC BY 4.0**. You're free to share and adapt the content,
as long as you give appropriate credit, link to the license, and indicate if changes were made.

Built with [Hugo](https://github.com/gohugoio/hugo) and the [**OINK**](https://oink.pgsty.com/) theme.

- Hugo: [Apache 2.0 License](https://github.com/gohugoio/hugo)
- OINK: [Apache 2.0 License](https://github.com/pgsty/oink/blob/main/LICENSE)
