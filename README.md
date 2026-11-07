# Filip — projekty

Osobní projekty Filipa Lněničky. Pracuje se tu s **Claude Code** — pravidla,
podle kterých se Claude chová, jsou v [`CLAUDE.md`](CLAUDE.md) a načítá si je sám.

## Projekty

| Projekt | O čem | Stav |
|---|---|---|
| [01 — Hotel reporter](projekty/01-hotel-reporter/README.md) | Streamlit appka na denní uzávěrku tržeb hotelu z exportu dokladů | probíhá |

Stavy: nápad · probíhá · pozastaveno · hotovo

## Struktura

```
CLAUDE.md                pravidla pro Clauda
projekty/<NN>-<popis>/   jeden projekt = jedna složka (README.md se stavem, poznamky.md, kod/)
procesy/                 osvědčené postupy k opakovanému použití
.claude/skills/          návody pro Clauda na opakovanou práci
```

## Co sem nepatří

Repo je **veřejné**.

| Nepatří sem | Patří to |
|---|---|
| hesla, klíče, tokeny, `.env` | správce hesel / proměnné prostředí |
| cokoliv z Webkompletu, Boldemu a stáže | `webkomplet-ai` |
| osobní údaje | nikam veřejně |
| videa, velké exporty, modely | `vystupy/` (ignorované gitem) nebo mimo repo |
