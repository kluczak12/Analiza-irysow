import csv, random, matplotlib.pyplot as plt, pandas as pd

plikIrysy = open("data2.csv")
tabelaDanych = [rzad for rzad in csv.reader(plikIrysy)]
plikIrysy.close()

for rzad in tabelaDanych:
    for i in range(len(rzad)):
        rzad[i] = float(rzad[i])

def srednia(tablica, kolumna):
    suma = 0
    for rzad in tablica:
        suma += rzad[kolumna]
    return suma / len(tablica)

def odchylenie(tablica, kolumna):
    pom = 0
    sredniaKolumny = srednia(tablica, kolumna)
    for rzad in tablica:
        pom += (rzad[kolumna] - sredniaKolumny) ** 2
    pom = (pom/(len(tablica)-1)) ** 0.5
    return pom

def standaryzacjaZ(tablica):
    daneZnormalizowane = []
    for i in range(len(tablica)):
        wiersz = []
        for j in range(len(tablica[0])):
            if odchylenie(tablica, j) != 0:
                pom = (tablica[i][j] - srednia(tablica, j))/odchylenie(tablica, j)
                wiersz.append(pom)
            else:
                wiersz.append(0)
        daneZnormalizowane.append(wiersz)
    return daneZnormalizowane

def deStandaryzacjaZ(tablica):
    daneZwykle = []
    for i in range(len(tablica)):
        wiersz = []
        for j in range(len(tablica[0])):
            if odchylenie(tabelaDanych, j) != 0:
                pom = tablica[i][j] * odchylenie(tabelaDanych, j) + srednia(tabelaDanych, j)
                wiersz.append(pom)
            else:
                wiersz.append(srednia(tabelaDanych, j))
        daneZwykle.append(wiersz)
    return daneZwykle

def losowanieCentroidow(tabelaStand, ilosc):
    return random.sample(tabelaStand, ilosc)

def odlegloscPC(punkt, centroid):
    pom = 0
    for i in range(len(punkt)):
        pom += (punkt[i] - centroid[i]) ** 2
    return pom

def wyborCentroidu(punkt, centroidy):
    aktualnaOdleglosc = odlegloscPC(punkt, centroidy[0])
    wybor = 0
    for i in range(1, len(centroidy)):
        if odlegloscPC(punkt, centroidy[i]) < aktualnaOdleglosc:
            aktualnaOdleglosc = odlegloscPC(punkt, centroidy[i])
            wybor = i

    return wybor

def srodekCiezkosci(klaster):
    if not klaster:
        return [0] * len(tabelaDanych[0])
    srodek = []
    for i in range(len(klaster[0])):
        srodek.append(srednia(klaster, i))
    return srodek

def WCSS(klastry, centroidy):
    WCSS = 0
    for i in range(len(klastry)):
        for j in range(len(klastry[i])):
            WCSS += odlegloscPC(klastry[i][j], centroidy[i])
    return WCSS

def wykresPunktowy(nrKolumnaX, nrKolumnaY, etykietaX, etykietaY, centroidy, ktoryKlaster):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    for i in range(len(ktoryKlaster)):
        if ktoryKlaster[i]==0:
            x1.append(tabelaDanych[i][nrKolumnaX])
            y1.append(tabelaDanych[i][nrKolumnaY])
        elif ktoryKlaster[i] == 1:
            x2.append(tabelaDanych[i][nrKolumnaX])
            y2.append(tabelaDanych[i][nrKolumnaY])
        else:
            x3.append(tabelaDanych[i][nrKolumnaX])
            y3.append(tabelaDanych[i][nrKolumnaY])

    cx1 = centroidy[0][nrKolumnaX]
    cy1 = centroidy[0][nrKolumnaY]
    cx2 = centroidy[1][nrKolumnaX]
    cy2 = centroidy[1][nrKolumnaY]
    cx3 = centroidy[2][nrKolumnaX]
    cy3 = centroidy[2][nrKolumnaY]

    plt.scatter(x1, y1, c="mediumpurple",s=50)
    plt.scatter(x2, y2, c="palegreen", s=50)
    plt.scatter(x3, y3, c="skyblue",s=50)
    plt.scatter(cx1, cy1, c="mediumpurple",linewidths=2,marker="d", edgecolors="darkviolet", s=200)
    plt.scatter(cx2, cy2, c="palegreen",linewidths=2,marker="d", edgecolors="seagreen",s=200)
    plt.scatter(cx3, cy3, c="skyblue",linewidths=2,marker="d", edgecolors="steelblue",s=200)
    plt.xlabel(etykietaX, fontsize=14)
    plt.ylabel(etykietaY, fontsize=14)
    plt.show()

def kSrednich(liczbaCentroidow):
    dStandaryzowane = standaryzacjaZ(tabelaDanych)
    centroidyStand = losowanieCentroidow(dStandaryzowane, liczbaCentroidow)
    czyZmiana = True
    iterator = 0
    wcss = 0
    klastry = []
    ktoryKlaster = []
    while(czyZmiana):
        klastry = [[] for _ in range(liczbaCentroidow)]
        ktoryKlaster = [0] * len(tabelaDanych)

        numer=0
        for punkt in dStandaryzowane:
            klastry[wyborCentroidu(punkt, centroidyStand)].append(punkt)
            ktoryKlaster[numer] = wyborCentroidu(punkt, centroidyStand)
            numer+=1

        srodki = []
        for klaster in klastry:
            srodki.append(srodekCiezkosci(klaster))

        if centroidyStand == srodki:
            czyZmiana = False
            wcss = WCSS(klastry, centroidyStand)

        centroidyStand = srodki
        iterator += 1
    return centroidyStand, iterator, wcss, klastry, ktoryKlaster

def najlepszekSrednich(liczbaWywolan, k):
    najCentroidy, najIteracja, najWCSS, najKlastry, najListaPunktow = kSrednich(k)
    for i in range(1,liczbaWywolan):
        nCentroidy, nIterator, nWCSS, nklastry, nktoryKlaster = kSrednich(k)
        if (nWCSS < najWCSS):
            najWCSS = nWCSS
            najIteracja = nIterator
            najCentroidy = nCentroidy
            najListaPunktow = nktoryKlaster
            najKlastry = nklastry
    return najCentroidy, najIteracja, najWCSS, najKlastry, najListaPunktow

def wykresZaleznosci(tablicaWCSS, tablicaK):
    plt.figure(figsize=(8, 6))
    plt.plot(tablicaK, tablicaWCSS, marker='o', color='b', linestyle='-', markersize=8)
    plt.title("Zależność WCSS od liczby klastrów (k)", fontsize=14)
    plt.xlabel("Liczba klastrów (k)", fontsize=12)
    plt.ylabel("WCSS", fontsize=12)
    plt.xticks(tablicaK)
    plt.show()

iloscK = []
wcssTabela = []
iteratory = []
iterator3 = 0
numeryKlastrow3 = []
wcss3 = 0
centroidy3 = []
klastry3 = []

for k in range(2,11):
    gCentroidy, gIterator, gWCSS, gklastry, gktoryKlaster = najlepszekSrednich(10, k)
    iteratory.append(gIterator)
    wcssTabela.append(gWCSS)
    iloscK.append(k)

    if k == 3:
        iterator3 = gIterator
        wcss3 = gWCSS
        numeryKlastrow3 = gktoryKlaster
        centroidy3 = gCentroidy
        klastry3 = gklastry

tabela = pd.DataFrame({
    "Liczba klastrów": iloscK,
    "Liczba iteracji": iteratory,
    "WCSS": wcssTabela
})
print("Tabela 1. Wartości WCSS oraz ilości iteracji dla poszczególnych wartości k.")
print(tabela.to_string(index=False, justify='center'))

centroidy3 = deStandaryzacjaZ(centroidy3)
wykresZaleznosci(wcssTabela, iloscK)

wykresPunktowy(0, 1, "Długość działki kielicha (cm)", "Szerokość działki kielicha (cm)", centroidy3, numeryKlastrow3)
wykresPunktowy(0, 2, "Długość działki kielicha (cm)", "Długość płatka (cm)", centroidy3, numeryKlastrow3)
wykresPunktowy(0, 3, "Długość działki kielicha (cm)", "Szerokość płatka (cm)", centroidy3, numeryKlastrow3)
wykresPunktowy(1, 2, "Szerokość działki kielicha (cm)", "Długość płatka (cm)", centroidy3, numeryKlastrow3)
wykresPunktowy(1, 3, "Szerokość działki kielicha (cm)", "Szerokość płatka (cm)", centroidy3, numeryKlastrow3)
wykresPunktowy(2, 3, "Długość płatka (cm)", "Szerokość płatka (cm)", centroidy3, numeryKlastrow3)