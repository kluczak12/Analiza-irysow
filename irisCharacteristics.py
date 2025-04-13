import csv
import pandas as pd
from matplotlib import pyplot as plt

def minimum(nrKolumny):
    min = tabelaDanych[0][nrKolumny]
    for i in range(1, N):
        if tabelaDanych[i][nrKolumny] < min:
            min = tabelaDanych[i][nrKolumny]
    return min

def maksimum(nrKolumny):
    max = tabelaDanych[0][nrKolumny]
    for i in range(1, N):
        if tabelaDanych[i][nrKolumny] > max:
            max = tabelaDanych[i][nrKolumny]
    return max

def sredniaAr(nrKolumny):
    suma = 0.0
    for rzad in tabelaDanych:
        suma += rzad[nrKolumny]
    return suma / N

def wariancja(nrKolumny):
    pom = 0.0
    sredniaKolumny = sredniaAr(nrKolumny)
    for rzad in tabelaDanych:
        pom += (rzad[nrKolumny] - sredniaKolumny) ** 2
    return pom / (N - 1)

def odchylenie(kolumna):
    return wariancja(kolumna) ** 0.5

def sortowanie(nrKolumny):
    pomTablica = []
    for rzad in tabelaDanych:
        pomTablica.append(rzad[nrKolumny])
    for i in range(N):
        for j in range(N - 1):
            if pomTablica[j] > pomTablica[j+1]:
                pom = pomTablica[j]
                pomTablica[j] = pomTablica[j+1]
                pomTablica[j + 1] = pom
    return pomTablica

def mediana(tab):
    if N % 2 != 0:
        return tab[(N - 1) // 2]                    #w tablicy indeksujemy od 0, więc zamiast n+1 jest n-1
    return (tab[N // 2] + tab[N // 2 - 1]) / 2

def kwartylDolny(tab):
    if N % 2 != 0:
        n = (N - 1) // 2
        if n % 2 != 0:
            return tab[(n - 1) // 2]
        return (tab[n // 2] + tab[n // 2 - 1]) / 2
    n = (N - 2) // 2
    if n % 2 != 0:
        return tab[(n - 1) // 2]
    return (tab[n // 2] + tab[n // 2 - 1]) / 2

def kwartylGorny(tab):
    if N % 2 != 0:
        n = (N - 1) // 2
        if n % 2 != 0:
            return tab[N - 1 - (n - 1) // 2]
        return (tab[N - 1 - n // 2] + tab[N - n // 2]) / 2
    n = (N - 2) // 2
    if n % 2 != 0:
        return tab[N - 1 - (n - 1) // 2]
    return (tab[N - 1 - n // 2] + tab[N - n // 2]) / 2

def kowariancja(kolumnaX, kolumnaY):
    iloczyn = 0
    sredniaDanejX = sredniaAr(kolumnaX)
    sredniaDanejY = sredniaAr(kolumnaY)
    for rzad in tabelaDanych:
        iloczyn += ((rzad[kolumnaX] - sredniaDanejX) * (rzad[kolumnaY] - sredniaDanejY))
    return iloczyn / (N - 1)

def wspolczynnikPearsona(kolumnaX, kolumnaY):
    return kowariancja(kolumnaX, kolumnaY) / (odchylenie(kolumnaX) * odchylenie(kolumnaY))

def wspolczynnikA(kolumnaX, kolumnaY):
    if wariancja(kolumnaX) == 0:
        return 0
    return kowariancja(kolumnaX, kolumnaY) / wariancja(kolumnaX)

def wspolczynnikB(kolumnaX, kolumnaY):
    pomA = wspolczynnikA(kolumnaX, kolumnaY)
    sredniaX = sredniaAr(kolumnaX)
    sredniaY = sredniaAr(kolumnaY)
    return sredniaY - (pomA * sredniaX)

def przedzialy(poczatek, koniec, iloscPrzedzialow):
    dlugoscPodzialki = (koniec - poczatek) / iloscPrzedzialow
    podzialka = [poczatek + (dlugoscPodzialki * ktoraPodzialka) for ktoraPodzialka in range(0, iloscPrzedzialow + 1)]
    return podzialka

def maxPrzedzial(podzialka, kolumna):
    pomTab = []
    sortKolumna = sortowanie(kolumna)
    index = 0
    for i in range(len(podzialka)):
        pomTab.append(0)

    for i in range(len(podzialka)-1):
        while index < len(sortKolumna) and sortKolumna[index] < podzialka[i+1] and sortKolumna[index] >= podzialka[i]:
            pomTab[i]+=1
            index += 1
    max=pomTab[0]
    for i in pomTab:
        if i > max:
            max = i
    if max <= round(max,-1):
        return round(max,-1)
    return round(max,-1)+5

def histogram(poczatek, koniec, iloscPrzedzialow, nrKolumny, tytul, etykietaX, limitY):
    pomTablica = [rzad[nrKolumny] for rzad in tabelaDanych]
    plt.figure(figsize=[7, 5])
    plt.hist(pomTablica, bins=przedzialy(poczatek, koniec, iloscPrzedzialow), ec="black")
    plt.title(tytul, fontsize=16)
    plt.ylim(0, limitY)
    plt.xlabel(etykietaX, fontsize=14)
    plt.ylabel("Liczebność", fontsize=14)
    plt.tick_params(axis="both", labelsize=12)
    plt.subplots_adjust(right=0.98, bottom=0.14)
    plt.show()

def histogramPudelkowy(poczatek, koniec, iloscPrzedzialow, kolumna, etykietaY):
    kolumna_wartosc = "Wartość"
    kolumna_gatunek = "Gatunek"
    data = pd.DataFrame({
        kolumna_wartosc: [rzad[kolumna] for rzad in tabelaDanych],
        kolumna_gatunek: [rzad[kolumnaGatunkow] for rzad in tabelaDanych]
    })

    plt.figure(figsize=[7, 5])
    data.boxplot(column=kolumna_wartosc, by=kolumna_gatunek, grid=False, whiskerprops = dict(color="black"),
                 boxprops = dict(color="black"), medianprops = dict(color="orange"))
    plt.yticks(przedzialy(poczatek, koniec, iloscPrzedzialow))
    plt.ylim(poczatek, koniec)
    plt.ylabel(etykietaY, fontsize=14)
    plt.xlabel("Gatunek", fontsize=14)
    plt.title("", fontsize=16)
    plt.suptitle("")
    plt.tick_params(axis="both", labelsize=12)
    plt.subplots_adjust(right=0.98, bottom=0.14, left=0.13)
    plt.show()

def wykresPunktowy(nrKolumnaX, nrKolumnaY, etykietaX, etykietaY, poczatekX, koniecX, iloscPrzedzialowX, poczatekY, koniecY, iloscPrzedzialowY):
    pomTablicaX = [rzad[nrKolumnaX] for rzad in tabelaDanych]
    pomTablicaY = [rzad[nrKolumnaY] for rzad in tabelaDanych]
    podzialkaX = przedzialy(poczatekX, koniecX, iloscPrzedzialowX)
    podzialkaY = przedzialy(poczatekY, koniecY, iloscPrzedzialowY)

    plt.xlim(poczatekX-0.1, koniecX+0.1)
    plt.scatter(pomTablicaX, pomTablicaY, s=100)
    plt.xticks(podzialkaX)
    plt.yticks(podzialkaY)
    r = str(round(wspolczynnikPearsona(nrKolumnaX, nrKolumnaY), 2))
    a = str(round(wspolczynnikA(nrKolumnaX, nrKolumnaY), 1))
    b = round(wspolczynnikB(nrKolumnaX, nrKolumnaY), 1)
    if(b >= 0):
        b = "+ "+str(b)
    else:
        b = "- "+str(b*(-1))
    tytul = "r = "+r+" y = "+a+"x "+b

    plt.title(tytul, fontsize=16)
    plt.subplots_adjust(left=0.15)
    plt.subplots_adjust(bottom=0.15)
    pomYProstej =[x * wspolczynnikA(nrKolumnaX, nrKolumnaY) + wspolczynnikB(nrKolumnaX, nrKolumnaY) for x in pomTablicaX]
    plt.plot(pomTablicaX, pomYProstej, color="red")
    plt.xlabel(etykietaX, fontsize=14)
    plt.ylabel(etykietaY, fontsize=14)
    plt.tick_params(axis="both", labelsize=12)
    plt.show()

#WCZYTANIE DANYCH
plikIrysy = open("data1.csv")
tabelaDanych = [rzad for rzad in csv.reader(plikIrysy)]
plikIrysy.close()

kolumnaGatunkow = 4
for rzad in tabelaDanych:
    for i in range(len(rzad)):
        if i != kolumnaGatunkow:
            rzad[i] = float(rzad[i])
        else:
            if (rzad[i] == "0"):
                rzad[i] = "setosa"
            elif (rzad[i] == "1"):
                rzad[i] = "versicolor"
            elif (rzad[i] == "2"):
                rzad[i] = "virginica"

#TABELA 1
daneGatunkow = []
for rzad in tabelaDanych:
    gatunek = rzad[kolumnaGatunkow]
    czyDodany = False
    for i in range(len(daneGatunkow)):
        if daneGatunkow[i][0] == gatunek:
            daneGatunkow[i][1] += 1
            czyDodany = True
            break
    if not czyDodany:
        daneGatunkow.append([gatunek, 1])

N = len(tabelaDanych)       #liczba elementów w kolumnie
daneGatunkow.append(["Razem", N])
for i in range(len(daneGatunkow)):
    udzial = round(daneGatunkow[i][1] / N * 100, 1)
    daneGatunkow[i][1] = str(daneGatunkow[i][1]) + " (" + str(udzial) + "%)"

tabela1 = pd.DataFrame(daneGatunkow, columns=["Gatunek", "Liczebność (%)"])
print(tabela1.to_string(index=False))       #pominięcie indeksów wierszy

#Tabela 2
opisCech = []
for kolumna in range(len(tabelaDanych[0])):
    if kolumna != kolumnaGatunkow:
        opisCech.append([kolumna, f"{minimum(kolumna):.2f}", str(f"{sredniaAr(kolumna):.2f}") + " (±" + str(f"{odchylenie(kolumna):.2f}") + ")",
                         str(f"{mediana(sortowanie(kolumna)):.2f}") + " (" + str(f"{kwartylDolny(sortowanie(kolumna)):.2f}") + " - " +
                         str(f"{kwartylGorny(sortowanie(kolumna)):.2f}") +  ")", f"{maksimum(kolumna):.2f}"])

opisCech[0][0] = "Długość działki kielicha (cm)"
opisCech[1][0] = "Szerokość działki kielicha (cm)"
opisCech[2][0] = "Długość płatka (cm)"
opisCech[3][0] = "Szerokość płatka (cm)"

tabela2 = pd.DataFrame(opisCech, columns=["Cecha", " Minimum ", " Śr. arytm. (± odch. stand.) ", " Mediana (Q1 - Q3) ", " Maksimum"])
print(tabela2.to_string(index=False, justify='center'))

histogram(4.0, 8.0, 8, 0, "Długość działki kielicha","Długość (cm)", maxPrzedzial(przedzialy(4.0, 8.0, 8), 0))
histogram(2.0, 4.5, 5, 1, "Szerokość działki kielicha","Szerokość (cm)", maxPrzedzial(przedzialy(2.0, 4.5, 5), 1))
histogram(1.0, 7.0, 12, 2, "Długość płatka","Długość (cm)", maxPrzedzial(przedzialy(1.0, 7.0, 12), 2))
histogram(0.0, 2.5, 10, 3, "Szerokość płatka","Szerokość (cm)", maxPrzedzial(przedzialy(0.0, 2.5, 10), 3))

histogramPudelkowy(4.0, 8.0, 4, 0, "Długość (cm)")
histogramPudelkowy(1.5, 4.5, 5, 1, "Szerokość (cm)")
histogramPudelkowy(0.5, 7.0, 5, 2, "Długość (cm)")
histogramPudelkowy(0.0, 3.0, 4, 3, "Szerokość (cm)")

wykresPunktowy(0, 1, opisCech[0][0], opisCech[1][0], 4.0, 8.0, 4, 2.0, 4.5, 5)
wykresPunktowy(0, 2, opisCech[0][0], opisCech[2][0], 4.0, 8.0, 4, 1.0, 7.0, 4)
wykresPunktowy(0, 3, opisCech[0][0], opisCech[3][0], 4.0, 8.0, 4, 0.0, 2.5, 5)
wykresPunktowy(1, 2, opisCech[1][0], opisCech[2][0], 2.0, 4.5, 5, 1.0, 7.0, 4)
wykresPunktowy(1, 3, opisCech[1][0], opisCech[3][0], 2.0, 4.5, 5, 0.0, 2.5, 5)
wykresPunktowy(2, 3, opisCech[2][0], opisCech[3][0], 1.0, 7.0, 4, 0.0, 2.5, 5)