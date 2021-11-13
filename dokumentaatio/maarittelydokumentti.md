# Määrittelydokumentti

## Ratkaistava ongelma

Projektissa verrataan kahden eri algoritmin tehokkuutta toisiinsa erilaisissa satunnaisissa ruudukkoon perustuvissa sokkeloissa. Ongelmana on siis löytää tehokkaasti polku ulos sokkelosta.

## Ohjelmointikieli

Python. Vertaisarvioitavaksi sopii minulle myös Javalla ja C:llä toteutetut projektit. Olen myös kirjoittanut aiemmin hieman C#-kielellä.

## Toteutettavat algoritmit

Aion toteuttaa projektissa [Jump Point Search][1] (Harabor & Grastien 2011) algoritmin ja [Dijkstran algoritmin][2] (Edsger Dijkstra 1959) sekä vertailla niiden tehokkuutta keskenään.
Dijkstran algoritmin aikavaativuus on luokkaa O(n + m log n), n = |V|, m = |E|, kun taas A* + JPS
toimii Haraborin ja Grastienin mukaan yli 10 kertaa nopeammin (riippuen sokkelon muodosta) kuin pelkkä A*-algoritmi, jonka aikavaativuus on luokkaa O(m) = O(b^d) ('A* search algorithm' 2021).

JPS ei vaadi lisätilaa A*:n verrattuna, jonka tilavaativuus on O(n) = O(b^d). Dijkstran algoritmin tilavaativuus on O(n).

Valitsin JPS:n, koska en ollut aikaisemmin kuullut siitä. Dijkstra esitettiin vertailuvaihtoehtona kurssin sivuilla, joten päätin käyttää sitä toisena
algoritminä. Halusin myös hieman kerrata Tirassa esitettyä Primin algoritmiä, joten valitsin sen muunnoksen sokkeloiden luomisalgoritmiksi.

Tietorakenteina käytetään Pythonin valmiita toteutuksia. Testeissä käytettäviä karttoja luodaan käsin tekstipohjaisesti. 

## Ohjelman syöte

Ohjelman argumenttina on graafisen esityksen estäminen, jolloin se ajaa vain testit. Mahdollisesti myöhemmin myös tiedostonimen käyttäjän omaan tekstipohjaiseen karttaan.

## Opinto-ohjelma

Tietojenkäsittelytieteen kandidaatti (TKT)

## Kieli

Dokumentaatio on suomeksi, mutta koodi, kommentit ja github commitit ovat englanniksi.

## Lähteet
1. Harabor, D & Grastien, A 2011, 'Online Graph Pruning for Pathfinding on Grid Maps', <http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf>
2. Dijkstra, E 1959, 'A Note on Two Problems in Connexion with Graphs', <http://www-m3.ma.tum.de/foswiki/pub/MN0506/WebHome/dijkstra.pdf>
3. 'A* search algorithm', 2021, Wikipedia, <https://en.wikipedia.org/wiki/A*_search_algorithm>

[1]: <http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf> "JPS"
[2]: <http://www-m3.ma.tum.de/foswiki/pub/MN0506/WebHome/dijkstra.pdf> "Dijkstran algoritmi"

