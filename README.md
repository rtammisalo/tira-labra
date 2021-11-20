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

Sovelluksen voi nyt käynnistää ajamalla komennon:

``` bash
poetry run invoke start
```

Dijkstran algoritmin toimintaa voi seurata pitämällä space-nappia pohjassa. Suorituksen lopussa ohjelma piirtää löydetyn reitin risteillä.

## Dokumentaatio

- [Määrittelydokumentti](/dokumentaatio/maarittelydokumentti.md)
- [Testausdokumentti](/dokumentaatio/testausdokumentti.md)

## Viikkoraportit

- [Viikkoraportti 1](/dokumentaatio/viikkoraportti1.md)
- [Viikkoraportti 2](/dokumentaatio/viikkoraportti2.md)
- [Viikkoraportti 3](/dokumentaatio/viikkoraportti3.md)
