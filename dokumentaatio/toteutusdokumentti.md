# Toteutusdokumentti

## Ohjelman rakenne

Ohjelma on toteutettu eriyttäen sovelluslogiikka (entities ja services) ja käyttöliittymälogiikka (ui). Entity-mallinnettuna on käsite Grid, joka koostuu 
Cell-olioista taulukossa. Gridillä on tarkoitus mallintaa yleisemmällä tasolla jotakin ASCII-karttaa ja sitä luodessa konstruktori perkaa kartan ja luo "turvallisemman" rakenteen myöhemmälle käsittelylle.
Algoritmejä varten luodaan gridistä oma Graph-olio, joka koostuu Cell-luokan vastakohdan eli Node-luokan oliosta. Algoritmit siis käsittelevät tätä ylemmän tason
Graph-oliota. 

Hahmottelin algoritmit palveluiksi (sovelluslogiikka), eli ne on services-paketin sisällä. Toteutettu Dijkstran algoritmi on tehty niin, että sen toimintaa voidaan
seurata ajon aikana generaattorin (next_step) avulla. Uskon, että tämä lähestymistapa myös auttaa myöhemmän Jump Point Searchin toteuttamisessa.

Käyttöliittymä on toteutettu PyGame-kirjaston avulla. Käyttöliittymätason koodi on sijoitettu ui-pakettiin siten, että käyttöliittymäkoodia ei kutsuta erikseen tason 
ulkopuolelta. Suurin osa toteutuksesta tapahtuu ui/ui.py:n UI-luokassa, joka kysyy ajettavan algoritmin seuraavaa askelta aina, kun käyttäjä niin haluaa. 
Käyttöliittymätasolla on myös oma käsitteensä ruudukosta (Grid ja Cell), joista Cell perii PyGamen DirtySprite-luokan toiminnallisuuden. Tarkoituksena on helpottaa
ruudun päivitystä, kun tehdään yksittäisiin spriteihin muutoksia.

Ohjelma käynnistetään ajamalla src/main.py. Antamalla lisäkomennon "timer" voidaan ajaa ajanotto testidatalle ilman graafista käyttöliittymää.

## Saavutetut aikavaativuudet

Dijkstran algoritmin toteutuksessa kutsutaan korkeintaan 8V kertaa min_heapistä poistoa, eli O(V log V). Jokaisella nodella joudutaan käymään läpi ja mahdollisesti
päivittämään 8 naapurin sijaa min-heapissä. Päivitys tapahtuu pushaamalla sama Node uudestaan kekoon pienemmällä etäisyydellä. Myöhemmät versiot samasta Nodesta
hylätään. Päivitys tapahtuu O(log V) ajassa. Yhteensä Dijkstran algoritmin toteutuksen aikavaativuus on siis O(V log V).

Jump Point Search (JPS) algoritmin toteutuksessa pyöritään while-loopissa next_step-metodissa. Jokaisella askeleella haetaan min-heapistä uusi alkio, jonka
toiminallisuus on sama kuin ylempänä eli yhteisaikavaativuus sille on O(V log V). Keon päivitys, kuten ylempänä, ei muuta aikavaativuutta. Pahimmassa tapauksessa JPS:n jump-funktiolla (JPS-luokan `_jump_in_direction`-metodi) joudutaan käymään kuitenkin läpi kaikki ruudukon ruudut. Aikaa per ruutu kuluu O(1) ja tämä nostaa
pahimman aikavaativuuden luokkaan O(V^2). Yleisessä tapauksessa näin ei kuitenkaan tapahdu, sillä eteenpäin hyppääminen törmää nopeasti joko seinään tai uuteen hyppypisteeseen.

## Saavutetut tilavaativuudet

Dijkstran algoritmi on toteutettuna kartan ruudukon kokoisena taulukkona Nodeja, jotka sisältävät muutaman ylläpitoon liittyvän kentän. Graafin siirtymiä ei erikseen
säiltytetä missään, vaan ne haetaan taulukon muodosta (yhdellä nodella on korkeintaan 8 naapuria). Tallennus vie O(V) tilaa, jossa V on solmujen
määrä. Graphin avoimista Nodeista saadaan valittua Node, jolla on pienin etäisyys käyttämällä Pythonin heapq min-heap toteutusta (min-heapillä on tilavaativuus O(N)).
Yhteensä siis O(V).

JPS:n toteutus ei tarvitse lisärakenteita toimintaansa verrattuna Dijkstran algoritmiin, joten sen tilavaativuus on O(V).

## Suorituskyky

Mittaamalla algoritmien toteutuksien suoritusta kartalla, jossa on yli 1 000 000 solua, saadaan kuluneeksi ajaksi:

Dijkstra time: 16.28049 s
JPS time: 11.22136 s

## Puutteet

Timer karttoja ja eri yksikkötestejä tarvitaan lisää.

## Lähteet
- [PyGame](https://www.pygame.org/)
- [Binary Heap](https://en.wikipedia.org/wiki/Binary_heap)
- [Dijkstran algoritmi](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Pythonin heapq decrease_key toteutuksesta](https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes)
- [JPS](http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)

