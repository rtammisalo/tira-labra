# MazeFinder (tira-labra)

![Actions:CI](https://github.com/rtammisalo/tira-labra/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/rtammisalo/tira-labra/branch/main/graph/badge.svg?token=T9UVAQ8WRV)](https://codecov.io/gh/rtammisalo/tira-labra)

Projektin tarkoituksena on tehdä vertailua kahden reitinhakualgoritmin välillä (Jump Point Search ja Dijkstra). Testaus tapahtuu käsintehdyssä
kartassa, joka on toteutettuna ruudukkona.

Toteutuskielenä Python.

## Käyttöohjeet

Lataa sovellus ja asenna se ajamalla seuraava komento projektin juuressa:

``` bash
poetry install
```

Sovelluksen graafisen näkymäb voi nyt käynnistää ajamalla komennon:

``` bash
poetry run invoke start
```

- Dijkstran algoritmin toimintaa voi seurata pitämällä space-nappia pohjassa. 
- Painamalla e-nappia ohjelma etenee nopeasti loppuun. 
- Esc-napilla voi lopettaa ohjelman. 

Suorituksen lopussa ohjelma piirtää löydetyn reitin risteillä.

Jos haluaa ajaa yksinkertaisen nopeustestin Dijkstralle, niin käytä komentoa:

``` bash
poetry run invoke timer
```

## Dokumentaatio

- [Määrittelydokumentti](/dokumentaatio/maarittelydokumentti.md)
- [Testausdokumentti](/dokumentaatio/testausdokumentti.md)
- [Toteutusdokumentti](/dokumentaatio/toteutusdokumentti.md)

## Viikkoraportit

- [Viikkoraportti 1](/dokumentaatio/viikkoraportti1.md)
- [Viikkoraportti 2](/dokumentaatio/viikkoraportti2.md)
- [Viikkoraportti 3](/dokumentaatio/viikkoraportti3.md)
- [Viikkoraportti 4](/dokumentaatio/viikkoraportti4.md)
