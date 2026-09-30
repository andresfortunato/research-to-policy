---
name: ppt-creator
description: >
  Build Growth Lab PowerPoint decks from analysis outputs (charts, tables, notes) on the official GL
  template, with a fixed slide grammar — title, one kind of content, source — and a linter that enforces
  it. Use whenever the user asks to create a presentation, build or rebuild a slide deck, make a
  PowerPoint, turn analysis into slides, reformat an existing deck, or prepare a briefing ("make this
  into a deck", "slides for the meeting", "put this in PowerPoint", "reformat the ppt", "present this").
  Also use when resolving review comments on a deck, or when checking whether a deck follows the format.
---

# PPT Creator (Growth Lab)

A deck is an argument read one slide at a time. Every slide carries **one piece of evidence** and says
where it comes from. Nothing on the slide interprets the evidence for the audience: the reading is the
presenter's job, and it lives in the speaker notes.

Reference deck that gets this right: `~/research/city_diagnostics/deliverables/decks/20260923_rio_growth_challenge/`
(headline, chart title, bare chart, source — and nothing else).

## Slide grammar — the non-negotiables

Every content slide has exactly these parts, top to bottom:

1. **Title** — the slide headline. One sentence, **up to two lines**. It may state what the slide shows
   ("Brasil importa USD 12.780 M al año de la lista"), because the deck is an argument, but it is the
   *only* place a reading may appear on the slide.
2. **Content** — exactly **one kind**: a chart, a table, a list, an image, or text. Never mix kinds:
   no chart plus bullets, no table plus a reading paragraph, no chart plus a callout box.
3. **Notas** (only when needed) — the line that says **what a category IS** ("OPEX 312B: …",
   "Servicios compartidos: …", "DIE: derecho de importación extrazona …"), right above the source.
4. **Source** — `Fuente: …`, then the units a reader needs. Black, upright.

### Format — fixed for every deck (AF, 30/09/2026)

| Element | Rule |
|---|---|
| Font | **Arial, all text** (the builder also sets the theme's fonts to Arial) |
| Slide title | **24 pt**, navy, left, up to 2 lines |
| Chart title (the line naming the variables) | **14 pt bold**, **centred over the chart**, centred paragraph, up to 2 lines |
| Chart / image | **centred on the slide**: horizontally on the slide's centre, vertically in the band between the title and the Notas/Fuente block. Chart title and chart move as one group |
| Notas | **12 pt**, starts with «Notas:», **above the Fuente** |
| Fuente | **12 pt**, black, at the foot, above the footer band |
| References | **no internal evidence references** («Evidencia #288») on slides or in the speaker notes. The builder strips them and keeps them in `REFS`, so a deck can write a slide → evidence traceability file |
| Floor | nothing under 11 pt; never shrink text to fit — split the slide, cut rows, or move detail to notes |

The builder measures text with real Arial metrics (Liberation Sans is metric-compatible) and stacks the
blocks, so nothing overlaps and nothing reaches the footer. A title, chart title or table that does not
fit **raises an error** instead of spilling: shorten it, split the slide, or move detail to the notes.

Rules on the content:

- **Charts: one per slide, ideally.** At most **four**, and only of the **same type** (four line charts
  of the same variable across groups, not a line + a bar). Several panels means one shared chart title,
  one scale, one source.
- **Every chart has a chart title in live text** right above it that **only names the variables and the
  period** — a journal-caption line: `Importaciones de Brasil (USD M) por partida HS6 y país de origen,
  promedio 2021-2023`. Never the finding.
- **If the slide shows a category, industry, group or code the audience may not know** ("OPEX 312B",
  "servicios compartidos", "CRO", "principios activos", "DIE"), say **what it is** in the **Notas** line
  (`note=`) — a definition, ≤ 45 words. It never says what the chart shows, why, or what follows. (The
  v2 side-text column is gone: `chart_side_slide` still exists and routes its text to Notas.)
- **Delete all other text inside the slide**: reading lines, "the point is…", callouts, bold takeaways,
  hypotheses, "what we still need to know" columns. Move them to the **speaker notes**.
- **Bare charts, live text.** The PNG on a slide carries no title, subtitle or caption; those are slide
  text. In R projects `gl_save()` writes the bare PNG and a `_text.md` sidecar (Título / Subtítulo /
  Fuente / Notas). Map them: sidecar **Título → chart title line**, **Fuente → source**, **Notas →
  speaker notes**; the Subtítulo goes to the Notas line if it defines a category, to the chart title
  line if it only adds units, otherwise to the speaker notes. The slide headline is written for the
  deck, not taken from the chart.
- **Section dividers** between parts: a row of the deck's sections with the current one lit
  (`section_slide`). A reader always knows which part of the argument they are in. When a section has
  sub-topics, pass `subgroups=[...]`: arrows from the lit icon to one box per sub-topic.
- **Guiding questions** (the deck's parts as questions): `questions_slide(questions, current=i)` puts
  them side by side, the current one dark and the rest faded.
- **On-slide language** follows the project (Spanish for Córdoba and other LATAM decks).

A **list** or **text** slide is fine when the content really is a list (the firms, the steps of a value
chain, the measures) — the grammar is about not mixing kinds, not about banning words. Parallel lists
(the old "cards") are one list slide with 2–4 columns.

## Tools

Everything is in this skill's folder (`~/.claude/skills/ppt-creator/`, versioned in research-to-policy):

| File | What |
|---|---|
| `assets/GL_presentation_template.potx` | The official Growth Lab template. Decks are built **on its layouts**, never on blank slides. |
| `scripts/gl_deck.py` | Builder: `new_deck()`, `title_slide`, `section_slide` (with `subgroups=`), `questions_slide`, `chart_slide`, `charts_slide` (2–4), `table_slide` (rows auto-fit), `list_slide`, `icon_list_slide`, `image_slide`, `statement_slide`, `closing_slide`; content slides take `note=` for the Notas line. `chart_side_slide` is kept for old decks. Every shape it writes carries a role name (`gl:title`, `gl:chart`, `gl:note`, …). |
| `scripts/check_deck.py` | Linter for the grammar and the fixed format (font, sizes, centring, references), plus measured overflow, overlap and footer checks. Runs on any .pptx (role-less decks are classified by position; the format checks apply to builder-made slides). Exit 1 on errors. |

Template layouts used: *Title Slide*, *Single Visual* (every content slide: the builder places title,
content, Notas and Fuente itself), *Title + Blank* (section divider), *Statement Text* (statements and
guiding questions), *Closing Slide*.

```python
import sys; sys.path.insert(0, str(Path.home() / ".claude/skills/ppt-creator/scripts"))
import gl_deck as D
prs = D.new_deck()
D.chart_slide(prs, "Brasil importa USD 12.780 M al año de la lista",
              "Importaciones de Brasil (USD M) por partida HS6 y país de origen, promedio 2021-2023",
              "output/x/deck_assets/l07_bare.png", "Fuente: UN Comtrade, 2021-2023.",
              note="Lista: las 46 moléculas de volumen comercial relevante del reporte final.",
              notes="Lectura: China e India proveen el 68% del glifosato ...")
prs.save("deck.pptx")
```

Run with `uv run --with python-pptx --with pillow python build_deck.py`.

## Workflow

1. **Storyline first.** Write the sequence of slide headlines and section breaks before touching code.
   Read them in order: they should tell the whole argument. Each slide = one piece of evidence.
2. **Specs as data, one module per section.** The deck's `build_deck.py` imports `sections/NN_<slug>.py`
   modules, each exporting a list of slide specs, and assembles them in order. This is what lets several
   agents work on different sections in parallel without editing the same file.
3. **Charts come from the analysis pipeline** (bare PNG + sidecar). If a slide needs a chart that does
   not exist, make it in the project's chart system, not in the deck builder.
4. **Resolving review comments** (pptx comments live in `ppt/comments/*.xml`): extract them per slide,
   classify each as *format* (mechanical), *rework* (new chart / split slide / new table) or *research*
   (a fact must be checked before the slide can exist), and plan them in that order.
5. **Verify** — both are required before calling a deck done:
   - `python3 scripts/check_deck.py deck.pptx` → **0 errors**. Warnings (several charts on a slide, a long
     side text) need a reason.
   - Render and look: `soffice --headless --convert-to pdf deck.pptx && pdftoppm -r 50 -png deck.pdf s &&
     montage s-*.png -tile 4x -geometry +4+4 sheet.png`, then read the contact sheet. Check overflow,
     cut-off tables, charts too small to read.

## Anti-patterns (seen in real drafts)

- A bold "reading" line under the chart restating the headline with more numbers → speaker notes.
- Chart on the left, three bullets of interpretation on the right → chart slide + notes; if the bullets
  define the category, they become a ≤ 45-word side text.
- Three panels from three sources with different definitions on one slide → pick one.
- A table of 25 rows at 9 pt → two slides, or the top rows + the rest in an appendix.
- A card column "Lo que falta saber" → the team's to-do list, not the audience's; delete.
- Blank-layout slides with hand-drawn footers → build on the template layouts.
- "Evidencia #288" at the end of a source line → internal bookkeeping, not for the audience; keep it
  in the deck's traceability file (the builder collects it in `REFS`).
- A definition column beside the chart → the Notas line above the Fuente, and the chart centred.
