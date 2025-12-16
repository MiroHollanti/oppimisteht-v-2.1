# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

"""Listoja käyttävä koodi muutettu sanakirjoja käyttäväksi. 
Sanakirjoja käytettäessä koodi helppolukuisempaa, koska kenttien nimistä nähdään suoraan mihin viitataan toisin kuin alkioiden numeroihin viittaavissa listoissa."""

from datetime import datetime

def muunna_varaustiedot(varaus_lista: list[str]) -> dict: 
    return {
        "id": int(varaus_lista[0]),
        "nimi": str(varaus_lista[1]),
        "sähköposti": str(varaus_lista[2]),
        "puhelin": str(varaus_lista[3]),
        "varauksenPvm": datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        "varauksenKlo": datetime.strptime(varaus_lista[5], "%H:%M").time(),
        "varauksenKesto": int(varaus_lista[6]),
        "hinta": float(varaus_lista[7]),
        "varausVahvistettu": varaus_lista[8].lower() == "true",
        "varattuTila": str(varaus_lista[9]),
        "varausLuotu": datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S")
    }
from typing import Any

def hae_varaukset(varaustiedosto: str) -> dict[int, dict[str, Any]]:
    varaukset = dict[int, dict[str, Any]]()
    with open(varaustiedosto, 'r', encoding='utf-8') as f:
        for rivi in f:
            rivi = rivi.strip()
            if not rivi:
                continue
            kentat = rivi.split("|")
            varaus = muunna_varaustiedot(kentat)
            varaukset[varaus["id"]] = varaus
    return varaukset

def vahvistetut_varaukset(varaukset: dict[int, dict[str, Any]]) -> None: 
    for varaus in varaukset.values():
        if(varaus["varausVahvistettu"]):
            print(f"{varaus['nimi']}, {varaus['varattuTila']}, {varaus['varauksenPvm'].strftime('%d.%m.%Y')}, {varaus['varauksenKlo'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: dict[int, dict[str, Any]]) -> None: 
    for varaus in varaukset.values():
        if(varaus['varauksenKesto'] >= 3):
            print(f"{varaus['nimi']}, {varaus['varauksenPvm'].strftime('%d.%m.%Y')} klo {varaus['varauksenKlo'].strftime('%H.%M')}, kesto {varaus['varauksenKesto']} h, {varaus['varattuTila']}")
    print()

def varausten_vahvistusstatus(varaukset: dict[int, dict[str, Any]]) -> None:
    for varaus in varaukset.values():
        if(varaus["varausVahvistettu"]):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")

    print()

def varausten_lkm(varaukset: dict[int, dict[str, Any]]) -> None:
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset.values():
        if(varaus['varausVahvistettu']):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl", "\n")

def varausten_kokonaistulot(varaukset: dict[int, dict[str, Any]]) -> None:
    varaustenTulot = 0
    for varaus in varaukset.values():
        if(varaus['varausVahvistettu']):
            varaustenTulot += varaus['varauksenKesto']*varaus['hinta']
    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€","\n") 

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)

    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)

    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)

    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()