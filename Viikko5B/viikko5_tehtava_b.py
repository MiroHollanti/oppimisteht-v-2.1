# Copyright 2025 Miro Hollanti
# MIT License
"""
Ohjelma joka laskee ja tulostaa sähkön viikkokulutuksen tiedostosta luettujen tietojen perusteella.
"""

from datetime import date, datetime

def muunna_tiedot(kulutus: list) -> list:
    """Muunnetahan tiedot oikeisiin tietotyyppeihin. Ensimmäinen sarake datetime, loput int."""
    #print(varaus)
    return [
        datetime.fromisoformat(kulutus[0]),  # aikaleima
        int(kulutus[1]),  # kulutus vaihe 1
        int(kulutus[2]),  # kulutus vaihe 2
        int(kulutus[3]),  # kulutus vaihe 3
        int(kulutus[4]),  # tuotanto vaihe 1
        int(kulutus[5]),  # tuotanto vaihe 2
        int(kulutus[6])   # tuotanto vaihe 3
    ]

def lue_data(tiedoston_nimi: str) -> list:
    """Luetaan CSV-tiedosto ja palautetaan rivit sopivassa rakenteessa."""
    Sahkotiedot = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # Ohitetaan otsikkorivi
        for Sahkotieto in f:
            Sahkotieto = Sahkotieto.strip()
            SahkotietoSarakkeet = Sahkotieto.split(';')
            Sahkotiedot.append(muunna_tiedot(SahkotietoSarakkeet))
    return Sahkotiedot

def paivanarvot(pvm: date, Lukuarvot: list) -> list:
    Kulutus = [0, 0, 0]
    Tuotanto = [0, 0, 0]
    for lukuarvo in Lukuarvot:
        if lukuarvo[0].date() == pvm:
            Kulutus[0] += lukuarvo[1] / 1000  # muutetaan Wh kWh:ksi
            Kulutus[1] += lukuarvo[2] / 1000
            Kulutus[2] += lukuarvo[3] / 1000
            Tuotanto[0] += lukuarvo[4] / 1000
            Tuotanto[1] += lukuarvo[5] / 1000
            Tuotanto[2] += lukuarvo[6] / 1000
    return [
        f"{pvm.day}.{pvm.month}.{pvm.year}",
        f"{Kulutus[0]:.2f}".replace(".", ","),
        f"{Kulutus[1]:.2f}".replace(".", ","),
        f"{Kulutus[2]:.2f}".replace(".", ","),
        f"{Tuotanto[0]:.2f}".replace(".", ","),
        f"{Tuotanto[1]:.2f}".replace(".", ","),
        f"{Tuotanto[2]:.2f}".replace(".", ",")
    ]
def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin yhteenvetotiedostoon."""
    #print(lue_data("viikko42.csv"))
    LukuarvotViikko41 = lue_data("viikko41.csv")
    LukuarvotViikko42 = lue_data("viikko42.csv")
    LukuarvotViikko43 = lue_data("viikko43.csv")

    #Viikko41    
    Viikko41 = "\nViikon 41 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    Viikko41 += "Päivä\t\t\tPvm\t\t Kulutus [kWh]\t\tTuotanto [kWh]\n"
    Viikko41 += "\t\t\t(pv.kk.vvvv) v1\t\tv2\t\tv3\t\tv1\t\tv2\t\tv3\n"
    Viikko41 += "--------------------------------------------------------------------------------\n"
    Viikko41 += "maanantai\t" + "\t".join(paivanarvot(date(2025, 10, 6), LukuarvotViikko41)) + "\n"
    Viikko41 += "tiistai\t\t" + "\t".join(paivanarvot(date(2025, 10, 7), LukuarvotViikko41)) + "\n"
    Viikko41 += "keskiviikko\t" + "\t".join(paivanarvot(date(2025, 10, 8), LukuarvotViikko41)) + "\n"
    Viikko41 += "torstai\t\t" + "\t".join(paivanarvot(date(2025, 10, 9), LukuarvotViikko41)) + "\n"
    Viikko41 += "perjantai\t" + "\t".join(paivanarvot(date(2025, 10, 10), LukuarvotViikko41)) + "\n"
    Viikko41 += "lauantai\t" + "\t".join(paivanarvot(date(2025, 10, 11), LukuarvotViikko41)) + "\n"
    Viikko41 += "sunnuntai\t" + "\t".join(paivanarvot(date(2025, 10, 12), LukuarvotViikko41)) + "\n\n"

    #Viikko42
    Viikko42 = "\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    Viikko42 += "Päivä\t\t\tPvm\t\t Kulutus [kWh]\t\tTuotanto [kWh]\n"
    Viikko42 += "\t\t\t(pv.kk.vvvv) v1\t\tv2\t\tv3\t\tv1\t\tv2\t\tv3\n"
    Viikko42 += "--------------------------------------------------------------------------------\n"
    Viikko42 += "maanantai\t" + "\t".join(paivanarvot(date(2025, 10, 13), LukuarvotViikko42)) + "\n"
    Viikko42 += "tiistai\t\t" + "\t".join(paivanarvot(date(2025, 10, 14), LukuarvotViikko42)) + "\n"
    Viikko42 += "keskiviikko\t" + "\t".join(paivanarvot(date(2025, 10, 15), LukuarvotViikko42)) + "\n"
    Viikko42 += "torstai\t\t" + "\t".join(paivanarvot(date(2025, 10, 16), LukuarvotViikko42)) + "\n"
    Viikko42 += "perjantai\t" + "\t".join(paivanarvot(date(2025, 10, 17), LukuarvotViikko42)) + "\n"
    Viikko42 += "lauantai\t" + "\t".join(paivanarvot(date(2025, 10, 18), LukuarvotViikko42)) + "\n"
    Viikko42 += "sunnuntai\t" + "\t".join(paivanarvot(date(2025, 10, 19), LukuarvotViikko42)) + "\n\n"

    #Viikko43
    Viikko43 = "\nViikon 43 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
    Viikko43 += "Päivä\t\t\tPvm\t\t Kulutus [kWh]\t\tTuotanto [kWh]\n"
    Viikko43 += "\t\t\t(pv.kk.vvvv) v1\t\tv2\t\tv3\t\tv1\t\tv2\t\tv3\n"
    Viikko43 += "--------------------------------------------------------------------------------\n"
    Viikko43 += "maanantai\t" + "\t".join(paivanarvot(date(2025, 10, 20), LukuarvotViikko43)) + "\n"
    Viikko43 += "tiistai\t\t" + "\t".join(paivanarvot(date(2025, 10, 21), LukuarvotViikko43)) + "\n"
    Viikko43 += "keskiviikko\t" + "\t".join(paivanarvot(date(2025, 10, 22), LukuarvotViikko43)) + "\n"
    Viikko43 += "torstai\t\t" + "\t".join(paivanarvot(date(2025, 10, 23), LukuarvotViikko43)) + "\n"
    Viikko43 += "perjantai\t" + "\t".join(paivanarvot(date(2025, 10, 24), LukuarvotViikko43)) + "\n"
    Viikko43 += "lauantai\t" + "\t".join(paivanarvot(date(2025, 10, 25), LukuarvotViikko43)) + "\n"
    Viikko43 += "sunnuntai\t" + "\t".join(paivanarvot(date(2025, 10, 26), LukuarvotViikko43)) + "\n\n"

    #Kirjoita raportti tiedostoon
    with open("yhteenveto.txt", "w", encoding="utf-8") as f: 
        f.write(Viikko41)
        f.write(Viikko42)
        f.write(Viikko43)

if __name__ == "__main__":
    main()