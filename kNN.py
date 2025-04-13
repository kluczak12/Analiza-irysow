import csv, matplotlib.pyplot as plt

def wczytaj_dane(plik):
    with open(plik) as f:
        return [[float(x) for x in rzad] for rzad in csv.reader(f)]

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
    pom = (pom / (len(tablica) - 1)) ** 0.5
    return pom

def standaryzacjaZ(tablica):
    daneZnormalizowane = []
    for i in range(len(tablica)):
        wiersz = []
        for j in range(len(tablica[0])):
            if j != nrKolGatunku:
                if odchylenie(tablica, j) != 0:
                    pom = (tablica[i][j] - srednia(tablica, j))/odchylenie(tablica, j)
                    wiersz.append(pom)
                else:
                    wiersz.append(0)
        daneZnormalizowane.append(wiersz)
    return daneZnormalizowane

def odleglosc(punkt1, punkt2):
    pom = 0
    for i in range(len(punkt1)):
        pom += (punkt1[i] - punkt2[i]) ** 2
    return pom

def wyborMaxGatunku(tablica):
    maxIndexGatunku = 0
    for i in range(1, len(tablica)):
        if tablica[i] > tablica[maxIndexGatunku]:
            maxIndexGatunku = i
    licznik = sum(1 for i in tablica if i == tablica[maxIndexGatunku])
    if licznik > 1:                         # czyli gdy więcej niż jedna wartość jest równa max
        maxIndexGatunku = -1                # remis, trochę jak rzucanie wyjątku
    return maxIndexGatunku                  #zwracamy pozycje elementu, czyli nr gatunku

#tworzymy tabele ze srednią i odchyleniem dla każdej kolumny tabeli treningowej oprócz tej z gatunkiem
def treningSredniejIOdchylenia():
    for j in range(len(tabelaTreningowa[0])):
        if j != nrKolGatunku:
            srednieTab.append(srednia(tabelaTreningowa, j))
            odchyleniaTab.append(odchylenie(tabelaTreningowa, j))

def punktTestowyStandaryzacja(punktTestowy):
    znormalizowanyTestowy=[]
    for i in range(len(punktTestowy)):
        if i != nrKolGatunku:
            if odchyleniaTab[i] != 0:
                znormalizowanyTestowy.append((punktTestowy[i]-srednieTab[i])/odchyleniaTab[i])
            else:
                znormalizowanyTestowy.append(0)
    return znormalizowanyTestowy

def kNajSasiadow(punktTestowyStand, k, przypadkiTreningowe):
    listaOdleglosciGatunkow = []
    #lista odleglosci od danego sąsiada i jego gatunek - tylko te informacje nas interesują przy wybieraniu dla punktu gatunku
    for i in range(len(przypadkiTreningowe)):
        listaOdleglosciGatunkow.append([odleglosc(punktTestowyStand, przypadkiTreningowe[i]), int(tabelaTreningowa[i][nrKolGatunku])])

    # lista zawierającą k najbliższych sąsiadów danego punktu
    kNajOdleglosciGatunkow = []
    for i in range(k):
        minOdleglosc = listaOdleglosciGatunkow[0][0]
        minIndex = 0
        for j in range(1, len(listaOdleglosciGatunkow)):
            if listaOdleglosciGatunkow[j][0] < minOdleglosc:
                minOdleglosc = listaOdleglosciGatunkow[j][0]
                minIndex = j

        # po przejściu całej listy listaOdleglosciGatunkow dodaje element minimalny do drugiej listy
        kNajOdleglosciGatunkow.append(listaOdleglosciGatunkow[minIndex])
        #usuwamy min element, żeby funkcja znalazła kolejną najmniejszą wartość
        listaOdleglosciGatunkow.pop(minIndex)

    sumaGatunkowSasiadow = [0] * liczbaGatunkow         #do zsumowania gatunków najbliższych sąsiadów
    for wiersz in kNajOdleglosciGatunkow:
        sumaGatunkowSasiadow[wiersz[1]] += 1

    return wyborMaxGatunku(sumaGatunkowSasiadow)        # tutaj kończy się algorytm k najblizszych sasiadow i zaczyna problem remisów

def program(punktTestowyStand, k, przypadkiTreningowe):
    wybranyGatunek = kNajSasiadow(punktTestowyStand, k, przypadkiTreningowe)
    while (wybranyGatunek == -1 and k > 1):
        k -= 1
        wybranyGatunek = kNajSasiadow(punktTestowyStand, k, przypadkiTreningowe)
    return wybranyGatunek           #zwracamy uzyskany gatunek punktu

def wyborKolumn(kolumna1, kolumna2):
    ograniczonaTestowa = []
    ograniczonaTreningowa = []
    for i in range(len(testoweStand)):
        ograniczonaTestowa.append([testoweStand[i][kolumna1], testoweStand[i][kolumna2]])
    for i in range(len(treningoweStand)):
        ograniczonaTreningowa.append([treningoweStand[i][kolumna1], treningoweStand[i][kolumna2]])
    return ograniczonaTestowa, ograniczonaTreningowa

def przypisanieTabeli(tabela):
    tabelaPom = []
    for i in range(len(tabela)):
        tabelaPom.append(tabela[i])
    return tabelaPom

def glownyProgram(kolumna1, kolumna2, tytul):
    poprawnieDobrane = [0] * 15
    if kolumna1 == 4 & kolumna2 == 4:
        przypadkiTestowe = przypisanieTabeli(testoweStand)
        przypadkiTreningowe = przypisanieTabeli(treningoweStand)
    else:
        przypadkiTestowe, przypadkiTreningowe = wyborKolumn(kolumna1, kolumna2)
    macierzPomylekNaj = [[0, 0, 0] for _ in range(3)]
    najPoprawnych = 0
    for k in range(1,16):
        macierzPomylek = [[0, 0, 0] for _ in range(3)]
        for i in range(len(przypadkiTestowe)):
            wynik = int(program(przypadkiTestowe[i], k, przypadkiTreningowe))
            oczekiwany = int(tabelaTestowa[i][nrKolGatunku])
            if  wynik == oczekiwany:
                poprawnieDobrane[k-1] += 1
                macierzPomylek[wynik][wynik] += 1
            else:
                macierzPomylek[oczekiwany][wynik] += 1
        poprawnieDobrane[k-1] *= 100/len(przypadkiTestowe)
        if poprawnieDobrane[k-1] > najPoprawnych:
            najPoprawnych = poprawnieDobrane[k-1]
            macierzPomylekNaj = przypisanieTabeli(macierzPomylek)
    wykresZaleznosci(tytul, poprawnieDobrane)
    print(macierzPomylekNaj)

def wykresZaleznosci(tytul, poprawnieDobrane):
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, 16), poprawnieDobrane, color='palegreen', alpha=0.7)
    plt.title(tytul, fontsize=14)
    plt.xlabel("Liczba najbliższych sąsiadów (k)", fontsize=12)
    plt.ylabel("Poprawność (%)", fontsize=12)
    plt.xticks(range(1, 16))
    plt.ylim(60, 101)
    plt.show()

# Główny program
tabelaTreningowa = wczytaj_dane("data3_train.csv")
tabelaTestowa = wczytaj_dane("data3_test.csv")
nrKolGatunku = 4
liczbaGatunkow = int(max(rzad[nrKolGatunku] for rzad in tabelaTreningowa)) + 1
srednieTab = []
odchyleniaTab = []
treningoweStand = standaryzacjaZ(tabelaTreningowa)      #bez kolumny z gatunkiem
treningSredniejIOdchylenia()

testoweStand = []                                       #bez kolumny z gatunkiem
for wiersz in tabelaTestowa:
    testoweStand.append(punktTestowyStandaryzacja(wiersz))

glownyProgram(4, 4, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN dla 4 cech")
glownyProgram(0, 1, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla długości i szerokości działki kielicha")
glownyProgram(0, 2, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla długości działki kielicha i długości płatka")
glownyProgram(0, 3, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla długości działki kielicha i szerokości płatka")
glownyProgram(1, 2, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla szerokości działki kielicha i długości płatka")
glownyProgram(1, 3, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla szerokości działki kielicha i szerokości płatka")
glownyProgram(2, 3, "Poprawność przydziału punktu testowego do gatungu wg liczby kNN\n dla długości i szerokości płatka")