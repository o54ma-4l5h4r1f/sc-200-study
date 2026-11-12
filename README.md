# SC-200 Study System

Offline study system for **Microsoft SC-200: Microsoft Security Operations Analyst**
→ cert *Microsoft Certified: Security Operations Analyst Associate*.

Built for **beginners**: no prior Azure, Microsoft 365 or security-operations experience assumed. Every
lesson opens with the Azure building blocks it relies on ("Azure first") and links to a short
**Foundations** track that teaches them. Builds to static HTML that opens from `file://` with zero
network. Pages are written in a plain, point-first voice — the opposite of Microsoft Learn's padded
style — with every factual claim cited back to a Learn URL and every Learn screenshot included.

## What's here

- `build.py` — the stdlib-only build engine: parse TOML + markdown → render → lint → emit `site/`.
- `content/domains.toml` — the exam blueprint: 3 domains, 9 subdomains, 54 objective bullets
  ("Skills measured as of October 21, 2026").
- `content/foundations/` — Azure / Microsoft 365 / SOC primers, read in order before week 1.
- `content/learn-map.toml` — the official Microsoft Learn curriculum (10 SC-200 paths) mapped to
  blueprint IDs.
- `content/{objectives,questions,labs,reference,cheatsheets,diagrams,snippets,notes}/` — the study material.
- `assets/` — CSS/JS. `progress/` — local, git-ignored (attempt log, notes, study plan).

## Status

- ✅ Blueprint captured (`content/domains.toml`, 54 bullets, verbatim via Microsoft Learn MCP).
- ✅ Written for full beginners (no Azure / SOC experience); labs assume an Azure subscription only.
- ✅ Foundations track (25 primers) and all 54 objective pages, independently reviewed.
- ✅ Cheatsheets and diagrams pages for D1–D3.
- ⬜ Practice questions and labs — generated on demand with the `/study` and
  `generate-question-batch` skills.

## Page shape

Every objective page: **Azure first** → In one sentence → Why it exists → Mental model → What actually
matters → Where it lives → Exam traps → Skip. Every claim cites a Microsoft Learn URL; every Learn image
from the cited articles is included. Markdown subset only (headings, lists, tables, fenced code incl.
`svg`, images, `==highlight==` spans with `@` term / `!` trap / `+` correct sigils) — no raw HTML.

## Build

```bash
python3 build.py              # emits site/
python3 build.py --lint       # schema + ref checks + foundations slugs + near-duplicate question stems
python3 build.py --report     # coverage / progress stats as JSON
python3 build.py --check-learn-map   # curriculum coverage (no network)
python3 build.py --fetch-images      # cache remote images for offline use (network)
python3 build.py --check-links       # probe cited URLs for rot (network)
python3 serve.py              # optional: localhost server so page notes save to progress/notes.json
```

Open `site/index.html` from `file://`. `site/` is disposable — delete it and rebuild.

## How to study

1. `python3 build.py && open site/index.html` — the dashboard shows readiness and weak areas.
2. New to Azure? Read **Foundations** (top nav) in order first.
3. Follow the order: Foundations → D1 → D2 → D3, reading each domain's cheatsheet and diagrams page at the end.
4. Practise KQL daily in the free Log Analytics demo environment.
5. Export progress weekly (footer button) — `localStorage` on `file://` is not durable.
