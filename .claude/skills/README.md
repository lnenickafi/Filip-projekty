# Návody pro Claude (skills)

**Zatím prázdné.** Návod má vzniknout, až se **ta samá práce udělá ručně
podruhé nebo potřetí stejně** — dřív nemá cenu ho vymýšlet.

## Struktura — na hloubce záleží

```
.claude/skills/<nazev>/SKILL.md
```

**Přesně jedna úroveň.** `.claude/skills/neco/<nazev>/SKILL.md` Claude Code
nenajde. Název plochý, malými písmeny, pomlčky: `strih-videa`, ne `video/strih`.

## Jak napsat nový

1. Složka s `SKILL.md`, v hlavičce `name` a `description`.
2. **`description` je nejdůležitější řádek** — podle něj se Claude rozhoduje,
   kdy návod použít. Piš do něj, *kdy* ho použít a jakými slovy o tom mluvíš.
3. Vyvolá se jménem (`/nazev`) nebo si ho Claude vezme sám, když se hodí.
4. Nový návod se načte až v nové session.

## Pravidla pro všechny návody

- **Nic neodesílat ani nepublikovat** — návod připraví, Filip pošle.
- **Nevymýšlet** — když chybí kontext, zeptat se.
- **Žádná tajemství** — repo je veřejné.
