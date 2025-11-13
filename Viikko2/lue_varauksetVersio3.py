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

from datetime import datetime, timedelta

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Luetaan tiedosto rivi kerrallaan
    with open(varaukset, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) != 10:
                print(f"Virhe rivillä {lineno}: odotettiin 10 kenttää, löytyi {len(parts)} — {parts}")
                continue

            (varausnumero, varaaja, varauspäivä, aloitusaika, tuntimäärä,
             tuntihinta, maksettu, varauskohde, puhelinnumero, sähköposti) = parts

            try:
                varausnumero = int(varausnumero)
                varauspäivä = datetime.strptime(varauspäivä, "%d.%m.%Y").date()
                aloitusaika = datetime.strptime(aloitusaika, "%H:%M").time()
                tuntimäärä = int(tuntimäärä)
                tuntihinta = float(tuntihinta.replace(',', '.'))
            except Exception as e:
                print(f"Muunnosvirhe rivillä {lineno}: {e}")
                continue

            päättymisaika = (datetime.combine(datetime.today(), aloitusaika) + timedelta(hours=tuntimäärä)).time()
            maksettu = maksettu.strip()

            # Tulostetaan vain ne varaukset, joita ei ole maksettu
            if maksettu.lower() in ('kyllä', 'true', 'yes'):
                continue

            print(f"Varausnumero: {varausnumero}")
            print(f"Varaaja: {varaaja}")
            print(f"Varauspäivä: {varauspäivä.strftime('%d.%m.%Y')}")
            print(f"Aloitusaika: {aloitusaika.strftime('%H:%M')}")
            print(f"Tuntimäärä: {tuntimäärä}")
            print(f"Päättymisaika: {päättymisaika.strftime('%H:%M')}")
            print(f"Tuntihinta: {tuntihinta:.2f}".replace('.', ',') + " €")
            print(f"Kokonaishinta: {(tuntimäärä * tuntihinta):.2f}".replace('.', ',') + " €")
            print(f"Maksettu: {'Kyllä' if maksettu.lower() in ('kyllä','true','yes') else 'Ei'}")
            print(f"Varauskohde: {varauskohde}")
            print(f"Puhelinnumero: {puhelinnumero}")
            print(f"Sähköposti: {sähköposti}")
            print("-" * 30)


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