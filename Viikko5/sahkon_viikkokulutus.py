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


def tulosta_paivarivi(viikonpaiva_nimi: str, pvm_str: str, arvot: list) -> None:
    # arvot = [k1,k2,k3,t1,t2,t3] kWh
    netto = (arvot[0] + arvot[1] + arvot[2]) - (arvot[3] + arvot[4] + arvot[5])
    # korvaa piste pilkulla tulostuksessa
    fmt = lambda x: f"{x:.2f}".replace(".", ",")
    print(
        f"{viikonpaiva_nimi}\t{pvm_str}\t"
        f"{fmt(arvot[0])}\t{fmt(arvot[1])}\t{fmt(arvot[2])}\t\t"
        f"{fmt(arvot[3])}\t{fmt(arvot[4])}\t{fmt(arvot[5])}\t"
               f"{fmt(netto)}"
    )
   
VIIKONPAIVAT_FI = ["Maanantai", "Tiistai\t", "Keskiviikko", "Torstai\t", "Perjantai", "Lauantai", "Sunnuntai"]

def viikonpaiva_nimi(dt: datetime) -> str:
    return VIIKONPAIVAT_FI[dt.weekday()]  # 0=maanantai, 6=sunnuntai


def hae_uniikit_paivat(Lukuarvot: list) -> list[date]:
    # Lukuarvo[0] on datetime; otetaan .date() ja laitetaan settiin
    paivat = sorted({lr[0].date() for lr in Lukuarvot})
   
    return paivat


def paivanarvot_date(pvm: date, Lukuarvot: list) -> list:
    Kulutus1 = Kulutus2 = Kulutus3 = 0
    Tuotanto1 = Tuotanto2 = Tuotanto3 = 0
    for lukuarvo in Lukuarvot:
        if lukuarvo[0].date() == pvm:
            Kulutus1 += lukuarvo[1]
            Kulutus2 += lukuarvo[2]
            Kulutus3 += lukuarvo[3]
            Tuotanto1 += lukuarvo[4]
            Tuotanto2 += lukuarvo[5]
            Tuotanto3 += lukuarvo[6]
    # muutetaan kWh:ksi
    return [
        Kulutus1/1000, Kulutus2/1000, Kulutus3/1000,
        Tuotanto1/1000, Tuotanto2/1000, Tuotanto3/1000
    ]


def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin."""
    #print(lue_data("viikko42.csv"))
    Lukuarvot = lue_data("viikko42.csv")

    print("\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain):\n")
    print("Päivä\t\tPvm\t\t Kulutus [kWh]\t\t\tTuotanto [kWh]\t\tNetto [kWh]")
    print("\t\t(pv.kk.vvvv)\t v1\tv2\tv3\t\tv1\tv2\tv3")
    print("-----------------------------------------------------------------------------------------------------------")

    # A) iterointi uniikeista päivistä datassa
    for pvm in hae_uniikit_paivat(Lukuarvot):
        arvot = paivanarvot_date(pvm, Lukuarvot)
        viikonpaiva = viikonpaiva_nimi(datetime.combine(pvm, datetime.min.time()))
        pvm_str = pvm.strftime("%d.%m.%Y")
        tulosta_paivarivi(viikonpaiva, pvm_str, arvot)


if __name__ == "__main__":
    main()