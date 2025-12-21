---
title: Understanding Character Encoding
date: 2018-07-01
hero: /hero/character-encoding.jpg
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Code is literally “encoding,” and everything collapses if you mishandle text. Here’s a practical tour of characters, glyphs, Unicode, and UTF encodings.
menu:
  sidebar:
    parent: note
---

> [WeChat original](https://mp.weixin.qq.com/s/Yzd64oCjjlk4brERhKBuKA)

Programmers spend their lives with **code**—both source code and encodings. Representing text with bits is harder than it looks: character sets, comparators, normalization, locale rules, variable-length encodings, BOMs, surrogate pairs, regex compatibility, even security bugs lurk beneath. Here’s the field guide.

## 0x01 Basics

Computers only understand binary. **Encoding** bridges abstract data types and bit patterns. Take the number 42: encoding maps it to `00101010`; decoding reverses the mapping. Strings are sequences of **characters**, so “string encoding” maps abstract characters to bits.

### Characters vs. glyphs

A character is an abstract textual atom; a glyph is its visual rendering. Most of the time they’re 1–1, but not always: `à` can be a precomposed character or the combination of `a` + grave accent. Conversely, a single character in Arabic or Devanagari might comprise many glyph components. Don’t confuse the abstract entity with its shapes.

### Character sets

A **character set** is the inventory of characters you care about. A **coded character set** assigns each abstract character a number (a code point). ASCII, GB2312, JIS X 0208, ISO-8859-1 are all different sets tailored to different languages.

## 0x02 Unicode

Unicode tries to be the superset of all sets: one code point per abstract character. It currently defines ~150k characters. Unicode separates layers:

1. **Abstract characters** (the idea of “A,” “é,” “汉”).
2. **Code points** (U+0041, U+00E9, U+6C49).
3. **Glyphs** (fonts decide how to draw them).

It also catalogs metadata: combining marks, directional controls, normalization forms, case folding, collation rules, emoji properties, etc.

## 0x03 From code points to code units

Assigning numbers isn’t enough; we must turn those numbers into byte sequences. Enter **code units**—the minimal bit chunks used to store/exchange characters. Typical choices are 8, 16, or 32 bits. Unicode defines three mainstream encodings:

- **UTF-32** – fixed length, one 32-bit code unit per code point. Simple but wasteful.
- **UTF-16** – variable length, 16-bit units. Most characters fit in one unit; supplementary planes use surrogate pairs.
- **UTF-8** – variable length, 8-bit units. ASCII stays single-byte; other characters use 2–4 bytes.

Self-synchronizing encodings are critical: if a byte flips, the decoder should recover at the next boundary. UTF-8 and UTF-16 were designed with that in mind (no prefix of a multi-byte sequence is itself a valid start byte).

### UTF-32

Pros: fixed length → O(1) indexing, trivial implementation. Cons: 4× the storage of ASCII text, often 2×–4× other encodings. Useful inside APIs where convenience outweighs memory cost.

### UTF-16

Uses 16-bit units. Characters in the Basic Multilingual Plane (U+0000–U+FFFF) fit in one unit; supplementary characters (U+10000–U+10FFFF) require a surrogate pair. Endianness matters, hence BOMs (`FE FF` vs `FF FE`). Historically popular on Windows and Java. Downsides: variable length, surrogate pain, awkward for pure ASCII.

### UTF-8

Dominates the web. ASCII bytes map to themselves; higher code points use multi-byte sequences with leading bits indicating length (`0xxxxxxx`, `110xxxxx`, `1110xxxx`, `11110xxx`). Advantages: backward-compatible with ASCII, compact for Latin text, byte-order agnostic, easy to resync after corruption. The main cost is variable length—`s[i]` is not the i‑th character unless you scan.

## 0x04 Normalization & combining marks

Because multiple code-point sequences can render the same glyph (`é` vs `e` + combining acute), Unicode defines normalization forms (NFC, NFD, NFKC, NFKD). Comparing strings safely often means normalizing first. Regexes, sorting, case folding, and database uniqueness constraints must choose a consistent form.

## 0x05 Pitfalls

- **BOMs**: UTF-8 doesn’t need one, but some files start with `EF BB BF`; know how your parser handles it.
- **Grapheme clusters**: “emoji with skin tone” is multiple code points. Counting “characters” really means counting grapheme clusters, not code points.
- **Security**: visually confusable characters (homoglyph attacks) and overlong encodings can bypass filters if you’re sloppy.
- **APIs**: know what your language uses internally (`char` in C++ vs Java vs Go). Never assume “one byte = one character.”

## 0x06 Takeaways

1. A character is an abstract symbol; glyphs are its shapes.
2. Unicode assigns code points; UTFs encode them into bytes.
3. UTF-8 is the lingua franca, UTF-16 survives in Windows/Java land, UTF-32 is a niche convenience.
4. Always normalize, validate, and respect boundaries when comparing or slicing strings.
5. Understand your stack’s encoding assumptions—otherwise “你好” will become mojibake at the worst possible time.
