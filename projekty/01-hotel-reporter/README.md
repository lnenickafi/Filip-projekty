# 01 — Hotel reporter

**Stav:** probíhá · **Vzniklo:** 2026-04-17 · **Převzato sem:** 2026-11-07

Webová appka ve Streamlitu na denní uzávěrku tržeb hotelu. Nahraje se export
dokladů z hotelového systému (`.xlsx`) a appka z něj vyrobí Excel report
s doklady od 10:00 prvního dne do 12:00 dalšího dne a se součty plateb
hotově a kartou.

- Kód: [`kod/app.py`](kod/app.py), závislosti v [`kod/requirements.txt`](kod/requirements.txt)
- Původní repo `lnenickafi/hotel-reporter` je od 2026-11-07 **soukromé
  a archivované** (jen pro čtení). Převzat stav z commitu `993ffec`,
  historie zůstala tam. **Vyvíjí se už jen tady.**

## Aktuální stav (2026-11-07)

- Hotovo: kód převzatý sem, původní repo archivované. Přepracováno:
  - bere **přímo export `.xls` z hotelového systému** (bez ručního otevírání,
    povolování úprav a převodu na `.xlsx`),
  - sloupce podle přesných názvů — opravena chyba, kdy se do sloupce Číslo
    dostávalo PR + **číslo rezervace** místo PR + variabilní symbol,
  - Číslo jako hotový text `PR<variabilní symbol>`, porovnané s exportem,
  - den uzávěrky se předvyplní podle posledního dokladu (jde změnit),
    soubor se jmenuje číslem dne (`6.xlsx`),
  - před stažením přehled: počet dokladů, součty a upozornění,
  - tabulka všech dokladů se zaškrtávátky — doklady jde ručně odebrat
    nebo přidat i ty mimo rozsah (součty i report se přepočítají),
  - tabulka v reportu má tenké ohraničení.
- Ověřeno: export z 6.–7. 11. dává výstup shodný s ručně připraveným
  `6.xlsx` (0 rozdílů v buňkách); hraniční případ „jen tržby 6. večer“ → `6.xlsx`.
- Teď: Filip zkouší appku lokálně, pak push a napojení Streamlit Cloudu
  (main file: `projekty/01-hotel-reporter/kod/app.py`).
- Blokuje: nic

## Jak to funguje

- Uzávěrka dne D = doklady od **D 10:00 do D+1 12:00**.
- Navržený den: poslední doklad po 12:00 → jeho den; jinak den předtím.
- Logika je v [`kod/zpracovani.py`](kod/zpracovani.py) (bez Streamlitu),
  [`kod/app.py`](kod/app.py) je jen rozhraní.
- Export ze systému je `.xls` s drobně poškozenou vnitřní strukturou — Excel
  to toleruje, `xlrd` jen s `ignore_workbook_corruption=True`.

## Testovací data

Skutečné exporty obsahují jména hostů a tržby → **nikdy do repa** (je veřejné).
Leží lokálně v `C:\Users\Fikus\Filip-projekty-data\01-hotel-reporter\`
(`vstupy/` originály, `vystupy/` vygenerované reporty).

## Spuštění lokálně

```
cd kod
pip install -r requirements.txt
streamlit run app.py
```
