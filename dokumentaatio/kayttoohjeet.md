# Käyttöohjeet

## Asennus

Lataa sovellus ja asenna se ajamalla seuraava komento projektin juuressa:

``` bash
poetry install
```

## Käynnistys

Sovelluksen graafisen näkymän algoritmeille saa ajamalla komennon:

``` bash
poetry run invoke start
```

## Ohjelman käyttö

- `mouse 1`-nappi siirtää lähtöruutua, `mouse 2` siirtää maaliruutua, `mouse 3` vaihtaa seinän tyhjäksi (tai toisinpäin).
- `vasen shift + mouse 1` vaihtaa ruudun keskipisteeksi kursorin alla olevan kohdan.
- `d`-napilla vaihdetaan Dijkstran algoritmiin.
- `j`-napilla vaihdetaan JPS algoritmiin.
- `r`-nappi ajaa nopeasti algoritmin toiminnan loppuun.
- `c`-nappi tyhjentää koko ruudun seinistä.
- `n`-nappi täyttää ruudun alkuperäisellä konfiguraatiolla.
- välilyönnillä voi seurata algoritmin toimintaa. 
- `esc`-napilla voi lopettaa ohjelman. 

Suorituksen lopussa ohjelma piirtää löydetyn reitin risteillä.


## Tehokkuustestit

Jos haluaa ajaa nopeustestit, niin käytä komentoa:

``` bash
poetry run invoke timer
```
