# Engagement knowledge base

An engagement collects decks, spreadsheets, PDFs, screenshots, exports and web research. Agents and new team members re-read them for weeks. Store each source twice so nobody re-parses a 40-page deck to find one date.

## Folder contract

```
resources/<area>/<collection>/
  docs/        originals, never edited (pptx, docx, xlsx, pdf, png, html, sources.md for web research)
  docs-md/     LLM-ready Markdown
    00_INDEX.md      file -> source -> covers -> method, plus source precedence and known conflicts
    NN_<slug>.md     one Markdown file per source, numbered in reading order
    raw/             optional untouched converter output
```

Areas that work for most engagements: `programme` or `contract` (rules, SOW, gates), `client` (their documents and exports), `solutions` (existing products, the legacy system, competitors, research).

## Every Markdown file starts with frontmatter

```yaml
---
title: "<document title>"
source_file: <name in ../docs/>
source_type: <deck | document | workbook | image | web page | repo>
converted_with: <tool and version | manual transcription | curated digest>
converted_on: YYYY-MM-DD
---
```

## Conversion choice

| Source | Method |
|---|---|
| pptx, docx, xlsx, pdf with text | A converter such as Microsoft MarkItDown, then clean: drop image placeholders, reorder slides, keep speaker notes |
| Scanned or image-only PDF | Render pages to images, transcribe by hand or with a vision model. Say so in `converted_with` |
| Images (diagrams, posters) | Transcribe by hand |
| HTML apps whose content sits in JavaScript | Converters return only headings. Write a curated digest from the data and say so |
| A git repo | Do not convert. Write an overview from README, docs and roadmap, and record the commit hash |
| Web research | `docs/sources.md` lists URLs and access dates; the profile goes in `docs-md` |

## Token discipline

- Cut boilerplate, repeated headers, empty cells and image placeholders.
- Keep numbers, dates, names, role and permission tables, and anything a decision rests on.
- Split on `## ` headings so each section stands alone.
- Record conflicts between sources in `00_INDEX.md`. Name the conflict when it touches an answer.
- Keep a top-level `resources/README.md` map with a size guide, so an agent can pick the smallest file that answers the question.

## Project instructions

Write a short `CLAUDE.md` (or the agent equivalent) at the repo root: what the engagement is, the reading order, the folder contract, and the facts that must hold (dates, decisions, source weights, data rules). Put long rules in path-scoped rule files. Write it in STE strict mode, because agents act on it.
