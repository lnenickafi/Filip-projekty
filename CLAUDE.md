# Pravidla pro Claude — Filip-projekty

Tenhle soubor se načítá automaticky v každé session nad tímhle repozitářem.
Píše se pro Clauda. Vychází z pravidel firemního repa `webkomplet-ai`, ale je
upravený pro **osobní projekty, které si Filip dělá sám pro sebe**.

---

## S kým mluvíš

**Filip Lněnička.** Tykáme si. Česky, pokud si nevyžádá jiný jazyk.

- Repo je jeho osobní, **nikdo jiný do něj nepíše** a nikdo nic neschvaluje.
- GitHub účet tohohle repa: **`lnenickafi`**. Firemní účet
  `filip-lnenicka-wk` patří k `webkomplet-ai` a sem se nepoužívá.
- Pracuje v Claude Code na Windows (appka i terminál).
- Odpovědi stručně a k věci. Když bude chtít víc, řekne si.

## Režim práce

**Osobní režim: rychle, bez procesu.** Žádné pull requesty, žádné schvalování.

- **Commituje se a pushuje přímo do `main`.** Malé, srozumitelné commity —
  jeden commit = jedna logická změna.
- **Větev jen na větší pokus**, u kterého není jisté, že se povede
  (`pokus/<co>`). Když se povede, sloučí se do `main`, když ne, smaže se.
  Před smazáním větve se vždy zeptej.
- **Necommituj a nepushuj bez pokynu.** Změny připrav a řekni, co je hotové.
  „Ulož to“, „commitni“, „pushni“ = pokyn. Když Filip řekne, že u daného
  projektu má commitovat průběžně sám, platí to jen pro ten projekt.
- **Než začneš měnit soubory**, zkontroluj `git status`. Rozdělanou cizí
  práci (neuložené změny) nezahazuj — zeptej se.
- **Nic destruktivního bez ptaní:** `reset --hard`, `push --force`, mazání
  souborů a složek, přepis historie.

### Git: dva účty na tomhle PC

Repo je na tomhle PC napevno svázané s účtem `lnenickafi` (lokální
`credential.helper` v `.git/config`), takže `git push/pull` funguje bez
přepínání. Příkazy `gh` ale jedou pod **aktivním** účtem — pro tohle repo
je spouštěj takhle:

```
GH_TOKEN=$(gh auth token -u lnenickafi) gh <příkaz>
```

## Repo je VEŘEJNÉ

**Všechno, co se sem commitne, uvidí kdokoliv na internetu — i po smazání
zůstává v historii.** Proto:

- **Žádná hesla, klíče, tokeny, `.env`** — ani v příkladech, ani zakomentované.
  Tajné hodnoty patří do proměnných prostředí nebo správce hesel; v repu
  nanejvýš `.env.example` s prázdnými hodnotami.
- **Nic z Webkompletu ani Boldemu**, co není veřejné: interní postupy, data
  zákazníků, kód z firemních repozitářů, zadání ze stáže. Na stáž je
  `webkomplet-ai`.
- **Žádné osobní údaje** (svoje ani cizí) — adresy, telefony, rodná čísla,
  e-maily třetích osob, přihlašovací údaje.
- Velká data a binárky (videa, exporty, modely) do gitu nepatří — patří
  do `vystupy/` nebo mimo repo (`vystupy/` je v `.gitignore`).

Když si nejsi jistý, jestli něco smí ven, **zeptej se před commitem**.

## Struktura

```
CLAUDE.md                   tenhle soubor
README.md                   přehled projektů
projekty/<NN>-<popis>/      jeden projekt = jedna složka
procesy/                    postupy, které se osvědčily a dají se použít znovu
.claude/skills/             návody (skills) pro opakovanou práci
```

### Každý projekt má vlastní složku

```
projekty/<NN>-<popis>/
  README.md        o čem projekt je (2–3 věty) + Aktuální stav
  poznamky.md      postup, zádrhele, rozhodnutí (nejnovější nahoře)
  kod/             kód (když nějaký je)
```

- `NN` = další volné číslo se dvěma číslicemi (`01`, `02`, …), nikdy se
  nepřečíslovává ani nerecykluje.
- `popis` malými písmeny, bez diakritiky, pomlčky místo mezer.
- **Jeden projekt = jedna složka.** Nový nápad, který není pokračováním
  rozběhnutého projektu, je nový projekt.
- Projekt s vlastním ekosystémem (web, appka s `package.json` apod.) může
  mít uvnitř složky vlastní strukturu — `kod/` není povinný.

### Vždy aktualizuj README projektu

Kdo chce vědět, jak je projekt daleko, otevře jeho `README.md`.

- **Kdykoli se v projektu něco změní**, aktualizuj v jeho `README.md` sekci
  **Aktuální stav** a datum v jejím nadpisu — ve stejném commitu, ne „pak“.
- Stav = co je hotovo, na čem se pracuje, co zbývá, co blokuje. Pár řádků.
- Změní-li se stav (nápad / probíhá / hotovo / pozastaveno), přepiš ho
  i v tabulce projektů v kořenovém `README.md`.
- Chybí-li projektu `README.md`, založ ho podle vzoru níže.
- Před koncem práce zkontroluj, že README odpovídá tomu, co jsi udělal.
  Když ne, nejsi hotový.

Vzor `README.md` projektu:

```markdown
# NN — Název projektu

**Stav:** probíhá · **Založeno:** 2026-11-07

O čem projekt je a proč ho dělám — 2–3 věty.

## Aktuální stav (2026-11-07)

- Hotovo: …
- Teď: …
- Zbývá: …
- Blokuje: nic
```

## Jak se chovat, když něco nevíš

- **Zeptej se, nedomýšlej si.** Odhad, který vypadá jako fakt, je horší než
  otázka.
- **Neuváděj čísla bez zdroje** — ceny, verze, limity API: vždy odkud to je.
- **Netvrď, že něco funguje, dokud to není ověřené.** Rozlišuj: napsaný kód /
  spuštěný kód / otestovaný kód / nasazené.
- Když vyjde najevo něco, co se bude hodit i příště (nástroj, postup, zádrhel),
  **nabídni, že se to zapíše** — do `procesy/` nebo do tohohle souboru.

## Co nikdy

- **Neposílej nic za Filipa** — e-maily, zprávy, příspěvky. Připravíš,
  odeslání je na něm.
- **Nepublikuj ani nenasazuj bez pokynu** (deploy webu, zveřejnění balíčku,
  změna viditelnosti repa).
- **Neměň globální nastavení PC ani gitu** (`git config --global`, přihlášení
  `gh`) bez zeptání — sdílí ho s firemní prací.
- **Necommituj tajemství ani firemní věci** — viz „Repo je VEŘEJNÉ“.
