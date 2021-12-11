# Viikkoraportti 6

## Toteutettu viikon aikana

- Koodin refaktorointia.
- Koodin docstring kommentointia.
- UI:n uusia toiminnallisuuksia: 
  - lähtö/maalipaikan muuttaminen,
  - algoritmin vaihto ajossa,
  - kartan tyhjennys seinistä, 
  - alkuperäisen kartan palautus, 
  - seinän muuttaminen tyhjäksi, 
  - tyhjän tilan muutto seinäksi, 
  - skrollaus isommille kartoille
- Uusi MapsRepository, jolla voi ladata [movingai.com](https://www.movingai.com/benchmarks/bg512/index.html):n karttaformaatin karttoja.
- Latasin muutaman kartan ajastusta varten.
- Uusi ajastin palvelu, joka ajaa kaikki kartat 5 kertaa kummallakin algoritmillä ja palauttaa tulokset
- Muutamia yksikkötestejä
- Muutin etäisyydenlaskennan JPS:ssä käyttämään octile-etäisyyttä

## Tuntikirjanpito

Käytin aikaa n. 18 tuntia tällä viikolla.

## Mitä opin

Octile-etäisyydestä.

## Ohjelman edistyminen

Ohjelman toiminnallisuudet ovat suurelta osin toteutettu. 

## Seuraavalla viikkolla

- Aioin vielä kirjoittaa lisää yksikkötestejä kummallekkin algoritmille ja siivota toteutuksia.
- Dokumentointia
