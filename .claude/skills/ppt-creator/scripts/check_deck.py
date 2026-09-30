#!/usr/bin/env python3
# Script:   .claude/skills/ppt-creator/scripts/check_deck.py (research-to-policy)
# Inputs:   a .pptx
# Outputs:  a per-slide report on stdout; exit 1 if any ERROR
# Seed:     none
# Env:      python3, python-pptx
#
# Lints a deck against the slide grammar in ../SKILL.md:
#   title + ONE kind of content + source; <= 4 charts; no free text that reads
#   the chart; side text only next to a chart, and short; nothing under 11 pt.
#
# Shapes written by gl_deck.py carry a role name ("gl:title", "gl:chart", ...).
# Shapes from any other builder are classified by placeholder type and shape
# kind, so the lint also runs on decks this skill did not build (a text box it
# cannot place is reported as free text — the thing the grammar forbids).
#
#   python3 check_deck.py deck.pptx            # report, exit 1 on errors
#   python3 check_deck.py deck.pptx --quiet    # only slides with findings

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.util import Pt

PT_MIN = 11
SIDE_MAX_WORDS = 45

# Layouts whose content is not a title/content/source slide.
FREE_LAYOUTS = {"Title Slide", "Title Slide With Background Image", "Statement Text",
                "Closing Slide", "Full Image"}

TITLE_ZONE_IN = 1.3     # a role-less text box starting above this is the headline
SUBTITLE_ZONE_IN = 2.0  # ...and the next one above this, the chart title

CONTENT_ROLES = {"gl:chart": "chart", "gl:table": "table", "gl:list": "list",
                 "gl:image": "image", "gl:statement": "text"}
TEXT_ROLES = {"gl:title", "gl:subtitle", "gl:source", "gl:side", "gl:meta",
              "gl:list-head", "gl:section-label", "gl:section-icon"}
FOOTER_PH = {PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.DATE}


def role(shape) -> str:
    """Best guess at what a shape is doing on the slide."""
    if shape.name.startswith("gl:"):
        return shape.name
    if shape.is_placeholder:
        t = shape.placeholder_format.type
        if t in FOOTER_PH:
            return "footer"
        if t in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE):
            return "gl:title"
        if t == PP_PLACEHOLDER.SUBTITLE:
            return "gl:subtitle"
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        return "gl:chart"
    if getattr(shape, "has_table", False) and shape.has_table:
        return "gl:table"
    if getattr(shape, "has_chart", False) and shape.has_chart:
        return "gl:chart"
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        return "diagram"
    if shape.has_text_frame:
        txt = shape.text_frame.text.strip()
        if not txt:
            return "empty"
        if txt.lower().startswith(("fuente", "source")) or "Fuente:" in txt:
            return "gl:source"
        if len(txt) <= 5:          # page labels such as "4b", "12"
            return "footer"
        return "free-text"
    return "other"


def small_runs(shape):
    """Explicit run sizes under the floor (inherited sizes are the template's)."""
    frames = []
    if shape.has_text_frame:
        frames.append(shape.text_frame)
    if getattr(shape, "has_table", False) and shape.has_table:
        frames += [c.text_frame for row in shape.table.rows for c in row.cells]
    out = []
    for tf in frames:
        for p in tf.paragraphs:
            for r in p.runs:
                size = r.font.size or p.font.size
                if size is not None and size < Pt(PT_MIN) and r.text.strip():
                    out.append((size.pt, r.text.strip()[:40]))
    return out


def check_slide(slide):
    errors, warns = [], []
    layout = slide.slide_layout.name.strip()
    roles = [(role(sh), sh) for sh in slide.shapes]
    # Decks not built by gl_deck.py: promote the top text boxes to headline and
    # chart title by position, so only the text below them counts as free text.
    if not any(r == "gl:title" for r, _ in roles):
        loose = sorted((sh.top, k) for k, (r, sh) in enumerate(roles)
                       if r == "free-text" and sh.top is not None)
        for pos, (top, k) in enumerate(loose[:2]):
            zone = TITLE_ZONE_IN if pos == 0 else SUBTITLE_ZONE_IN
            if top < zone * 914400:
                roles[k] = ("gl:title" if pos == 0 else "gl:subtitle", roles[k][1])
    names = [r for r, _ in roles]

    for r, sh in roles:
        for pt, txt in small_runs(sh):
            errors.append(f"text at {pt:g} pt < {PT_MIN} pt: “{txt}”")

    if layout in FREE_LAYOUTS:
        return errors, warns

    is_section = "gl:section-label" in names
    if "gl:title" not in names:
        errors.append("no title")
    if is_section:
        return errors, warns

    kinds = {CONTENT_ROLES[r] for r in names if r in CONTENT_ROLES}
    if "diagram" in names:
        kinds.add("diagram")
    if not kinds:
        errors.append("no content (chart, table, list, image or text)")
    elif len(kinds) > 1:
        errors.append(f"mixes content kinds: {sorted(kinds)} — one kind per slide")

    n_charts = names.count("gl:chart")
    if n_charts > 4:
        errors.append(f"{n_charts} charts — at most 4")
    elif n_charts > 1:
        warns.append(f"{n_charts} charts — ideally one per slide")

    if "gl:source" not in names:
        errors.append("no source line")
    if "chart" in kinds and "gl:subtitle" not in names:
        warns.append("chart without a chart title (the line naming the variables)")

    for r, sh in roles:
        if r == "free-text":
            errors.append(f"free text box (reads or explains the content?): "
                          f"“{sh.text_frame.text.strip()[:70]}”")
        if r == "gl:side":
            if "chart" not in kinds:
                errors.append("side text without a chart")
            n = len(sh.text_frame.text.split())
            if n > SIDE_MAX_WORDS:
                warns.append(f"side text has {n} words (> {SIDE_MAX_WORDS}): define the "
                             "category, do not read the chart")
    return errors, warns


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        sys.exit(__doc__ or "usage: check_deck.py deck.pptx [--quiet]")
    path, quiet = Path(argv[0]), "--quiet" in argv
    prs = Presentation(str(path))
    n_err = n_warn = 0
    for i, slide in enumerate(prs.slides, 1):
        errors, warns = check_slide(slide)
        n_err += len(errors)
        n_warn += len(warns)
        if quiet and not (errors or warns):
            continue
        title = next((sh.text_frame.text.strip() for sh in slide.shapes
                      if role(sh) == "gl:title" and sh.has_text_frame), "")
        print(f"{i:3d} [{slide.slide_layout.name.strip()}] {title[:70]}")
        for e in errors:
            print(f"      ERROR  {e}")
        for w in warns:
            print(f"      warn   {w}")
    print(f"\n{len(prs.slides)} slides · {n_err} errors · {n_warn} warnings")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
