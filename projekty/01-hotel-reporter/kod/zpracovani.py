"""Zpracování exportu dokladů z hotelového systému na denní uzávěrku tržeb.

Bez Streamlitu, aby šlo logiku spustit a otestovat i samostatně.
"""

import io
import re
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

import openpyxl
import xlrd
import xlsxwriter

# Uzávěrka dne D = doklady od D 10:00 do D+1 12:00.
ZACATEK = time(10, 0, 0)
KONEC = time(12, 0, 0)

# Sloupce exportu, které potřebujeme — PŘESNÉ názvy (bez ohledu na velikost
# písmen a mezery na krajích). Hledání podle části názvu dřív bralo
# „Číslo rezervace“ místo „Číslo“.
SLOUPCE = {
    "vystaveno": "Vystaveno",
    "stav": "Stav",
    "cislo": "Číslo",
    "vs": "Variabilní symbol",
    "forma": "Forma úhrady",
    "splatnost": "Splatnost",
    "zaklad0": "Základ 0%",
    "dph12": "DPH - snížená sazba 12% (15%)",
    "dph21": "DPH - základní sazba 21%",
    "bez_dph": "Celkem bez DPH",
    "s_dph": "Celkem s DPH",
}

HLAVICKA_VYSTUPU = [
    "Vystaveno", "Stav", "Číslo", "Variabilní symbol", "Forma úhrady",
    "Splatnost", "Základ 0%", "DPH - 12%", "DPH 21%", "Celkem bez DPH",
    "Celkem s DPH",
]

FORMY_UHRADY = {"Hotově", "Kartou"}


class ChybaExportu(Exception):
    """Export nejde zpracovat — zpráva je určená uživateli."""


@dataclass
class Doklad:
    vystaveno: datetime
    vystaveno_text: str
    stav: str
    cislo_export: str
    vs: str
    forma: str
    splatnost: str
    zaklad0: float
    dph12: float
    dph21: float
    bez_dph: float
    s_dph: float

    @property
    def cislo(self) -> str:
        return f"PR{self.vs}"


@dataclass
class Uzaverka:
    den: date
    doklady: list[Doklad]
    mimo_rozsah: list[Doklad]
    upozorneni: list[str] = field(default_factory=list)

    @property
    def od(self) -> datetime:
        return datetime.combine(self.den, ZACATEK)

    @property
    def do(self) -> datetime:
        return datetime.combine(self.den + timedelta(days=1), KONEC)

    @property
    def nazev_souboru(self) -> str:
        return f"{self.den.day}.xlsx"

    def soucet(self, forma: str) -> float:
        return round(sum(d.s_dph for d in self.doklady if d.forma == forma), 2)

    @property
    def celkem(self) -> float:
        return round(sum(d.s_dph for d in self.doklady), 2)


# ---------------------------------------------------------------- načtení

def nacti_radky(data: bytes, nazev: str) -> list[list]:
    """Vrátí list řádků (hodnoty buněk) z .xls nebo .xlsx."""
    if data[:4] == b"PK\x03\x04":  # .xlsx je zip
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        ws = wb.worksheets[0]
        return [list(r) for r in ws.iter_rows(values_only=True)]
    if data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":  # starý .xls
        # Export z hotelového systému má drobně poškozenou vnitřní strukturu;
        # Excel to toleruje, xlrd jen s ignore_workbook_corruption.
        try:
            kniha = xlrd.open_workbook(
                file_contents=data, ignore_workbook_corruption=True,
                logfile=io.StringIO(),
            )
        except Exception as e:
            raise ChybaExportu(f"Soubor {nazev} nejde přečíst jako .xls: {e}") from e
        list_ = kniha.sheet_by_index(0)
        return [list_.row_values(i) for i in range(list_.nrows)]
    raise ChybaExportu(f"Soubor {nazev} není .xls ani .xlsx.")


def _text(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, datetime):
        return f"{v.day}.{v.month}.{v.year} {v:%H:%M:%S}"
    if isinstance(v, date):
        return f"{v.day}.{v.month}.{v.year}"
    return str(v).strip()


def _cislo(v) -> float:
    if v is None or v == "":
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("\xa0", "").replace(" ", "").replace("CZK", "").replace("Kč", "")
    s = s.replace(",", ".")
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        raise ValueError(f"„{v}“ není číslo")
    return float(s)


def _datum_cas(v) -> datetime | None:
    if isinstance(v, datetime):
        return v
    m = re.fullmatch(r"\s*(\d{1,2})\.(\d{1,2})\.(\d{4})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*", str(v or ""))
    if not m:
        return None
    d, mo, r, h, mi, s = m.groups()
    return datetime(int(r), int(mo), int(d), int(h), int(mi), int(s or 0))


def nacti_doklady(radky: list[list]) -> list[Doklad]:
    hlavicka_idx = next(
        (i for i, r in enumerate(radky)
         if any(_text(c).lower() == "vystaveno" for c in r)),
        None,
    )
    if hlavicka_idx is None:
        raise ChybaExportu("V souboru chybí tabulka dokladů (sloupec „Vystaveno“).")

    hlavicka = [_text(c).lower() for c in radky[hlavicka_idx]]
    idx = {}
    chybi = []
    for klic, nazev in SLOUPCE.items():
        if nazev.lower() in hlavicka:
            idx[klic] = hlavicka.index(nazev.lower())
        else:
            chybi.append(nazev)
    if chybi:
        raise ChybaExportu("V exportu chybí sloupce: " + ", ".join(f"„{c}“" for c in chybi))

    doklady = []
    for cislo_radku, r in enumerate(radky[hlavicka_idx + 1:], start=hlavicka_idx + 2):
        r = list(r) + [None] * (len(hlavicka) - len(r))
        vyst = _datum_cas(r[idx["vystaveno"]])
        if vyst is None:
            # souhrnný řádek na konci exportu, prázdné řádky
            continue
        try:
            d = Doklad(
                vystaveno=vyst,
                vystaveno_text=_text(r[idx["vystaveno"]]),
                stav=_text(r[idx["stav"]]),
                cislo_export=_text(r[idx["cislo"]]),
                vs=_text(r[idx["vs"]]),
                forma=_text(r[idx["forma"]]),
                splatnost=_text(r[idx["splatnost"]]),
                zaklad0=_cislo(r[idx["zaklad0"]]),
                dph12=_cislo(r[idx["dph12"]]),
                dph21=_cislo(r[idx["dph21"]]),
                bez_dph=_cislo(r[idx["bez_dph"]]),
                s_dph=_cislo(r[idx["s_dph"]]),
            )
        except ValueError as e:
            raise ChybaExportu(f"Řádek {cislo_radku} exportu: {e}") from e
        doklady.append(d)

    if not doklady:
        raise ChybaExportu("V exportu nejsou žádné doklady.")
    return doklady


# ---------------------------------------------------------------- uzávěrka

def navrhni_den(doklady: list[Doklad]) -> date:
    """Den uzávěrky odvozený z posledního dokladu.

    Poslední doklad po 12:00 → uzávěrka toho dne (např. jen tržby 6. večer).
    Poslední doklad do 12:00 → patří do uzávěrky předchozího dne.
    """
    posledni = max(d.vystaveno for d in doklady)
    if posledni.time() > KONEC:
        return posledni.date()
    return posledni.date() - timedelta(days=1)


def je_v_rozsahu(d: Doklad, den: date) -> bool:
    od = datetime.combine(den, ZACATEK)
    do = datetime.combine(den + timedelta(days=1), KONEC)
    return od <= d.vystaveno <= do


def sestav_uzaverku(doklady: list[Doklad], den: date, zahrnout: set[int] | None = None) -> Uzaverka:
    """Uzávěrka za den.

    `zahrnout` = indexy dokladů (v seznamu `doklady`), které mají jít do
    reportu — ruční výběr v appce. Bez něj se vezmou doklady v rozsahu dne.
    """
    if zahrnout is None:
        zahrnout = {i for i, d in enumerate(doklady) if je_v_rozsahu(d, den)}
    vybrane = sorted((doklady[i] for i in zahrnout), key=lambda d: d.vystaveno)
    mimo = [d for i, d in enumerate(doklady) if i not in zahrnout]
    u = Uzaverka(den=den, doklady=vybrane, mimo_rozsah=mimo)

    if not vybrane:
        u.upozorneni.append("Není vybraný žádný doklad.")
    for d in vybrane:
        if d.cislo_export and d.cislo_export != d.cislo:
            u.upozorneni.append(
                f"Doklad {d.vystaveno_text}: číslo v exportu {d.cislo_export} "
                f"≠ PR + variabilní symbol ({d.cislo})."
            )
        if d.forma not in FORMY_UHRADY:
            u.upozorneni.append(
                f"Doklad {d.cislo} má formu úhrady „{d.forma}“ — "
                "nezapočítá se do součtu Hotově ani Kartou."
            )
        if d.stav != "Uhrazeno":
            u.upozorneni.append(f"Doklad {d.cislo} má stav „{d.stav}“.")
    return u


# ---------------------------------------------------------------- výstup

def vytvor_xlsx(u: Uzaverka) -> bytes:
    out = io.BytesIO()
    wb = xlsxwriter.Workbook(out, {"in_memory": True})
    ws = wb.add_worksheet("Report")
    tucne = wb.add_format({"bold": True})
    cislo = wb.add_format({"num_format": "#,##0.00"})
    ramecek = wb.add_format({"border": 1})  # tenké ohraničení buněk tabulky

    ws.write("B1", f"Tržba ze dne {u.od:%d.%m.} - {u.do:%d.%m. %Y}", tucne)

    prvni = 3  # 0-based řádek prvního dokladu = Excel řádek 4
    ws.write_row(prvni - 1, 0, HLAVICKA_VYSTUPU, ramecek)
    for i, d in enumerate(u.doklady):
        ws.write_row(prvni + i, 0, [
            d.vystaveno_text, d.stav, d.cislo, d.vs, d.forma, d.splatnost,
        ], ramecek)
        ws.write_row(prvni + i, 6, [d.zaklad0, d.dph12, d.dph21, d.bez_dph, d.s_dph], ramecek)

    n = len(u.doklady)
    if n:
        r1, r2 = prvni + 1, prvni + n  # Excel řádky
        sr = prvni + n + 2  # dva prázdné řádky pod tabulkou, jako ve vzoru
        # Vzorec i s předpočítanou hodnotou — v chráněném zobrazení Excel
        # nepřepočítává a bez ní by ukázal 0.
        ws.write(sr, 2, "Hotově:", tucne)
        ws.write_formula(sr, 3, f'=SUMIF(E{r1}:E{r2}, "*Hotově*", K{r1}:K{r2})', cislo, u.soucet("Hotově"))
        ws.write(sr + 1, 2, "Kred. kartou:", tucne)
        ws.write_formula(sr + 1, 3, f'=SUMIF(E{r1}:E{r2}, "*Kartou*", K{r1}:K{r2})', cislo, u.soucet("Kartou"))

    ws.set_column("A:K", 18)
    wb.close()
    return out.getvalue()
