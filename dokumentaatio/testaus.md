# Testausdokumentti
Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestillä sekä manuaalisesti tapahtunein järjestelmätason testein.

## Yksikkö- ja integraatiotestaus

### Pelilogiikka
Pelimenujen logiikasta vastaava ’menu_class’-luokkaa testataan [test_menu]( https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/Sports-Rally/src/tests/test_menu.py)-testiluokalla.  ’menu-class’-olioilla pyritään luomaan pelin peruskehys käyttäen Pygame-kirjastoa, joka mahdollistaa pelien alustamisen Pythonilla. Koodissa määritellään joitakin globaaleja asetuksia, kuten ruudun mitat, ruudunpäivitysnopeus ja fontit. ’menu_class’ sisältää seuraavat luokat:

-	`SoundManager`-luokka vastaa erilaisten äänitehosteiden ja taustamusiikkitiedostojen lataamisesta ja toistamisesta. Sillä on metodeja kunkin äänitehosteen ja taustamusiikkiraidan toistamiseen. Äänet sisältävät pelin maila-, seinä-, pisteet-, boostattu-, painike- ja hyppyäänet, sen vuoksi ’SoundManager’:iä on käytetty kutsumalla myös pong ja long jump pelien koodissa. Luokassa on myös taustamusiikkia pong-, pituushyppy- ja valikkonäyttöjä varten.
-	`create_text_surface`- ja `create_shadow_surface`-funktioita käytetään tekstipintojen ja varjopintojen luomiseen määritetyllä tekstillä, koolla ja värillä.
-	 `draw_text_with_shadow` piirtää tekstin ruudulle varjoefektillä renderöimällä ensin varjopinnan ja sitten tekstipinnan.
-	`start_game` pysäyttää nykyisen taustamusiikin, suorittaa määritetyn komennon ja jatkaa sitten taustamusiikkia.
-	`Button`-luokkaa käytetään interaktiivisten painikkeiden luomiseen pelin käyttöliittymään. Sillä on metodeja painikkeen piirtämiseen, sen tarkistamiseen, onko objekteja painikkeen alueen sisällä, ja komennon suorittamiseen, kun painiketta napsautetaan. Sillä on myös metodi poistumispainikkeen piirtämiseen.

**Pong**-pelin logiikasta vastaavaa `pong_class`-luokkaa testataan [test_pong](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/Sports-Rally/src/tests/test_pong.py)-testiluokalla. `Pong_class’ sisältää seuraavat luokat:
-	’Paddle’ määrittelee pelin ’mailat’. Se sisältää metodeja mailojen siirtämiseen käyttäjän syötteen perusteella ja mailien piirtämiseen peliruudulle.
-	’Ball’ määrittelee pelin pallon. Se sisältää metodit pallon liikuttamiseen, törmäysten havaitsemiseen mailojen tai pelialueen rajojen kanssa sekä pallon sijainnin palauttamiseen sen jälkeen, kun se on mennyt rajojen ulkopuolelle tai osunut mailaan.

Koska **long jump**-pelin logiikasta vastaavat metodit käytetään ainoastaan long jump:ssa, niistä ei ole sen vuoksi perustettu erillisen luokka tiedosto [classes] (https://github.com/KirinPoersti/ot-harjoitustyo/tree/main/Sports-Rally/src/classes):iin, vaan ne ovat kaikki long jump:n pelitiedostossa. `longjump’ sisältää seuraavat luokat:
-	`draw_text`: Piirtää tekstiä näytölle määritetyllä koolla, sijainnilla ja värillä.
-	`draw_region_lines`: Piirtää ruudulle alueviivat, jotka ilmaisevat pituushypyn etäisyysvälit.
-	`get_player_name`: Kehottaa pelaajaa syöttämään nimensä Pygamen tapahtumajärjestelmää ja tekstin renderöintiä käyttäen. Se palauttaa syötetyn nimen.
-	`calculate_landing_point`: Laskee laskeutumispisteen ruudulle pituushypyssä saavutetun pistemäärän perusteella.
-	`save_score`: Tallentaa pelaajan nimen ja pisteet CSV-tiedostoon, joka edustaa tulostaulukkoa.
-	`display_leaderboard`: Lataa pisteet leaderboard-tiedostosta, lajittelee ne laskevaan järjestykseen ja näyttää ne näytöllä.
-	`load_scores`: Lataa pisteet määritetystä CSV-tiedostosta ja palauttaa ne tupleluettelona.

Pelin päälogiikka on toteutettu `game_loop`-funktiossa. Se käsittelee pelin tilat, pelaajan syötteet, pelielementtien piirtämisen ruudulle ja näytön päivittämisen. Peli etenee eri tilojen kautta, kuten lähtölaskenta, nopeuden lisääminen, hyppy, ratkaisu, epäonnistunut yritys ja loppupeli.
Koodissa käytetään `SoundManager`-luokkaa pelin äänien, kuten taustamusiikin ja äänitehosteiden, käsittelyyn.

### Testauskattavuus
Vaikka [test_longjump]( https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/Sports-Rally/src/tests/test_longjump.py) kattavuus on melko alhainen, testauksen haarautumakattavuus on siitä huolimatta 70%.

![](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/dokumentaatio/kuvat/testikattavuus.PNG)

`long jump`:n metodeista on testattu vain osaa, sillä suuri osa metodeista ovat melko riippuvaisia olemassa olevista pinnasta ja syötteistä. Tämän vuoksi metodit testatiin niin paljon kuin pystyttiin [test_longjump]( https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/Sports-Rally/src/tests/test_longjump.py)-testiluokalla.

### Asennus ja konfigurointi
Peli on tehty ja sitä on testattu [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla sekä Windows- että Linux-ympäristöön.

### Toiminnallisuudet
Kaikki [määrittelydokumentin](https://github.com/KirinPoersti/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md) ja käyttöohjeen listaamat toiminnallisuudet on käyty läpi. 
## Sovellukseen jääneet laatuongelmat
- Pituushypyn tulostaulukkoa pääsee tarkastamaan ainoastaan sen jälkeen, kun se on saanut 10 parasta pistemäärää pelaajilta tallenettua.
- Useammassa koodissa on käytetty kopioitut/samat määrittely tiedot
- Pygame:n oliot (esim. pygame.quit()) on kirjoitettu "väärällä" tavalla (Module 'pygame' has no 'quit' memberPylint(E1101:no-member))
- Jotkut rivit voi olla sellaisia, että se toimii kyllä koodin tasolla, butta se ei koodauksen tasolla ole siisti
```
 if button_exit.clicked(click, lambda: pygame.quit() or sys.exit()):
            pass

   pygame.display.flip() 
```
(Unreachable codePylint(W0101:unreachable))
