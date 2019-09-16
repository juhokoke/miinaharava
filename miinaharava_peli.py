"""
Kaiken pelin pyörittämiseen tarvitsevat funktiot löytyy täältä.
"""
from random import *
from math import *
import time
import random
import gameui

tila = {
    "kentta": None, # Näytölle piirrettävä kenttä
    "avaamaton_k": None, # Avaamaton, piilossa oleva pelikenttä, johon laskettu miinat ja niiden määrä.
    "nimi": "",
    "miinat": 0,
    "miinojen_paikat": [], # Miinojen sijainnit koordinaatistossa.
    "avatut": [], # Avatut ruudut
    "siirrot": 0,
    "aika_a": 0, # Aloitus aika
    "aika_l": 0, # Lopetusaika
    "avaamatta": 0, # Avaamatta olevat ruudut liekkö kättämätön tarkista!
    "leveys": 0,
    "korkeus": 0,
    "loppu": False
}

def miinoita(kentta1, sijainnit, vapaat_ruudut, miinat):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    Lisää myös miinojen koordinaatit listaan.
    """
    for i in range(miinat):
        x, y = choice(vapaat_ruudut)
        kentta1[x][y] = "x"
        sijainnit.append((x, y))
        vapaat_ruudut.remove((x, y))

def tulvataytto(avaamatta, kentta, y_aloitus, x_aloitus):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    Lisää ruudut myös näytettävälle kentälle. 
    Palauttaa listan avatuista ruuduista.
    """
    avatut = []
    koordinaatit = [(y_aloitus,x_aloitus)]
    vaihda = None
    avatut.append((y_aloitus, x_aloitus))
    while len(koordinaatit) > 0:
        x,y = koordinaatit.pop()
        if kentta[x][y] == "x":
            pass
        elif kentta[x][y] == " ":
                kentta[x][y] = "0"
                avaamatta[x][y] = "0"
                avatut.append((x, y))
                if (x, y) not in tila["avatut"]:
                    tila["avatut"].append((x, y))

                mahdolliset_miinat = [[x - 1, y + 1],
                                [x - 1, y],
                                [x - 1, y - 1],
                                [x, y - 1],
                                [x + 1, y - 1],
                                [x + 1, y],
                                [x + 1, y + 1],
                                [x, y + 1]]

                for i in range(0, 8):
                    local_x, local_y = mahdolliset_miinat[i]
                    try:
                        if local_x < 0:
                            pass
                        elif local_y < 0:
                            pass
                        elif kentta[local_x][local_y] == " ":
                            koordinaatit.append((local_x,local_y))
                        elif kentta[local_x][local_y] == "x":
                            pass
                        elif kentta[local_x][local_y] == "0":
                            pass
                        else:
                            pass
                    except IndexError:
                        pass

    return avatut

def laske_miinat(x_koordinaatti, y_koordinaatti, kentta):
    """
    Laskee annetun xy koordinaatin ympärillä olvat miinat.
    Funktio toimii sillä oletuksella, että valitussa ruudussa ei
    ole miinaa - jos on, sekin lasketaan mukaan.
    """
    mahdolliset_miinat = [[x_koordinaatti - 1, y_koordinaatti + 1],
                        [x_koordinaatti - 1, y_koordinaatti],
                        [x_koordinaatti - 1, y_koordinaatti - 1],
                        [x_koordinaatti, y_koordinaatti - 1],
                        [x_koordinaatti + 1, y_koordinaatti - 1],
                        [x_koordinaatti + 1, y_koordinaatti],
                        [x_koordinaatti + 1, y_koordinaatti + 1],
                        [x_koordinaatti, y_koordinaatti + 1]]                 
    miinat = 0
    
    for i in range(0, 8):
        local_y = mahdolliset_miinat[i][0]
        local_x = mahdolliset_miinat[i][1]
        try:
            if local_x < 0:
                pass
            elif local_y < 0:
                pass
            elif kentta[local_x][local_y] == "x":
                miinat += 1
            else:
                pass
        except IndexError:
            pass
                
    return miinat

def avaa_numerot(luukut):
    """
    Piirtää kentälle miinojen määrän avatauille ruuduille.
    """
    l = tila["leveys"] - 1
    k = tila["korkeus"] - 1
    if len(luukut) > 1:
        for i in range(len(luukut)):
            x, y = luukut[i]
            avattavat = [[x - 1, y + 1],
                        [x - 1, y],
                        [x - 1, y - 1],
                        [x, y - 1],
                        [x + 1, y - 1],
                        [x + 1, y],
                        [x + 1, y + 1],
                        [x, y + 1]]

            for z in range(0, 8):
                x1, y1 = avattavat[z]
                if x1 <= k and y1 <= l and x1 >= 0 and y1 >= 0:
                    if tila["kentta"][x1][y1] != "x":
                        tila["avaamaton_k"][x1][y1] = tila["kentta"][x1][y1]
                        if (x1, y1) not in tila["avatut"]:
                            tila["avatut"].append((x1, y1))
    else:
        x1, y1 = luukut[0]
        if tila["kentta"][x1][y1] != "x":
            tila["avaamaton_k"][x1][y1] = tila["kentta"][x1][y1]
            if (x1, y1) not in tila["avatut"]:
                    tila["avatut"].append((x1, y1))

def tarkista_koordinaatit(y, x):
    """
    Tarkistaa ovatko koordinaatit pelikentällä ja palauttaa arvon True jos on.
    """
    leveys = tila["leveys"] - 1
    korkeus = tila["korkeus"] - 1
    if x < 0 or y < 0:
        return False
    elif int(y) > int(korkeus) or int(x) > int(leveys):
        return False
    else:
        return True

def luo_kentta(vaikeus):
    """
    Funktio luo käyttäjälle piirrettävän kentän sekä piilossa olevan kentän,
    jolle on ennakkoon laskettu miinojen määrät sekä miinojen sijainnit.
    Funktio asettaa kirjastoon myös kentän korkeuden ja leveyden.
    """
    alusta()
    a = 0 # Korkeus
    b = 0 # Leveys
    c = 0 # Miinat

    a, b, c = vaikeus

    tila["korkeus"] = int(a)
    tila["leveys"] = int(b)
    tila["miinat"] = int(c)

    kentta = []
    tyhja_kentta = []

    for rivi in range(a):
        kentta.append([])
        for sarake in range(b):
            kentta[-1].append(" ")

    for rivi in range(a):
        tyhja_kentta.append([])
        for sarake in range(b):
            tyhja_kentta[-1].append(" ")

    tila["kentta"] = kentta
    tila["avaamaton_k"] = tyhja_kentta

    jaljella = []

    for x in range(a):
        for y in range(b):
            jaljella.append((x, y))
    
    tila["avaamatta"] = int((a * b) - c)
    miinoita(kentta, tila["miinojen_paikat"], jaljella, c)

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """
    Käsittelee hiiren napin klikkaukset.
    """
    hiiri = {
        "vasen": gameui.HIIRI_VASEN,
        "oikea": gameui.HIIRI_OIKEA,
        "keski": gameui.HIIRI_KESKI,
    }
    vasen = hiiri["vasen"]
    oikea = hiiri["oikea"]
    keski = hiiri["keski"]

    x = ceil((x / 40) - 1)
    y = ceil((y / 40) - 1)
    arvo = tarkista_koordinaatit(y, x)
    if tila["aika_a"] == 0 and arvo == True:
        tila["aika_a"] = round(time.time())
        #if tila["kentta"][x][y] == "x":
        #    taso = {tila["leveys"], tila["korkeus"], tila["miinat"]}
        #    luo_kentta(taso)
        #    pelaa()

    if tila["kentta"][y][x] == "x" and nappi == vasen and arvo == True and tila["loppu"] == False:
        tila["siirrot"] += 1
        tarkista_voitto(y ,x)

    if nappi == vasen and arvo == True and tila["loppu"] == False:
        tila["siirrot"] += 1
        avattu = tulvataytto(tila["avaamaton_k"], tila["kentta"], y, x)
        avaa_numerot(avattu)
        tarkista_voitto(y ,x)

    elif nappi == oikea and tila["avaamaton_k"][y][x] == " " and arvo == True and tila["loppu"] == False:
        tila["avaamaton_k"][y][x] = "f"
        tila["siirrot"] += 1
    elif nappi == oikea and tila["avaamaton_k"][y][x] == "f" and arvo == True and tila["loppu"] == False:
        tila["avaamaton_k"][y][x] = " "
        tila["siirrot"] += 1


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    gameui.tyhjaa_ikkuna()
    gameui.piirra_tausta()
    gameui.piirra_tekstia("Miinoja: {}".format(tila["miinat"]), 1, tila["korkeus"]*40 + 2)
    gameui.aloita_ruutujen_piirto()
    
    for x, rivi in enumerate(tila["avaamaton_k"]):
        for y, ruutu in enumerate(rivi):
            x1 = x * 40
            y1 = y * 40
            
            gameui.lisaa_piirrettava_ruutu(ruutu, y1, x1)
            
    gameui.piirra_ruudut()

def pelaa():
    """
    Funktio aloittaa pelin ja laskee piilotetulle kentälle miinojen määrät.
    """
    for i in range(len(tila["kentta"])):
        for j in range(len(tila["kentta"][i])):
            if tila["kentta"][i][j] != "x":
                maara = laske_miinat(j, i, tila["kentta"])
                if maara == 0:
                    tila["kentta"][i][j] = " "
                else:
                    tila["kentta"][i][j] = maara

    gameui.luo_ikkuna(tila["leveys"]*40, tila["korkeus"] * 40 + 30)
    gameui.aseta_piirto_kasittelija(piirra_kentta)
    gameui.aseta_hiiri_kasittelija(kasittele_hiiri)
    gameui.aseta_toistuva_kasittelija(paivita_naytto)
    gameui.aloita()

def paivita_naytto(aika):
    """
    Käsittelijä funktio ajan päivittämiseen näytölle.
    """
    #aika_a = tila["aika_a"] - round(time.time())
    #piirra_kentta(98, 77)
    #gameui.tyhjaa_ikkuna()
    #gameui.aloita_ruutujen_piirto()
    #gameui.piirra_tekstia("Aika: 10", 1, tila["korkeus"]*40 + 10)

    #gameui.aloita_ruutujen_piirto()
    #gameui.piirra_ruudut()

def tarkista_voitto(x ,y):
    if tila["kentta"][x][y] == "x":
        tila["loppu"] = True
        tila["aika_l"] = round(time.time()) - tila["aika_a"]
        tallenna_peli("Häviö")
        try:
            for i in range(len(tila["miinojen_paikat"])):
                x, y = tila["miinojen_paikat"][i]
                tila["avaamaton_k"][x][y] = "x"
        except IndexError:
            pass

    elif int(tila["avaamatta"]) == int(len(tila["avatut"])):
        tila["loppu"] = True
        tila["aika_l"] = round(time.time()) - tila["aika_a"]
        tallenna_peli("Voitto")
        gameui.lopeta()
        print("\n ONNEKSI OLKOON VOITIT PELIN! ")
        input("\n Paina enteriä jatkaaksesi ")
        #gameui.piirra_tekstia("Hävisit pelin!", 10, 10)

def tallenna_peli(lopputulos):
    pvm = time.strftime("%d.%m.%Y %H:%M", time.localtime())
    try:
        with open("tilastot.csv", "a") as kohde:
            kohde.write("{},{},{},{},{},{},{},{}\n".format(tila["nimi"], pvm, tila["aika_l"], tila["siirrot"], lopputulos, tila["korkeus"], tila["leveys"], tila["miinat"]))
    except IOError:
        print("Tallennus epäonnistui.")

def alusta():
    tila["kentta"] = None
    tila["avaamaton_k"] = None
    tila["miinat"] = 0
    tila["miinojen_paikat"] = []
    tila["avatut"] = []
    tila["siirrot"] = 0
    tila["aika_a"] = 0
    tila["aika_l"] = 0
    tila["avaamatta"] = 0
    tila["leveys"] = 0
    tila["korkeus"] = 0
    tila["loppu"] = False