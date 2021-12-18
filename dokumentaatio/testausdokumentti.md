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

IDA* algoritmin toteutuksen yksikkötesteissä varmistetaan, ettei iteratiiviset polut koskaan käy jo polulla ollutta pistettä ja etteivät ne kulje ulos 'nähtyjen' (solu jossa käytiin jossakin polussa) solujen joukosta. Testeissä varmistetaan, myös ettei kyseisten polkujen pituudet ole koskaan yli rajan (bound/threshold). Sama tehdään myös jokaiselle 'nähdylle' pisteelle. Näille myös varmistetaan, etteivät ne ole yksin (eli algoritmi jotenkin olisi päässyt hyppäämään). Rajan nostolle on myös oma testinsä, jossa yritetään varmistetaa, ettei rajaa nosteta kuin minimi arvolla.

Olen pyrkinyt myös kattavasti yksikkötestata algoritmeihin liittyvää sovelluslogiikkaa ja rakenteita.

Ohjelmaa on testattu käsin muutamalla eri kartalla. Käytössä on myös 
kattava automaattinen yksikkötestaus.

## Nopeustestit

Nopeustestit ajetaan 16 eri kartalle, joista suurin osa on otettu [movingai.com](https://movingai.com/benchmarks/grids.html) sivustolta. Käytän myös muutamaa omaa karttaa, joista esim. `maps/jps_loses.map` on tarkoituksella luotu niin, että JPS häviää kummallekkin algoritmille luonteensa takia. Dokumentin lopussa on tekstimuotoinen raportti (`invoke timer`-kutsu) eräästä ajastuksesta.

## Testien toistaminen

Aja komento `poetry run invoke timer`, jolloin ohjelma alkaa laskemaan tuloksia. Laskenta on hidasta, ja siinä tulee kuitenkin kestämään monta minuuttia.

## Testitulokset

Kartat koon mukaan:

![image](https://user-images.githubusercontent.com/81182631/146653136-73ace727-8f86-43b6-941c-23e58cb3030c.png)

Tulokset, jossa IDA* pystyi löytämään reitin järkevässä ajassa:

![image](https://user-images.githubusercontent.com/81182631/146652627-fe48a41a-92d4-4d80-b5da-57ff27bff474.png)

Ylläolevien kolmen kartan kuvat:

![image](https://user-images.githubusercontent.com/81182631/146653028-b63b06a7-6ed9-424c-81ea-2dd0fafb4a48.png)

Loput kartat:

![image](https://user-images.githubusercontent.com/81182631/146652631-503ab25b-13e4-4bd4-844e-14aaf209c477.png)
![image](https://user-images.githubusercontent.com/81182631/146652635-0b1fff94-0fdd-4ea4-9b26-ea50dcf392a2.png)
![image](https://user-images.githubusercontent.com/81182631/146652636-75bd45de-ba16-41f4-90f0-d763c7e535a1.png)
![image](https://user-images.githubusercontent.com/81182631/146652641-fab9425d-c387-4504-8aae-c595e5e5dd3e.png)


Kaikki tulokset:

![image](https://user-images.githubusercontent.com/81182631/146653201-ed40624d-b010-4244-a0a1-b9d09755ff5d.png)

### Tekstiraportti


```
Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/w_sundermount.map, 770x770 = 592900 cells.
Dijkstra average time taken: 0.34388 s
JPS average time taken: 0.08182 s
IDA* ran over time limit of 30 s
Found path length of 613 with a total cost of 702.71277.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0012SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.32459 s
JPS average time taken: 0.05320 s
IDA* ran over time limit of 30 s
Found path length of 195 with a total cost of 223.40916.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0400SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.78177 s
JPS average time taken: 0.18015 s
IDA* ran over time limit of 30 s
Found path length of 468 with a total cost of 548.60007.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/huge.map, 999x1050 = 1048950 cells.
Dijkstra average time taken: 10.72657 s
JPS average time taken: 10.55836 s
IDA* ran over time limit of 30 s
Found path length of 1615 with a total cost of 1805.78088.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/dr_0_deeproads.map, 560x733 = 410480 cells.
Dijkstra average time taken: 0.42451 s
JPS average time taken: 0.14326 s
IDA* ran over time limit of 30 s
Found path length of 875 with a total cost of 955.60007.


Running...
Run 1
Run 2
Run 3
Run 4
Run 5


Map file: maps/ht_store.map, 37x37 = 1369 cells.
Dijkstra average time taken: 0.00388 s
JPS average time taken: 0.00134 s
IDA* average time taken: 0.55902 s
Found path length of 16 with a total cost of 17.48528.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0700SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.50738 s
JPS average time taken: 0.09010 s
IDA* ran over time limit of 30 s
Found path length of 370 with a total cost of 480.42345.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0516SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.40388 s
JPS average time taken: 0.08952 s
IDA* ran over time limit of 30 s
Found path length of 324 with a total cost of 367.73506.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0011SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.30624 s
JPS average time taken: 0.31939 s
IDA* ran over time limit of 30 s
Found path length of 477 with a total cost of 503.75231.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0203SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 1.16181 s
JPS average time taken: 0.30357 s
IDA* ran over time limit of 30 s
Found path length of 405 with a total cost of 485.18586.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0511SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.90013 s
JPS average time taken: 0.12486 s
IDA* ran over time limit of 30 s
Found path length of 379 with a total cost of 464.15642.


Running...
Run 1
Run 2
Run 3
Run 4
Run 5


Map file: maps/lt_gallowsprison_n.map, 116x242 = 28072 cells.
Dijkstra average time taken: 0.02716 s
JPS average time taken: 0.00242 s
IDA* average time taken: 0.00283 s
Found path length of 122 with a total cost of 121.41421.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/lt_foundry_n.map, 109x92 = 10028 cells.
Dijkstra average time taken: 0.02990 s
JPS average time taken: 0.00593 s
IDA* ran over time limit of 30 s
Found path length of 67 with a total cost of 78.42641.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/AR0711SR.map, 512x512 = 262144 cells.
Dijkstra average time taken: 0.29289 s
JPS average time taken: 0.09415 s
IDA* ran over time limit of 30 s
Found path length of 616 with a total cost of 680.03153.


Running...
Run 1
Timelimit of 30 s reached for IDA*
Run 2
Run 3
Run 4
Run 5


Map file: maps/ca_caverns1_mines.map, 324x597 = 193428 cells.
Dijkstra average time taken: 0.09675 s
JPS average time taken: 0.01927 s
IDA* ran over time limit of 30 s
Found path length of 201 with a total cost of 233.13708.


Running...
Run 1
Run 2
Run 3
Run 4
Run 5


Map file: maps/jps_loses.map, 999x1050 = 1048950 cells.
Dijkstra average time taken: 0.00133 s
JPS average time taken: 3.40875 s
IDA* average time taken: 0.00040 s
Found path length of 8 with a total cost of 8.24264.
```
