# Toteutusdokumentti

## Ohjelman rakenne

Ohjelma on toteutettu eriyttäen sovelluslogiikka (entities ja services) ja käyttöliittymälogiikka (ui). Entity-mallinnettuna on käsite Grid, joka koostuu 
Cell-olioista taulukossa. Gridillä on tarkoitus mallintaa yleisemmällä tasolla jotakin ASCII-karttaa ja sitä luodessa konstruktori perkaa kartan ja luo "turvallisemman" rakenteen myöhemmälle käsittelylle.
Algoritmejä varten luodaan gridistä oma Graph-olio, joka koostuu Cell-luokan vastakohdan eli Node-luokan oliosta. Algoritmit siis käsittelevät tätä ylemmän tason
Graph-oliota.

Hahmottelin algoritmit palveluiksi (sovelluslogiikka), eli ne on services-paketin sisällä. Toteutetut Dijkstran algoritmi, JPS ja IDA* on tehty niin, että niiden toimintaa voidaan seurata ajon aikana generaattorin (next_step) avulla. Kaikki algoritmit perivät Algorithm-luokan, joka toteuttaa run()-metodin. Kutsumalla tätä metodia, voidaan etsiä polku annetussa kartassa (Grid) ilman väliaskelien ottamista.

Käyttöliittymä on toteutettu PyGame-kirjaston avulla. Käyttöliittymätason koodi on sijoitettu ui-pakettiin siten, että käyttöliittymäkoodia ei kutsuta erikseen tason 
ulkopuolelta. Suurin osa sen toteutuksesta tapahtuu ui/ui.py:n UI-luokassa, joka kysyy ajettavan algoritmin seuraavaa askelta aina, kun käyttäjä niin haluaa. 
Käyttöliittymätasolla on myös oma käsitteensä ruudukosta (Grid ja Cell), joista Cell perii PyGamen DirtySprite-luokan toiminnallisuuden. Tarkoituksena on helpottaa
ruudun päivitystä, kun tehdään yksittäisiin spriteihin muutoksia.

Karttojen luku tapahtuu src/repositories/maps_repositoryn MapRepository-luokan avulla. Luokka tukee [movingai.com](https://movingai.com/benchmarks/grids.html):n karttaformaattia. Kaikki ohjelman kartat ovat maps-hakemistossa projektin juuressa.

IDA* on valitettavasti sen verran hidas, että jouduin myös toteuttamaan sille ajastimen (services/timer.py), jonka avulla voidaan lopettaa ajo kesken, kun annettu aikaraja ylittyy.

Ohjelma käynnistetään ajamalla src/main.py. Antamalla lisäkomennon "timer" voidaan ajaa ajanotto testidatalle ilman graafista käyttöliittymää.

## Saavutetut aikavaativuudet

Dijkstran algoritmin toteutuksessa kutsutaan korkeintaan 8V kertaa min_heapistä poistoa, eli O(V log V). Jokaisella nodella joudutaan käymään läpi ja mahdollisesti
päivittämään 8 naapurin sijaa min-heapissä. Päivitys tapahtuu pushaamalla sama Node uudestaan kekoon pienemmällä etäisyydellä. Myöhemmät versiot samasta Nodesta
hylätään. Päivitys tapahtuu O(log V) ajassa. Yhteensä Dijkstran algoritmin toteutuksen aikavaativuus on siis O(V log V).

Jump Point Search (JPS) algoritmin toteutuksessa pyöritään while-loopissa next_step-metodissa. Jokaisella askeleella haetaan min-heapistä uusi alkio, jonka
toiminallisuus on sama kuin ylempänä eli yhteisaikavaativuus sille on O(V log V). Keon päivitys, kuten ylempänä, ei muuta aikavaativuutta. Pahimmassa tapauksessa JPS:n jump-funktiolla (JPS-luokan `_jump_in_direction`-metodi) joudutaan käymään kuitenkin läpi kaikki ruudukon ruudut. Aikaa per ruutu kuluu O(1) ja tämä nostaa
pahimman aikavaativuuden luokkaan O(V^2), kun [A*-algoritmin](https://en.wikipedia.org/wiki/A*_search_algorithm) aikavaativuus on luokkaa O(V). Hieman vähemmän avoimissa kartoissa näin ei kuitenkaan tapahdu, sillä eteenpäin hyppääminen törmää nopeasti joko seinään tai uuteen hyppypisteeseen. Ohjelman toteutuksessa tapaus esiintyy, kun ajetaan algoritmiä kartalla `maps/jps_loses.map`. Ongelmaa voisi korjata antamalla JPS:lle hyppyrajan, jonka jälkeen pakotetaan uusi hyppypiste kekoon ja hyppääminen lopetetaan kesken.

IDA*:n pahin aikavaativuus on [Wikipedian](https://en.wikipedia.org/wiki/Iterative_deepening_A*) nojalla luokkaa O(b^d). En osaa sanoa, miten paljon A*-heuristiikka auttaa haussa. Polkujahan kuitenkin syntyy todella suuria määriä, vaikka niiden pituus olisikin rajattu joka kerralla ja suuntaa ohjataan heuristisella etäisyydellä. Kaikki polut myös joudutaan käymään aina uudestaan ja uudestaan läpi joka kerta, kun rajaa (bound) kasvatetaan. Algoritmin hitaus näkyy heti, kun kartassa on muutamaa ruutua enemmän yhtenäistä seinää maalin edessä.

## Saavutetut tilavaativuudet

Dijkstran algoritmi on toteutettuna kartan ruudukon kokoisena taulukkona Nodeja, jotka sisältävät muutaman ylläpitoon liittyvän kentän. Graafin siirtymiä ei erikseen
säiltytetä missään, vaan ne haetaan taulukon muodosta (yhdellä nodella on korkeintaan 8 naapuria). Tallennus vie O(V) tilaa, jossa V on solmujen
määrä. Graphin avoimista Nodeista saadaan valittua Node, jolla on pienin etäisyys käyttämällä Pythonin heapq min-heap toteutusta (min-heapillä on tilavaativuus O(N)).
Yhteensä siis O(V).

JPS:n toteutus ei tarvitse lisärakenteita toimintaansa verrattuna Dijkstran algoritmiin, joten sen tilavaativuus on O(V).

IDA* ei tarvitse edes kekoa, mutta kuitenkin vaatii koko Graph-olion, joten senkin tilavaativuus on O(V). IDA*:n pino on toteutettu epäsuorasti käyttäen Graphin Node-olioiden previous-kenttää linkitetyn listan tavalla. Jos node-oliolla on previous-kenttä asetettuna, niin se katsotaan olevan iteratiivisella polulla.

## Suorituskyky

Testikartoissa on yleisesti käsinvalittu alku- ja maalipisteet niin, että polunhaussa olisi laskettavaa. Tuloksien mukaan suurimmassa osassa kartoista JPS saavuttaa huomattavia nopeusetuja verrattuna Dijkstraan.

Kaikkien 16 kartan keskiarvot:
```
Dijkstra: 1.145791875 s
JPS:      0.967255625 s, 0.17853625 s nopeampi
IDA*:     aivan liian hidas
```

Jos poistetaan kartat jps_loses.map, joka on tahallaan viritetty ansa JPS-algoritmille (maali on ihan vieressä seinän takana, mutta JPS joutuu tutkimaan koko miljoonan solun kartan hypyillä) ja maps/huge.map (suuri kartta, jossa on paljon tyhjää, mutta myös rakennuksia), niin keskiarvot ovat:

```
Dijkstra: 0.5431978571 s
JPS:      0.1077842857 s, 0.4354135714 s nopeampi (5x)
```

IDA* ei kuitenkaan ole ihan täysin huono, sillä se onnistuu pienillä avoimilla kartoilla ja kartassa, jossa on suora reitti maaliin (maps/lt_gallowsprison_n.map). Se myös voittaa JPS:n kartassa jps_loses.map.

```
Map file: maps/ht_store.map, 37x37 = 1369 cells.
Dijkstra average time taken: 0.00388 s
JPS average time taken: 0.00134 s
IDA* average time taken: 0.55902 s

Map file: maps/lt_gallowsprison_n.map, 116x242 = 28072 cells.
Dijkstra average time taken: 0.02716 s
JPS average time taken: 0.00242 s
IDA* average time taken: 0.00283 s
```

Ajamalla kaikki kartat maps-hakemistosta kummallakin algoritmillä antaa seuraavat tulokset:
```
Map file: maps/w_sundermount.map, 770x770 = 592900 cells.
Dijkstra average time taken: 0.34388 s
JPS average time taken: 0.08182 s
IDA* ran over time limit of 30 s
Found path length of 613 with a total cost of 702.71277.

Map file: maps/AR0012SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.32459 s
JPS average time taken: 0.05320 s
IDA* ran over time limit of 30 s
Found path length of 195 with a total cost of 223.40916.

Map file: maps/AR0400SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.78177 s
JPS average time taken: 0.18015 s
IDA* ran over time limit of 30 s
Found path length of 468 with a total cost of 548.60007.

Map file: maps/huge.map, 999x1050 = 1048950 cells.
Dijkstra average time taken: 10.72657 s
JPS average time taken: 10.55836 s
IDA* ran over time limit of 30 s
Found path length of 1615 with a total cost of 1805.78088.

Map file: maps/dr_0_deeproads.map, 560x733 = 410480 cells.
Dijkstra average time taken: 0.42451 s
JPS average time taken: 0.14326 s
IDA* ran over time limit of 30 s
Found path length of 875 with a total cost of 955.60007.

Map file: maps/ht_store.map, 37x37 = 1369 cells.
Dijkstra average time taken: 0.00388 s
JPS average time taken: 0.00134 s
IDA* average time taken: 0.55902 s
Found path length of 16 with a total cost of 17.48528.

Map file: maps/AR0700SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.50738 s
JPS average time taken: 0.09010 s
IDA* ran over time limit of 30 s
Found path length of 370 with a total cost of 480.42345.

Map file: maps/AR0516SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.40388 s
JPS average time taken: 0.08952 s
IDA* ran over time limit of 30 s
Found path length of 324 with a total cost of 367.73506.

Map file: maps/AR0011SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.30624 s
JPS average time taken: 0.31939 s
IDA* ran over time limit of 30 s
Found path length of 477 with a total cost of 503.75231.

Map file: maps/AR0203SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.16181 s
JPS average time taken: 0.30357 s
IDA* ran over time limit of 30 s
Found path length of 405 with a total cost of 485.18586

Map file: maps/AR0511SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.90013 s
JPS average time taken: 0.12486 s
IDA* ran over time limit of 30 s
Found path length of 379 with a total cost of 464.15642.

Map file: maps/lt_gallowsprison_n.map, 116x242 = 28072 cells.
Dijkstra average time taken: 0.02716 s
JPS average time taken: 0.00242 s
IDA* average time taken: 0.00283 s
Found path length of 122 with a total cost of 121.41421.

Map file: maps/lt_foundry_n.map, 109x92 = 10028 cells.
Dijkstra average time taken: 0.02990 s
JPS average time taken: 0.00593 s
IDA* ran over time limit of 30 s
Found path length of 67 with a total cost of 78.42641.

Map file: maps/AR0711SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.29289 s
JPS average time taken: 0.09415 s
IDA* ran over time limit of 30 s
Found path length of 616 with a total cost of 680.03153.

Map file: maps/ca_caverns1_mines.map, 324x597 = 193428 cells.
Dijkstra average time taken: 0.09675 s
JPS average time taken: 0.01927 s
IDA* ran over time limit of 30 s
Found path length of 201 with a total cost of 233.13708.

Map file: maps/jps_loses.map, 999x1050 = 1048950 cells.
Dijkstra average time taken: 0.00133 s
JPS average time taken: 3.40875 s
IDA* average time taken: 0.00040 s
Found path length of 8 with a total cost of 8.24264.
```

## Puutteet

Hieman kömpelö käyttöliittymä. Mahdollisuus esim. zoomata kartalla.

## Lähteet
- [PyGame](https://www.pygame.org/)
- [Binary Heap](https://en.wikipedia.org/wiki/Binary_heap)
- [Dijkstran algoritmi](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Pythonin heapq decrease_key toteutuksesta](https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes)
- [JPS](http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)
- [IDA*](https://en.wikipedia.org/wiki/Iterative_deepening_A*)
- [movingai.com:n kartat](https://www.movingai.com/benchmarks/bg512/index.html)

