import streamlit as st

from zpracovani import (
    ChybaExportu, je_v_rozsahu, navrhni_den, nacti_doklady, nacti_radky,
    sestav_uzaverku, vytvor_xlsx,
)

st.set_page_config(page_title="Uzávěrka tržeb", page_icon="🏨")
st.title("🏨 Uzávěrka tržeb")

st.markdown("""
Nahrajte **export dokladů přímo ze systému** (`.xls` tak, jak se stáhne —
není potřeba ho otevírat ani převádět; `.xlsx` funguje taky).

Uzávěrka bere doklady **od 10:00 vybraného dne do 12:00 dne následujícího**.
Den se předvyplní podle posledního dokladu, dá se změnit. Jednotlivé doklady
jde v tabulce ručně odebrat nebo přidat.
""")


def castka(x: float) -> str:
    return f"{x:,.2f}".replace(",", " ")


soubor = st.file_uploader("Export dokladů", type=["xls", "xlsx"])

if soubor:
    try:
        doklady = nacti_doklady(nacti_radky(soubor.getvalue(), soubor.name))
    except ChybaExportu as e:
        st.error(f"❌ {e}")
        st.stop()

    den = st.date_input("Uzávěrka za den", value=navrhni_den(doklady), format="DD.MM.YYYY")
    v_rozsahu = {i for i, d in enumerate(doklady) if je_v_rozsahu(d, den)}
    poradi = sorted(range(len(doklady)), key=lambda i: doklady[i].vystaveno)

    st.subheader("Doklady")
    st.caption(
        "Zaškrtnuté jdou do reportu. Předvybrané jsou doklady v rozsahu "
        "10:00–12:00; zaškrtnutím přidáte doklad mimo rozsah, odškrtnutím ho odeberete."
    )
    tabulka = st.data_editor(
        [{
            "Zahrnout": i in v_rozsahu,
            "Vystaveno": doklady[i].vystaveno_text,
            "Číslo": doklady[i].cislo,
            "Forma úhrady": doklady[i].forma,
            "Celkem s DPH": doklady[i].s_dph,
            "V rozsahu": "ano" if i in v_rozsahu else "—",
        } for i in poradi],
        column_config={
            "Zahrnout": st.column_config.CheckboxColumn(),
            "Celkem s DPH": st.column_config.NumberColumn(format="%.2f"),
        },
        disabled=["Vystaveno", "Číslo", "Forma úhrady", "Celkem s DPH", "V rozsahu"],
        hide_index=True,
        height=(len(poradi) + 1) * 35 + 3,  # všechny doklady bez posouvání
        # Při změně souboru nebo dne se výběr vrátí na výchozí.
        key=f"vyber-{soubor.file_id}-{den}",
    )
    zahrnout = {i for i, radek in zip(poradi, tabulka) if radek["Zahrnout"]}

    u = sestav_uzaverku(doklady, den, zahrnout)

    pridane = sorted(zahrnout - v_rozsahu, key=lambda i: doklady[i].vystaveno)
    odebrane = sorted(v_rozsahu - zahrnout, key=lambda i: doklady[i].vystaveno)
    if pridane:
        st.info("Ručně přidáno (mimo rozsah): " + ", ".join(doklady[i].cislo for i in pridane))
    if odebrane:
        st.info("Ručně odebráno: " + ", ".join(doklady[i].cislo for i in odebrane))
    for zprava in u.upozorneni:
        st.warning(zprava)

    if u.doklady:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dokladů", len(u.doklady))
        c2.metric("Hotově", castka(u.soucet("Hotově")))
        c3.metric("Kartou", castka(u.soucet("Kartou")))
        c4.metric("Celkem s DPH", castka(u.celkem))

        st.download_button(
            f"📥 Stáhnout {u.nazev_souboru}",
            vytvor_xlsx(u),
            file_name=u.nazev_souboru,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )

st.caption("Když něco nefunguje, napište Filipovi.")
