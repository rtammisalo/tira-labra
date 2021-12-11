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

Sovelluksen graafisen näkymän algoritmeille saa ajamalla komennon:

``` bash
poetry run invoke start
```

- `mouse 1`-nappi siirtää lähtöruutua, `mouse 2` siirtää maaliruutua, `mouse 3` vaihtaa seinän tyhjäksi (tai toisinpäin).
- `d`-napilla vaihdetaan Dijkstran algoritmiin.
- `j`-napilla vaihdetaan JPS algoritmiin.
- `r`-nappi ajaa nopeasti algoritmin toiminnan loppuun.
- `c`-nappi tyhjentää koko ruudun seinistä ja `n`-nappi täyttää ruudun alkuperäisellä konfiguraatiolla.
- välilyönnillä voi seurata algoritmin toimintaa. 
- `esc`-napilla voi lopettaa ohjelman. 

Suorituksen lopussa ohjelma piirtää löydetyn reitin risteillä.

Jos haluaa ajaa yksinkertaisen nopeustestin, niin käytä komentoa:

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
- [Viikkoraportti 5](/dokumentaatio/viikkoraportti5.md)
