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

JPS:n toteutuksessa käytettävän A*-algoritmin pahimman tapauksen aikavaativuus on O(b^d) Wikipedian mukaan ([A*](https://en.wikipedia.org/wiki/A*_search_algorithm)), jossa b on haarautuvuuskerroin ja d polun syvyys. Haarautuvuuskerrointa saa pienennettyä käyttämällä hyvää heurististafunktiota. Koska JPS:n toteutuksessa käytetään myös kekoa, niin pahimman aikavaativuuden voisi myös ajatella olevan luokkaa O(V log V) tapauksissa, missä joudutaan käymään läpi koko kartta. JPS käyttää hyppyoperaatioita vähentämään A*-kekoon laitettavien ruutujen määrää. Tätä varten on testikartoista löytyvät `maps/pillars-x.map` kartat suunniteltu niin, että JPS joutuu käyttämään silti noin puolet koko kartan vapaista ruuduista hyppypisteinä. Pahimman tapauksen aikavaativuus ei siis voi olla pienempi, kuin puhtaassa A* tapauksessa.

IDA*:n pahin aikavaativuus on [Wikipedian](https://en.wikipedia.org/wiki/Iterative_deepening_A*) esittelemän pseudokoodin nojalla luokkaa O(b^d) eli sama kuin [IDS](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search):n. Polkujahan kuitenkin syntyy todella suuria määriä, vaikka niiden pituus olisikin rajattu joka kerralla ja suuntaa ohjataan heuristisella etäisyydellä. Kaikki polut myös joudutaan käymään aina uudestaan ja uudestaan läpi joka kerta, kun rajaa (bound) kasvatetaan. Algoritmin hitaus näkyy heti, kun kartassa on muutamaa ruutua enemmän yhtenäistä seinää maalin edessä.

Vertailutesteissä algoritmien toteutuksien kuluneet ajat sopivat yllä olevien aikavaativuuksien olettamuksiin. Esim. tuplaamalla tyhjissä `empty-x.map` kartoissa ruutujen määrän kasvaa Dijkstran ja JPS:n kuluttama aika noin kaksinkertaiseksi. Sama tapahtuu myös `pillars-x.map` kartoilla.

```
kartat          Dijkstra        JPS             IDA*
empty-100.map	0.117708	0.0328797	0.0027998
empty-140.map	0.2361574	0.0606722	0.003259
empty-200.map	0.4926179	0.1295996	0.0047159
```

## Saavutetut tilavaativuudet

Dijkstran algoritmi on toteutettuna kartan ruudukon kokoisena taulukkona Nodeja, jotka sisältävät muutaman ylläpitoon liittyvän kentän. Verkon siirtymiä ei erikseen
säilytetä missään, vaan ne haetaan taulukosta (yhdellä solmulla (Node) on korkeintaan 8 naapuria). Tallennus vie O(V) tilaa, jossa V on solmujen
määrä. Graphin avoimista Nodeista saadaan valittua Node, jolla on pienin etäisyys käyttämällä Pythonin heapq min-heap toteutusta (min-heapillä on tilavaativuus O(N)).
Yhteensä siis O(V).

JPS:n toteutus ei tarvitse lisärakenteita toimintaansa verrattuna Dijkstran algoritmiin, joten sen tilavaativuus on O(V).

IDA* toteutus ei tarvitse edes kekoa, mutta kuitenkin vaatii koko Graph-olion, joten senkin tilavaativuus on O(V). IDA*:n pino on toteutettu epäsuorasti käyttäen Graphin Node-olioiden previous-kenttää linkitetyn listan tavalla. Jos Node-oliolla on previous-kenttä asetettuna, niin se katsotaan olevan iteratiivisella polulla.

Tilansäästö ei ollut tarkoituksena toteutuksissa. Ohjelmassa pidetään esim. karttaa kaksi kertaa eri muodoissa muistissa (Grid- ja Graph-oliot). IDA* pitää myös koko verkon muistissa. Muistiprofilointi käyttäen miljoonan ruudun `maps/ida_wins.map` karttaa antaa tuloksena odotettuja arvoja:

```
Algoritmi AVG           MAX (MB)
Dijkstra  575.3099024	626.195312
JPS       529.2931309	614.332031
IDA*      484.263869	598.9375
```

IDA*:n toteutus vaatii vähemmän muistia kuin JPS ja Dijkstra, sillä se ei tarvitse erillistä kekoa toimiakseen.

## Suorituskyky

Testikartoissa on yleisesti käsinvalittu alku- ja maalipisteet niin, että polunhaussa olisi laskettavaa. Tuloksien mukaan suurimmassa osassa kartoista JPS saavuttaa huomattavia nopeusetuja verrattuna Dijkstraan.

Kaikkien 33 kartan keskiarvot:
```
Dijkstra: 1.024803124 s, (n. 2x aikaa vs JPS)
JPS:      0.6365040788 s,
IDA*:     2.264157742 s (ei oteta huomioon keskeytettyjä 21 karttaa, keskiarvo ei ole vertailukelpoinen)
```

Jos poistetaan kartat ida_wins.map ja jps_loses.map, joka on tahallaan viritetty ansa JPS-algoritmille (maali on ihan vieressä seinän takana, mutta JPS joutuu tutkimaan koko miljoonan solun kartan hypyillä) sekä huge.map (suuri kartta, jossa on paljon tyhjää, mutta myös rakennuksia), niin keskiarvot ovat:

```
Dijkstra: 0.34757978 s (n 3.2x aikaa vs JPS),
JPS:      0.1078690067 s
```

Movingai.com sivuston Baldurs Gate 2 kartat (`maps/AR*.map`) olivat suotuisia JPS-algoritmille valituilla alku- ja loppuruuduilla. Niissä keskiarvot olivat seuraavat:

```
Dijkstra: 0.831961825 s, (n. 5.3x aikaa vs JPS)
JPS:      0.157765175 s
```

Kartassa `maps/AR0700SR.map` Dijkstra oli n. `17.6` kertaa hitaampi. Tulos on ymmärrettävä ottaen huomioon alku- ja maaliruutujen sijainnit ja kartan muoto. Niiden takia Dijkstra tutkii paljon turhia ruutuja ja JPS hyötyy huomattavasti heuristiikasta ja hypyistä. Tuloksista on lisää [testausdokumentissa](/dokumentaatio/testausdokumentti.md).

Algoritmeistä IDA* ei kuitenkaan ole ihan täysin huono, sillä se onnistuu pienillä avoimilla kartoilla ja kartassa, jossa on suora reitti maaliin (esim `lt_gallowsprison_n.map`). Se myös voittaa JPS:n kartassa `jps_loses.map`, joka on suurimmaksi osaksi tyhjä miljoonan ruudun kartta, jossa lähtö- sekä maaliruutu ovat melkein vierekkäin. Kartassa `maps/ida_wins.map`, joka on täysin tyhjä kartta, voittaa IDA* selvästi molemmat algoritmit. Tyhjässä miljoonan ruudun `ida_wins.map`-kartassa JPS silti pärjää paremmin kuin Dijkstra, jota myös tukee JPS toiminnan perusteet: Dijkstrassa joudutaan tekemään hitaampia keko-operaatioita ajassa O(log V), kun taas JPS tekee kartan läpikäynnin nopeammin hyppyoperaatioilla ajassa O(1). IDA* toimii sekunnin sisällä pienemmillä kartoilla, joissa on esteitä tiellä, kuten `ht_store.map` ja 11x11 sokkelossa `maze-11.map`. Ei tyhjillä kartoilla yleisesti katsottuna mitä lyhyempi reitti maaliin (d), sitä nopeampi IDA* on. Tähän myös vaikuttaa mahdollisten haarautumien määrä (b).

```
Kartta         Dijkstra     JPS         IDA*
jps_loses.map  0.0013052s   3.5919679s  0.0003933s
ida_wins.map   12.8282026s  3.5459878s  0.0215891s
maze-11.map    0.000817s    0.0004958s  0.4332852s
ht_store.map   0.0188726s   0.0017542s  0.5703822s
```

Ongelmana JPS:llä on siis myös testien perusteella avoimet kartat, jossa tehdään liikaa turhia hyppyjä, sekä kartat, joissa A*-heuristiikka haittaa toimintaa (esim. sokkelot, missä nopein polku lähtee alkuruudusta maaliruutua päinvastaiseen suuntaan). Dijkstralle tuottaa vaikeuksia kartat, joissa on "väärässä" suunnassa paljon avoimia ruutuja, joita se joutuu tutkimaan turhaan.


## Puutteet

IDA* on toteutettu rekursiivisesti ja sitä ei siten voi käyttää kartoilla, joissa polku on liian pitkä tai ohjelma kaatuu.

Hieman kömpelö käyttöliittymä ja hidas. Mahdollisuus zoomata karttaa puuttuu, joka tekee suurempien karttojen seuraamisesti sekavaa.

## Lähteet
- [PyGame](https://www.pygame.org/)
- [Binary Heap](https://en.wikipedia.org/wiki/Binary_heap)
- [Dijkstran algoritmi](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [A*](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Pythonin heapq decrease_key toteutuksesta](https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes)
- [JPS](http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)
- [IDA*](https://en.wikipedia.org/wiki/Iterative_deepening_A*)
- [IDS](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search)
- [movingai.com:n kartat](https://www.movingai.com/benchmarks/bg512/index.html)

