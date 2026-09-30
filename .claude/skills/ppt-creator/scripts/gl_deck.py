#!/usr/bin/env python3
# Script:   .claude/skills/ppt-creator/scripts/gl_deck.py (research-to-policy)
# Inputs:   ../assets/GL_presentation_template.potx
# Outputs:  none (library; the caller saves the Presentation)
# Seed:     none
# Env:      python3, python-pptx, Pillow
#
# Growth Lab deck builder on the layouts of the official GL template. Every slide
# is one of a few grammars (see ../SKILL.md § Slide grammar): title, content,
# source. The builder names each shape it writes with a role ("gl:title",
# "gl:chart", "gl:source", ...) so check_deck.py can verify the grammar
# afterwards without guessing.
#
# Usage:
#   import sys; sys.path.insert(0, "<skill>/scripts"); import gl_deck as D
#   prs = D.new_deck()
#   D.title_slide(prs, "Título", "Subtítulo", "Harvard Growth Lab | Septiembre 2026")
#   D.chart_slide(prs, "Titular de la lámina", "Variables (eje x) vs. variables (eje y), 2025",
#                 "output/x/deck_assets/x_bare.png", "Fuente: ...", notes="Lectura para el orador")
#   prs.save("deck.pptx")

from __future__ import annotations

import io
import tempfile
import zipfile
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / "assets" / "GL_presentation_template.potx"

# Type scale for the text this module draws itself (placeholders inherit the
# template's own sizes). Nothing goes below PT_MIN; check_deck.py enforces it.
PT_MIN = 11
PT_SUBTITLE = 15
PT_SIDE = 14
PT_LIST = 16
PT_TABLE = 12
PT_SECTION = 14

INK = RGBColor(0x14, 0x45, 0x62)      # GL navy, as in the template's title placeholders
MUTED = RGBColor(0x59, 0x59, 0x59)
FADED = RGBColor(0xBF, 0xBF, 0xBF)
RULE = RGBColor(0xD9, 0xD9, 0xD9)
HEAD_FILL = RGBColor(0x14, 0x45, 0x62)
ZEBRA = RGBColor(0xF2, 0xF4, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SUBTITLE_H = 0.42  # inches reserved under the title for the chart's variable line

# Layout names in the GL template (trailing spaces in the .potx are stripped).
L_TITLE = "Title Slide"
L_SINGLE = "Single Visual"
L_TWO = "Two Visuals"
L_SIDE = "1_Two Visuals"
L_STATEMENT = "Statement Text"
L_TITLE_BLANK = "Title + Blank"
L_CLOSING = "Closing Slide"


# ── Deck ────────────────────────────────────────────────────────────────
def new_deck(template: Path = TEMPLATE):
    """A Presentation on the GL template, with the template's sample slides removed.

    python-pptx refuses a .potx, so the main part's content type is rewritten
    to the .pptx one in memory; the template file is never modified.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(template) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(b"presentationml.template.main+xml",
                                    b"presentationml.presentation.main+xml")
            zout.writestr(item, data)
    buf.seek(0)
    prs = Presentation(buf)
    for sld_id in list(prs.slides._sldIdLst):
        prs.part.drop_rel(sld_id.rId)
        prs.slides._sldIdLst.remove(sld_id)
    return prs


def _layout(prs, name):
    for lay in prs.slide_layouts:
        if lay.name.strip() == name:
            return lay
    raise KeyError(f"layout {name!r} not in template")


def _new(prs, layout_name, notes=""):
    slide = prs.slides.add_slide(_layout(prs, layout_name))
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def _ph(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    raise KeyError(f"placeholder idx={idx} not on layout {slide.slide_layout.name!r}")


def _fill(slide, idx, text, role):
    ph = _ph(slide, idx)
    ph.text = text
    ph.name = role
    return ph


def _take_box(slide, idx):
    """Remove a placeholder and return its box (left, top, width, height) in EMU."""
    ph = _ph(slide, idx)
    box = (ph.left, ph.top, ph.width, ph.height)
    ph._element.getparent().remove(ph._element)
    return box


def _drop_empty(slide, keep=()):
    """Delete placeholders nobody filled, so no 'Click to add text' survives."""
    for ph in list(slide.placeholders):
        idx = ph.placeholder_format.idx
        if idx in keep:
            continue
        if ph.has_text_frame and not ph.text_frame.text.strip():
            ph._element.getparent().remove(ph._element)


# ── Text primitives ──────────────────────────────────────────────────────
def _textbox(slide, role, text, box, *, size, color=MUTED, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    left, top, width, height = box
    tb = slide.shapes.add_textbox(left, top, width, height)
    tb.name = role
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = text if isinstance(text, (list, tuple)) else [text]
    for i, line in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = str(line)
        p.alignment = align
        if i:
            p.space_before = Pt(6)
        p.font.size = Pt(max(size, PT_MIN))
        p.font.bold = bold
        p.font.color.rgb = color
    return tb


def _subtitle(slide, text, visual_box):
    """Chart title (names the variables) as live text right above the visual.

    Returns the visual box shrunk by the room the line took.
    """
    left, top, width, height = visual_box
    h = Inches(SUBTITLE_H)
    _textbox(slide, "gl:subtitle", text, (left, top, width, h), size=PT_SUBTITLE)
    return (left, top + h, width, height - h)


def _picture(slide, path, box, role="gl:chart"):
    """Place an image inside `box`, aspect preserved, centred."""
    left, top, width, height = box
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(width / iw, height / ih)
    w, h = int(iw * scale), int(ih * scale)
    pic = slide.shapes.add_picture(str(path), left + (width - w) // 2, top + (height - h) // 2, w, h)
    pic.name = role
    return pic


def _grid(box, n, gap=Inches(0.2)):
    """Split a box into n cells: 1, 2 side by side, 3 in a row, 4 as 2x2."""
    left, top, width, height = box
    cols, rows = {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (2, 2)}[n]
    cw = (width - gap * (cols - 1)) // cols
    rh = (height - gap * (rows - 1)) // rows
    return [(left + c * (cw + gap), top + r * (rh + gap), cw, rh)
            for r in range(rows) for c in range(cols)][:n]


# ── Slide grammars ───────────────────────────────────────────────────────
def title_slide(prs, title, subtitle="", metadata="", notes=""):
    s = _new(prs, L_TITLE, notes)
    _fill(s, 0, title, "gl:title")
    if subtitle:
        _fill(s, 10, subtitle, "gl:subtitle")
    if metadata:
        _fill(s, 11, metadata, "gl:meta")
    _drop_empty(s)
    return s


def section_slide(prs, heading, items, current, notes=""):
    """Section divider: a row of the deck's sections with the current one lit.

    items: list of (label, icon_path or None). The others are drawn faded, as
    in the Córdoba ministers' deck.
    """
    s = _new(prs, L_TITLE_BLANK, notes)
    _fill(s, 14, heading, "gl:title")
    n = len(items)
    area_l, area_w = Inches(0.47), Inches(12.41)
    cell = area_w // n
    icon = Inches(1.1)
    top_icon, top_label = Inches(2.9), Inches(2.1)
    tmp = Path(tempfile.mkdtemp())
    for i, (label, icon_path) in enumerate(items):
        lit = i == current
        x = area_l + i * cell
        _textbox(s, "gl:section-label", label, (x, top_label, cell, Inches(0.7)),
                 size=PT_SECTION, bold=lit, color=INK if lit else FADED,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        if icon_path:
            src = Path(icon_path)
            if not lit:
                faded = tmp / f"faded_{i}{src.suffix or '.png'}"
                with Image.open(src).convert("RGBA") as im:
                    alpha = im.getchannel("A").point(lambda a: int(a * 0.25))
                    im.putalpha(alpha)
                    im.save(faded)
                src = faded
            _picture(s, src, (x + (cell - icon) // 2, top_icon, icon, icon), role="gl:section-icon")
    return s


def chart_slide(prs, title, subtitle, image, source, notes=""):
    """One chart: headline, chart title (the variables), bare chart, source."""
    s = _new(prs, L_SINGLE, notes)
    _fill(s, 14, title, "gl:title")
    _fill(s, 15, source, "gl:source")
    box = _take_box(s, 16)
    if subtitle:
        box = _subtitle(s, subtitle, box)
    _picture(s, image, box)
    return s


def charts_slide(prs, title, subtitle, images, source, notes=""):
    """Two to four charts of the same type, one shared chart title and source."""
    if not 2 <= len(images) <= 4:
        raise ValueError("charts_slide takes 2 to 4 images; use chart_slide for one")
    s = _new(prs, L_SINGLE, notes)
    _fill(s, 14, title, "gl:title")
    _fill(s, 15, source, "gl:source")
    box = _take_box(s, 16)
    if subtitle:
        box = _subtitle(s, subtitle, box)
    for cell, img in zip(_grid(box, len(images)), images):
        _picture(s, img, cell)
    return s


def chart_side_slide(prs, title, subtitle, image, side, source, notes=""):
    """One chart plus a short side text that says what the category IS.

    `side` defines the industry / group / product on the chart. It never reads
    the chart: no verdicts, no causes, no 'this shows'.
    """
    s = _new(prs, L_SIDE, notes)
    _fill(s, 14, title, "gl:title")
    _fill(s, 15, source, "gl:source")
    box = _take_box(s, 17)
    if subtitle:
        box = _subtitle(s, subtitle, box)
    _picture(s, image, box)
    side_box = _take_box(s, 18)
    _textbox(s, "gl:side", side, side_box, size=PT_SIDE, color=MUTED)
    return s


def table_slide(prs, title, subtitle, header, rows, source, *, col_widths=None,
                align=None, size=PT_TABLE, notes=""):
    """A native table (live text). col_widths in inches; align per column 'l'/'r'/'c'."""
    s = _new(prs, L_SINGLE, notes)
    _fill(s, 14, title, "gl:title")
    _fill(s, 15, source, "gl:source")
    left, top, width, height = _take_box(s, 16)
    if subtitle:
        left, top, width, height = _subtitle(s, subtitle, (left, top, width, height))
    n_rows, n_cols = len(rows) + 1, len(header)
    row_h = Inches(0.1 + size / 72 * 1.35)
    shape = s.shapes.add_table(n_rows, n_cols, left, top, width, row_h * n_rows)
    shape.name = "gl:table"
    tbl = shape.table
    if col_widths:
        scale = width / sum(Inches(w) for w in col_widths)
        for j, w in enumerate(col_widths):
            tbl.columns[j].width = int(Inches(w) * scale)
    al = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT, "c": PP_ALIGN.CENTER}
    for i in range(n_rows):
        tbl.rows[i].height = row_h
        for j in range(n_cols):
            cell = tbl.cell(i, j)
            cell.text = str(header[j] if i == 0 else rows[i - 1][j])
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = HEAD_FILL if i == 0 else (ZEBRA if i % 2 == 0 else WHITE)
            for p in cell.text_frame.paragraphs:
                p.alignment = al[(align or "l" * n_cols)[j]]
                p.font.size = Pt(max(size, PT_MIN))
                p.font.bold = i == 0
                p.font.color.rgb = WHITE if i == 0 else RGBColor(0x26, 0x26, 0x26)
    return s


def list_slide(prs, title, items, source="", *, subtitle="", columns=None, notes=""):
    """A list is the content. `items` are bullets; or `columns` = [(heading, [bullets]), ...]
    for two to four parallel lists (the old 'cards'). Keep bullets factual."""
    s = _new(prs, L_SINGLE, notes)
    _fill(s, 14, title, "gl:title")
    if source:
        _fill(s, 15, source, "gl:source")
    box = _take_box(s, 16)
    if subtitle:
        box = _subtitle(s, subtitle, box)
    if columns:
        for cell, (head, bullets) in zip(_grid(box, len(columns)), columns):
            l, t, w, h = cell
            _textbox(s, "gl:list-head", head, (l, t, w, Inches(0.5)), size=PT_LIST + 1,
                     bold=True, color=INK)
            _textbox(s, "gl:list", [f"•  {b}" for b in bullets],
                     (l, t + Inches(0.6), w, h - Inches(0.6)), size=PT_LIST, color=MUTED)
    else:
        _textbox(s, "gl:list", [f"•  {b}" for b in items], box, size=PT_LIST + 2, color=MUTED)
    _drop_empty(s)
    return s


def image_slide(prs, title, image, source, *, subtitle="", notes=""):
    """A photo, map or diagram image (not a data chart)."""
    s = chart_slide(prs, title, subtitle, image, source, notes)
    for sh in s.shapes:
        if sh.name == "gl:chart":
            sh.name = "gl:image"
    return s


def statement_slide(prs, text, notes=""):
    """Text is the content: one statement, a question, a transition."""
    s = _new(prs, L_STATEMENT, notes)
    _fill(s, 14, text, "gl:statement")
    return s


def closing_slide(prs, notes=""):
    return _new(prs, L_CLOSING, notes)
