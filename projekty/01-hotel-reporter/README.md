# 01 — Hotel reporter

**Stav:** hotovo · **Vzniklo:** 2026-04-17 · **Převzato sem:** 2026-11-07

Webová appka ve Streamlitu na denní uzávěrku tržeb hotelu. Nahraje se export
dokladů z hotelového systému (`.xlsx`) a appka z něj vyrobí Excel report
s doklady od 10:00 prvního dne do 12:00 dalšího dne a se součty plateb
hotově a kartou.

- Kód: [`kod/app.py`](kod/app.py), závislosti v [`kod/requirements.txt`](kod/requirements.txt)
- Původní repo: [`lnenickafi/hotel-reporter`](https://github.com/lnenickafi/hotel-reporter)
  (zkopírován stav z commitu `993ffec`, historie zůstala tam)

## Aktuální stav (2026-11-07)

- Hotovo: appka funguje (podle původního repa), kód převzatý sem.
- Neověřeno: jestli a kde běží nasazená verze (např. Streamlit Cloud
  napojený na původní repo) — kopie sem na ni nemá vliv.
- Zbývá: rozhodnout, jestli se dál vyvíjí tady, nebo v původním repu.
- Blokuje: nic

## Spuštění lokálně

```
cd kod
pip install streamlit -r requirements.txt
streamlit run app.py
```

`streamlit` v `requirements.txt` chybí (Streamlit Cloud ho doinstaluje sám),
lokálně se musí doinstalovat zvlášť.
