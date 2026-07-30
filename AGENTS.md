# Repository Instructions

## English Blog Translation Policy

### Scope and file layout

- A blog leaf bundle is a directory under `content/{ai,cloud,db,misc,pg,pigsty,trip}/` containing `index.md`.
- Its English version, when required, must be the sibling file `index.en.md` in the same bundle.
- Section pages, taxonomy pages, author pages, and other non-blog content are outside this translation policy.

### Articles that must not be translated

Leave the following articles intentionally without `index.en.md`:

- `content/misc/fengzhenbiao/` — 冯振彪自传。
- `content/pg/pg-apt-loong64/` — 龙芯相关文章。
- Any Chinese article that is itself a translation or adaptation of somebody else's English article, talk, or publication. Do not translate such content back into English.

Determine whether an article is translation-derived from explicit attribution in the body and front matter, such as an original-source URL, a translation tag, or an external author. Older publication dates and multiple authors are useful clues, but are not sufficient evidence on their own. If the provenance remains genuinely ambiguous after reading the article, report it for confirmation instead of translating it automatically.

### Required English style

For every other original Chinese article that needs an English version:

- Write idiomatic, professional, concise English for a Western technical audience, in the style of a strong Hacker News submission or technical essay.
- Preserve the author's argument, technical meaning, evidence, and distinctive voice. Be concise without turning the article into a summary.
- Prefer direct sentences, concrete verbs, short coherent paragraphs, and restrained wording. Avoid Chinglish, inflated marketing language, bureaucratic phrasing, and ornamental prose.
- Translate ideas rather than surface wording. Recast Chinese idioms, memes, jokes, wordplay, historical allusions, and culture-specific references into an equivalent that works naturally in an English-speaking context. Add a compact explanation when needed; never force a literal translation that sounds awkward or loses the point.
- Use established English technical terminology and Western naming, capitalization, punctuation, date, and number conventions.
- Preserve valid front matter semantics, Markdown structure, code, commands, URLs, images, captions, tables, and other bundle assets. Do not introduce new factual claims or silently remove substantive content.

### Per-article workflow and quality bar

- Use one brand-new SubAgent with a clean context for each article. That SubAgent must work on that article only; never batch multiple articles into one translation context.
- Use the highest available reasoning effort. Give the SubAgent the Chinese source, relevant local assets or references, this policy, and the target `index.en.md` path.
- The assigned SubAgent must complete three review passes and three proofreading passes before finalizing:
  1. Check fidelity, completeness, structure, and preservation of nuance.
  2. Check technical accuracy, terminology, names, figures, code, links, and captions.
  3. Check idiomatic English, cultural adaptation, Hacker News tone, concision, and narrative flow.
  4. Proofread grammar, spelling, punctuation, typography, and sentence-level clarity.
  5. Proofread terminology consistency, front matter, Markdown, links, media, and formatting.
  6. Read the entire English article once more as a standalone essay and polish any remaining stiffness, repetition, or ambiguity.
- After all articles are finished, run a Hugo production build, check internal links, and rescan the leaf bundles for missing `index.en.md` files. Report intentional exclusions separately from actionable omissions.
