#!/usr/bin/env python3
# Script:   .claude/skills/ppt-creator/scripts/gl_deck.py (research-to-policy)
# Inputs:   ../assets/GL_presentation_template.potx
# Outputs:  none (library; the caller saves the Presentation)
# Seed:     none
# Env:      python3, python-pptx, Pillow; Liberation Sans or Arial TTFs for text measurement
#
# Growth Lab deck builder on the layouts of the official GL template. Every slide
# is one of a few grammars (see ../SKILL.md § Slide grammar): title, content,
# notes, source. The builder names each shape it writes with a role ("gl:title",
# "gl:chart", "gl:note", "gl:source", ...) so check_deck.py can verify the grammar
# afterwards without guessing.
#
# Format (AF, 30/09/2026, fixed for every deck): all text Arial; slide title 24 pt
# (up to two lines); chart title 14 pt bold, centred above the chart, up to two
# lines; Notas and Fuente 12 pt at the foot, Notas above Fuente; charts centred
# horizontally on the slide and vertically in the band between the title and the
# foot; no internal evidence references ("Evidencia #288") anywhere in the deck.
#
# The layout is measured, not guessed: text is wrapped with the real Arial
# metrics (Liberation Sans is metric-compatible), and each block is stacked
# under the previous one, so nothing overlaps and nothing spills into the footer.
#
# Usage:
#   import sys; sys.path.insert(0, "<skill>/scripts"); import gl_deck as D
#   prs = D.new_deck()
#   D.title_slide(prs, "Título", "Subtítulo", "Harvard Growth Lab | Septiembre 2026")
#   D.chart_slide(prs, "Titular de la lámina", "Variables (eje x) vs. variables (eje y), 2025",
#                 "output/x/deck_assets/x_bare.png", "Fuente: ...",
#                 note="OPEX 312B: grupo de ...", notes="Lectura para el orador")
#   prs.save("deck.pptx")

from __future__ import annotations

import io
import re
import tempfile
import zipfile
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / "assets" / "GL_presentation_template.potx"

# ── Format ───────────────────────────────────────────────────────────────
FONT = "Arial"
PT_MIN = 11          # floor for any text
PT_TITLE = 24        # slide headline
PT_CHART_TITLE = 14  # the line naming the variables, bold, centred over the content
PT_SOURCE = 12       # Fuente
PT_NOTE = 12         # Notas (what a category IS), above the Fuente
PT_LIST = 16
PT_TABLE = 12
PT_SECTION = 14
PT_STATEMENT = 32
TITLE_MAX_LINES = 2
CHART_TITLE_MAX_LINES = 2
NOTE_LABEL = "Notas: "

INK = RGBColor(0x14, 0x45, 0x62)      # GL navy, as in the template's title placeholders
TEXT = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x59, 0x59, 0x59)
FADED = RGBColor(0xBF, 0xBF, 0xBF)
RULE = RGBColor(0xD9, 0xD9, 0xD9)
HEAD_FILL = RGBColor(0x14, 0x45, 0x62)
ZEBRA = RGBColor(0xF2, 0xF4, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)

# Geometry of the GL template (inches). Content spans the template's margins;
# the navy footer band starts at FOOTER_TOP.
SLIDE_W, SLIDE_H = 13.333, 7.5
CONTENT_L, CONTENT_W = 0.47, 12.41
TITLE_TOP = 0.27
FOOTER_TOP = 6.91
FOOT_PAD = 0.12      # between the Fuente and the footer band
GAP = 0.14           # between stacked blocks
LINE = 1.2           # line height as a multiple of the point size

# Internal evidence references never reach a slide or its notes. The ids are
# collected per slide in REFS so a deck can write its own traceability file.
EVIDENCE_RE = re.compile(
    r"\s*\(?\b[Ee]videncias?\s*(?:n\.?\s*)?#\s*\d+(?:\s*(?:,|y|e|–|-|/)\s*#?\s*\d+)*\)?\.?")
REFS: dict[int, list[str]] = {}

# Layout names in the GL template (trailing spaces in the .potx are stripped).
L_TITLE = "Title Slide"
L_SINGLE = "Single Visual"
L_STATEMENT = "Statement Text"
L_TITLE_BLANK = "Title + Blank"
L_CLOSING = "Closing Slide"


# ── Text measurement ─────────────────────────────────────────────────────
_FONT_FILES = {
    False: ["LiberationSans-Regular.ttf", "Arial.ttf", "arial.ttf"],
    True: ["LiberationSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
}
_FONT_DIRS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/msttcorefonts",
              "/Library/Fonts", "/System/Library/Fonts/Supplemental", "C:/Windows/Fonts"]


@lru_cache(maxsize=None)
def _font(bold: bool):
    for d in _FONT_DIRS:
        for f in _FONT_FILES[bold]:
            p = Path(d) / f
            if p.exists():
                return ImageFont.truetype(str(p), 1000)
    raise FileNotFoundError("need Liberation Sans or Arial TTFs to measure text "
                            "(apt install fonts-liberation)")


def text_width(text: str, pt: float, bold=False) -> float:
    """Width of one line of Arial text, in inches."""
    return _font(bold).getlength(text) / 1000 * pt / 72


def wrap(text: str, pt: float, width_in: float, bold=False) -> list[str]:
    """Greedy word wrap with Arial metrics; paragraphs split on newlines."""
    out = []
    for par in str(text).split("\n"):
        words, line = par.split(), ""
        if not words:
            out.append("")
            continue
        for w in words:
            cand = f"{line} {w}".strip()
            if line and text_width(cand, pt, bold) > width_in:
                out.append(line)
                line = w
            else:
                line = cand
        out.append(line)
    return out


def n_lines(text, pt, width_in, bold=False) -> int:
    return len(wrap(text, pt, width_in, bold))


def line_h(pt) -> float:
    return LINE * pt / 72


def block_h(text, pt, width_in, bold=False, space_before_pt=0) -> float:
    """Height in inches of a wrapped text block (paragraph spacing included)."""
    pars = str(text).split("\n")
    return n_lines(text, pt, width_in, bold) * line_h(pt) + (len(pars) - 1) * space_before_pt / 72


def strip_refs(text: str, slide_no: int | None = None) -> str:
    """Remove "Evidencia #288, #292." style references; remember them in REFS."""
    if not text:
        return text
    if isinstance(text, (list, tuple)):
        text = "\n".join(str(t) for t in text)
    found = EVIDENCE_RE.findall(text)
    if found and slide_no is not None:
        REFS.setdefault(slide_no, []).extend(f.strip() for f in found)
    out = EVIDENCE_RE.sub("", text)
    return re.sub(r"[ \t]{2,}", " ", out).strip()


# ── Deck ────────────────────────────────────────────────────────────────
def new_deck(template: Path = TEMPLATE):
    """A Presentation on the GL template, with the template's sample slides removed.

    python-pptx refuses a .potx, so the main part's content type is rewritten
    to the .pptx one in memory; the theme's major and minor fonts are set to
    Arial so inherited text is Arial too. The template file is never modified.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(template) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(b"presentationml.template.main+xml",
                                    b"presentationml.presentation.main+xml")
            if re.match(r"ppt/theme/theme\d+\.xml", item.filename):
                data = re.sub(rb'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]*"',
                              rb'\1' + FONT.encode() + b'"', data)
            zout.writestr(item, data)
    buf.seek(0)
    prs = Presentation(buf)
    for sld_id in list(prs.slides._sldIdLst):
        prs.part.drop_rel(sld_id.rId)
        prs.slides._sldIdLst.remove(sld_id)
    REFS.clear()
    return prs


def _layout(prs, name):
    for lay in prs.slide_layouts:
        if lay.name.strip() == name:
            return lay
    raise KeyError(f"layout {name!r} not in template")


def _new(prs, layout_name, notes=""):
    slide = prs.slides.add_slide(_layout(prs, layout_name))
    n = len(prs.slides)
    slide._gl_no = n
    if notes:
        slide.notes_slide.notes_text_frame.text = strip_refs(notes, n)
    return slide


def _no(slide):
    """1-based position of the slide in its deck (set by _new)."""
    return getattr(slide, "_gl_no", None)


def _ph(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    raise KeyError(f"placeholder idx={idx} not on layout {slide.slide_layout.name!r}")


def _drop_ph(slide, idx):
    try:
        ph = _ph(slide, idx)
    except KeyError:
        return
    ph._element.getparent().remove(ph._element)


def _drop_empty(slide, keep=()):
    """Delete placeholders nobody filled, so no 'Click to add text' survives."""
    for ph in list(slide.placeholders):
        idx = ph.placeholder_format.idx
        if idx in keep:
            continue
        if ph.has_text_frame and not ph.text_frame.text.strip():
            ph._element.getparent().remove(ph._element)


def _style_frame(tf, *, size, bold=False, color=None, align=None, anchor=MSO_ANCHOR.TOP):
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for p in tf.paragraphs:
        if align is not None:
            p.alignment = align
        pPr = p._p.get_or_add_pPr()          # the template's body placeholders hang-indent
        pPr.set("marL", "0")
        pPr.set("indent", "0")
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(max(size, PT_MIN))
            r.font.bold = bold
            if color is not None:
                r.font.color.rgb = color


def arialize(slide):
    """Every run on the slide in Arial (placeholders, text boxes, tables, shapes)."""
    for sh in slide.shapes:
        frames = []
        if sh.has_text_frame:
            frames.append(sh.text_frame)
        if getattr(sh, "has_table", False) and sh.has_table:
            frames += [c.text_frame for row in sh.table.rows for c in row.cells]
        for tf in frames:
            for p in tf.paragraphs:
                for r in p.runs:
                    r.font.name = FONT


# ── Text primitives ──────────────────────────────────────────────────────
def _textbox(slide, role, text, box, *, size, color=MUTED, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_before=6, italic=False):
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
            p.space_before = Pt(space_before)
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(max(size, PT_MIN))
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
    return tb


def _in(x):
    return Inches(x)


def _frame(slide, title, source="", note="", *, title_idx=14, source_idx=15):
    """Title on top, Notas + Fuente at the foot, measured. Returns the free band
    (left, top, width, height) in EMU between them. Drops the layout's visual
    placeholders: content is placed by the caller inside the band.
    """
    n = _no(slide)
    title = strip_refs(title, n)
    ph = _ph(slide, title_idx)
    ph.name = "gl:title"
    ph.text = title
    t_lines = n_lines(title, PT_TITLE, CONTENT_W)
    if t_lines > TITLE_MAX_LINES:
        raise ValueError(f"slide title takes {t_lines} lines at {PT_TITLE} pt (max "
                         f"{TITLE_MAX_LINES}): «{title}»")
    t_h = t_lines * line_h(PT_TITLE)
    ph.left, ph.top, ph.width, ph.height = _in(CONTENT_L), _in(TITLE_TOP), _in(CONTENT_W), _in(t_h)
    _style_frame(ph.text_frame, size=PT_TITLE, color=INK, align=PP_ALIGN.LEFT)
    top = TITLE_TOP + t_h + GAP * 2

    bottom = FOOTER_TOP - FOOT_PAD
    source = strip_refs(source, n)
    if source:
        s_h = block_h(source, PT_SOURCE, CONTENT_W)
        sp = _ph(slide, source_idx)
        sp.name = "gl:source"
        sp.text = source
        sp.left, sp.top, sp.width, sp.height = (_in(CONTENT_L), _in(bottom - s_h),
                                                _in(CONTENT_W), _in(s_h))
        _style_frame(sp.text_frame, size=PT_SOURCE, color=BLACK, align=PP_ALIGN.LEFT,
                     anchor=MSO_ANCHOR.BOTTOM)
        for p in sp.text_frame.paragraphs:
            for r in p.runs:
                r.font.italic = False
        bottom -= s_h + GAP / 2
    else:
        _drop_ph(slide, source_idx)
    note = strip_refs(note, n)
    if note:
        if not note.lower().startswith("nota"):
            note = NOTE_LABEL + note
        n_h = block_h(note, PT_NOTE, CONTENT_W)
        _textbox(slide, "gl:note", note, (_in(CONTENT_L), _in(bottom - n_h), _in(CONTENT_W),
                                          _in(n_h)),
                 size=PT_NOTE, color=BLACK, anchor=MSO_ANCHOR.BOTTOM, space_before=0)
        bottom -= n_h + GAP / 2
    bottom -= GAP
    if bottom - top < 1.5:
        raise ValueError(f"no room left for content ({bottom - top:.2f} in) under «{title[:50]}»: "
                         "shorten the title, notes or source")
    return (_in(CONTENT_L), _in(top), _in(CONTENT_W), _in(bottom - top))


def _chart_title(slide, text, width_in=CONTENT_W):
    """The line naming the variables: 14 pt bold, centred. Returns its height (in)."""
    lines = n_lines(text, PT_CHART_TITLE, width_in, bold=True)
    if lines > CHART_TITLE_MAX_LINES:
        raise ValueError(f"chart title takes {lines} lines at {PT_CHART_TITLE} pt bold (max "
                         f"{CHART_TITLE_MAX_LINES}): «{text}»")
    return lines * line_h(PT_CHART_TITLE)


def _put_chart_title(slide, text, top_in, h_in, width_in=CONTENT_W):
    left = (SLIDE_W - width_in) / 2
    return _textbox(slide, "gl:subtitle", text, (_in(left), _in(top_in), _in(width_in), _in(h_in)),
                    size=PT_CHART_TITLE, color=TEXT, bold=True, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.BOTTOM, space_before=0)


def _img_size(path):
    with Image.open(path) as im:
        return im.size


def _place_visuals(slide, band, subtitle, images, role="gl:chart", gap_in=0.2):
    """Chart title + 1-4 images as one group, centred horizontally on the slide and
    vertically in the band. Grid: 1, 2 side by side, 3 in a row, 4 as 2x2."""
    left, top, width, height = (Emu(v).inches for v in band)
    ct_h = _chart_title(slide, subtitle) if subtitle else 0.0
    avail_h = height - (ct_h + GAP if subtitle else 0)
    n = len(images)
    cols, rows = {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (2, 2)}[n]
    cell_w = (width - gap_in * (cols - 1)) / cols
    cell_h = (avail_h - gap_in * (rows - 1)) / rows
    sizes = [_img_size(p) for p in images]
    # one scale for all panels so same-type charts read at the same size
    scale = min(min(cell_w / w, cell_h / h) for w, h in sizes)
    dims = [(w * scale, h * scale) for w, h in sizes]
    grid_w = max(d[0] for d in dims) * cols + gap_in * (cols - 1)
    grid_h = max(d[1] for d in dims) * rows + gap_in * (rows - 1)
    group_h = (ct_h + GAP if subtitle else 0) + grid_h
    y0 = top + (height - group_h) / 2
    if subtitle:
        _put_chart_title(slide, subtitle, y0, ct_h)
        y0 += ct_h + GAP
    x0 = (SLIDE_W - grid_w) / 2
    cw, ch = max(d[0] for d in dims), max(d[1] for d in dims)
    pics = []
    for k, (path, (w, h)) in enumerate(zip(images, dims)):
        r, c = divmod(k, cols)
        cx = x0 + c * (cw + gap_in) + (cw - w) / 2
        cy = y0 + r * (ch + gap_in) + (ch - h) / 2
        pic = slide.shapes.add_picture(str(path), _in(cx), _in(cy), _in(w), _in(h))
        pic.name = role
        pics.append(pic)
    return pics


def _top_subtitle(slide, band, subtitle):
    """Chart-title line at the top of the band (tables, lists); returns the rest."""
    if not subtitle:
        return band
    left, top, width, height = (Emu(v).inches for v in band)
    h = _chart_title(slide, subtitle)
    _put_chart_title(slide, subtitle, top, h)
    return (_in(left), _in(top + h + GAP), _in(width), _in(height - h - GAP))


def _grid(box, n, gap=Inches(0.2)):
    """Split a box into n cells: 1, 2 side by side, 3 in a row, 4 as 2x2."""
    left, top, width, height = box
    cols, rows = {1: (1, 1), 2: (2, 1), 3: (3, 1), 4: (2, 2)}[n]
    cw = (width - gap * (cols - 1)) // cols
    rh = (height - gap * (rows - 1)) // rows
    return [(left + c * (cw + gap), top + r * (rh + gap), cw, rh)
            for r in range(rows) for c in range(cols)][:n]


def _content_slide(prs, title, source, note, notes):
    s = _new(prs, L_SINGLE, notes)
    band = _frame(s, title, source, note)
    _drop_ph(s, 16)
    return s, band


# ── Slide grammars ───────────────────────────────────────────────────────
def title_slide(prs, title, subtitle="", metadata="", notes=""):
    s = _new(prs, L_TITLE, notes)
    for idx, text, role in ((0, title, "gl:title"), (10, subtitle, "gl:subtitle"),
                            (11, metadata, "gl:meta")):
        if text:
            ph = _ph(s, idx)
            ph.text = text
            ph.name = role
    _drop_empty(s)
    arialize(s)
    return s


def section_slide(prs, heading, items, current, notes="", subgroups=None):
    """Section divider: a row of the deck's sections with the current one lit.

    items: list of (label, icon_path or None). The others are drawn faded, as
    in the Córdoba ministers' deck.
    subgroups: optional list of labels (2-6) drawn as boxes under the row, each
    reached by an arrow from the lit icon — the sub-topics of the current section.
    """
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    from pptx.oxml.ns import qn

    s = _new(prs, L_TITLE_BLANK, notes)
    ph = _ph(s, 14)
    ph.text = heading
    ph.name = "gl:title"
    _style_frame(ph.text_frame, size=PT_TITLE, color=INK)
    n = len(items)
    area_l, area_w = Inches(CONTENT_L), Inches(CONTENT_W)
    cell = area_w // n
    icon = Inches(1.1)
    shift = Inches(-0.6) if subgroups else 0
    top_icon, top_label = Inches(2.9) + shift, Inches(2.1) + shift
    tmp = Path(tempfile.mkdtemp())
    lit_center = None
    for i, (label, icon_path) in enumerate(items):
        lit = i == current
        x = area_l + i * cell
        _textbox(s, "gl:section-label", label, (x, top_label, cell, Inches(0.7)),
                 size=PT_SECTION, bold=lit, color=INK if lit else FADED,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        if lit:
            lit_center = x + cell // 2
        if icon_path:
            src = Path(icon_path)
            if not lit:
                faded = tmp / f"faded_{i}{src.suffix or '.png'}"
                with Image.open(src).convert("RGBA") as im:
                    alpha = im.getchannel("A").point(lambda a: int(a * 0.25))
                    im.putalpha(alpha)
                    im.save(faded)
                src = faded
            left, top = x + (cell - icon) // 2, top_icon
            pic = s.shapes.add_picture(str(src), left, top, icon, icon)
            pic.name = "gl:section-icon"
    if subgroups:
        k = len(subgroups)
        if not 2 <= k <= 6:
            raise ValueError("section_slide takes 2 to 6 subgroups")
        box_top, box_h, gap = Inches(5.0), Inches(0.9), Inches(0.2)
        box_w = (area_w - gap * (k - 1)) // k
        start_y = top_icon + icon + Inches(0.1)
        for j, lab in enumerate(subgroups):
            bx = area_l + j * (box_w + gap)
            box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, box_top, box_w, box_h)
            box.name = "gl:section-sub"
            box.adjustments[0] = 0.12
            box.fill.solid()
            box.fill.fore_color.rgb = WHITE
            box.line.color.rgb = INK
            box.line.width = Pt(1.25)
            box.shadow.inherit = False
            tf = box.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = Inches(0.08)
            tf.paragraphs[0].text = lab
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            for r in tf.paragraphs[0].runs:
                r.font.name, r.font.size, r.font.bold = FONT, Pt(PT_SECTION), True
                r.font.color.rgb = INK
            arrow = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, lit_center, start_y,
                                           bx + box_w // 2, box_top - Inches(0.05))
            arrow.name = "gl:section-arrow"
            arrow.line.color.rgb = INK
            arrow.line.width = Pt(1.5)
            ln = arrow.line._get_or_add_ln()
            tail = ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"})
            ln.append(tail)
    arialize(s)
    return s


def chart_slide(prs, title, subtitle, image, source, notes="", *, note=""):
    """One chart: headline, chart title (the variables), bare chart centred, Notas, Fuente."""
    s, band = _content_slide(prs, title, source, note, notes)
    _place_visuals(s, band, subtitle, [image])
    arialize(s)
    return s


def charts_slide(prs, title, subtitle, images, source, notes="", *, note=""):
    """Two to four charts of the same type, one shared chart title, Notas and Fuente."""
    if not 2 <= len(images) <= 4:
        raise ValueError("charts_slide takes 2 to 4 images; use chart_slide for one")
    s, band = _content_slide(prs, title, source, note, notes)
    _place_visuals(s, band, subtitle, list(images))
    arialize(s)
    return s


def chart_side_slide(prs, title, subtitle, image, side, source, notes=""):
    """Kept for existing decks: the text that says what the category IS now goes
    in the Notas line above the Fuente, and the chart is centred like any other."""
    return chart_slide(prs, title, subtitle, image, source, notes, note=side)


def fit_table_rows(slide, size=PT_TABLE, line=LINE):
    """Grow each row of the slide's gl:table to the lines its longest cell needs,
    measured with Arial metrics. Renderers that do not auto-grow rows (LibreOffice,
    PDF export) would otherwise draw wrapped text over the next row. Returns the
    table's height in inches. table_slide() calls it; call it again after editing
    cells by hand. (First version by W6, Córdoba ministers' deck v2, 30/09/2026.)
    """
    shape = next(sh for sh in slide.shapes if sh.name == "gl:table")
    tbl = shape.table
    total = 0
    for i, row in enumerate(tbl.rows):
        need = 1
        for j, cell in enumerate(row.cells):
            usable = Emu(tbl.columns[j].width).inches - 0.12
            need = max(need, n_lines(cell.text, size, usable, bold=(i == 0)))
        h = _in(need * line * size / 72 + 0.08)
        row.height = h
        total += h
    shape.height = total
    return Emu(total).inches


def table_slide(prs, title, subtitle, header, rows, source, *, col_widths=None,
                align=None, size=PT_TABLE, notes="", note=""):
    """A native table (live text). col_widths in inches (relative); align per column 'l'/'r'/'c'."""
    s, band = _content_slide(prs, title, source, note, notes)
    left, top, width, height = _top_subtitle(s, band, subtitle)
    n = _no(s)
    n_rows, n_cols = len(rows) + 1, len(header)
    shape = s.shapes.add_table(n_rows, n_cols, left, top, width, _in(0.3) * n_rows)
    shape.name = "gl:table"
    tbl = shape.table
    if col_widths:
        scale = width / sum(Inches(w) for w in col_widths)
        for j, w in enumerate(col_widths):
            tbl.columns[j].width = int(Inches(w) * scale)
    al = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT, "c": PP_ALIGN.CENTER}
    for i in range(n_rows):
        for j in range(n_cols):
            cell = tbl.cell(i, j)
            cell.text = strip_refs(str(header[j] if i == 0 else rows[i - 1][j]), n)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = HEAD_FILL if i == 0 else (ZEBRA if i % 2 == 0 else WHITE)
            for p in cell.text_frame.paragraphs:
                p.alignment = al[(align or "l" * n_cols)[j]]
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(max(size, PT_MIN))
                    r.font.bold = i == 0
                    r.font.color.rgb = WHITE if i == 0 else TEXT
    h = fit_table_rows(s, size)
    if h > Emu(height).inches + 0.05:
        raise ValueError(f"table is {h:.2f} in tall, {Emu(height).inches:.2f} in available under "
                         f"«{title[:50]}»: cut rows, split the slide or move columns to notes")
    arialize(s)
    return s


def list_slide(prs, title, items, source="", *, subtitle="", columns=None, notes="", note=""):
    """A list is the content. `items` are bullets; or `columns` = [(heading, [bullets]), ...]
    for two to four parallel lists (the old 'cards'). Keep bullets factual."""
    s, band = _content_slide(prs, title, source, note, notes)
    box = _top_subtitle(s, band, subtitle)
    if columns:
        for cell, (head, bullets) in zip(_grid(box, len(columns)), columns):
            l, t, w, h = cell
            _textbox(s, "gl:list-head", head, (l, t, w, Inches(0.5)), size=PT_LIST + 1,
                     bold=True, color=INK)
            _textbox(s, "gl:list", [f"•  {b}" for b in bullets],
                     (l, t + Inches(0.6), w, h - Inches(0.6)), size=PT_LIST, color=MUTED)
    else:
        _textbox(s, "gl:list", [f"•  {b}" for b in items], box, size=PT_LIST + 2, color=MUTED)
    arialize(s)
    return s


def _hex(color):
    if isinstance(color, RGBColor):
        return color
    return RGBColor.from_string(str(color).lstrip("#"))


def icon_list_slide(prs, title, columns, source, *, subtitle="", notes="", note=""):
    """Parallel lists whose items carry an icon: a coloured header band per column
    and one card per item (icon + label, optional sub-bullets). Same grammar as
    `list_slide(columns=...)` (the content is a list), for when the icons are part
    of how the audience recognises the list — e.g. an earlier deck's slide rebuilt
    natively. Added 30/09/2026 for the Córdoba ministers' «Tres vías» slide.

    columns: [{"heading": str, "lead": str (optional, italic under the heading),
               "color": "#RRGGBB" or RGBColor (optional, default INK),
               "items": [(icon_path or None, label, [sub-bullets]), ...]}, ...]
    Two to four columns. Card heights follow the item with most sub-bullets; rows
    line up across columns while every column has the same number of plain items.
    """
    from pptx.enum.shapes import MSO_SHAPE

    if not 2 <= len(columns) <= 4:
        raise ValueError("icon_list_slide takes 2 to 4 columns")
    s, band = _content_slide(prs, title, source, note, notes)
    left, top, width, height = _top_subtitle(s, band, subtitle)
    gap = Inches(0.3)
    cw = (width - gap * (len(columns) - 1)) // len(columns)
    head_h, card_gap = Inches(0.78), Inches(0.14)
    # one weight unit = one plain card; a sub-bullet adds 0.3 of a card
    weights = [[1 + 0.3 * len(it[2] if len(it) > 2 else []) for it in col["items"]]
               for col in columns]
    units = max(max(sum(w), len(w)) for w in weights)
    avail = height - head_h - Inches(0.15)
    unit = (avail - card_gap * (max(len(w) for w in weights) - 1)) / units
    for c, col in enumerate(columns):
        x = left + c * (cw + gap)
        color = _hex(col.get("color", INK))
        band_ = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top, cw, head_h)
        band_.name = "gl:list-head"
        band_.adjustments[0] = 0.06
        band_.fill.solid()
        band_.fill.fore_color.rgb = color
        band_.line.fill.background()
        band_.shadow.inherit = False
        tf = band_.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.18)
        p = tf.paragraphs[0]
        p.text = col["heading"]
        p.alignment = PP_ALIGN.LEFT
        p.font.size, p.font.bold, p.font.color.rgb = Pt(PT_LIST + 3), True, WHITE
        if col.get("lead"):
            q = tf.add_paragraph()
            q.text = col["lead"]
            q.alignment = PP_ALIGN.LEFT
            q.font.size, q.font.italic, q.font.color.rgb = Pt(PT_MIN + 2), True, WHITE
        y = top + head_h + Inches(0.15)
        for it, w in zip(col["items"], weights[c]):
            icon, label = it[0], it[1]
            subs = it[2] if len(it) > 2 else []
            h = int(unit * w)
            card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, h)
            card.name = "gl:list"
            card.adjustments[0] = 0.05
            card.fill.solid()
            card.fill.fore_color.rgb = WHITE
            card.line.color.rgb = RULE
            card.line.width = Pt(1)
            card.shadow.inherit = False
            icon_w = Inches(0.42)
            pad = Inches(0.2)
            tf = card.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.TOP if subs else MSO_ANCHOR.MIDDLE
            tf.margin_left = pad + (icon_w + Inches(0.18) if icon else 0)
            tf.margin_right = Inches(0.12)
            tf.margin_top = Inches(0.14) if subs else Inches(0.06)
            tf.margin_bottom = Inches(0.06)
            p = tf.paragraphs[0]
            p.text = label
            p.alignment = PP_ALIGN.LEFT
            p.font.size, p.font.bold = Pt(PT_LIST), True
            p.font.color.rgb = TEXT
            for sub in subs:
                q = tf.add_paragraph()
                q.text = f"•  {sub}"
                q.alignment = PP_ALIGN.LEFT
                q.font.size, q.font.color.rgb = Pt(PT_MIN + 3), MUTED
                q.space_before = Pt(2)
            if icon:
                icon_top = y + (h - icon_w) // 2 if not subs else y + Inches(0.14)
                pic = s.shapes.add_picture(str(icon), x + pad, icon_top, icon_w, icon_w)
                pic.name = "gl:list-icon"
            y += h + card_gap
    arialize(s)
    return s


def image_slide(prs, title, image, source, *, subtitle="", notes="", note=""):
    """A photo, map or diagram image (not a data chart), centred like a chart."""
    s, band = _content_slide(prs, title, source, note, notes)
    _place_visuals(s, band, subtitle, [image], role="gl:image")
    arialize(s)
    return s


def statement_slide(prs, text, notes=""):
    """Text is the content: one statement, a question, a transition."""
    s = _new(prs, L_STATEMENT, notes)
    ph = _ph(s, 14)
    ph.text = text
    ph.name = "gl:statement"
    arialize(s)
    return s


def questions_slide(prs, questions, current=None, notes=""):
    """Two to four questions side by side (the deck's guiding questions). With
    `current`, that one is dark and the others faded — the part of the argument
    the audience is in; without it, all are dark."""
    if not 2 <= len(questions) <= 4:
        raise ValueError("questions_slide takes 2 to 4 questions")
    s = _new(prs, L_STATEMENT, notes)
    _drop_ph(s, 14)
    k = len(questions)
    gap = 0.6
    w = (CONTENT_W - 1.6 - gap * (k - 1)) / k
    x0 = CONTENT_L + 0.8
    heights = [block_h(q, PT_STATEMENT, w) for q in questions]
    h = max(heights)
    top = (FOOTER_TOP - h) / 2
    for i, q in enumerate(questions):
        color = TEXT if current is None or i == current else FADED
        _textbox(s, "gl:statement", q, (_in(x0 + i * (w + gap)), _in(top), _in(w), _in(h)),
                 size=PT_STATEMENT, color=color, bold=(current is not None and i == current))
    arialize(s)
    return s


def closing_slide(prs, notes=""):
    s = _new(prs, L_CLOSING, notes)
    arialize(s)
    return s
