# Methods index

One file per methodological object. Each merges what earlier r2p versions split
across `decisions/` (why), `methods/` (the rule) and `learnings/` (the traps).

| Topic | Title | v1 records merged |
|---|---|--:|
| [`EXAMPLE_topic`](EXAMPLE_topic.md) | <what the rule governs> | — |
| [`_craft`](_craft.md) | Cross-cutting numerical and reasoning traps | — |

`triggers:` frontmatter in each file is the pull index: grep it with
`grep -il '^triggers:.*<keyword>' research/methods/*.md` before assuming a
topic is undocumented. Nothing pushes these docs into context.
Source-specific gotchas live with the source in `research/sources/`, not here.

**Sizing:** 20–35 topic files is normal for a multi-theme 6-month engagement.
Past ~40, check whether topics are being split at evidence granularity.
