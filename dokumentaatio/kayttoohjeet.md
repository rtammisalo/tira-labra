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

Antamalla lisäkomennon `-m kartannimi` voi vaihtaa ladattavaa karttaa käyttöliittymässä, eli vaikkapa

``` bash
poetry run invoke start -m maps/ht_store.map
```

Kaikki testikartat löytyy kansiosta `maps`.

## Ohjelman käyttö

- `mouse 1`-nappi siirtää lähtöruutua, 
- `vasen shift + mouse 1` siirtää maaliruutua,
- `mouse 2` vaihtaa ruudun keskipisteeksi kursorin alla olevan kohdan.
- `mouse 3` vaihtaa seinän tyhjäksi (tai toisinpäin).
- `d`-napilla vaihdetaan Dijkstran algoritmiin,
- `j`-napilla vaihdetaan JPS algoritmiin,
- `i`-napilla vaihdetaan IDA* algoritmiin,
- `r`-nappi ajaa nopeasti algoritmin toiminnan loppuun,
- `s`-nappi lopettaa r-komennon kesken / lopettaa IDA* polun näyttämisen,
- `c`-nappi tyhjentää koko ruudun seinistä.
- `n`-nappi täyttää ruudun alkuperäisellä konfiguraatiolla.
- `h`-nappi tulostaa käyttöohjeet konsoliin
- välilyönnillä voi seurata algoritmin toimintaa. 
- `esc`-napilla voi lopettaa ohjelman. 

Suorituksen lopussa ohjelma piirtää löydetyn reitin risteillä. Dijkstra- ja JPS-algoritmeillä keltainen ruutu tarkoittaa kekoon pistettyä ruutua, ja pieni keltainen piste keskellä ruutua tarkoittaa keosta pois otettua ruutua (vierailtu). IDA*-algoritmissä keltainen ruutu tarkoittaa vain ruutua, joka on mukana jossakin iteratiivisessa polussa. Polut näytetään vihreillä ruuduilla ja näytön voi keskeyttää painamalla `s`-nappia.

## Tehokkuustestit

Jos haluaa ajaa nopeustestit, niin käytä komentoa:

``` bash
poetry run invoke timer
```

Pythonin muistiprofiloinnin (memory-profiler) voi ajaa per algoritmi komennoilla 

``` bash
poetry run mprof run src/main.py idastar maps/ida_wins.map
poetry run mprof run src/main.py jps maps/ida_wins.map
poetry run mprof run src/main.py dijkstra maps/ida_wins.map
```
