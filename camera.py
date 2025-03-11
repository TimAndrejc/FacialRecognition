import cv2 as cv
import numpy as np


def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]].
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass


def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere.
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    g = 0
    b = 0
    r = 0
    count = (desno_spodaj[0] - levo_zgoraj[0]) * (desno_spodaj[1] - levo_zgoraj[1])
    for i in range (levo_zgoraj[1], desno_spodaj[1]):
        for j in range (levo_zgoraj[0], desno_spodaj[0]):
            g += int(slika[i, j][0]) / count
            b += int(slika[i, j][1]) / count
            r += int(slika[i, j][2]) / count
    return tuple([int(g), int(b), int(r)])

def povprecna_barva(slika, sirina, visina) -> tuple:
    g = 0
    b = 0
    r = 0
    div = sirina*visina
    for i in range(visina -1):
        for j in range(sirina -1):

            g += int(slika[i, j][0]) / div
            b += int(slika[i, j][1]) / div
            r += int(slika[i, j][2]) / div

    return tuple([int(g), int(b), int(r)])
if __name__ == '__main__':
    # Pripravi kamero
    tolerance = 30
    camy = 220
    camx = 340
    x = 30
    y = 30
    skin = 0
    camera = cv.VideoCapture(1)
    ret, frame = camera.read()
    num = 0
    while True:
        ret, frame = camera.read()
        if ret:
            frame = cv.flip(frame, 1)
            frame = zmanjsaj_sliko(frame, camx, camy)
            if num < 40:
                cv.rectangle(frame, [140, 50], [210,150], (255, 0, 0), 3)
                num += 1
            elif num == 40:
                skin = doloci_barvo_koze(frame, [140, 50], [210, 150])
                #print(skin)
                num += 1
            else:
                for i in range(0, camy, y):
                    for j in range(0, camx, x):
                        tempx = x
                        tempy = y
                        if(j + x > camx):
                            tempx = camx - j
                        if(i + y > camy):
                            tempy = camy - i
                        barva = povprecna_barva(frame[i:i + y, j:j + x], tempx, tempy)
                        if (skin[0] + tolerance > barva[0] > skin[0] - tolerance and
                                skin[1] + tolerance > barva[1] > skin[1] - tolerance and
                                skin[2] + tolerance > barva[2] > skin[2] - tolerance):
                            cv.rectangle(frame, (j, i), (j + x, i + y), (0, 255, 0), 2)
                        else:
                            cv.rectangle(frame, (j, i), (j + x, i + y), (0, 0, 255), 1)
            cv.imshow('frame', frame)
        if(cv.waitKey(1) & 0xFF == ord('q')):
            break
    camera.release()
    cv.destroyAllWindows()

    # Zajami prvo sliko iz kamere

    # Izračunamo barvo kože na prvi sliki

    # Zajemaj slike iz kamere in jih obdeluj

    # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
    # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
    # Vprašanje 2: Kako prešteti število ljudi?

    # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
    # in ne pozabite, da ni nujno da je škatla kvadratna.
    pass