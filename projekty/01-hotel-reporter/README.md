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

- Hotovo: kód převzatý sem, původní repo archivované.
- Teď: Filip napojuje Streamlit Cloud na tohle repo
  (main file: `projekty/01-hotel-reporter/kod/app.py`).
- Zbývá: ověřit, že nasazená appka z tohohle repa běží.
- Blokuje: nic

## Spuštění lokálně

```
cd kod
pip install streamlit -r requirements.txt
streamlit run app.py
```

`streamlit` v `requirements.txt` chybí (Streamlit Cloud ho doinstaluje sám),
lokálně se musí doinstalovat zvlášť.
