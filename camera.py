import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]].
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    tabela = []
    for i in range(0, camy, visina_skatle):
        vrstica = []
        for j in range(0, camx, sirina_skatle):
            tempx = sirina_skatle
            tempy = visina_skatle
            if (j + x > camx):
                tempx = camx - j
            if (i + y > camy):
                tempy = camy - i
            if prestej_piklse_z_barvo_koze(slika[i:i + tempy, j:j + tempx], barva_koze) > sirina_skatle * visina_skatle/ 2:
                vrstica.append(1)
                #cv.rectangle(frame2, (j, i), (j + tempx, i + tempy), (0, 255, 0), 3)
            else:
                vrstica.append(0)
                #cv.rectangle(frame2, (j, i), (j + tempx, i + tempy), (0, 0, 255), 1)
        tabela.append(vrstica)
    return tabela
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    res = 0
    for i in range(slika.shape[0]):
        for j in range(slika.shape[1]):
            if (barva_koze[0] < slika[i][j][0] < barva_koze[3] and barva_koze[1] < slika[i][j][1] < barva_koze[4]
                and barva_koze[2] < slika[i][j][2] < barva_koze[5]):
                    res += 1
    return res

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
    return tuple([int(g) - tolerance, int(b) - tolerance, int(r) - tolerance, int(g) + tolerance,
                 int(b) + tolerance, int(r) + tolerance])

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

def staro_barvanje():
    for i in range(0, camy, y):
        for j in range(0, camx, x):
            tempx = x
            tempy = y
            if (j + x > camx):
                tempx = camx - j
            if (i + y > camy):
                tempy = camy - i
            barva = povprecna_barva(frame[i:i + y, j:j + x], tempx, tempy)
            if (skin[0] + tolerance > barva[0] > skin[0] - tolerance and
                    skin[1] + tolerance > barva[1] > skin[1] - tolerance and
                    skin[2] + tolerance > barva[2] > skin[2] - tolerance):
                cv.rectangle(frame, (j, i), (j + x, i + y), (0, 255, 0), 2)
            else:
                cv.rectangle(frame, (j, i), (j + x, i + y), (0, 0, 255), 1)

def odstrani_osamelce(skatle):
    removed = 0
    for i in range(0, len(skatle) - 1):
         for j in range(0, len(skatle[0]) -1):
            if skatle[i][j] == 1:
                if(skatle[i + 1][j] != 1 and skatle[i][j+1] != 1 and skatle[i - 1][j] != 1
                and skatle[i][j -1] != 1):
                    skatle[i][j] = 0
                    removed +=1
    #print(removed)
    return skatle

def izrisi_skatle(slika, skatle, sirina_skatle, visina_skatle):
    for i in range(0, len(skatle)):
        for j in range(0, len(skatle[i])):
            if skatle[i][j] == 1:
                cv.rectangle(slika, (j*sirina_skatle, i*visina_skatle), ((j+1) * sirina_skatle, (i + 1) * visina_skatle), (0, 255, 0), 3)
            else:
                cv.rectangle(slika, (j * sirina_skatle, i * visina_skatle),((j + 1) * sirina_skatle, (i + 1) * visina_skatle), (0, 0, 255), 1)

    return slika

if __name__ == '__main__':
    # Pripravi kamero
    camy = 220
    camx = 340
    odstrani = True
    x = 4
    y = 4
    tolerance = 40
    start_time = time.time()
    skin = 0
    camera = cv.VideoCapture(0)
    ret, frame = camera.read()
    num = 0
    complete = True
    while True:
        ret, frame = camera.read()
        if ret:
            frame = cv.flip(frame, 1)
            frame = zmanjsaj_sliko(frame, camx, camy)
            if num < 40 and complete:
                frame = cv.rectangle(frame, [140, 50], [210,150], (255, 0, 0), 3)
            elif num == 40 and complete:
                skin = doloci_barvo_koze(frame, [140, 50], [210, 150])
                print(skin)
                complete = False
            else:
                skatle = obdelaj_sliko_s_skatlami(frame, x, y, skin)
                if odstrani:
                    skatle = odstrani_osamelce(skatle)
                frame = izrisi_skatle(frame, skatle, x, y)
                fps = num / (time.time() - start_time)
                start_time = time.time()

                num = 0
                #cv.imshow
            num += 1
            cv.imshow('frame', frame)
        if(cv.waitKey(1) & 0xFF == ord('q')):
            break
        if(cv.waitKey(1) & 0xFF == ord('x')):
            if odstrani:
                print("brez odstranjevanja")
                odstrani = False
            else:
                print("z odstranjevanjem")
                odstrani = True

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