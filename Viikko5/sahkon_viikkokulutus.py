# Copyright 2025 Miro Hollanti
"""
Ohjelma joka laskee ja tulostaa sähkön viikkokulutuksen tiedostosta luettujen tietojen perusteella.
"""

def muunna_tiedot(kulutus: list) -> list:
    """Muunnetahan tiedot oikeisiin tietotyyppeihin."""
    #print(varaus)
    muutettu_tieto = []
    muutettu_tieto.append(datetime.fromisoformat(kulutus[0]))
    muutettu_tieto.append(int(kulutus[1]))
    muutettu_tieto.append(int(kulutus[2]))
    muutettu_tieto.append(int(kulutus[3]))
    muutettu_tieto.append(int(kulutus[4]))
    muutettu_tieto.append(int(kulutus[5]))
    muutettu_tieto.append(int(kulutus[6]))
    return muutettu_tieto

from datetime import date, datetime

def lue_data(tiedoston_nimi: str) -> list:
    """Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa."""
    Sahkotiedot = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # Ohitetaan otsikkorivi
        for Sahkotieto in f:
            Sahkotieto = Sahkotieto.strip()
            SahkotietoSarakkeet = Sahkotieto.split(';')
            Sahkotiedot.append(muunna_tiedot(SahkotietoSarakkeet))

    #Sahkotiedot.pop(0)  # Poistetaan otsikkorivi
    return Sahkotiedot

def paivanarvot(paiva: str, Lukuarvot: list) -> int:
    """Laskee annetun päivän kulutuksen vaiheessa 1."""
    pv = int(paiva.split('.')[0])
    kk = int(paiva.split('.')[1])
    vuosi = int(paiva.split('.')[2])
    lasketutArvot =[]
    Kulutus1 = 0
    Kulutus2 = 0
    Kulutus3 = 0
    Tuotanto1 = 0
    Tuotanto2 = 0
    Tuotanto3 = 0
    for lukuarvo in Lukuarvot:
        if lukuarvo[0].date() == date(vuosi, kk, pv):
            Kulutus1 += lukuarvo[1]
            Kulutus2 += lukuarvo[2]
            Kulutus3 += lukuarvo[3]
            Tuotanto1 += lukuarvo[4]
            Tuotanto2 += lukuarvo[5]
            Tuotanto3 += lukuarvo[6]

    lasketutArvot.append(Kulutus1/1000)
    lasketutArvot.append(Kulutus2/1000)
    lasketutArvot.append(Kulutus3/1000)
    lasketutArvot.append(Tuotanto1/1000)
    lasketutArvot.append(Tuotanto2/1000)
    lasketutArvot.append(Tuotanto3/1000)
    return lasketutArvot

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin."""
    #print(lue_data("viikko42.csv"))
    Lukuarvot = lue_data("viikko42.csv")
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain):")
    print()        
    print("Päivä\t\tPvm\t\tKulutus [kWh]\t\t\tTuotanto [kWh]")
    print("\t\t(pv.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
    print("-------------------------------------------------------------------------------------")
    maanantainarvot = paivanarvot("13.10.2025", Lukuarvot)
    print(f"Maanantai\t13.10.2025\t", f"{maanantainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{maanantainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[5]:.2f}".replace(".", ","))



if __name__ == "__main__":
    main()