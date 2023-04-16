import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import random
import mplcursors

#funkcije:
def odstrani(slovar, a, b): #sprejme slovar in meji
    '''funkcija bo vrnila slovar samo z željenimi ključi'''
    kljuci = list(slovar.keys()) #tabela ključev
    ostalo = dict() #shranimo kar ne potrebujemo
    for i in range(a, b):
        ostalo[kljuci[i]] = slovar[kljuci[i]]
        del slovar[kljuci[i]] #odstranimo ključe na izbranih mestih
    return slovar, ostalo #vrne dva slovarja

def povprecje(slovar): 
    '''vrne povprečno vrednost, od vrednosti v slovarju'''
    vrednosti = [] #shranimo vse vr. v slovarju
    for vr in slovar.values():
        vrednosti.append(vr)
    povprecna = sum(float(x) for x in vrednosti) / len(vrednosti) # izračuna povprečno vr. 
    return round(povprecna, 2) #vrne povprečno vr. zaokroženo na dve decimalni mesti

def uredi(slovar):
    '''uredi slovar po vrednostih od min do max'''
    urejen = {k: v for k, v in sorted(slovar.items(), key=lambda item: float(item[1]))} 
    return urejen

def izbrane(slovar, a, b):
    '''vrne slovar z izbranimi kljuci'''
    kljuci = list(slovar.keys())
    nov = dict()
    for i in range(a, b):
        nov[kljuci[i]] = slovar[kljuci[i]]
    return nov

def izpis_vr(sel): #sel se nanaša na objekt mplcursors._Selection # dostopamo do lastnosti objekta sel
    '''funkcija omogoči, da ko se pomaknemo s miško po grafu se nam izpiše vrednost grafa'''
    artist = sel.artist #ustreza izbrani vrstici
    value = sel.target[0] #vrne zbirko položaja (x, y) kazalca miške znotraj koordinatnega sistema izbranega Artista
    label = artist.get_label()
    annotation_text = f'{label}: {value:.1f}'
    sel.annotation.set_text(annotation_text)

def graf(slovar, naslov):
    '''nariše graf slovarja'''
    drzave = list(slovar.keys())
    st = [float(st) for st in slovar.values()]
    f, x = plt.subplots()
    colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(drzave))] #nabor naključnih barv
    x.barh(drzave, st, color=colors) 
    bars = x.barh(drzave, st, color=colors) # vsaka država svojo barvo
    x.set_ylabel('Države')
    plt.yticks(rotation=0)
    x.set_xlabel('Št. samomorov na 100,000 prebivalcev')
    x.set_xlim([0, max(st)*1.1])
    x.set_title(naslov)
    st_smrti = mplcursors.cursor(bars, hover=True)
    st_smrti.connect('add', izpis_vr)
    plt.show()
    
def odstrani_napacne(slovar): #nekatere države so bile čudno izpisane, tu jih popravimo
    '''ostrani napačne znake pri imenih'''
    slovar1 = {k.replace('\u202f*', ''): v for k, v in slovar.items()}
    return slovar1

#web scraping
url = "https://en.wikipedia.org/wiki/List_of_countries_by_suicide_rate"
wiki = requests.get(url)
soup = BeautifulSoup(wiki.content, 'html.parser')
tabela = soup.find_all('table')[1]


#slovarji s podatki po državah
vsi = {}
moski = {}
zenske = {}

for vrsta in tabela.find_all('tr'):
    celica = vrsta.find_all(['th', 'td'])
    
    if len(celica) >= 4:
        drzava = celica[0].get_text(strip=True)
        vsi_podatki = celica[1].get_text(strip=True)
        moski_podatki = celica[2].get_text(strip=True)
        zenske_podatki = celica[3].get_text(strip=True)
        
        if drzava != '':
            vsi[drzava] = vsi_podatki
            moski[drzava] = moski_podatki
            zenske[drzava] = zenske_podatki
            
del vsi['Country']
del moski['Country']
del zenske['Country']

vsi = odstrani_napacne(vsi)
moski = odstrani_napacne(moski)
zenske = odstrani_napacne(zenske)

#ločimo slovarje z državami, celinami in globalim
vsi, vsi_celine = odstrani(vsi, -7, 0)
moski, moski_celine = odstrani(moski, -7, 0)
zenske, zenske_celine = odstrani(zenske, -7, 0)

vsi_celine, vse_vsi = odstrani(vsi_celine, -1, 0)
moski_celine, vse_moski= odstrani(moski_celine, -1, 0)
zenske_celine, vse_zesnke = odstrani(zenske_celine, -1, 0)

#povprečja:
povp_vsi_drzave = povprecje(vsi)
povp_moski_drzave = povprecje(moski)
povp_zenske_drzave = povprecje(zenske)

#max 10 držav:
max_vsi_drzave = izbrane(uredi(vsi), -10, 0)
max_moski_drzave = izbrane(uredi(moski), -10, 0)
max_zenske_drzave = izbrane(uredi(zenske), -10, 0)

#min 10 držav:
min_vsi_drzave = izbrane(uredi(vsi), 0, 11)
min_moski_drzave = izbrane(uredi(moski), 0, 11)
min_zenske_drzave = izbrane(uredi(zenske), 0, 11)

#evropske države
url1 = 'https://en.wikipedia.org/wiki/List_of_European_countries_by_area'
wiki1 = requests.get(url1)
soup1 = BeautifulSoup(wiki1.content, 'html.parser')
tabela1 = soup1.find('table', class_='wikitable sortable')
vrste = tabela1.find_all('tr')[1:]  #spusti prvo vrstico

eu_drzave = []
for vrsta in vrste:
    celice1 = vrsta.find_all('td')
    try:
        drzava = celice1[1].get_text(strip=True)
        eu_drzave.append(drzava)
    except IndexError:
        continue  #spusti manjkajoče celice

eu_drzave1 = [c.replace('*', '') for c in eu_drzave]

eu_vsi = dict()
eu_moski = dict()
eu_zenske = dict()
for dr in eu_drzave1:
    if dr in vsi:
        eu_vsi[dr] = vsi[dr]
        eu_moski[dr] = moski[dr]
        eu_zenske[dr] = zenske[dr]
        
#izbrana država:
vse_drzave = list(vsi.keys())

def izbrana_dr(drzava):
    '''prikaže podatke za točno določeno državo'''
    vsi_dr = vsi[drzava]
    m_dr = moski[drzava]
    z_dr = zenske[drzava]
    return 'V ' + drzava + ' je bilo leta 2019, ' + vsi_dr + ' samomorov na 100,000 prebivalcev.\n' + 'Moških samomorov je bilo ' + m_dr + ' na 100,000 moških, ženskih pa ' + z_dr + ' na 100,000 žensk.'
        
#Začetek programa
print('Pozdravljeni!\n' +
      'V tem programu sva analizirali podatke o samomorilnosti ljudi v letu 2019. Pripravili sva nekaj analiz in grafov, ki si jih lahko ogledate tako, da vpišete številko pred željeno analizo.\n' +
      '1: Število samomorov v letu 2019 v različnih državah in njihovo povprečje.\n' +
      '2: Število moških samomorov v letu 2019 v različnih državah in njihovo povprečje.\n' +
      '3: Število ženskih samomorov v letu 2019 v različnih državah in njihovo povprečje.\n' +
      '4: Število samomorov v letu 2019 na različnih celinah + graf.\n' +
      '5: Število moških samomorov v letu 2019 na različnih celinah + graf.\n' +
      '6: Število ženskih samomorov v letu 2019 na različnih celinah + graf.\n' +
      '7: Grafični prikaz 10 držav z največjim številom samomorov v letu 2019.\n' +
      '8: Grafični prikaz 10 držav z največjim številom samomorov moških v letu 2019.\n' +
      '9: Grafični prikaz 10 držav z največjim številom samomorov žensk v letu 2019.\n' +
      '10: Grafični prikaz 10 držav z najmanjšim številom samomorov v letu 2019.\n' +
      '11: Grafični prikaz 10 držav z najmanjšim številom samomorov moških v letu 2019.\n' +
      '12: Grafični prikaz 10 držav z najmanjšim številom samomorov žensk v letu 2019.\n' +
      '13: Prikaz števila smrti v Evropi.\n' +
      '14: Prikaz podatkov za izbrano državo.\n' +
      'S pregledom analiz lahko zaključite tako, da vpišete število 0!') 
st = int(input('Katera analiza vas zanima? '))
while st != 0:
    if st == 1:
        print("Število samomorov na 100,000 prebivalcev leta 2019:")
        print(vsi)
        print('Povprečno število samomorov na 100,000 prebivalcev leta 2019:')
        print(povprecje(vsi))
    if st == 2:
        print("Število samomorov moških na 100,000 prebivalcev leta 2019:")
        print(moski)
        print('Povprečno število samomorov moških na 100,000 prebivalcev leta 2019:')
        print(povprecje(moski))
    if st == 3:
        print("Število samomorov žensk na 100,000 prebivalcev leta 2019:")
        print(zenske)
        print('Povprečno število samomorov žensk na 100,000 prebivalcev leta 2019:')
        print(povprecje(zenske))
    if st == 4:
        print("Število samomorov na 100,000 prebivalcev leta 2019 po celinah:")
        print(vsi_celine)
        graf(vsi_celine, 'Število samomorov na 100,000 prebivalcev leta 2019 po celinah')
    if st == 5:
        print("Število samomorov moških na 100,000 prebivalcev leta 2019 po celinah:")
        print(moski_celine)
        graf(moski_celine, 'Število samomorov moških na 100,000 prebivalcev leta 2019 po celinah')
    if st == 6:
        print("Število samomorov žensk na 100,000 prebivalcev leta 2019 po celinah:")
        print(zenske_celine)
        graf(zenske_celine, 'Število samomorov žensk na 100,000 prebivalcev leta 2019 po celinah')
    if st == 7:
        print('Države z največjim številom samomorov na 100,000 prebivalcev leta 2019: ')
        print(max_vsi_drzave)
        graf(max_vsi_drzave, 'Države z največjim številom samomorov na 100,000 prebivalcev leta 2019')
    if st == 8:
        print('Države z največjim številom samomorov moških na 100,000 prebivalcev leta 2019: ')
        print(max_moski_drzave)
        graf(max_moski_drzave, 'Države z največjim številom samomorov moških na 100,000 prebivalcev leta 2019')
    if st == 9:
        print('Države z največjim številom samomorov žensk na 100,000 prebivalcev leta 2019: ')
        print(max_zenske_drzave)
        graf(max_zenske_drzave, 'Države z največjim številom samomorov žensk na 100,000 prebivalcev leta 2019')
    if st == 10:
        print('Države z najmanjšim številom samomorov na 100,000 prebivalcev leta 2019: ')
        print(min_vsi_drzave)
        graf(min_vsi_drzave, 'Države z najmanjšim številom samomorov na 100,000 prebivalcev leta 2019')
    if st == 11:
        print('Države z najmanjšim številom samomorov moških na 100,000 prebivalcev leta 2019: ')
        print(min_moski_drzave)
        graf(min_moski_drzave, 'Države z najmanjšim številom samomorov moških na 100,000 prebivalcev leta 2019')
    if st == 12:
        print('Države z najmanjšim številom samomorov žensk na 100,000 prebivalcev leta 2019: ')
        print(min_zenske_drzave)
        graf(min_zenske_drzave, 'Države z najmanjšim številom samomorov žensk na 100,000 prebivalcev leta 2019')
    if st == 13:
        print('Število samomorov na 100,000 prebivalcev leta 2019 v Evropi: ')
        print(eu_vsi)
        print('Število samomorov moških na 100,000 prebivalcev leta 2019 v Evropi: ')
        print(eu_moski)
        print('Število samomorov žensk na 100,000 prebivalcev leta 2019 v Evropi: ')
        print(eu_zenske)
        graf(eu_vsi, 'Število samomorov na 100,000 prebivalcev leta 2019 v Evropi')
        graf(eu_moski, 'Število samomorov moških na 100,000 prebivalcev leta 2019 v Evropi')
        graf(eu_zenske, 'Število samomorov žensk na 100,000 prebivalcev leta 2019 v Evropi')
    if st == 14:
        print('Iz med spodnjih držav si izberite eno.')
        print(vse_drzave)
        izbrana = input('Izbrana država: ')
        print(izbrana_dr(izbrana))
    st = int(input('Katera analiza vas zanima? '))
print('Nasvidenje!')