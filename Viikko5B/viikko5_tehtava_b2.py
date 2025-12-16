# Copyright 2025 Miro Hollanti
# MIT License
"""
Ohjelma joka laskee ja tulostaa sähkön viikkokulutuksen tiedostosta luettujen tietojen perusteella.
"""

from datetime import date, datetime, timedelta

#Muuttujat viikonpäiville
Viikonpaivat = ["Maanantai", "Tiistai\t", "Keskiviikko", "Torstai\t", "Perjantai", "Lauantai", "Sunnuntai"]

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

def luo_viikkoraportti(start_pvm: date, Lukuarvot: list, viikonnumero: int) -> str:
    """Luo viikkoraportti annetulle viikolle käyttäen Viikonpaivat-listaa."""
    otsikko = (
        f"\nViikon {viikonnumero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n"
        "Päivä\t\t\tPvm\t\t Kulutus [kWh]\t\tTuotanto [kWh]\n"
        "\t\t\t(pv.kk.vvvv) v1\t\tv2\t\tv3\t\tv1\t\tv2\t\tv3\n"
        "--------------------------------------------------------------------------------\n"
    )

    rivit = []
    for i, paiva_nimi in enumerate(Viikonpaivat):
        pvm = start_pvm + timedelta(days=i)
#Lyhyt viikonpäivän nimi = kaksi tabulaattoria
        if paiva_nimi in ("tiistai", "torstai"):
            paiva_kentta = paiva_nimi + "\t\t"
        else:
            paiva_kentta = paiva_nimi + "\t"
        rivit.append(paiva_kentta + "\t".join(paivanarvot(pvm, Lukuarvot)))
    return otsikko + "\n".join(rivit) + "\n\n"     

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin yhteenvetotiedostoon."""
    #print(lue_data("viikko42.csv"))
    LukuarvotViikko41 = lue_data("viikko41.csv")
    LukuarvotViikko42 = lue_data("viikko42.csv")
    LukuarvotViikko43 = lue_data("viikko43.csv")

    Viikko41 = luo_viikkoraportti(date(2025, 10, 6), LukuarvotViikko41, 41)
    Viikko42 = luo_viikkoraportti(date(2025, 10, 13), LukuarvotViikko42, 42)
    Viikko43 = luo_viikkoraportti(date(2025, 10, 20), LukuarvotViikko43, 43)

    #Kirjoita raportti tiedostoon
    with open("yhteenveto.txt", "w", encoding="utf-8") as f: 
        f.write(Viikko41)
        f.write(Viikko42)
        f.write(Viikko43)

if __name__ == "__main__":
    main()