# Testausdokumentti

## Kattavuusraportti

[![codecov](https://codecov.io/gh/rtammisalo/tira-labra/branch/main/graph/badge.svg?token=T9UVAQ8WRV)](https://codecov.io/gh/rtammisalo/tira-labra)

Kattavuuteen ei ole laskettu käyttöliittymää tai ajastus/kartanluku-palveluita.

## Yksikkötesteistä

Automaattisissa yksikkötesteissä on laskettu muutaman testikartan pituudet kaikilla kolmella algoritmilla (Dijkstra, JPS ja IDA*) ja verrattu
käsinlaskettuun arvoon. Testeissä myös kokeillaan, että algoritmit toimivat oikein syötteillä, joissa ei ole polkua maalisoluun. Poluttomista
kartoista myös testataan kartta, jossa ei ole yhtään vapaata solua lähtösolun vieressä.

Dijkstran yksikkötesteissä katsotaan testissä keon sisällöstä, että sen seuraavat solut ovat lähimmät solut. Toteutuksessa oli myös aiemmin bugi, jonka takia Dijkstra antoi harvoin väärän polun, jonka takia loin sille testitapauksen regressiotestauksena. Testeissä katsotaan, että Dijkstran algoritmi laittaa kaikki kartan solut kekoon heti alussa. Harvaa karttaa käytetään varmistamaan, että Dijkstra todellakin joutuu käymään siitä yli 90% soluista läpi, ennen kuin löytää maalin.

Jump Point Search on monimutkaisin algoritmeistä, joten toteutin sille eniten yksikkötestejä. Kaikille ajettavien pituustestien lisäksi testaan kaikki tavat löytää uusia pakotettujen naapurien (forced neighbors) takia luotavia jump pointteja ja sen, että jump pointista myös käydään läpi pakotetun naapurin suunta. Jos näin ei ole tehty, niin karttaan voin jäädä tyhjiä kohtia. Testeissä varmistetaan myös, että JPS pistää alle 10% kartan soluista jump pointeiksi kekoon harvassa kartassa. Varmistan myös toisessa testissä, että JPS joutuu kuitenkin käymään hypyillä huomattavan osan karttaa.

IDA* algoritmin toteutuksen yksikkötesteissä varmistetaan, ettei iteratiiviset polut koskaan käy jo polulla ollutta pistettä ja etteivät ne kulje ulos 'nähtyjen'  solujen (solu jossa käytiin jossakin polussa) joukosta eli ettei nähtyjä soluja raportoida väärin. Testeissä varmistetaan myös, ettei kyseisten polkujen pituudet ole koskaan yli rajan (bound/threshold). Sama tehdään myös jokaiselle 'nähdylle' pisteelle. Näille myös varmistetaan, etteivät ne ole yksin (eli algoritmi jotenkin olisi päässyt hyppäämään). Rajan nostolle on myös oma testinsä, jossa yritetään varmistetaa, ettei rajaa nosteta kuin minimi arvolla.

Olen pyrkinyt myös kattavasti yksikkötestata algoritmeihin liittyvää sovelluslogiikkaa ja rakenteita. Ohjelmaa on myös testattu käyttöliittymän kautta käsin.

## Nopeustestit

Nopeustestit ajetaan 27 eri kartalle, joista suurin osa on otettu [movingai.com](https://movingai.com/benchmarks/grids.html) sivustolta. Käytän myös muutamaa omaa karttaa, joista esim. `maps/jps_loses.map` on tarkoituksella luotu niin, että JPS häviää kummallekkin algoritmille hyppyjen takia. On olemassa myös karttoja, kuten `maps/pillars-X.map`, joissa kartta koostuu yhden kokoisista seinistä muuten tyhjällä kartalla.

Pillars karttojen peruskuvio, joka aiheuttaa JPS:n pakotettuja naapureita ja häiritsee siten hyppyoperaatioiden toimintaa:

```
#.#.#.#
.......
.#.#.#.
.......
```

Maze-alkuisissa kartoissa on kyseessä tavallisista sokkeloista, joita loin [maze-generator](https://www.dcode.fr/maze-generator):n avulla.

`maps/ida_wins.map` on tyhjä kartta, joka on suunniteltu suosimaan IDA*-algoritmin toimintaa Dijkstran ja JPS:iin verrattuna.

Dokumentin lopussa on tekstimuotoinen raportti (`invoke timer`-kutsu) eräästä ajastuksesta. 

## Testien toistaminen

Aja komento `poetry run invoke timer`, jolloin ohjelma alkaa laskemaan tuloksia. Laskenta on hidasta, ja siinä tulee kuitenkin kestämään monta minuuttia.

## Testitulokset

Kartat koon mukaan:

![image](https://user-images.githubusercontent.com/81182631/147485066-003e6cd5-6d41-48b5-8bbd-71d3d5c1cc55.png)

Tulokset kartoille, joissa IDA* pystyi löytämään reitin edes vähän järkevässä ajassa. Kun sokkelokarttojen (`maze-x.map`) koko kasvaa 11x11 ruudukosta 15x15 ruudukkoon, ei IDA* enää kyennyt aikarajassa löytämään reittiä. `maze-15-straight.amp` on sokkelokartta, johon tahallaan loin suoremman reitin.

![image](https://user-images.githubusercontent.com/81182631/147463444-4ffc6ea8-ef0f-4eeb-9464-4d2893549055.png)

IDA*:n kyky selvitä järkevässä ajassa pillars-kartoissa, kun koko kasvaa yhdellä rivillä ja sarakkeella:

![image](https://user-images.githubusercontent.com/81182631/147463495-148df65c-13a4-4edd-b33d-efbab1c765c5.png)

Muutaman ylläolevan (ida_wins.map on tyhjä kartta, jossa maali- ja alkuruutu ovat kartan toisella puolella) kartan kuvat. IDA* selvästi pärjää parhaiten tyhjillä kartoilla ja kartoilla, joissa on olemassa tasan heuristiikan pituinen polku maaliin.

![image](https://user-images.githubusercontent.com/81182631/146653028-b63b06a7-6ed9-424c-81ea-2dd0fafb4a48.png)

Alla loput kartat, joissa IDA* ei pärjännyt ja testit keskeytettiin aikarajan takia. Huomioitavaa on, että kaikissa satunnaisesti luoduissa sokkelokartoissa (`maze-x.map`) JPS silti voittaa Dijkstran. `AR*.map`-kartoissa Dijkstra kuluttaa aikaa n. 5.3 kertaa enemmän. Kartat sisältävät paljon sopivan kokoisia avoimia alueita, joita JPS:n hyppyoperaatiot tehokkaasti käyvät läpi. Niiden kuvat ilman alku- ja loppupisteitä löytyvät sivulta [movingai.com](https://movingai.com/benchmarks/bg512/index.html).

![image](https://user-images.githubusercontent.com/81182631/147464653-50d60849-b371-49d2-9654-4ad0f1c9fb66.png)

![image](https://user-images.githubusercontent.com/81182631/147466792-c9bc733f-ebb1-4439-91a0-8a4f1e34e0a1.png)
![image](https://user-images.githubusercontent.com/81182631/147468600-e8dabf12-3d0d-4348-8dfb-c8ea2f24fc1e.png)


Isossa miljoonan ruudun kartassa, joka on suurimmiten tyhjää, pärjäävät kummatkin algoritmit samalla tavalla. `huge.map`-kartassa selvästi JPS:n heuristiikasta ei ole apua ja liian suuret hypyt muodostuvat haitaksi.

![image](https://user-images.githubusercontent.com/81182631/147464858-25c54464-43c9-42b5-9ba7-056e7ea01855.png)

Aiemmin mainituissa pillars-tyylisissä kartoissa JPS silti päihittää Dijkstran. `pillars-maze-260.map` on kuitenkin suunniteltu niin, että JPS:n heuristiikka hidastaa toimintaa, joka johtaa Dijkstran selvään voittoon.

![image](https://user-images.githubusercontent.com/81182631/147464991-a5314292-f4fc-4c4e-9f9a-32a0b24411e9.png)

Alla pillars ja empty-karttojen skaalautuvuudesta. Dijkstran ja JPS:n kuluttuma aika tuplaantuu, kun ruutujen määrää tuplataan (100x100 -> 140x140 -> 200x200 ruudukoilla).

![image](https://user-images.githubusercontent.com/81182631/147484113-9e94f2d9-f63d-4352-b631-b2c1a59a2f5e.png)

Kaikki tulokset yhdessä:

![image](https://user-images.githubusercontent.com/81182631/147484638-79725d26-a06b-44c3-becc-d120c3baa1c1.png)

### Tekstiraportti

[timer_results.txt](/dokumentaatio/timer_results.txt)
