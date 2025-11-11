"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

from datetime import datetime


def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        (varausnumero, varaaja, varauspäivä, aloitusaika, tuntimäärä, tuntihinta, maksettu, varauskohde, puhelinnumero, sähköposti) = varaus.split('|')
        varausnumero = int(varausnumero)
        varaaja = str(varaaja)
        varauspäivä = datetime.strptime(varauspäivä, "%d.%m.%Y").date()
        aloitusaika = datetime.strptime(aloitusaika, "%H.%M").time()
        tuntimäärä = int(tuntimäärä)
        tuntihinta = float(tuntihinta)
        maksettu = bool(maksettu)
        varauskohde = str(varauskohde)
        puhelinnumero = str(puhelinnumero)
        sähköposti = str(sähköposti)

    print(f"varausnumero: {varausnumero}")
    print(f"varaaja: {varaaja}")
    print(f"varauspäivä: {varauspäivä}")
    print(f"aloitusaika: {aloitusaika}")
    print(f"tuntimäärä: {tuntimäärä}")
    print(f"tuntihinta: {tuntihinta} €")
    print(f"Kokonaishinta: {tuntimäärä * tuntihinta} €")
    print(f"maksettu: {maksettu}")
    print(f"varauskohde: {varauskohde}")
    print(f"puhelinnumero: {puhelinnumero}")
    print(f"sähköposti: {sähköposti}")
    
    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))

    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu 
    """
    
if __name__ == "__main__":
    main()