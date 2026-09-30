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

Every content slide has exactly three parts:

1. **Title** — the slide headline. One sentence. It may state what the slide shows ("Brasil importa
   USD 12.780 M al año de la lista"), because the deck is an argument, but it is the *only* place a
   reading may appear on the slide.
2. **Content** — exactly **one kind**: a chart, a table, a list, an image, or text. Never mix kinds:
   no chart plus bullets, no table plus a reading paragraph, no chart plus a callout box.
3. **Source** — one footnote line: `Fuente: …`, then the definitions a reader needs (units, what a code
   means). Black, small (≥ 11 pt), upright.

Rules on the content:

- **Charts: one per slide, ideally.** At most **four**, and only of the **same type** (four line charts
  of the same variable across groups, not a line + a bar). Several panels means one shared chart title
  and one source.
- **Every chart has a chart title in live text** right above it that **only names the variables and the
  period** — a journal-caption line: `Importaciones de Brasil (USD M) por partida HS6 y país de origen,
  promedio 2021-2023`. Never the finding.
- **If the chart shows a category, industry or group the audience may not know** ("OPEX 312B",
  "servicios compartidos", "CRO", "principios activos"), put a **side text** next to the chart that says
  **what the category is** — a definition, ≤ 45 words. It never says what the chart shows, why, or what
  follows.
- **Delete all other text inside the slide**: reading lines, "the point is…", callouts, bold takeaways,
  hypotheses, "what we still need to know" columns. Move them to the **speaker notes**.
- **Bare charts, live text.** The PNG on a slide carries no title, subtitle or caption; those are slide
  text. In R projects `gl_save()` writes the bare PNG and a `_text.md` sidecar (Título / Subtítulo /
  Fuente / Notas). Map them: sidecar **Título → chart title line**, **Fuente → source**, **Notas →
  speaker notes**; the Subtítulo joins the chart title line only if it names units or definitions,
  otherwise it goes to the notes. The slide headline is written for the deck, not taken from the chart.
- **Section dividers** between parts: a row of the deck's sections with the current one lit
  (`section_slide`). A reader always knows which part of the argument they are in.
- **Type floor 11 pt.** Never shrink text to fit — split the slide, cut rows, or move detail to notes.
- **On-slide language** follows the project (Spanish for Córdoba and other LATAM decks).

A **list** or **text** slide is fine when the content really is a list (the firms, the steps of a value
chain, the measures) — the grammar is about not mixing kinds, not about banning words. Parallel lists
(the old "cards") are one list slide with 2–4 columns.

## Tools

Everything is in this skill's folder (`~/.claude/skills/ppt-creator/`, versioned in research-to-policy):

| File | What |
|---|---|
| `assets/GL_presentation_template.potx` | The official Growth Lab template. Decks are built **on its layouts**, never on blank slides. |
| `scripts/gl_deck.py` | Builder: `new_deck()`, `title_slide`, `section_slide`, `chart_slide`, `charts_slide` (2–4), `chart_side_slide`, `table_slide`, `list_slide`, `image_slide`, `statement_slide`, `closing_slide`. Every shape it writes carries a role name (`gl:title`, `gl:chart`, …). |
| `scripts/check_deck.py` | Linter for the grammar. Runs on any .pptx (role-less decks are classified by position). Exit 1 on errors. |

Template layouts used: *Title Slide*, *Single Visual* (title · visual · source — chart, table, list,
image), *1_Two Visuals* (chart + side text), *Title + Blank* (section divider), *Statement Text*,
*Closing Slide*.

```python
import sys; sys.path.insert(0, str(Path.home() / ".claude/skills/ppt-creator/scripts"))
import gl_deck as D
prs = D.new_deck()
D.chart_slide(prs, "Brasil importa USD 12.780 M al año de la lista",
              "Importaciones de Brasil (USD M) por partida HS6 y país de origen, promedio 2021-2023",
              "output/x/deck_assets/l07_bare.png", "Fuente: UN Comtrade, 2021-2023. Evidencia #288.",
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
