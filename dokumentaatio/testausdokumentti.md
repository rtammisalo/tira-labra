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

Tulokset kartoille, joissa IDA* pystyi löytämään reitin edes vähän järkevässä ajassa:

![image](https://user-images.githubusercontent.com/81182631/146656429-0c1709e4-91a6-4fcb-8656-f3214e4d30de.png)

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

[timer_results.txt](/dokumentaatio/timer_results.txt)
