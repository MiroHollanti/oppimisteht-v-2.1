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

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        (varausnumero, varaaja, varauspäivä, aloitusaika, tuntimäärä, tuntihinta, maksettu, varauskohde, puhelinnumero, sähköposti) = varaus.split('|')

    # Tulostetaan varaus konsoliin
    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaaja}")
    print(f"Pavämä: {varauspäivä}")
    print(f"Aloitusaika: {aloitusaika}")
    print(f"Tuntimäärä: {tuntimäärä}")
    print(f"Tuntihinta: {tuntihinta} €")
    print(f"Kokonaishinta: {float(tuntimäärä) * float(tuntihinta)} €")
    print(f"Maksettu: {maksettu}")
    print(f"Kohde: {varauskohde}")
    print(f"Puhelin: {puhelinnumero}")
    print(f"Sähköposti: {sähköposti}")

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