"""
Pääohjelma, joka käsittelee käyttäjän antamat syötteet.
"""
from sys import exit
import os
import miinaharava_peli
import gameui

vaikeustaso = {
    "helppo": (9, 9, 10),
    "keskivaikea": (16, 16, 40),
    "vaikea": (16, 30, 90),
    "custom": (0, 0, 0)
    }
    
def main():
    while True:
        try:
            print("\n Tervetuloa pelaamaan miinaharavaa!")
            kysy_nimi()
            tyhjenna()
            print("\n 1. Pelaa")
            print(" 2. Ennätykset")
            print(" 3. Sulje")
            valinta = input("\n Valitse antamalla numero: ")
            
            if valinta == "1":
                tyhjenna()
                valittu_taso = kysy_vaikeustaso()
                tyhjenna()
                gameui.lataa_kuvat("grafiikat")
                miinaharava_peli.luo_kentta(valittu_taso)
                miinaharava_peli.pelaa()

            elif valinta == "2":
                tyhjenna()
                nayta_tilastot()
            elif valinta == "3":
                tyhjenna()
                exit()
            else:
                tyhjenna()
                print("\n ET ANTANUT OIKEAA NUMEROA!")
                input("\n Paina enteriä jatkaaksesi ")
                tyhjenna()
        except KeyboardInterrupt:
            continue
             
def kysy_vaikeustaso():
    """
    Funktio pyytää vaikeutason.
    """
    while True:
        try:
            print("\n Valitse vaikeustaso")
            print("\n 1. Helppo")
            print(" 2. Keskivaikea")
            print(" 3. Vaikea")
            print(" 4. Muu")
            #print(" 5. Takaisin")
            taso = input("\n Valitse antamalla numero: ")
            
            if taso == "1":
                return vaikeustaso["helppo"]
            elif taso == "2":
                return vaikeustaso["keskivaikea"]
            elif taso == "3":
                return vaikeustaso["vaikea"]
            elif taso == "4":
                pyyda_taso()
                return vaikeustaso["custom"]
            #elif taso == "5":
                #break
            else:
                tyhjenna()
                print("\n ET ANTANUT OIKEAA NUMEROA!")
                input("\n Paina enteriä jatkaaksesi ")
                tyhjenna()
            
        except KeyboardInterrupt:
            continue
            
def pyyda_taso():
    """
    Pyytää ja asettaa käyttäjan antaman oman vaikeustason.
    """
    leveys = 0
    korkeus = 0
    miinat = 0
    tyhjenna()
    while True:
        try:
            korkeus = int(input("\n Anna kentän korkeus: "))
        except ValueError:
            tyhjenna()
            print("\n Et antanut kokonaislukua.")
        if korkeus < 1:
            tyhjenna()
            print("\n Korkeus on liian pieni.")
            print(" Yritä uudestaan.")
        elif korkeus > 1:
            break
        else:
            tyhjenna()
            print("\n Jotain meni pileen, yritä uudelleen.")
    tyhjenna()
    while True:
        try:
            leveys = int(input("\n Anna kentän leveys: "))
        except ValueError:
            tyhjenna()
            print("\n Et antanut kokonaislukua.")
        if leveys < 1:
            tyhjenna()
            print("\n Leveys on liian pieni.")
            print(" Yritä uudestaan.")
        elif leveys > 1:
            break
        else:
            tyhjenna()
            print("\n Jotain meni pileen, yritä uudelleen.")
    tyhjenna()
    while True:
        try:
            miinat = int(input("\n Anna miinojen määrä: "))
        except ValueError:
            tyhjenna()
            print("\n Et antanut kokonaislukua.")
        if miinat <= 1:
            tyhjenna()
            print("\n Liian vähän miinoja.")
            print(" Yritä uudestaan.")
        elif miinat > 1:
            break
        else:
            tyhjenna()
            print("\n Jotain meni pileen, yritä uudelleen.")
    
    vaikeustaso["custom"] = {korkeus, leveys, miinat}

def nayta_tilastot():
    """
    Lataa ennätykset csv tiedostosta ja tulostaa ne näytölle.
    """
    i = 0
    try:
        with open ("tilastot.csv") as tilastot:
            for rivi in tilastot.readlines():
                tiedot = rivi.rstrip("\n").split(",")
                m, s= divmod(int(tiedot[2]), 60)
                print("\n Päivämäärä: {}, aika: {} min {} sek, nimi: {}".format(tiedot[1], m, s, tiedot[0])) # muotoile aika hh:mm
                print(" Lopputulos: {}, siirrot: {}, kentän koko: {}x{}, miinat: {}".format(tiedot[4], tiedot[3], tiedot[6], tiedot[5], tiedot[7]))

    except FileNotFoundError:
        print("\n Aikaisempia ennätyksiä ei löytynyt.")
        input("\n Paina enteriä jatkaaksesi ")
    except IOError:
        print("\n Tiedosto vioittunut.")
        print(" Tilastoja ei voitu ladata.")
        input("\n Paina enteriä jatkaaksesi ")
        
    input("\n Paina enteriä palataksesi valikkoon ")
    tyhjenna()
    
def kysy_nimi():
    global nimi
    while True:
        try:
            print("\n Jättämällä nimikentän tyhjäksi voit pelata vieraana.")
            miinaharava_peli.tila["nimi"] = input("\n Anna käyttäjänimi: ")
            if miinaharava_peli.tila["nimi"] == "":
                miinaharava_peli.tila["nimi"] = "Vieras"
            return miinaharava_peli.tila["nimi"]
        except KeyboardInterrupt:
            tyhjenna()
            continue
            
def tyhjenna():
    """
    Funktio tyhjentää komentorivin käyttöjärjestelmästä huolimatta.
    """
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
    tyhjenna()
    main()
