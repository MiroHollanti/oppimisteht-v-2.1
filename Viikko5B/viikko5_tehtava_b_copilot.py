
# Copyright 2025 Miro Hollanti
# MIT License
"""
Ohjelma, joka lukee useiden viikkojen sähkötiedot CSV-tiedostoista,
laskee päivä- ja viikkokohtaiset yhteenvedot (kWh, vaiheittain),
ja kirjoittaa raportin tekstitiedostoon.

CSV-oletus: otsikkorivi ohitetaan, sarakkeet eroteltu ';'
Sarakkeet: ISO8601-aikaleima; Kulutus_v1; Kulutus_v2; Kulutus_v3; Tuotanto_v1; Tuotanto_v2; Tuotanto_v3
"""

from datetime import datetime, date
from collections import defaultdict
import argparse
import os

def muunna_tiedot(kulutus: list) -> list:
    """Muunnetaan tiedot oikeisiin tietotyyppeihin."""
    # kulutus: [iso, k1, k2, k3, t1, t2, t3]
    return [
        datetime.fromisoformat(kulutus[0]),
        int(kulutus[1]),
        int(kulutus[2]),
        int(kulutus[3]),
        int(kulutus[4]),
        int(kulutus[5]),
        int(kulutus[6]),
    ]

def lue_data_yksi(tiedoston_nimi: str) -> list:
    """Luetaan yksi CSV-tiedosto ja palautetaan rivit listana."""
    rivit = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # ohita otsikkorivi
        for rivi in f:
            rivi = rivi.strip()
            if not rivi:
                continue
            sarakkeet = rivi.split(';')
            # odotetaan 7 kenttää
            if len(sarakkeet) < 7:
                continue
            rivit.append(muunna_tiedot(sarakkeet))
    return rivit

def lue_data_useat(tiedostot: list) -> list:
    """Lue ja ketjuta useiden tiedostojen rivit."""
    kaikki = []
    for nimi in tiedostot:
        if not os.path.exists(nimi):
            print(f"Varoitus: tiedostoa ei löydy: {nimi}")
            continue
        kaikki.extend(lue_data_yksi(nimi))
    # Halutessasi voit lajitella aikaleiman mukaan:
    kaikki.sort(key=lambda r: r[0])
    return kaikki

def laske_paivittaiset(rivit: list) -> dict:
    """
    Aggregoi päiväkohtaiset summat. Palauttaa dictin:
    {date: {'kulutus': [v1, v2, v3], 'tuotanto': [v1, v2, v3]}}
    Arvot kWh: muunnetaan lopuksi Wh -> kWh (jakamalla 1000).
    """
    paiva_summa = defaultdict(lambda: {'kulutus': [0, 0, 0], 'tuotanto': [0, 0, 0]})
    for r in rivit:
        dt, k1, k2, k3, t1, t2, t3 = r
        d = dt.date()
        paiva_summa[d]['kulutus'][0] += k1
        paiva_summa[d]['kulutus'][1] += k2
        paiva_summa[d]['kulutus'][2] += k3
        paiva_summa[d]['tuotanto'][0] += t1
        paiva_summa[d]['tuotanto'][1] += t2
        paiva_summa[d]['tuotanto'][2] += t3

    # Muunna kWh-yksikköön
    for d in paiva_summa:
        paiva_summa[d]['kulutus'] = [x/1000 for x in paiva_summa[d]['kulutus']]
        paiva_summa[d]['tuotanto'] = [x/1000 for x in paiva_summa[d]['tuotanto']]
    return dict(sorted(paiva_summa.items(), key=lambda kv: kv[0]))

def ryhmittele_viikoittain(paivittaiset: dict) -> dict:
    """
    Ryhmittelee päiväkohtaiset arvot kalenteriviikoittain (ISO week).
    Palauttaa: { (vuosi, viikko): {'kulutus':[v1,v2,v3], 'tuotanto':[v1,v2,v3], 'paivat': {date: ...}} }
    """
    viikot = defaultdict(lambda: {'kulutus':[0,0,0], 'tuotanto':[0,0,0], 'paivat':{}})
    for d, arvot in paivittaiset.items():
        iso_year, iso_week, _ = d.isocalendar()
        key = (iso_year, iso_week)
        viikot[key]['paivat'][d] = arvot
        # kumuloi viikkosummat
        for i in range(3):
            viikot[key]['kulutus'][i] += arvot['kulutus'][i]
            viikot[key]['tuotanto'][i] += arvot['tuotanto'][i]
    # Järjestys
    return dict(sorted(viikot.items(), key=lambda kv: kv[0]))

def muodosta_raportti(paivittaiset: dict, viikot: dict) -> str:
    """Rakentaa raporttitekstin."""
    def fnum(x):  # suomalainen desimaalipilkku
        return f"{x:.2f}".replace('.', ',')

    lines = []
    lines.append("Sähkön kulutus ja tuotanto kolmen viikon ajalta (kWh, vaiheittain)")
    lines.append("")
    lines.append("Päiväkohtaiset arvot:")
    lines.append("Päivä\t\t(v1)\t(v2)\t(v3)\t\tTuotanto (v1)\t(v2)\t(v3)")
    lines.append("-"*90)

    for d, arvot in paivittaiset.items():
        pvm = d.strftime("%d.%m.%Y")
        k = arvot['kulutus']
        t = arvot['tuotanto']
        lines.append(f"{pvm}\t {fnum(k[0])}\t{fnum(k[1])}\t{fnum(k[2])}\t\t{fnum(t[0])}\t\t{fnum(t[1])}\t{fnum(t[2])}")

    lines.append("")
    lines.append("Viikkoyhteenvedot (ISO-viikot):")
    lines.append("Viikko\tKulutus v1\tv2\tv3\t| Tuotanto v1\tv2\tv3\t| Netto (kulutus-tuotanto)")
    lines.append("-"*110)
    kokonais_kulutus = [0,0,0]
    kokonais_tuotanto = [0,0,0]

    for (vy, vw), data in viikot.items():
        k = data['kulutus']
        t = data['tuotanto']
        netto = [k[i]-t[i] for i in range(3)]
        # kumuloi kokonaissummat
        for i in range(3):
            kokonais_kulutus[i] += k[i]
            kokonais_tuotanto[i] += t[i]
        lines.append(
            f"{vy}-W{vw}\t{fnum(k[0])}\t{fnum(k[1])}\t{fnum(k[2])}\t| "
            f"{fnum(t[0])}\t{fnum(t[1])}\t{fnum(t[2])}\t| "
            f"{fnum(netto[0])}\t{fnum(netto[1])}\t{fnum(netto[2])}"
        )

    lines.append("")
    lines.append("Kokonaisyhteenveto (kolmen viikon kumulatiiviset):")
    kokonais_netto = [kokonais_kulutus[i]-kokonais_tuotanto[i] for i in range(3)]
    lines.append(
        "Kulutus v1/v2/v3: "
        f"{fnum(kokonais_kulutus[0])} / {fnum(kokonais_kulutus[1])} / {fnum(kokonais_kulutus[2])}"
    )
    lines.append(
        "Tuotanto v1/v2/v3: "
        f"{fnum(kokonais_tuotanto[0])} / {fnum(kokonais_tuotanto[1])} / {fnum(kokonais_tuotanto[2])}"
    )
    lines.append(
        "Netto (kulutus-tuotanto) v1/v2/v3: "
        f"{fnum(kokonais_netto[0])} / {fnum(kokonais_netto[1])} / {fnum(kokonais_netto[2])}"
    )

    return "\n".join(lines)

def kirjoita_tiedostoon(sisalto: str, polku: str) -> None:
    with open(polku, "w", encoding="utf-8") as f:
        f.write(sisalto)

def main():
    parser = argparse.ArgumentParser(
        description="Laske kolmen viikon sähkön kulutus/tuotanto ja tuota tekstiraportti."
    )
    parser.add_argument(
        "--tiedostot", "-t",
        nargs="+",
        default=["viikko42.csv", "viikko43.csv", "viikko44.csv"],
        help="Luettavat CSV-tiedostot (oletus: viikko42.csv viikko43.csv viikko44.csv)"
    )
    parser.add_argument(
        "--ulostulo", "-o",
        default="kolmen_viikon_yhteenveto.txt",
        help="Raportin polku (oletus: kolmen_viikon_yhteenveto.txt)"
    )
    args = parser.parse_args()

    rivit = lue_data_useat(args.tiedostot)
    if not rivit:
        print("Ei luettavaa dataa. Tarkista tiedostopolut.")
        return

    paivittaiset = laske_paivittaiset(rivit)
    viikot = ryhmittele_viikoittain(paivittaiset)
    raportti = muodosta_raportti(paivittaiset, viikot)
    kirjoita_tiedostoon(raportti, args.ulostulo)

    print(f"Valmis! Raportti kirjoitettu tiedostoon: {args.ulostulo}")

if __name__ == "__main__":
    main()