"""Vyrobí smyšlený export dokladů pro ukázku a screenshoty appky.

Struktura (názvy a pořadí sloupců, souhrnný řádek na konci) odpovídá
skutečnému exportu z hotelového systému. Data jsou vymyšlená — jména,
částky ani čísla dokladů nepatří nikomu skutečnému.

    python vytvor_demo_export.py   →  demo-export.xlsx
"""

from pathlib import Path

import xlsxwriter

HLAVICKA = [
    "Číselná řada", "Zkontrolováno", "Vystaveno", "Stav", "Číslo", "Označení",
    "Odběratel", "Variabilní symbol", "Specifický symbol", "Forma úhrady",
    "Splatnost", "DUZP", "Základ 0%", "Základ - druhá snížená sazba 10%",
    "DPH - druhá snížená sazba 10%", "Základ - snížená sazba 12% (15%)",
    "DPH - snížená sazba 12% (15%)", "Základ - základní sazba 21%",
    "DPH - základní sazba 21%", "Celkem bez DPH", "Celkem s DPH", "Záloha",
    "Celkem k úhradě", "Poplatek za platbu kartou", "Haléřové vyrovnání",
    "Měna", "Kurz", "Uhrazeno", "ICO", "FIK", "BKP", "Dodavatel",
    "Celkem v domácí měně", "Příjezd", "Odjezd", "Číslo rezervace", "Original ID",
]

# (vystaveno, označení, odběratel, forma, ubytování s DPH 12 %, poplatek 0 %, číslo rezervace)
DOKLADY = [
    ("14.3.2026 07:41:12", "Ubytovací služby - 12.3.2026 - 14.3.2026", "Petr Novák", "Hotově", 3900, 100, "900101"),
    ("14.3.2026 08:05:47", "Ubytovací služby - 13.3.2026 - 14.3.2026", "Jana Dvořáková", "Kartou", 1850, 50, "900102"),
    ("14.3.2026 09:12:03", "Parkovné", "", "Hotově", 0, 70, "900102"),
    ("14.3.2026 11:24:55", "Ubytovací služby - 13.3.2026 - 14.3.2026", "Ukázková firma s.r.o.", "Kartou", 4100, 100, "900103"),
    ("14.3.2026 14:02:31", "Ubytovací služby - 14.3.2026 - 16.3.2026", "Tomáš Svoboda", "Kartou", 5980, 200, "900104"),
    ("14.3.2026 14:40:18", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Lucie Černá", "Hotově", 2700, 50, "900105"),
    ("14.3.2026 15:17:09", "Parkovné", "", "Hotově", 0, 70, "900104"),
    ("14.3.2026 16:33:44", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Martin Procházka", "Kartou", 2810, 50, "900106"),
    ("14.3.2026 17:51:27", "Ubytovací služby - 14.3.2026 - 16.3.2026", "Ukázková agentura a.s.", "Převodem", 7600, 200, "900107"),
    ("14.3.2026 19:08:02", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Eva Králová", "Kartou", 2350, 50, "900108"),
    ("14.3.2026 20:46:39", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Karel Veselý", "Hotově", 1900, 50, "900109"),
    ("15.3.2026 06:58:14", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Hana Marková", "Hotově", 2300, 100, "900110"),
    ("15.3.2026 08:20:50", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Ondřej Pokorný", "Kartou", 1770, 50, "900111"),
    ("15.3.2026 09:35:26", "Ubytovací služby - 14.3.2026 - 15.3.2026", "Veronika Horáková", "Kartou", 2000, 50, "900112"),
    ("15.3.2026 11:47:05", "Minibar", "", "Kartou", 0, 0, "900112"),
]


def main() -> None:
    cesta = Path(__file__).with_name("demo-export.xlsx")
    wb = xlsxwriter.Workbook(cesta)
    ws = wb.add_worksheet("Worksheet")
    ws.write_row(0, 0, HLAVICKA)

    soucty = [0.0] * len(HLAVICKA)
    for i, (vyst, oznaceni, odberatel, forma, ubyt, popl, rez) in enumerate(DOKLADY, start=1):
        vs = 202600100 + i
        den = vyst.split()[0]
        z12 = round(ubyt / 1.12, 2)
        d12 = round(ubyt - z12, 2)
        z21 = d21 = 0.0
        if oznaceni == "Minibar":
            z21, d21 = 123.97, 26.03
        bez = round(popl + z12 + z21, 2)
        s_dph = round(popl + ubyt + z21 + d21, 2)
        cisla = {
            "Základ 0%": popl, "Základ - druhá snížená sazba 10%": 0,
            "DPH - druhá snížená sazba 10%": 0,
            "Základ - snížená sazba 12% (15%)": z12, "DPH - snížená sazba 12% (15%)": d12,
            "Základ - základní sazba 21%": z21, "DPH - základní sazba 21%": d21,
            "Celkem bez DPH": bez, "Celkem s DPH": s_dph, "Záloha": 0,
            "Celkem k úhradě": s_dph, "Poplatek za platbu kartou": 0,
            "Haléřové vyrovnání": 0, "Kurz": 1, "Celkem v domácí měně": s_dph,
        }
        radek = {
            "Číselná řada": " Prodejky", "Zkontrolováno": "Ano", "Vystaveno": vyst,
            "Stav": "Uhrazeno", "Číslo": f"PR{vs}", "Označení": oznaceni,
            "Odběratel": odberatel, "Variabilní symbol": vs, "Forma úhrady": forma,
            "Splatnost": den, "DUZP": den, "Měna": "CZK", "Uhrazeno": "Ano",
            "Dodavatel": "Hotel Ukázka s. r. o.", "Číslo rezervace": f"2026{rez}",
            **cisla,
        }
        for j, nazev in enumerate(HLAVICKA):
            if nazev in radek:
                ws.write(i, j, radek[nazev])
            if nazev in cisla:
                soucty[j] += cisla[nazev]

    # souhrnný řádek na konci, jako ve skutečném exportu
    for j, nazev in enumerate(HLAVICKA):
        if soucty[j] and nazev != "Kurz":
            ws.write(len(DOKLADY) + 1, j, round(soucty[j], 2))
    wb.close()
    print(cesta)


if __name__ == "__main__":
    main()
