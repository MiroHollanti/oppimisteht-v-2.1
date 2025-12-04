# Copyright 2025 Miro Hollanti
# MIT License
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
    """Luetaan CSV-tiedosto ja palautetaan rivit sopivassa rakenteessa."""
    Sahkotiedot = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # Ohitetaan otsikkorivi
        for Sahkotieto in f:
            Sahkotieto = Sahkotieto.strip()
            SahkotietoSarakkeet = Sahkotieto.split(';')
            Sahkotiedot.append(muunna_tiedot(SahkotietoSarakkeet))
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
    print("\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain):", end="\n\n")
    print("Päivä\t\tPvm\t\t Kulutus [kWh]\t\t\tTuotanto [kWh]\t\tNetto [kWh]")
    print("\t\t(pv.kk.vvvv)\t v1\tv2\tv3\t\tv1\tv2\tv3")
    print("---------------------------------------------------------------------------------------------------")
    maanantainarvot = paivanarvot("13.10.2025", Lukuarvot)
    print(f"Maanantai\t13.10.2025\t", f"{maanantainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{maanantainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{maanantainarvot[0]+maanantainarvot[1]+maanantainarvot[2]-maanantainarvot[3]-maanantainarvot[4]-maanantainarvot[5]:.2f}".replace(".", ","), end="\n")

    tiistainarvot = paivanarvot("14.10.2025", Lukuarvot)
    print(f"Tiistai \t14.10.2025\t", f"{tiistainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{tiistainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{tiistainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{tiistainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{tiistainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{tiistainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{tiistainarvot[0]+tiistainarvot[1]+tiistainarvot[2]-tiistainarvot[3]-tiistainarvot[4]-tiistainarvot[5]:.2f}".replace(".", ","), end="\n")

    keskiviikonarvot = paivanarvot("15.10.2025", Lukuarvot)
    print(f"Keskiviikko\t15.10.2025\t", f"{keskiviikonarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{keskiviikonarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{keskiviikonarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{keskiviikonarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{keskiviikonarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{keskiviikonarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{keskiviikonarvot[0]+keskiviikonarvot[1]+keskiviikonarvot[2]-keskiviikonarvot[3]-keskiviikonarvot[4]-keskiviikonarvot[5]:.2f}".replace(".", ","), end="\n")

    torstainarvot = paivanarvot("16.10.2025", Lukuarvot)
    print(f"Torstai \t16.10.2025\t", f"{torstainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{torstainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{torstainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{torstainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{torstainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{torstainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{torstainarvot[0]+torstainarvot[1]+torstainarvot[2]-torstainarvot[3]-torstainarvot[4]-torstainarvot[5]:.2f}".replace(".", ","), end="\n")

    perjantainarvot = paivanarvot("17.10.2025", Lukuarvot)
    print(f"Perjantai \t17.10.2025\t", f"{perjantainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{perjantainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{perjantainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{perjantainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{perjantainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{perjantainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{perjantainarvot[0]+perjantainarvot[1]+perjantainarvot[2]-perjantainarvot[3]-perjantainarvot[4]-perjantainarvot[5]:.2f}".replace(".", ","), end="\n")

    lauantainarvot = paivanarvot("18.10.2025", Lukuarvot)
    print(f"Lauantai \t18.10.2025\t", f"{lauantainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{lauantainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{lauantainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{lauantainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{lauantainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{lauantainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{lauantainarvot[0]+lauantainarvot[1]+lauantainarvot[2]-lauantainarvot[3]-lauantainarvot[4]-lauantainarvot[5]:.2f}".replace(".", ","), end="\n")

    sunnuntainarvot = paivanarvot("19.10.2025", Lukuarvot)
    print(f"Sunnuntai \t19.10.2025\t", f"{sunnuntainarvot[0]:.2f}".replace(".", ","), end="\t")
    print(f"{sunnuntainarvot[1]:.2f}".replace(".", ","), end="\t")
    print(f"{sunnuntainarvot[2]:.2f}".replace(".", ","), end="\t\t")
    print(f"{sunnuntainarvot[3]:.2f}".replace(".", ","), end="\t")
    print(f"{sunnuntainarvot[4]:.2f}".replace(".", ","), end="\t")
    print(f"{sunnuntainarvot[5]:.2f}".replace(".", ","), end="\t")
    print(f"{sunnuntainarvot[0]+sunnuntainarvot[1]+sunnuntainarvot[2]-sunnuntainarvot[3]-sunnuntainarvot[4]-sunnuntainarvot[5]:.2f}".replace(".", ","), end="\n")

if __name__ == "__main__":
    main()