#!/usr/bin/env python3
"""
SC-200 study system builder.

Reads content/ and progress/, writes site/. Standard library only — no pip, no network.
The output opens directly from file:// with no server.

Usage:
    python3 build.py              # build site/
    python3 build.py --lint       # validate content, no output written
    python3 build.py --report     # print progress/coverage stats as JSON
    python3 build.py --quiet      # build with warnings only

Design constraints that are NOT negotiable:
  * Emitted data is .js assigning to window.SC200, never .json — Chrome blocks
    fetch() of file:// URLs, so a JSON file the page tries to fetch would silently fail.
  * No ES modules in the output — Chrome blocks `import` over file:// via CORS.
  * TOML for structured content because Python's stdlib parses TOML but not YAML.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
PROGRESS = ROOT / "progress"
SITE = ROOT / "site"

FRONTMATTER_DELIM = "+++"

WARNINGS: list[str] = []
ERRORS: list[str] = []
EXAM_CODE = "SC-200"  # overwritten from domains.toml exam_code in main()
ONLINE = False  # --online: render uncached remote images as live (hosted build), no offline chip


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def error(msg: str) -> None:
    ERRORS.append(msg)


# ---------------------------------------------------------------------------
# Markdown — a deliberately small subset (see the README for what is supported).
# Anything outside the subset produces a warning rather than silently mangling.
# ---------------------------------------------------------------------------

_INLINE_CODE = re.compile(r"`([^`]+)`")
_MARK = re.compile(r"==([!+@]?)(.+?)==")
_MARK_CLASS = {"": "hl", "@": "hl-accent", "!": "hl-risk", "+": "hl-ok"}
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_RAW_HTML = re.compile(r"<(?!br\s*/?>)[a-zA-Z/][^>]*>")
_IMAGE_LINE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)(?:\s*\{([^}]*)\})?$")


def render_inline(text: str, ctx: str = "") -> str:
    """Escape, then apply inline markdown. Code spans are protected from other rules."""
    if _RAW_HTML.search(text):
        warn(f"{ctx}: raw HTML in markdown is not supported and was escaped: {text[:60]!r}")

    placeholders: list[str] = []

    def stash_code(m: re.Match[str]) -> str:
        placeholders.append(m.group(1))
        return f"\x00{len(placeholders) - 1}\x00"

    text = _INLINE_CODE.sub(stash_code, text)
    text = html.escape(text, quote=False)
    text = _MARK.sub(
        lambda m: f'<mark class="{_MARK_CLASS[m.group(1)]}">{m.group(2)}</mark>', text
    )
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)
    text = _IMAGE.sub(
        lambda m: f'<img class="inline-img" src="{html.escape(m.group(2), quote=True)}" '
        f'alt="{html.escape(m.group(1), quote=True)}" loading="lazy">',
        text,
    )
    text = _LINK.sub(
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', text
    )

    def unstash(m: re.Match[str]) -> str:
        return f"<code>{html.escape(placeholders[int(m.group(1))], quote=False)}</code>"

    return re.sub(r"\x00(\d+)\x00", unstash, text)


def render_markdown(src: str, ctx: str = "") -> str:
    """Line-oriented renderer for the supported subset."""
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_paragraph(buf: list[str]) -> None:
        if buf:
            out.append("<p>" + render_inline(" ".join(buf), ctx) + "</p>")
            buf.clear()

    para: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code block
        if stripped.startswith("```"):
            flush_paragraph(para)
            lang = stripped[3:].strip()
            body: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            if i >= n:
                warn(f"{ctx}: unterminated code fence")
            i += 1

            # ```svg blocks pass through raw. Inline SVG is how diagrams work here: it is
            # self-contained (no network), scales, and can pick up theme colours via currentColor.
            if lang.lower() == "svg":
                svg = "\n".join(body).strip()
                if not svg.startswith("<svg"):
                    error(f"{ctx}: svg block does not start with <svg")
                elif "<script" in svg.lower() or "onload=" in svg.lower():
                    error(f"{ctx}: svg block contains script — not allowed")
                else:
                    out.append(f'<figure class="diagram">{svg}</figure>')
                continue

            cls = f' class="lang-{html.escape(lang, quote=True)}"' if lang else ""
            code = html.escape("\n".join(body), quote=False)
            out.append(
                f'<div class="codeblock"><button class="copy-btn" type="button">copy</button>'
                f"<pre><code{cls}>{code}</code></pre></div>"
            )
            continue

        # blank
        if not stripped:
            flush_paragraph(para)
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flush_paragraph(para)
            out.append("<hr>")
            i += 1
            continue

        # standalone image line -> block-level figure with optional {caption}
        m_img = _IMAGE_LINE.match(stripped)
        if m_img:
            flush_paragraph(para)
            alt, src, caption = m_img.group(1), m_img.group(2), (m_img.group(3) or "")
            remote = src.startswith(("http://", "https://"))
            # A remote image that has been pulled down by --fetch-images is served from the local
            # cache instead, so the page keeps working offline while still being authored as a
            # plain Microsoft Learn URL.
            cached = cached_image_path(src) if remote else None
            if cached:
                remote = False
                src = cached
            # {{UP}} is swapped for the right number of ../ by page(), since objective pages sit
            # one directory deeper than the site root and file:// has no root-relative paths.
            esc_src = html.escape(src if remote else "{{UP}}" + src, quote=True)
            cap = caption or alt
            # Remote images need the network. On the offline file:// build they degrade to alt text
            # plus a working link and a "needs network" chip. On a hosted (--online) build they load
            # straight from Microsoft, so drop the chip and the degraded styling.
            degraded = remote and not ONLINE
            if remote:
                chip = '<span class="offline-note">needs network</span>' if degraded else ""
                note = (
                    f'<figcaption>{render_inline(cap, ctx)} '
                    f'<a class="src-link" href="{esc_src}">source</a>{chip}</figcaption>'
                )
            else:
                note = f"<figcaption>{render_inline(cap, ctx)}</figcaption>" if cap else ""
            if not remote and not (ASSETS / src).exists():
                warn(f"{ctx}: image {src!r} not found under assets/")
            out.append(
                f'<figure class="figure{" remote" if degraded else ""}">'
                f'<img src="{esc_src}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
                f"{note}</figure>"
            )
            i += 1
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_paragraph(para)
            level = len(m.group(1))
            text = m.group(2).strip()
            slug = slugify(text)
            out.append(f'<h{level} id="{slug}">{render_inline(text, ctx)}</h{level}>')
            i += 1
            continue

        # table (pipe row followed by a separator row)
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_paragraph(para)
            header = split_row(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            thead = "".join(f"<th>{render_inline(c, ctx)}</th>" for c in header)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c, ctx)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(
                f'<div class="tablewrap"><table><thead><tr>{thead}</tr></thead>'
                f"<tbody>{tbody}</tbody></table></div>"
            )
            continue

        # blockquote
        if stripped.startswith(">"):
            flush_paragraph(para)
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + render_inline(" ".join(quote), ctx) + "</p></blockquote>")
            continue

        # lists
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+[.)]\s+", line):
            flush_paragraph(para)
            m_ord = re.match(r"^\s*(\d+)[.)]\s+", line)
            ordered = bool(m_ord)
            tag = "ol" if ordered else "ul"
            # Honour the author's starting number so a list interrupted by a code block or a
            # paragraph can resume its count instead of silently restarting at 1.
            start_attr = ""
            if ordered and m_ord.group(1) != "1":
                start_attr = f' start="{int(m_ord.group(1))}"'
            items: list[str] = []
            while i < n:
                cur = lines[i]
                m_item = re.match(r"^(\s*)(?:[-*]|\d+[.)])\s+(.*)$", cur)
                if not m_item:
                    if cur.strip() and items and cur.startswith((" ", "\t")):
                        items[-1] += " " + cur.strip()  # lazy continuation
                        i += 1
                        continue
                    break
                if len(m_item.group(1)) >= 2 and items:
                    items[-1] += "\x01" + m_item.group(2)  # one nest level, marked
                else:
                    items.append(m_item.group(2))
                i += 1
            out.append(f"<{tag}{start_attr}>")
            for item in items:
                parts = item.split("\x01")
                li = render_inline(parts[0], ctx)
                if len(parts) > 1:
                    nested = "".join(f"<li>{render_inline(p, ctx)}</li>" for p in parts[1:])
                    li += f"<ul>{nested}</ul>"
                out.append(f"<li>{li}</li>")
            out.append(f"</{tag}>")
            continue

        para.append(stripped)
        i += 1

    flush_paragraph(para)
    return "\n".join(out)


IMG_CACHE = "img/cache"


def cache_name(url: str) -> str:
    """Stable local filename for a remote image."""
    import hashlib

    ext = Path(url.split("?")[0]).suffix.lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
        ext = ".png"
    return f"{IMG_CACHE}/{hashlib.sha1(url.encode()).hexdigest()[:12]}{ext}"


def cached_image_path(url: str) -> str | None:
    """Return the cache-relative path if this remote image has been downloaded, else None."""
    rel = cache_name(url)
    return rel if (ASSETS / rel).exists() else None


def split_row(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


# ---------------------------------------------------------------------------
# Content model
# ---------------------------------------------------------------------------


@dataclass
class Objective:
    id: str
    text: str
    domain: str
    subdomain: str
    prior_cert: str = "none"
    hours: float = 0.0
    week: int = 0
    high_risk: bool = False
    license_blocked: bool = False
    # populated from content/objectives/<id>.md if it exists
    title: str = ""
    body_md: str = ""
    body_html: str = ""
    ms_learn_urls: list[str] = field(default_factory=list)
    status: str = "missing"
    last_reviewed: str = ""
    related: list[str] = field(default_factory=list)
    foundations: list[str] = field(default_factory=list)

    @property
    def has_content(self) -> bool:
        return bool(self.body_md.strip())

    @property
    def display_title(self) -> str:
        return self.title or self.text


@dataclass
class Question:
    id: str
    fmt: str
    objective_ids: list[str]
    data: dict
    path: Path

    @property
    def verified(self) -> bool:
        return bool(self.data.get("verified"))


@dataclass
class Lab:
    id: str
    title: str
    objective_ids: list[str]
    minutes: int
    body_html: str
    blocked: bool = False
    blocked_reason: str = ""


@dataclass
class Reference:
    """A standing reference page. Not exam content — context the exam never tests but the job does."""

    slug: str
    title: str
    summary: str
    body_md: str
    body_html: str
    source_urls: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    captured: str = ""
    volatile: bool = False


@dataclass
class Cheatsheet:
    """A one-page, print-first domain recap. IS exam content — the whole domain condensed to what
    survives into the exam room. One per domain, keyed by domain id (D1, D2, ...)."""

    domain: str
    title: str
    summary: str
    body_md: str
    body_html: str
    captured: str = ""


@dataclass
class DiagramPage:
    """A curated set of big cross-page diagrams for one domain — how its concepts wire together,
    plus look-alike/same-job constructs (some outside the domain, drawn as forward-links). Inline
    SVG only, so it works offline and follows the theme. One per domain, keyed by domain id."""

    domain: str
    title: str
    summary: str
    body_md: str
    body_html: str
    captured: str = ""


@dataclass
class Foundation:
    """An Azure / security-basics primer page. The beginner on-ramp: every objective page opens
    with an "Azure first" box that links the foundations it leans on. Not tied to one domain."""

    slug: str
    title: str
    summary: str
    order: int
    body_md: str
    body_html: str
    ms_learn_urls: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    captured: str = ""


def parse_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    """Split a `+++ TOML +++` frontmatter block from the markdown body."""
    text = text.replace("\r\n", "\n")
    if not text.startswith(FRONTMATTER_DELIM):
        error(f"{path}: missing '{FRONTMATTER_DELIM}' frontmatter block")
        return {}, text
    end = text.find(f"\n{FRONTMATTER_DELIM}", len(FRONTMATTER_DELIM))
    if end == -1:
        error(f"{path}: unterminated frontmatter")
        return {}, text
    raw = text[len(FRONTMATTER_DELIM) : end]
    body = text[end + len(FRONTMATTER_DELIM) + 1 :].lstrip("\n")
    try:
        meta = tomllib.loads(raw)
    except tomllib.TOMLDecodeError as exc:
        error(f"{path}: bad TOML frontmatter — {exc}")
        return {}, body
    return meta, body


def load_domains() -> tuple[dict, list[Objective]]:
    path = CONTENT / "domains.toml"
    if not path.exists():
        error(f"{path} not found — this file is the backbone, nothing works without it")
        return {}, []
    with path.open("rb") as fh:
        spec = tomllib.load(fh)

    objectives: list[Objective] = []
    for dom in spec.get("domains", []):
        for sub in dom.get("subdomains", []):
            for obj in sub.get("objectives", []):
                objectives.append(
                    Objective(
                        id=obj["id"],
                        text=obj["text"],
                        domain=dom["id"],
                        subdomain=sub["id"],
                        prior_cert=obj.get("prior_cert", "none"),
                        hours=float(obj.get("hours", 0.0)),
                        week=int(obj.get("week", 0)),
                        high_risk=bool(obj.get("high_risk", False)),
                        license_blocked=bool(obj.get("license_blocked", False)),
                    )
                )
    return spec, objectives


def load_learn_map(valid_ids: set[str]) -> dict:
    """Load the official Learn path/module/unit map and check it against the blueprint.

    This file is the join between two documents Microsoft wrote separately: the skills-measured
    outline and the training curriculum. They do not line up, and the mismatches are the point —
    an objective with no unit behind it has to be written from product docs, and a unit with no
    objective behind it is Skip-section material.
    """
    path = CONTENT / "learn-map.toml"
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        lm = tomllib.load(fh)

    modules = {m["slug"]: m for m in lm.get("modules", [])}
    units = lm.get("units", [])
    lm["units"] = units
    lm.setdefault("modules", [])
    lm.setdefault("paths", [])
    lm["_modules_by_slug"] = modules

    seen: dict[str, list[int]] = {}
    for u in units:
        slug = u["module"]
        if slug not in modules:
            error(f"learn-map.toml: unit '{u.get('title', '?')}' names unknown module '{slug}'")
            continue
        seen.setdefault(slug, []).append(u["n"])
        for oid in u.get("objectives", []):
            if oid not in valid_ids:
                error(f"learn-map.toml: {slug}#{u['n']} references unknown objective '{oid}'")

    for slug, mod in modules.items():
        ns = sorted(seen.get(slug, []))
        if ns != list(range(1, mod["unit_count"] + 1)):
            error(
                f"learn-map.toml: module '{slug}' declares {mod['unit_count']} units "
                f"but {len(ns)} are listed (numbering must be a contiguous 1..N)"
            )

    total = lm.get("unit_total")
    if total is not None and total != len(units):
        error(f"learn-map.toml: unit_total says {total} but {len(units)} units are listed")

    # Coverage the other way round: blueprint bullets the official curriculum never teaches.
    covered: dict[str, list[str]] = {}
    for u in units:
        for oid in u.get("objectives", []):
            covered.setdefault(oid, []).append(f"{u['module']}#{u['n']}")
    lm["_covered"] = covered
    lm["_uncovered"] = sorted(oid for oid in valid_ids if oid not in covered)
    lm["_single_unit"] = sorted(oid for oid, us in covered.items() if len(us) == 1)
    return lm


def load_objective_bodies(objectives: list[Objective]) -> None:
    by_id = {o.id: o for o in objectives}
    d = CONTENT / "objectives"
    if not d.exists():
        return
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        oid = meta.get("id") or path.stem
        obj = by_id.get(oid)
        if obj is None:
            error(f"{path}: objective id {oid!r} is not in domains.toml")
            continue
        obj.title = meta.get("title", "")
        obj.body_md = body
        obj.body_html = render_markdown(body, ctx=str(path.relative_to(ROOT)))
        obj.ms_learn_urls = list(meta.get("ms_learn_urls", []))
        obj.status = meta.get("status", "draft")
        lr = meta.get("last_reviewed", "")
        obj.last_reviewed = lr.isoformat() if isinstance(lr, (date, datetime)) else str(lr)
        obj.related = list(meta.get("related_objectives", []))
        obj.foundations = list(meta.get("foundations", []))
        if not obj.ms_learn_urls and obj.status == "verified":
            warn(f"{path}: status=verified but no ms_learn_urls cited")


VALID_FORMATS = {
    "multiple_choice",
    "multiple_response",
    "drag_and_drop",
    "build_list",
    "hot_area",
    "active_screen",
    "case_study",
    "problem_solution_set",
}


def load_questions(valid_ids: set[str]) -> list[Question]:
    questions: list[Question] = []
    d = CONTENT / "questions"
    if not d.exists():
        return questions
    for path in sorted(d.rglob("*.toml")):
        try:
            with path.open("rb") as fh:
                data = tomllib.load(fh)
        except tomllib.TOMLDecodeError as exc:
            error(f"{path}: bad TOML — {exc}")
            continue

        qid = data.get("id") or path.stem
        fmt = data.get("format") or data.get("type") or ""
        if fmt not in VALID_FORMATS:
            error(f"{path}: unknown format {fmt!r} (expected one of {sorted(VALID_FORMATS)})")
            continue

        oids = list(data.get("objective_ids", []))
        if not oids:
            error(f"{path}: no objective_ids")
        for oid in oids:
            if oid not in valid_ids:
                error(f"{path}: objective_ids references unknown objective {oid!r}")

        validate_question(data, fmt, path)
        questions.append(Question(id=qid, fmt=fmt, objective_ids=oids, data=data, path=path))

    seen: dict[str, Path] = {}
    for q in questions:
        if q.id in seen:
            error(f"{q.path}: duplicate question id {q.id!r} (also in {seen[q.id]})")
        seen[q.id] = q.path
    return questions


def validate_question(data: dict, fmt: str, path: Path) -> None:
    """Per-format schema checks. Catches the mistakes an LLM actually makes."""
    if fmt in ("multiple_choice", "multiple_response"):
        options = data.get("options", [])
        if not options:
            error(f"{path}: no options")
            return
        ids = [o.get("id") for o in options]
        if len(set(ids)) != len(ids):
            error(f"{path}: duplicate option ids")
        correct = [o["id"] for o in options if o.get("correct")]
        answer = data.get("answer", [])
        if sorted(correct) != sorted(answer):
            error(f"{path}: answer {answer} does not match options marked correct {correct}")
        if fmt == "multiple_choice" and len(correct) != 1:
            error(f"{path}: multiple_choice needs exactly 1 correct option, found {len(correct)}")
        if fmt == "multiple_response":
            want = data.get("select_count")
            if want is not None and want != len(correct):
                error(f"{path}: select_count={want} but {len(correct)} options marked correct")
        for o in options:
            if not o.get("explanation"):
                warn(f"{path}: option {o.get('id')!r} has no explanation")

    elif fmt == "drag_and_drop":
        item_ids = {d.get("id") for d in data.get("drag_items", [])}
        if not item_ids:
            error(f"{path}: no drag_items")
        for t in data.get("targets", []):
            if t.get("correct_item") not in item_ids:
                error(f"{path}: target {t.get('id')!r} correct_item not in drag_items")

    elif fmt == "build_list":
        item_ids = {it.get("id") for it in data.get("items", [])}
        order = data.get("correct_order", [])
        if not order:
            error(f"{path}: no correct_order")
        for sid in order:
            if sid not in item_ids:
                error(f"{path}: correct_order references unknown item {sid!r}")

    elif fmt in ("hot_area", "active_screen"):
        # Two supported shapes: a table of yes/no statements, or a set of controls with correct values.
        stmts = data.get("statements", [])
        controls = data.get("controls") or data.get("regions") or []
        if not stmts and not controls:
            error(f"{path}: needs statements (yes/no rows) or controls/regions (dropdowns)")
        for s in stmts:
            if "correct" not in s:
                error(f"{path}: statement {s.get('id')!r} missing correct")
            if not s.get("explanation"):
                warn(f"{path}: statement {s.get('id')!r} has no explanation")
        for c in controls:
            if not c.get("correct"):
                error(f"{path}: control {c.get('id')!r} missing correct")
            opts = c.get("options", [])
            if opts and c.get("correct") not in opts:
                error(f"{path}: control {c.get('id')!r} correct value is not among its options")

    elif fmt == "case_study":
        if not data.get("linked_question_ids"):
            error(f"{path}: case study has no linked_question_ids")
        if not data.get("background"):
            error(f"{path}: case study has no background")

    elif fmt == "problem_solution_set":
        props = data.get("proposals", [])
        if len(props) != 3:
            warn(f"{path}: problem/solution sets are normally 3 proposals, found {len(props)}")
        for p in props:
            if "meets_goal" not in p:
                error(f"{path}: proposal {p.get('id')!r} missing meets_goal")

    if not data.get("source_urls"):
        warn(f"{path}: no source_urls — every question must cite the docs it came from")


def load_labs(valid_ids: set[str]) -> list[Lab]:
    labs: list[Lab] = []
    d = CONTENT / "labs"
    if not d.exists():
        return labs
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        oids = list(meta.get("objective_ids", []))
        for oid in oids:
            if oid not in valid_ids:
                error(f"{path}: unknown objective {oid!r}")
        labs.append(
            Lab(
                id=meta.get("id", path.stem),
                title=meta.get("title", path.stem),
                objective_ids=oids,
                minutes=int(meta.get("estimated_minutes", 0)),
                body_html=render_markdown(body, ctx=str(path.relative_to(ROOT))),
                blocked=bool(meta.get("blocked", False)),
                blocked_reason=meta.get("blocked_reason", ""),
            )
        )
    return labs


def load_references(valid_ids: set[str]) -> list[Reference]:
    refs: list[Reference] = []
    d = CONTENT / "reference"
    if not d.exists():
        return refs
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        oids = list(meta.get("related_objectives", []))
        for oid in oids:
            if oid not in valid_ids:
                error(f"{path}: unknown objective {oid!r}")
        cap = meta.get("captured", "")
        refs.append(
            Reference(
                slug=meta.get("slug", path.stem),
                title=meta.get("title", path.stem),
                summary=meta.get("summary", ""),
                body_md=body,
                body_html=render_markdown(body, ctx=str(path.relative_to(ROOT))),
                source_urls=list(meta.get("source_urls", [])),
                related=oids,
                captured=cap.isoformat() if isinstance(cap, (date, datetime)) else str(cap),
                volatile=bool(meta.get("volatile", False)),
            )
        )
        if not meta.get("source_urls"):
            warn(f"{path}: reference page cites no source_urls")
    slugs = [r.slug for r in refs]
    for s in {x for x in slugs if slugs.count(x) > 1}:
        error(f"content/reference: duplicate slug {s!r}")
    return refs


def load_foundations(valid_ids: set[str]) -> list[Foundation]:
    found: list[Foundation] = []
    d = CONTENT / "foundations"
    if not d.exists():
        return found
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        oids = list(meta.get("related_objectives", []))
        for oid in oids:
            if oid not in valid_ids:
                error(f"{path}: unknown objective {oid!r}")
        cap = meta.get("captured", "")
        found.append(
            Foundation(
                slug=meta.get("slug", path.stem),
                title=meta.get("title", path.stem),
                summary=meta.get("summary", ""),
                order=int(meta.get("order", 999)),
                body_md=body,
                body_html=render_markdown(body, ctx=str(path.relative_to(ROOT))),
                ms_learn_urls=list(meta.get("ms_learn_urls", [])),
                related=oids,
                captured=cap.isoformat() if isinstance(cap, (date, datetime)) else str(cap),
            )
        )
        if not meta.get("ms_learn_urls"):
            warn(f"{path}: foundation page cites no ms_learn_urls")
    slugs = [f.slug for f in found]
    for x in {y for y in slugs if slugs.count(y) > 1}:
        error(f"content/foundations: duplicate slug {x!r}")
    found.sort(key=lambda f: (f.order, f.slug))
    return found


def check_foundation_refs(objectives: list[Objective], found: list[Foundation]) -> None:
    """Every written objective must open on the Azure concepts it relies on."""
    slugs = {f.slug for f in found}
    for o in objectives:
        for s in o.foundations:
            if s not in slugs:
                error(f"content/objectives/{o.id}.md: unknown foundation {s!r}")
        if o.has_content and not o.foundations:
            warn(f"content/objectives/{o.id}.md: no `foundations` listed — the Azure-first box will be empty")
        if o.has_content and "## Azure first" not in o.body_md:
            warn(f"content/objectives/{o.id}.md: missing '## Azure first' section")


def load_cheatsheets(valid_domains: set[str]) -> list[Cheatsheet]:
    sheets: list[Cheatsheet] = []
    d = CONTENT / "cheatsheets"
    if not d.exists():
        return sheets
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        dom = meta.get("domain", path.stem)
        if dom not in valid_domains:
            error(f"{path}: cheatsheet domain {dom!r} is not a known domain id")
        cap = meta.get("captured", "")
        sheets.append(
            Cheatsheet(
                domain=dom,
                title=meta.get("title", f"{dom} cheatsheet"),
                summary=meta.get("summary", ""),
                body_md=body,
                body_html=render_markdown(body, ctx=str(path.relative_to(ROOT))),
                captured=cap.isoformat() if isinstance(cap, (date, datetime)) else str(cap),
            )
        )
    doms = [s.domain for s in sheets]
    for x in {d2 for d2 in doms if doms.count(d2) > 1}:
        error(f"content/cheatsheets: duplicate domain {x!r}")
    return sheets


def load_diagrams(valid_domains: set[str]) -> list[DiagramPage]:
    pages: list[DiagramPage] = []
    d = CONTENT / "diagrams"
    if not d.exists():
        return pages
    for path in sorted(d.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        dom = meta.get("domain", path.stem)
        if dom not in valid_domains:
            error(f"{path}: diagram domain {dom!r} is not a known domain id")
        cap = meta.get("captured", "")
        pages.append(
            DiagramPage(
                domain=dom,
                title=meta.get("title", f"{dom} diagrams"),
                summary=meta.get("summary", ""),
                body_md=body,
                body_html=render_markdown(body, ctx=str(path.relative_to(ROOT))),
                captured=cap.isoformat() if isinstance(cap, (date, datetime)) else str(cap),
            )
        )
    doms = [p.domain for p in pages]
    for x in {d2 for d2 in doms if doms.count(d2) > 1}:
        error(f"content/diagrams: duplicate domain {x!r}")
    return pages


# ---------------------------------------------------------------------------
# Duplicate detection — 4-gram Jaccard over question stems within an objective
# ---------------------------------------------------------------------------


def ngrams(text: str, n: int = 4) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i : i + n]) for i in range(max(0, len(words) - n + 1))}


def stem_of(q: Question) -> str:
    return str(q.data.get("stem") or q.data.get("shared_stem") or q.data.get("background") or "")


def check_duplicates(questions: list[Question], threshold: float = 0.45) -> None:
    by_obj: dict[str, list[Question]] = {}
    for q in questions:
        for oid in q.objective_ids:
            by_obj.setdefault(oid, []).append(q)
    reported: set[tuple[str, str]] = set()
    for oid, group in by_obj.items():
        grams = {q.id: ngrams(stem_of(q)) for q in group}
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                ga, gb = grams[a.id], grams[b.id]
                if not ga or not gb:
                    continue
                j = len(ga & gb) / len(ga | gb)
                key = tuple(sorted((a.id, b.id)))
                if j >= threshold and key not in reported:
                    reported.add(key)
                    warn(f"{oid}: questions {a.id} and {b.id} are {j:.0%} similar — likely duplicate")


# ---------------------------------------------------------------------------
# Search index
# ---------------------------------------------------------------------------

STOPWORDS = {
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "her", "was", "one", "our",
    "out", "day", "get", "has", "him", "his", "how", "its", "new", "now", "old", "see", "two",
    "way", "who", "boy", "did", "use", "with", "this", "that", "from", "they", "have", "been",
    "will", "your", "what", "when", "which", "their", "would", "there", "about", "into", "than",
    "them", "then", "these", "some", "more", "only", "also", "such", "must", "each", "other",
}


def tokenize(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) >= 3 and w not in STOPWORDS]


def build_search_index(
    objectives: list[Objective],
    questions: list[Question],
    labs: list[Lab],
    refs: list[Reference] | None = None,
    found: list[Foundation] | None = None,
) -> dict:
    postings: dict[str, dict[str, int]] = {}
    docs: dict[str, dict] = {}

    def add(doc_id: str, title: str, body: str, url: str, kind: str) -> None:
        docs[doc_id] = {
            "t": title,
            "u": url,
            "k": kind,
            "s": re.sub(r"\s+", " ", body).strip()[:160],
        }
        for tok in tokenize(title):
            postings.setdefault(tok, {})
            postings[tok][doc_id] = postings[tok].get(doc_id, 0) + 3
        for tok in tokenize(body):
            postings.setdefault(tok, {})
            postings[tok][doc_id] = postings[tok].get(doc_id, 0) + 1

    for o in objectives:
        add(o.id, f"{o.id} — {o.display_title}", o.text + " " + o.body_md, f"objective/{o.id}.html", "objective")
    for q in questions:
        add(f"q:{q.id}", q.id, stem_of(q), f"quiz.html?q={q.id}", "question")
    for lab in labs:
        add(f"lab:{lab.id}", lab.title, lab.body_html, f"labs.html#{lab.id}", "lab")
    for ref in refs or []:
        add(
            f"ref:{ref.slug}",
            ref.title,
            ref.summary + " " + ref.body_md,
            f"reference/{ref.slug}.html",
            "reference",
        )
    for f in found or []:
        add(f"fnd:{f.slug}", f"Foundations — {f.title}", f.summary + " " + f.body_md, f"foundations/{f.slug}.html", "foundation")

    return {"postings": {k: sorted(v.items(), key=lambda kv: -kv[1]) for k, v in postings.items()}, "docs": docs}


# ---------------------------------------------------------------------------
# Progress (build-time fallback for when file:// localStorage misbehaves)
# ---------------------------------------------------------------------------


def load_progress_fallback() -> dict:
    for name in ("progress-export.json",):
        p = PROGRESS / name
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                warn(f"{p}: invalid JSON — {exc}")
    attempts_path = PROGRESS / "attempts.jsonl"
    if attempts_path.exists():
        attempts = []
        for line in attempts_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                attempts.append(json.loads(line))
            except json.JSONDecodeError:
                warn(f"{attempts_path}: skipped malformed line")
        return {"attempts": attempts}
    return {}


# ---------------------------------------------------------------------------
# HTML shell
# ---------------------------------------------------------------------------

NAV = [
    ("index.html", "Dashboard"),
    ("foundations/index.html", "Foundations"),
    ("curriculum.html", "Curriculum"),
    ("quiz.html", "Practice"),
    ("mock-exam.html", "Mock exam"),
    ("labs.html", "Labs"),
    ("diagram/index.html", "Diagrams"),
    ("cheatsheet/index.html", "Cheatsheets"),
    ("reviews.html", "Reviews"),
    ("reference/index.html", "Reference"),
]


def page(title: str, body: str, depth: int, scripts: list[str], active: str = "") -> str:
    up = "../" * depth
    nav = "".join(
        f'<a href="{up}{href}"{" class=\'active\'" if href == active else ""}>{label}</a>'
        for href, label in NAV
    )
    script_tags = "".join(f'<script src="{up}{s}"></script>' for s in scripts)
    body = body.replace("{{UP}}", up)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {EXAM_CODE}</title>
<link rel="stylesheet" href="{up}style.css">
<script>
// Inline and deliberate: set the theme before first paint so the page never flashes the wrong one.
try {{
  var t = localStorage.getItem('sc200.theme');
  if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
}} catch (e) {{ document.documentElement.setAttribute('data-theme', 'light'); }}
</script>
</head>
<body>
<header class="topbar">
  <a class="brand" href="{up}index.html">{EXAM_CODE}</a>
  <nav>{nav}</nav>
  <div class="search">
    <input type="search" id="q" placeholder="Search objectives, foundations, questions, labs…" autocomplete="off">
    <div id="results" class="results" hidden></div>
  </div>
  <button id="theme-toggle" class="icon-btn" type="button" title="Toggle theme">◐</button>
</header>
<main>
{body}
</main>
<footer class="foot">
  <span>{EXAM_CODE} study system · built {date.today().isoformat()}</span>
  <span class="spacer"></span>
  <button id="export-progress" class="linkish" type="button">Export progress</button>
  <label class="linkish" for="import-progress">Import progress</label>
  <input type="file" id="import-progress" accept="application/json" hidden>
</footer>
<script src="{up}content-data.js"></script>
<script src="{up}search-index.js"></script>
<script src="{up}app.js"></script>
<script src="{up}notes.js"></script>
{script_tags}
</body>
</html>
"""


def pct_bar(value: float, label: str = "") -> str:
    v = max(0.0, min(1.0, value))
    return (
        f'<div class="bar" role="img" aria-label="{html.escape(label)} {v:.0%}">'
        f'<span style="width:{v * 100:.1f}%"></span></div>'
    )


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------


def build_dashboard(
    spec: dict,
    objectives: list[Objective],
    questions: list[Question],
    labs: list[Lab],
    lm: dict | None = None,
) -> str:
    q_by_obj: dict[str, int] = {}
    for q in questions:
        for oid in q.objective_ids:
            q_by_obj[oid] = q_by_obj.get(oid, 0) + 1

    written = sum(1 for o in objectives if o.has_content)
    total = len(objectives)
    verified_q = sum(1 for q in questions if q.verified)

    cards = f"""
<section class="cards">
  <div class="card"><b>{written}/{total}</b><span>objectives written</span>{pct_bar(written / max(1, total), "content")}</div>
  <div class="card"><b>{len(questions)}</b><span>questions ({verified_q} verified)</span>{pct_bar(len(questions) / 250, "question bank")}</div>
  <div class="card"><b>{len(labs)}</b><span>labs</span>{pct_bar(len(labs) / 36, "labs")}</div>
  <div class="card" id="readiness-card"><b id="readiness">—</b><span>est. readiness</span><div class="bar"><span id="readiness-bar" style="width:0"></span></div></div>
</section>
<p class="note">Readiness is computed from your recorded quiz attempts, weighted by domain. It is an
estimate from this system's own question bank — not a prediction of your Microsoft score.</p>
"""

    sections: list[str] = []
    for dom in spec.get("domains", []):
        dom_objs = [o for o in objectives if o.domain == dom["id"]]
        dom_written = sum(1 for o in dom_objs if o.has_content)
        rows: list[str] = []
        for sub in dom.get("subdomains", []):
            sub_objs = [o for o in dom_objs if o.subdomain == sub["id"]]
            note = f'<p class="subnote">{render_inline(sub["note"])}</p>' if sub.get("note") else ""
            items: list[str] = []
            for o in sub_objs:
                flags = []
                if o.high_risk:
                    flags.append('<span class="flag risk" title="High-risk topic">risk</span>')
                if o.license_blocked:
                    flags.append('<span class="flag blocked" title="Needs Microsoft 365 E5 / Defender licences — portal tour + docs, no live lab">doc-only</span>')
                if o.prior_cert == "strong":
                    flags.append('<span class="flag known" title="Covered by your existing experience">known</span>')
                qn = q_by_obj.get(o.id, 0)
                state = "written" if o.has_content else "todo"
                items.append(
                    f'<li class="obj {state}" data-objective="{o.id}">'
                    f'<a href="objective/{o.id}.html"><code>{o.id}</code> {html.escape(o.display_title)}</a>'
                    f'<span class="meta">{"".join(flags)}'
                    f'<span class="flag hours">{o.hours:g}h</span>'
                    f'<span class="flag wk">wk{o.week}</span>'
                    f'<span class="flag qn">{qn}q</span>'
                    f'<span class="acc" data-acc-for="{o.id}"></span></span></li>'
                )
            rows.append(
                f'<div class="subdomain"><h3>{html.escape(sub["id"])} · {html.escape(sub["title"])}</h3>'
                f'{note}<ul class="objlist">{"".join(items)}</ul></div>'
            )
        sections.append(
            f'<section class="domain"><h2><a href="domain/{dom["id"]}.html">{html.escape(dom["id"])} · '
            f'{html.escape(dom["title"])}</a> <span class="weight">{dom["weight_min"]}–{dom["weight_max"]}%</span></h2>'
            f'<p class="progress-line">{dom_written}/{len(dom_objs)} objectives written</p>'
            f'{pct_bar(dom_written / max(1, len(dom_objs)), dom["id"])}{"".join(rows)}</section>'
        )

    body = f"""
<h1>{html.escape(str(spec.get('exam_code', EXAM_CODE)))} — {html.escape(str(spec.get('exam_title', '')))}</h1>
<p class="lede">{spec.get('total_planned_hours', 0)} planned hours · outline captured
{spec.get('outline_captured', '')}. New to Azure? Start with <a href="foundations/index.html">Foundations</a>
— every lesson links back to the Azure basics it relies on.</p>
{cards}
<div id="weak-areas"></div>
{"".join(sections)}
{build_dashboard_paths(lm or {}, objectives)}
"""
    return page("Dashboard", body, depth=0, scripts=["dashboard.js"], active="index.html")


def build_dashboard_paths(lm: dict, objectives: list[Objective]) -> str:
    """The official Learn curriculum on the dashboard: path -> module, each module showing which
    blueprint objectives it teaches and whether those pages are written yet. Unit-level detail
    stays on curriculum.html (linked per path and module)."""
    if not lm or not lm.get("paths"):
        return ""
    by_id = {o.id: o for o in objectives}
    units_by_mod: dict[str, list[dict]] = {}
    for u in lm["units"]:
        units_by_mod.setdefault(u["module"], []).append(u)

    def chip(oid: str) -> str:
        o = by_id.get(oid)
        done = bool(o and o.has_content)
        return (
            f'<a class="chip{"" if done else " chip-todo"}" href="objective/{oid}.html" '
            f'title="{html.escape(o.text if o else oid)}{"" if done else " — page not written yet"}">{oid}</a>'
        )

    cards: list[str] = []
    order = {d: i for i, d in enumerate(sorted({p["domain"] for p in lm["paths"]}))}
    for p in sorted(lm["paths"], key=lambda x: (order.get(x["domain"], 9), x["id"])):
        mods = [m for m in lm["modules"] if m["path"] == p["id"]]
        path_oids: set[str] = set()
        path_units = 0
        rows: list[str] = []
        for m in mods:
            us = units_by_mod.get(m["slug"], [])
            path_units += len(us)
            oids = sorted({o for u in us for o in u.get("objectives", [])}, key=lambda x: [int(n) for n in x[1:].split(".")])
            path_oids.update(oids)
            off = sum(1 for u in us if u.get("off_blueprint"))
            blocked = sum(1 for u in us if u.get("license_blocked"))
            written = sum(1 for o in oids if o in by_id and by_id[o].has_content)
            flags = ""
            if not m.get("exam_native", True):
                flags += f' <span class="flag risk">not written for {EXAM_CODE}</span>'
            if off:
                flags += f' <span class="flag" title="Units teaching material the exam never asks for — Skip-section fuel">{off} off-blueprint</span>'
            if blocked:
                flags += f' <span class="flag blocked" title="Exercises needing licences an Azure-only lab lacks">{blocked} no licence</span>'
            status = (
                '<span class="flag">no exam objective</span>'
                if not oids
                else f'<span class="flag{" known" if written == len(oids) else ""}">{written}/{len(oids)} written</span>'
            )
            rows.append(
                f'<tr><td><a href="{m["url"]}">{html.escape(m["title"])}</a>{flags}'
                f'<br><a class="note" href="curriculum.html#mod-{m["slug"]}">{len(us)} units →</a></td>'
                f'<td class="nowrap">{html.escape(m.get("level", ""))}</td>'
                f'<td><span class="u-obj dash-chips">{" ".join(chip(o) for o in oids) or "—"}</span></td>'
                f'<td class="nowrap">{status}</td></tr>'
            )
        p_written = sum(1 for o in path_oids if o in by_id and by_id[o].has_content)
        cards.append(f"""
<details class="path-card">
  <summary><span class="flag">{html.escape(p['domain'])}</span> <strong>{html.escape(p['title'])}</strong>
    <span class="meta"><span class="flag">{len(mods)} modules</span><span class="flag">{path_units} units</span>
    <span class="flag">{p_written}/{len(path_oids)} objectives written</span></span></summary>
  {pct_bar(p_written / max(1, len(path_oids)), p['id'])}
  <p class="note"><a href="{p['url']}">Open on Microsoft Learn</a> ·
    <a href="curriculum.html#path-{p['id']}">unit-by-unit map</a></p>
  <table class="path-mods"><thead><tr><th>Module</th><th>Level</th><th>Teaches objectives</th><th>Pages</th></tr></thead>
  <tbody>{''.join(rows)}</tbody></table>
</details>""")

    n_units = len(lm["units"])
    return f"""
<section class="domain paths-overview">
<h2>Official learning paths <span class="weight">{len(lm['paths'])} paths · {len(lm['modules'])} modules · {n_units} units</span></h2>
<p class="progress-line">Microsoft's SC-200 training, mapped to the exam objectives above. Grey chips = page not
written yet. Learn is a citation source here — read our objective page, not the module. Uncovered
bullets and off-blueprint units are on the <a href="curriculum.html">Curriculum</a> page.</p>
{''.join(cards)}
</section>"""


def build_domain_page(dom: dict, objectives: list[Objective], questions: list[Question]) -> str:
    q_by_obj: dict[str, int] = {}
    for q in questions:
        for oid in q.objective_ids:
            q_by_obj[oid] = q_by_obj.get(oid, 0) + 1

    blocks: list[str] = []
    for sub in dom.get("subdomains", []):
        sub_objs = [o for o in objectives if o.subdomain == sub["id"]]
        note = f'<blockquote><p>{render_inline(sub["note"])}</p></blockquote>' if sub.get("note") else ""
        rows = "".join(
            f'<tr><td><a href="../objective/{o.id}.html"><code>{o.id}</code></a></td>'
            f"<td>{html.escape(o.text)}</td>"
            f'<td class="nowrap">{o.prior_cert}</td>'
            f'<td class="nowrap">{o.hours:g}h</td>'
            f'<td class="nowrap">wk{o.week}</td>'
            f'<td class="nowrap">{q_by_obj.get(o.id, 0)}</td></tr>'
            for o in sub_objs
        )
        learn = ""
        if sub.get("learn_path"):
            learn = f'<p class="note">Official Learn path: <a href="{sub["learn_path"]}">{sub["learn_path"]}</a></p>'
        blocks.append(
            f'<section><h2>{html.escape(sub["id"])} · {html.escape(sub["title"])}</h2>{note}{learn}'
            f'<div class="tablewrap"><table><thead><tr><th>ID</th><th>Objective</th><th>Prior cert</th>'
            f"<th>Hours</th><th>Week</th><th>Qs</th></tr></thead><tbody>{rows}</tbody></table></div></section>"
        )

    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / {html.escape(dom['id'])}</p>
<h1>{html.escape(dom['id'])} · {html.escape(dom['title'])}</h1>
<p class="lede">Exam weight {dom['weight_min']}–{dom['weight_max']}%.</p>
{"".join(blocks)}
"""
    return page(dom["title"], body, depth=1, scripts=[])


def pager(prev: Objective | None, nxt: Objective | None, position: str = "") -> str:
    """Prev/next between objectives, in blueprint order. Keyboard: left/right arrows."""
    def side(o: Objective | None, kind: str, arrow: str) -> str:
        if o is None:
            return '<span class="pager-slot empty"></span>'
        return (
            f'<a class="pager-slot {kind}" href="{o.id}.html" data-pager="{kind}">'
            f'<span class="pager-dir">{arrow} {kind}</span>'
            f'<span class="pager-id">{o.id}</span>'
            f'<span class="pager-title">{html.escape(o.display_title)}</span></a>'
        )

    return (
        f'<nav class="pager {position}" aria-label="Objective navigation">'
        f'{side(prev, "prev", "←")}'
        f'<a class="pager-up" href="../index.html" title="All objectives">index</a>'
        f'{side(nxt, "next", "→")}</nav>'
    )


def build_objective_page(
    obj: Objective,
    questions: list[Question],
    labs: list[Lab],
    prev: Objective | None = None,
    nxt: Objective | None = None,
    lm: dict | None = None,
    refs: list[Reference] | None = None,
    found: list[Foundation] | None = None,
) -> str:
    qs = [q for q in questions if obj.id in q.objective_ids]
    related_labs = [lab for lab in labs if obj.id in lab.objective_ids]

    flags = []
    if obj.high_risk:
        flags.append('<span class="flag risk">high risk</span>')
    if obj.license_blocked:
        flags.append('<span class="flag blocked">needs Microsoft 365 E5 / Defender licences — portal tour + docs, no live lab</span>')
    if obj.prior_cert == "strong":
        flags.append('<span class="flag known">already covered by your experience — skim</span>')
    elif obj.prior_cert == "partial":
        flags.append('<span class="flag partial">partly covered by your experience</span>')

    azure_first = ""
    fmap = {f.slug: f for f in (found or [])}
    if obj.foundations:
        items = "".join(
            f'<li><a href="../foundations/{s}.html">{html.escape(fmap[s].title if s in fmap else s)}</a>'
            + (f'<br><span class="note">{html.escape(fmap[s].summary)}</span>' if s in fmap and fmap[s].summary else "")
            + "</li>"
            for s in obj.foundations
        )
        azure_first = (
            '<aside class="azure-first"><h2>Before you start — Azure foundations</h2>'
            "<p class=\"note\">New to Azure? Read these first. Each is short and links back here.</p>"
            f"<ul>{items}</ul></aside>"
        )

    if obj.has_content:
        content = obj.body_html
    else:
        content = f"""<div class="empty">
<p><strong>Not written yet.</strong> To author it:</p>
<pre><code>Write the objective page for {obj.id}</code></pre>
<p>Follow the page shape: Azure first, one-sentence definition, why it
exists, mental model, what actually matters, where it lives, exam traps, and a skip list.</p>
</div>"""

    sources = ""
    if obj.ms_learn_urls:
        items = "".join(f'<li><a href="{html.escape(u, quote=True)}">{html.escape(u)}</a></li>' for u in obj.ms_learn_urls)
        sources = f'<section class="sources"><h2>Sources</h2><ul>{items}</ul></section>'

    labs_html = ""
    if related_labs:
        items = "".join(
            f'<li><a href="../labs.html#{lab.id}">{html.escape(lab.title)}</a> '
            f'<span class="flag">{lab.minutes}m</span>'
            + ('<span class="flag blocked">blocked</span>' if lab.blocked else "")
            + "</li>"
            for lab in related_labs
        )
        labs_html = f'<section><h2>Labs</h2><ul>{items}</ul></section>'

    practice = (
        f'<p><a class="btn" href="../quiz.html?objective={obj.id}">Practice {len(qs)} question'
        f'{"s" if len(qs) != 1 else ""}</a></p>'
        if qs
        else '<p class="note">No questions yet for this objective.</p>'
    )

    related = ""
    if obj.related:
        items = "".join(f'<li><a href="{r}.html"><code>{r}</code></a></li>' for r in obj.related)
        related = f"<section><h2>Related</h2><ul>{items}</ul></section>"

    reference = ""
    mine_refs = [r for r in (refs or []) if obj.id in r.related]
    if mine_refs:
        items = "".join(
            f'<li><a href="../reference/{r.slug}.html">{html.escape(r.title)}</a>'
            + ('<span class="flag risk">volatile</span>' if r.volatile else "")
            + f'<br><span class="note">{html.escape(r.summary)}</span></li>'
            for r in mine_refs
        )
        reference = (
            '<section><h2>Reference <span class="flag">not exam content</span></h2>'
            f"<ul>{items}</ul></section>"
        )

    curriculum = ""
    if lm:
        mods = lm["_modules_by_slug"]
        mine = [u for u in lm["units"] if obj.id in u.get("objectives", [])]
        if mine:
            items = "".join(
                f'<li><a href="{mods[u["module"]]["url"]}{u["slug"]}">{html.escape(u["title"])}</a>'
                + (' <span class="flag">exercise</span>' if u["kind"] == "exercise" else "")
                + (' <span class="flag blocked">no licence</span>' if u.get("license_blocked") else "")
                + f'<br><span class="note">{html.escape(mods[u["module"]]["title"])} · unit {u["n"]}</span></li>'
                for u in mine
            )
            warn_thin = (
                '<p class="note"><strong>One unit only.</strong> The official curriculum barely '
                "touches this. Trust the product docs over the module here.</p>"
                if len(mine) == 1
                else ""
            )
            curriculum = (
                f'<section><h2>Official curriculum <span class="flag">{len(mine)} unit'
                f'{"s" if len(mine) != 1 else ""}</span></h2>{warn_thin}<ul>{items}</ul></section>'
            )
        else:
            curriculum = (
                '<section><h2>Official curriculum</h2>'
                f'<p class="note"><strong>No Learn unit covers this bullet.</strong> All {len(lm["units"])} captured units '
                'were checked. This page must be written from product documentation — see '
                '<a href="../curriculum.html">Curriculum</a>.</p></section>'
            )

    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / <a href="../domain/{obj.domain}.html">{obj.domain}</a> / {obj.id}</p>
{pager(prev, nxt, "top")}
<h1><code class="oid">{obj.id}</code> {html.escape(obj.display_title)}</h1>
<p class="blueprint">{html.escape(obj.text)}</p>
<p class="flags">{"".join(flags)}<span class="flag hours">{obj.hours:g}h planned</span><span class="flag wk">week {obj.week}</span></p>
{azure_first}
<div class="objective-body">{content}</div>
{practice}
{labs_html}
{curriculum}
{related}
{reference}
{sources}
<p class="note status">Status: <code>{obj.status}</code>{f" · last reviewed {obj.last_reviewed}" if obj.last_reviewed else ""}</p>
{pager(prev, nxt, "bottom")}
"""
    return page(obj.display_title, body, depth=1, scripts=[])


def build_quiz_page() -> str:
    body = """
<h1>Practice</h1>
<div id="quiz-setup" class="panel">
  <label>Scope
    <select id="scope"><option value="all">Everything</option></select>
  </label>
  <label>Count <input type="number" id="count" value="10" min="1" max="60"></label>
  <label class="check"><input type="checkbox" id="weak-first" checked> Weak areas first</label>
  <label class="check"><input type="checkbox" id="verified-only"> Verified questions only</label>
  <button id="start" class="btn" type="button">Start</button>
</div>
<div id="quiz-runner" hidden></div>
<div id="quiz-results" hidden></div>
"""
    return page("Practice", body, depth=0, scripts=["quiz.js"], active="quiz.html")


def build_mock_page() -> str:
    body = """
<h1>Mock exam</h1>
<div id="mock-setup" class="panel">
  <p>45–55 questions, sampled to the real domain weights (22.5% / 42.5% / 37.5%).
  100 minutes on the clock. Case studies and problem/solution sets are never split.</p>
  <p class="note"><strong>The 1–1000 score is a linear approximation.</strong> Microsoft's real
  scoring algorithm is undisclosed and near-certainly weights questions by difficulty. Treat the
  number as a trend line across attempts, not as a predicted result.</p>
  <button id="start-mock" class="btn" type="button">Start 100-minute mock</button>
</div>
<div id="mock-runner" hidden>
  <div id="mock-timer" class="timer"></div>
  <div id="mock-body"></div>
</div>
<div id="mock-results" hidden></div>
"""
    return page("Mock exam", body, depth=0, scripts=["quiz.js"], active="mock-exam.html")


def build_labs_page(labs: list[Lab], objectives: list[Objective]) -> str:
    by_id = {o.id: o for o in objectives}
    if not labs:
        body = """<h1>Labs</h1><div class="empty"><p><strong>No labs yet.</strong> To author one:</p>
<pre><code>Write the lab for D1.2.3 (Configure model and agent deployments)</code></pre></div>"""
        return page("Labs", body, depth=0, scripts=[], active="labs.html")

    items: list[str] = []
    for lab in labs:
        links = " ".join(
            f'<a href="objective/{oid}.html"><code>{oid}</code></a>'
            + (f" {html.escape(by_id[oid].display_title)}" if oid in by_id else "")
            for oid in lab.objective_ids
        )
        blocked = (
            f'<p class="blocked-note"><strong>Blocked:</strong> {render_inline(lab.blocked_reason)}</p>'
            if lab.blocked
            else ""
        )
        items.append(f"""
<section class="lab" id="{lab.id}">
  <h2>{html.escape(lab.title)} <span class="flag">{lab.minutes}m</span></h2>
  <p class="note">Covers: {links}</p>
  {blocked}
  <div class="lab-status" data-lab="{lab.id}">
    <label><input type="radio" name="st-{lab.id}" value="todo"> Not started</label>
    <label><input type="radio" name="st-{lab.id}" value="doing"> In progress</label>
    <label><input type="radio" name="st-{lab.id}" value="blocked"> Blocked</label>
    <label><input type="radio" name="st-{lab.id}" value="done"> Done</label>
  </div>
  <details><summary>Steps</summary>{lab.body_html}</details>
  <textarea class="lab-notes" data-lab="{lab.id}" placeholder="Notes from your Azure subscription…"></textarea>
</section>""")

    body = f"<h1>Labs</h1><p class='lede'>{len(labs)} labs against your own Azure subscription.</p>{''.join(items)}"
    return page("Labs", body, depth=0, scripts=["labs.js"], active="labs.html")


def build_reference_index(refs: list[Reference], objectives: list[Objective]) -> str:
    if not refs:
        body = (
            "<h1>Reference</h1><p class='note'>Nothing here yet. Reference pages live in "
            "<code>content/reference/*.md</code>.</p>"
        )
        return page("Reference", body, depth=1, scripts=[], active="reference/index.html")

    by_id = {o.id: o for o in objectives}
    cards = []
    for r in refs:
        links = "".join(
            f'<a class="chip" href="../objective/{o}.html" '
            f'title="{html.escape(by_id[o].display_title if o in by_id else o)}">{o}</a>'
            for o in r.related
        )
        stamp = f'<span class="flag">captured {r.captured}</span>' if r.captured else ""
        vol = '<span class="flag risk">prices move — re-check before quoting</span>' if r.volatile else ""
        cards.append(
            f'<li class="ref-card"><h2><a href="{r.slug}.html">{html.escape(r.title)}</a></h2>'
            f'<p>{html.escape(r.summary)}</p>'
            f'<p class="flags">{stamp}{vol}{links}</p></li>'
        )

    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / Reference</p>
<h1>Reference</h1>
<p class="blueprint">Working material that is <strong>not</strong> exam content. The exam never asks a
price, a SKU list price, or a partner programme detail. This section exists so that material has
somewhere to live other than an objective page, where it would dilute the study text.</p>
<ul class="ref-list">{"".join(cards)}</ul>
"""
    return page("Reference", body, depth=1, scripts=[], active="reference/index.html")


def build_reference_page(ref: Reference, objectives: list[Objective]) -> str:
    by_id = {o.id: o for o in objectives}
    related = ""
    if ref.related:
        items = "".join(
            f'<li><a href="../objective/{o}.html"><code>{o}</code></a> '
            f'{html.escape(by_id[o].display_title) if o in by_id else ""}</li>'
            for o in ref.related
        )
        related = f"<section><h2>Related objectives</h2><ul>{items}</ul></section>"

    sources = ""
    if ref.source_urls:
        items = "".join(
            f'<li><a href="{html.escape(u, quote=True)}">{html.escape(u)}</a></li>' for u in ref.source_urls
        )
        sources = f'<section class="sources"><h2>Sources</h2><ul>{items}</ul></section>'

    warning = ""
    if ref.volatile:
        warning = (
            '<div class="callout callout-risk"><p><strong>These numbers move.</strong> Everything '
            f'here was read from Microsoft\'s public pages on {html.escape(ref.captured or "capture")}. '
            "List price is not your price — re-check the live page and your own agreement before you "
            "quote anything to a customer.</p></div>"
        )

    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / <a href="index.html">Reference</a> / {html.escape(ref.title)}</p>
<h1>{html.escape(ref.title)}</h1>
<p class="blueprint">{html.escape(ref.summary)}</p>
{warning}
<div class="objective-body">{ref.body_html}</div>
{related}
{sources}
<p class="note status">Not exam content{f" · captured {ref.captured}" if ref.captured else ""}</p>
"""
    return page(ref.title, body, depth=1, scripts=[], active="reference/index.html")


def build_foundations_index(found: list[Foundation], objectives: list[Objective]) -> str:
    if not found:
        body = (
            "<p class=\"crumb\"><a href=\"../index.html\">Dashboard</a> / Foundations</p>"
            "<h1>Foundations</h1><p class='note'>Nothing here yet. Azure primers live in "
            "<code>content/foundations/*.md</code>.</p>"
        )
        return page("Foundations", body, depth=1, scripts=[], active="foundations/index.html")
    uses: dict[str, int] = {}
    for o in objectives:
        for s in o.foundations:
            uses[s] = uses.get(s, 0) + 1
    cards = "".join(
        f'<li class="ref-card"><h2><span class="flag">{i}</span> <a href="{f.slug}.html">{html.escape(f.title)}</a></h2>'
        f"<p>{html.escape(f.summary)}</p>"
        f'<p class="flags"><span class="flag">used by {uses.get(f.slug, 0)} lesson{"s" if uses.get(f.slug, 0) != 1 else ""}</span></p></li>'
        for i, f in enumerate(found, 1)
    )
    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / Foundations</p>
<h1>Foundations</h1>
<p class="blueprint">The Azure and security-operations basics every {html.escape(EXAM_CODE)} lesson stands on.
Read them in order before week 1 if Azure is new to you. Each lesson opens with a
<strong>Before you start</strong> box pointing back to the ones it needs.</p>
<ol class="ref-list">{cards}</ol>
"""
    return page("Foundations", body, depth=1, scripts=[], active="foundations/index.html")


def build_foundation_page(
    f: Foundation, found: list[Foundation], objectives: list[Objective]
) -> str:
    idx = found.index(f)
    prev = found[idx - 1] if idx > 0 else None
    nxt = found[idx + 1] if idx < len(found) - 1 else None
    pager_html = (
        '<nav class="pager" aria-label="Foundations navigation">'
        + (f'<a class="prev" href="{prev.slug}.html">← {html.escape(prev.title)}</a>' if prev else "<span></span>")
        + (f'<a class="next" href="{nxt.slug}.html">{html.escape(nxt.title)} →</a>' if nxt else "<span></span>")
        + "</nav>"
    )
    users = [o for o in objectives if f.slug in o.foundations]
    used = ""
    if users:
        items = "".join(
            f'<li><a href="../objective/{o.id}.html"><code>{o.id}</code> {html.escape(o.display_title)}</a></li>'
            for o in users
        )
        used = f"<section><h2>Lessons that rely on this</h2><ul>{items}</ul></section>"
    sources = ""
    if f.ms_learn_urls:
        items = "".join(f'<li><a href="{html.escape(u, quote=True)}">{html.escape(u)}</a></li>' for u in f.ms_learn_urls)
        sources = f'<section class="sources"><h2>Sources</h2><ul>{items}</ul></section>'
    stamp = f" · captured {f.captured}" if f.captured else ""
    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / <a href="index.html">Foundations</a> / {html.escape(f.title)}</p>
{pager_html}
<h1><span class="flag">Foundation {idx + 1}</span> {html.escape(f.title)}</h1>
<p class="blueprint">{html.escape(f.summary)}</p>
<div class="objective-body">{f.body_html}</div>
{used}
{sources}
<p class="note status">Foundations primer{html.escape(stamp)}</p>
{pager_html}
"""
    return page(f.title, body, depth=1, scripts=[], active="foundations/index.html")


def build_cheatsheet_index(sheets: list[Cheatsheet], spec: dict) -> str:
    dom_title = {d["id"]: d["title"] for d in spec.get("domains", [])}
    if not sheets:
        body = (
            "<p class=\"crumb\"><a href=\"../index.html\">Dashboard</a> / Cheatsheets</p>"
            "<h1>Cheatsheets</h1><p class='note'>Nothing here yet. One-page domain recaps live in "
            "<code>content/cheatsheets/D{n}.md</code> — authored after each domain is studied.</p>"
        )
        return page("Cheatsheets", body, depth=1, scripts=[], active="cheatsheet/index.html")

    cards = []
    for s in sorted(sheets, key=lambda x: x.domain):
        stamp = f'<span class="flag">captured {s.captured}</span>' if s.captured else ""
        cards.append(
            f'<li class="ref-card"><h2><a href="{s.domain}.html">{html.escape(s.title)}</a></h2>'
            f'<p>{html.escape(s.summary or dom_title.get(s.domain, ""))}</p>'
            f'<p class="flags">{stamp}'
            f'<a class="chip" href="../domain/{s.domain}.html">{s.domain} objectives</a></p></li>'
        )
    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / Cheatsheets</p>
<h1>Cheatsheets</h1>
<p class="blueprint">One page per domain — the whole thing condensed to what survives into the exam
room. Exam content, not reference. Open the domain's sheet, hit <strong>Ctrl/Cmd&nbsp;+&nbsp;P</strong>
to print or save a PDF. Review these last, the night before.</p>
<ul class="ref-list">{"".join(cards)}</ul>
"""
    return page("Cheatsheets", body, depth=1, scripts=[], active="cheatsheet/index.html")


def build_cheatsheet_page(sheet: Cheatsheet, spec: dict) -> str:
    dom_title = {d["id"]: d["title"] for d in spec.get("domains", [])}
    stamp = f" · captured {sheet.captured}" if sheet.captured else ""
    body = f"""
<p class="crumb no-print"><a href="../index.html">Dashboard</a> / <a href="index.html">Cheatsheets</a> / {html.escape(sheet.title)}</p>
<div class="objective-body cheatsheet">
<h1>{html.escape(sheet.title)}</h1>
<p class="blueprint no-print">{html.escape(sheet.summary or dom_title.get(sheet.domain, ""))} ·
<span class="print-hint">Ctrl/Cmd&nbsp;+&nbsp;P to print or save PDF</span></p>
{sheet.body_html}
</div>
<p class="note status no-print">Domain cheatsheet{html.escape(stamp)} · condensed from the {sheet.domain} objective pages</p>
"""
    return page(sheet.title, body, depth=1, scripts=[], active="cheatsheet/index.html")


def build_diagram_index(diagrams: list[DiagramPage], spec: dict) -> str:
    dom_title = {d["id"]: d["title"] for d in spec.get("domains", [])}
    if not diagrams:
        body = (
            "<p class=\"crumb\"><a href=\"../index.html\">Dashboard</a> / Diagrams</p>"
            "<h1>Diagrams</h1><p class='note'>Nothing here yet. Per-domain big-picture diagrams live in "
            "<code>content/diagrams/D{n}.md</code> — curated SVGs that wire a domain together.</p>"
        )
        return page("Diagrams", body, depth=1, scripts=[], active="diagram/index.html")

    cards = []
    for p in sorted(diagrams, key=lambda x: x.domain):
        stamp = f'<span class="flag">captured {p.captured}</span>' if p.captured else ""
        cards.append(
            f'<li class="ref-card"><h2><a href="{p.domain}.html">{html.escape(p.title)}</a></h2>'
            f'<p>{html.escape(p.summary or dom_title.get(p.domain, ""))}</p>'
            f'<p class="flags">{stamp}'
            f'<a class="chip" href="../domain/{p.domain}.html">{p.domain} objectives</a></p></li>'
        )
    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / Diagrams</p>
<h1>Diagrams</h1>
<p class="blueprint">One page per domain — a curated set of big pictures that connect the domain's
concepts, and map the Azure constructs that look alike or do the same job. Not every fact; the ones
that only make sense as a whole. Dashed/muted nodes are forward-links to other domains.</p>
<ul class="ref-list">{"".join(cards)}</ul>
"""
    return page("Diagrams", body, depth=1, scripts=[], active="diagram/index.html")


def build_diagram_page(dp: DiagramPage, spec: dict) -> str:
    dom_title = {d["id"]: d["title"] for d in spec.get("domains", [])}
    stamp = f" · captured {dp.captured}" if dp.captured else ""
    body = f"""
<p class="crumb"><a href="../index.html">Dashboard</a> / <a href="index.html">Diagrams</a> / {html.escape(dp.title)}</p>
<div class="objective-body diagrams">
<h1>{html.escape(dp.title)}</h1>
<p class="blueprint">{html.escape(dp.summary or dom_title.get(dp.domain, ""))}</p>
{dp.body_html}
</div>
<p class="note status">Domain diagrams{html.escape(stamp)} · cross-page big pictures for {dp.domain}</p>
"""
    return page(dp.title, body, depth=1, scripts=[], active="diagram/index.html")


def build_reviews_page(spec: dict) -> str:
    """Index of the full-topic reference reviews (the self-contained pages under
    assets/visuals/). Content may go beyond the exam blueprint — a standing exception
    the learner approved, so these live in their own section next to Reference."""
    d = ASSETS / "visuals"
    cards = []
    if d.exists():
        for path in sorted(d.glob("*.html")):
            if path.name == "index.html":
                continue
            txt = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"<title>(.*?)</title>", txt, re.IGNORECASE | re.DOTALL)
            title = html.unescape(m.group(1).strip()) if m else path.stem
            cards.append(
                f'<li class="ref-card"><h2><a href="visuals/{path.name}">{html.escape(title)}</a></h2>'
                f'<p>Full single-page reference review — open, print, or drop notes on it.</p></li>'
            )
    if not cards:
        body = (
            "<p class=\"crumb\"><a href=\"index.html\">Dashboard</a> / Reviews</p>"
            "<h1>Reference reviews</h1><p class='note'>Nothing here yet. Complete-topic reviews live in "
            "<code>assets/visuals/*.html</code>.</p>"
        )
        return page("Reference reviews", body, depth=0, scripts=[], active="reviews.html")
    body = f"""
<p class="crumb"><a href="index.html">Dashboard</a> / Reviews</p>
<h1>Reference reviews</h1>
<p class="blueprint">Complete single-page maps of a whole topic — more than an objective page, grounded
in Microsoft Learn. Content may go <strong>beyond</strong> the {EXAM_CODE} blueprint where it helps
understanding. Open one, print it (Ctrl/Cmd + P), or drop notes on it.</p>
<ul class="ref-list">{"".join(cards)}</ul>
"""
    return page("Reference reviews", body, depth=0, scripts=[], active="reviews.html")


def build_curriculum_page(lm: dict, objectives: list[Objective]) -> str:
    """Every official Learn unit, mapped to the blueprint bullet it actually serves."""
    if not lm:
        body = """<h1>Curriculum</h1><div class="empty"><p><strong>No learn map.</strong>
Expected <code>content/learn-map.toml</code>.</p></div>"""
        return page("Curriculum", body, depth=0, scripts=[], active="curriculum.html")

    by_id = {o.id: o for o in objectives}
    modules = lm["_modules_by_slug"]
    units = lm["units"]
    units_by_mod: dict[str, list[dict]] = {}
    for u in units:
        units_by_mod.setdefault(u["module"], []).append(u)

    def chips(u: dict) -> str:
        oids = u.get("objectives", [])
        if oids:
            return " ".join(
                f'<a class="chip" href="objective/{o}.html" '
                f'title="{html.escape(by_id[o].text if o in by_id else o)}">{o}</a>'
                for o in oids
            )
        # An intro or a summary teaches nothing; that is not the same as Microsoft teaching
        # something the blueprint never asks for. Only the latter is Skip-section material.
        if u.get("off_blueprint"):
            return '<span class="chip chip-skip">off blueprint</span>'
        return '<span class="chip chip-none">—</span>'

    off = sum(1 for u in units if u.get("off_blueprint"))
    blocked = sum(1 for u in units if u.get("license_blocked"))
    teaching = sum(1 for u in units if u["kind"] in ("concept", "exercise"))

    sections: list[str] = []
    for p in lm["paths"]:
        mods = [m for m in lm["modules"] if m["path"] == p["id"]]
        rows: list[str] = []
        for m in mods:
            lis: list[str] = []
            for u in units_by_mod.get(m["slug"], []):
                cls = []
                if u.get("off_blueprint"):
                    cls.append("u-skip")
                if u.get("thin_coverage"):
                    cls.append("u-thin")
                if u["kind"] in ("intro", "assessment", "summary"):
                    cls.append("u-filler")
                flags = ""
                if u.get("license_blocked"):
                    flags += ' <span class="flag">no licence</span>'
                if u.get("thin_coverage"):
                    flags += ' <span class="flag risk">thin</span>'
                note = (
                    f'<p class="note">{render_inline(u["note"])}</p>' if u.get("note") else ""
                )
                lis.append(
                    f'<li class="{" ".join(cls)}">'
                    f'<span class="u-n">{u["n"]}</span> '
                    f'<a href="{m["url"]}{u["slug"]}">{html.escape(u["title"])}</a>{flags}'
                    f'<span class="u-obj">{chips(u)}</span>{note}</li>'
                )
            native = (
                ""
                if m.get("exam_native", True)
                else f' <span class="flag risk">not written for {EXAM_CODE}</span>'
            )
            mnote = f'<p class="note">{render_inline(m["note"])}</p>' if m.get("note") else ""
            rows.append(f"""
<section class="module" id="mod-{m['slug']}">
  <h3><a href="{m['url']}">{html.escape(m['title'])}</a>
    <span class="flag">{m['unit_count']} units</span>
    <span class="flag">{html.escape(m.get('level', ''))}</span>{native}</h3>
  {mnote}
  <ol class="units">{''.join(lis)}</ol>
</section>""")
        sections.append(f"""
<section class="path" id="path-{p['id']}">
  <h2><a href="{p['url']}">{html.escape(p['title'])}</a>
    <span class="flag">{p['domain']}</span>
    <span class="flag">{p['modules']} modules</span></h2>
  {''.join(rows)}
</section>""")

    gaps = ""
    if lm.get("_uncovered"):
        items = "".join(
            f'<li><a href="objective/{o}.html"><code>{o}</code></a> '
            f"{html.escape(by_id[o].text if o in by_id else '')}</li>"
            for o in lm["_uncovered"]
        )
        gaps = f"""
<div class="callout callout-risk">
  <h2>On the exam, absent from the curriculum</h2>
  <p>These blueprint bullets have <strong>no unit anywhere in the 189</strong>. Microsoft will still
  ask about them. They have to be written from product documentation.</p>
  <ul>{items}</ul>
</div>"""

    thin = ""
    if lm.get("_single_unit"):
        items = "".join(
            f'<li><a href="objective/{o}.html"><code>{o}</code></a> '
            f"<span class='note'>{html.escape(lm['_covered'][o][0])}</span></li>"
            for o in lm["_single_unit"]
        )
        thin = f"""
<div class="callout">
  <h2>One unit deep</h2>
  <p>A single unit carries the whole bullet. Thin coverage is not the same as a small topic —
  check the product docs before trusting the depth.</p>
  <ul class="cols">{items}</ul>
</div>"""

    body = f"""<h1>Official curriculum</h1>
<p class="lede">Every Microsoft Learn unit for {EXAM_CODE}, mapped to the blueprint bullet it serves.
{len(lm['paths'])} paths · {len(lm['modules'])} modules · <strong>{len(units)} units</strong>
({teaching} teach something, {len(units) - teaching} are intros, knowledge checks and summaries).
Captured {lm.get('captured', '')}.</p>
<p class="note">{off} units teach material that is <strong>not on the blueprint</strong> —
they are marked <em>off blueprint</em> and are Skip-section material.
{blocked} units are exercises that need a live Azure subscription.</p>
{gaps}
{thin}
{''.join(sections)}"""
    return page("Curriculum", body, depth=0, scripts=[], active="curriculum.html")


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def js_data(name: str, payload: object) -> str:
    return (
        "/* GENERATED by build.py — do not edit. */\n"
        "window.SC200 = window.SC200 || {};\n"
        f"window.SC200.{name} = {json.dumps(payload, separators=(',', ':'), default=str)};\n"
    )


def emit(
    spec: dict,
    objectives: list[Objective],
    questions: list[Question],
    labs: list[Lab],
    lm: dict | None = None,
    refs: list[Reference] | None = None,
    sheets: list[Cheatsheet] | None = None,
    diagrams: list[DiagramPage] | None = None,
    found: list[Foundation] | None = None,
) -> None:
    refs = refs or []
    found = found or []
    sheets = sheets or []
    diagrams = diagrams or []
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "domain").mkdir(parents=True)
    (SITE / "objective").mkdir(parents=True)
    (SITE / "reference").mkdir(parents=True)
    (SITE / "cheatsheet").mkdir(parents=True)
    (SITE / "diagram").mkdir(parents=True)

    (SITE / "index.html").write_text(build_dashboard(spec, objectives, questions, labs, lm), encoding="utf-8")
    for dom in spec.get("domains", []):
        dom_objs = [o for o in objectives if o.domain == dom["id"]]
        (SITE / "domain" / f"{dom['id']}.html").write_text(
            build_domain_page(dom, dom_objs, questions), encoding="utf-8"
        )
    for idx, obj in enumerate(objectives):
        prev = objectives[idx - 1] if idx > 0 else None
        nxt = objectives[idx + 1] if idx < len(objectives) - 1 else None
        (SITE / "objective" / f"{obj.id}.html").write_text(
            build_objective_page(obj, questions, labs, prev, nxt, lm, refs, found), encoding="utf-8"
        )
    (SITE / "foundations").mkdir(parents=True, exist_ok=True)
    (SITE / "foundations" / "index.html").write_text(
        build_foundations_index(found, objectives), encoding="utf-8"
    )
    for f in found:
        (SITE / "foundations" / f"{f.slug}.html").write_text(
            build_foundation_page(f, found, objectives), encoding="utf-8"
        )
    (SITE / "reference" / "index.html").write_text(
        build_reference_index(refs, objectives), encoding="utf-8"
    )
    for ref in refs:
        (SITE / "reference" / f"{ref.slug}.html").write_text(
            build_reference_page(ref, objectives), encoding="utf-8"
        )
    (SITE / "cheatsheet" / "index.html").write_text(
        build_cheatsheet_index(sheets, spec), encoding="utf-8"
    )
    for sheet in sheets:
        (SITE / "cheatsheet" / f"{sheet.domain}.html").write_text(
            build_cheatsheet_page(sheet, spec), encoding="utf-8"
        )
    (SITE / "diagram" / "index.html").write_text(
        build_diagram_index(diagrams, spec), encoding="utf-8"
    )
    for dp in diagrams:
        (SITE / "diagram" / f"{dp.domain}.html").write_text(
            build_diagram_page(dp, spec), encoding="utf-8"
        )
    (SITE / "quiz.html").write_text(build_quiz_page(), encoding="utf-8")
    (SITE / "mock-exam.html").write_text(build_mock_page(), encoding="utf-8")
    (SITE / "labs.html").write_text(build_labs_page(labs, objectives), encoding="utf-8")
    (SITE / "curriculum.html").write_text(
        build_curriculum_page(lm or {}, objectives), encoding="utf-8"
    )
    (SITE / "reviews.html").write_text(build_reviews_page(spec), encoding="utf-8")

    payload = {
        "exam": {
            "code": spec.get("exam_code"),
            "title": spec.get("exam_title"),
            "captured": str(spec.get("outline_captured", "")),
        },
        "domains": [
            {
                "id": d["id"],
                "title": d["title"],
                "weight": d.get("sample_weight", 0),
                "weight_min": d.get("weight_min"),
                "weight_max": d.get("weight_max"),
            }
            for d in spec.get("domains", [])
        ],
        "objectives": [
            {
                "id": o.id,
                "title": o.display_title,
                "text": o.text,
                "domain": o.domain,
                "subdomain": o.subdomain,
                "hours": o.hours,
                "week": o.week,
                "prior": o.prior_cert,
                "risk": o.high_risk,
                "blocked": o.license_blocked,
                "written": o.has_content,
            }
            for o in objectives
        ],
        "questions": [
            {**q.data, "id": q.id, "format": q.fmt, "objective_ids": q.objective_ids}
            for q in questions
        ],
        "labs": [{"id": l.id, "title": l.title, "objective_ids": l.objective_ids, "minutes": l.minutes} for l in labs],
        "learnMap": {
            "captured": str((lm or {}).get("captured", "")),
            "unitTotal": len((lm or {}).get("units", [])),
            "byObjective": (lm or {}).get("_covered", {}),
            "uncovered": (lm or {}).get("_uncovered", []),
        },
        "progressFallback": load_progress_fallback(),
    }
    (SITE / "content-data.js").write_text(js_data("data", payload), encoding="utf-8")
    (SITE / "search-index.js").write_text(
        js_data("searchIndex", build_search_index(objectives, questions, labs, refs, found)), encoding="utf-8"
    )

    if ASSETS.exists():
        for asset in sorted(ASSETS.iterdir()):
            if asset.is_file():
                shutil.copy2(asset, SITE / asset.name)
            elif asset.is_dir():
                shutil.copytree(asset, SITE / asset.name)
    else:
        error("assets/ not found — the site will have no stylesheet or scripts")


def report(spec: dict, objectives: list[Objective], questions: list[Question], labs: list[Lab]) -> dict:
    q_by_obj: dict[str, int] = {}
    for q in questions:
        for oid in q.objective_ids:
            q_by_obj[oid] = q_by_obj.get(oid, 0) + 1
    return {
        "objectives_total": len(objectives),
        "objectives_written": sum(1 for o in objectives if o.has_content),
        "questions_total": len(questions),
        "questions_verified": sum(1 for q in questions if q.verified),
        "labs_total": len(labs),
        "planned_hours": sum(o.hours for o in objectives),
        "uncovered_objectives": [o.id for o in objectives if not q_by_obj.get(o.id)],
        "unwritten_objectives": [o.id for o in objectives if not o.has_content],
        "by_domain": {
            d["id"]: {
                "written": sum(1 for o in objectives if o.domain == d["id"] and o.has_content),
                "total": sum(1 for o in objectives if o.domain == d["id"]),
                "questions": sum(1 for q in questions if any(oid.startswith(d["id"]) for oid in q.objective_ids)),
            }
            for d in spec.get("domains", [])
        },
    }


def report_learn_map(lm: dict, objectives: list[Objective]) -> int:
    """Print curriculum coverage per objective. No network — reads the captured map."""
    if not lm:
        print("no content/learn-map.toml", file=sys.stderr)
        return 1

    units = lm["units"]
    covered = lm["_covered"]
    off = [u for u in units if u.get("off_blueprint")]
    thin = [u for u in units if u.get("thin_coverage")]

    print(
        f"{len(lm['paths'])} paths · {len(lm['modules'])} modules · {len(units)} units "
        f"(captured {lm.get('captured')})"
    )
    print(f"{len(off)} off-blueprint · {len(thin)} flagged thin · "
          f"{sum(1 for u in units if u.get('license_blocked'))} licence-blocked\n")

    print("objectives with NO unit in the official curriculum:")
    for oid in lm["_uncovered"]:
        o = next((x for x in objectives if x.id == oid), None)
        print(f"  {oid}  {o.text if o else ''}")
    if not lm["_uncovered"]:
        print("  none")

    print("\nobjectives carried by a single unit:")
    for oid in lm["_single_unit"]:
        print(f"  {oid}  {covered[oid][0]}")

    print("\noff-blueprint units (Skip-section material):")
    for u in off:
        print(f"  {u['module']}#{u['n']}  {u['title']}")

    for e in ERRORS:
        print(f"  ERROR: {e}", file=sys.stderr)
    return 1 if ERRORS else 0


def check_links(
    objectives: list[Objective],
    questions: list[Question],
    lm: dict | None = None,
    refs: list[Reference] | None = None,
    found: list[Foundation] | None = None,
) -> int:
    """Check every cited URL for rot. The only part of this tool that touches the network.

    Exists because a verification pass found 3 of 19 questions citing a dead, redirected or
    retirement-noticed page. Microsoft consolidates and retires docs constantly, and a citation
    that silently 301s to a different article is worse than one that 404s — it looks fine.
    """
    import concurrent.futures
    import urllib.error
    import urllib.request

    sources: dict[str, list[str]] = {}
    for o in objectives:
        for u in o.ms_learn_urls:
            sources.setdefault(u, []).append(o.id)
    for q in questions:
        for u in q.data.get("source_urls", []):
            sources.setdefault(u, []).append(q.id)
    # Reference pages rot faster than anything else here — pricing pages get restructured
    # constantly, and a 404 on a price source is the signal to go re-read the numbers.
    for r in refs or []:
        for u in r.source_urls:
            sources.setdefault(u, []).append(f"ref:{r.slug}")
    for f in found or []:
        for u in f.ms_learn_urls:
            sources.setdefault(u, []).append(f"fnd:{f.slug}")

    # The curriculum map is only useful if its 209 URLs still resolve. A renamed unit slug is
    # exactly the kind of silent drift this whole file exists to catch.
    if lm:
        mods = lm["_modules_by_slug"]
        for p in lm["paths"]:
            sources.setdefault(p["url"], []).append(f"path:{p['id']}")
        for m in lm["modules"]:
            sources.setdefault(m["url"], []).append(f"module:{m['slug']}")
        for u in lm["units"]:
            url = f"{mods[u['module']]['url']}{u['slug']}"
            sources.setdefault(url, []).append(f"unit:{u['module']}#{u['n']}")

    if not sources:
        print("no URLs cited yet")
        return 0

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.error.HTTPError(req.full_url, code, newurl, headers, fp)

    opener = urllib.request.build_opener(NoRedirect)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (SC-200 study system link check)")]

    def probe(url: str) -> tuple[str, str, str]:
        try:
            with opener.open(url, timeout=20) as resp:
                return url, "ok", str(resp.status)
        except urllib.error.HTTPError as exc:
            if exc.code in (301, 302, 303, 307, 308):
                target = str(exc.reason)
                # A redirect that only adds a locale or query string is noise, not rot.
                same = target.split("?")[0].rstrip("/").endswith(url.split("?")[0].rstrip("/").split("/")[-1])
                return url, "ok" if same else "redirect", target
            return url, "dead", f"HTTP {exc.code}"
        except Exception as exc:  # network down, DNS, TLS, timeout
            return url, "error", type(exc).__name__

    print(f"checking {len(sources)} cited URLs…\n")
    results: list[tuple[str, str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for r in pool.map(probe, sorted(sources)):
            results.append(r)

    bad = 0
    for status in ("dead", "redirect", "error"):
        rows = [r for r in results if r[1] == status]
        if not rows:
            continue
        label = {"dead": "DEAD", "redirect": "REDIRECTED", "error": "UNREACHABLE"}[status]
        print(f"{label} ({len(rows)}):")
        for url, _, detail in rows:
            print(f"  {url}\n    -> {detail}\n    cited by: {', '.join(sorted(set(sources[url])))}")
        print()
        if status != "error":
            bad += len(rows)

    ok = sum(1 for r in results if r[1] == "ok")
    print(f"{ok} ok, {bad} need attention, {sum(1 for r in results if r[1] == 'error')} unreachable")
    if bad:
        print("\nFix the citation, then re-verify the affected question or page against the new doc.")
    return 1 if bad else 0


def fetch_images() -> int:
    """Download every remote image referenced in content into assets/img/cache/.

    Authors write plain Microsoft Learn image URLs. This pulls them local so the site keeps
    working offline, which is the whole point of the thing. Run it after adding images.
    """
    import urllib.error
    import urllib.request

    urls: dict[str, list[str]] = {}
    for folder, pattern in (
        (CONTENT / "objectives", "*.md"),
        (CONTENT / "labs", "*.md"),
        (CONTENT / "foundations", "*.md"),
        (CONTENT / "reference", "*.md"),
    ):
        if not folder.exists():
            continue
        for path in sorted(folder.glob(pattern)):
            for m in _IMAGE.finditer(path.read_text(encoding="utf-8")):
                url = m.group(2)
                if url.startswith(("http://", "https://")):
                    urls.setdefault(url, []).append(path.stem)

    if not urls:
        print("no remote images referenced in content")
        return 0

    (ASSETS / IMG_CACHE).mkdir(parents=True, exist_ok=True)
    got = skipped = failed = 0

    for url in sorted(urls):
        rel = cache_name(url)
        dest = ASSETS / rel
        if dest.exists():
            skipped += 1
            continue
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (SC-200 study system)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 200:
                raise ValueError(f"suspiciously small ({len(data)} bytes)")
            dest.write_bytes(data)
            got += 1
            print(f"  fetched  {rel}  ({len(data) // 1024} KB)  <- {url}")
        except (urllib.error.URLError, ValueError, OSError) as exc:
            failed += 1
            print(f"  FAILED   {url}\n    {exc}\n    referenced by: {', '.join(urls[url])}")

    print(f"\n{got} fetched, {skipped} already cached, {failed} failed")
    if got or skipped:
        print("Run `python3 build.py` to rebuild with the local copies.")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the SC-200 study site.")
    ap.add_argument("--lint", action="store_true", help="validate only, write nothing")
    ap.add_argument("--report", action="store_true", help="print stats as JSON")
    ap.add_argument("--quiet", action="store_true", help="suppress the summary line")
    ap.add_argument(
        "--check-links",
        action="store_true",
        help="probe every cited Microsoft Learn URL for rot (needs network)",
    )
    ap.add_argument(
        "--fetch-images",
        action="store_true",
        help="download remote images into assets/img/cache so they work offline (needs network)",
    )
    ap.add_argument(
        "--check-learn-map",
        action="store_true",
        help="report official-curriculum coverage per objective and exit",
    )
    ap.add_argument(
        "--online",
        action="store_true",
        help="hosted build: remote (uncached) images load from Microsoft directly — no 'needs network' chip",
    )
    args = ap.parse_args()

    global ONLINE
    ONLINE = args.online

    if args.fetch_images:
        return fetch_images()

    spec, objectives = load_domains()
    if not objectives:
        if ERRORS:
            print("FATAL: no objectives loaded", file=sys.stderr)
            for e in ERRORS:
                print(f"  error: {e}", file=sys.stderr)
            return 2
        print(
            "note: no objectives defined yet — building an empty scaffold shell "
            "(fill content/domains.toml to add material)",
            file=sys.stderr,
        )

    global EXAM_CODE
    EXAM_CODE = str(spec.get("exam_code") or EXAM_CODE)

    load_objective_bodies(objectives)
    valid_ids = {o.id for o in objectives}
    lm = load_learn_map(valid_ids)
    questions = load_questions(valid_ids)
    labs = load_labs(valid_ids)
    refs = load_references(valid_ids)
    found = load_foundations(valid_ids)
    check_foundation_refs(objectives, found)
    sheets = load_cheatsheets({d["id"] for d in spec.get("domains", [])})
    diagrams = load_diagrams({d["id"] for d in spec.get("domains", [])})
    check_duplicates(questions)

    if args.check_learn_map:
        return report_learn_map(lm, objectives)

    if args.check_links:
        return check_links(objectives, questions, lm, refs, found)

    if args.report:
        print(json.dumps(report(spec, objectives, questions, labs), indent=2))
        return 0

    if not args.lint:
        emit(spec, objectives, questions, labs, lm, refs, sheets, diagrams, found)

    for w in WARNINGS:
        print(f"  warn:  {w}", file=sys.stderr)
    for e in ERRORS:
        print(f"  ERROR: {e}", file=sys.stderr)

    if not args.quiet:
        written = sum(1 for o in objectives if o.has_content)
        action = "linted" if args.lint else f"built site/ ->"
        print(
            f"{action} {len(objectives)} objectives ({written} written), "
            f"{len(questions)} questions, {len(labs)} labs, "
            f"{len(WARNINGS)} warnings, {len(ERRORS)} errors"
        )
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
