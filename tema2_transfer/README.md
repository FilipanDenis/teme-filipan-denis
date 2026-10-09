# Tema 2 — transfer de fișier între două procese

Scop: clientul citește un fișier, transmite conținutul prin TCP, iar serverul salvează o copie.
Funcționează pentru text, PDF, imagini sau alte fișiere binare; este acceptat și un fișier gol.

## Demonstrație rapidă

```bash
python3 demo.py 2
```

## Rulare manuală

Din rădăcina proiectului, în terminalul 1:

```bash
python3 -m tema2_transfer.server
```

Așteaptă `PREGATIT server: 127.0.0.1:5200`. În terminalul 2:

```bash
python3 -m tema2_transfer.client exemple/mesaj.txt
```

Serverul salvează `rezultate/tema2/mesaj.txt` și se închide după primirea fișierului.
Verificare manuală:

```bash
sha256sum exemple/mesaj.txt rezultate/tema2/mesaj.txt
```

Cele două amprente trebuie să fie identice. Pentru alt fișier, înlocuiește `exemple/mesaj.txt`
cu calea lui; dacă aceasta conține spații, scrie calea între ghilimele.

## Cum funcționează

1. Clientul trimite numele, mărimea și amprenta SHA-256 într-un mesaj JSON.
2. Serverul pregătește fișierul de ieșire și confirmă că poate primi conținutul.
3. Clientul trimite fișierul în blocuri de cel mult 64 KiB.
4. Serverul primește numărul exact de octeți anunțat și verifică SHA-256.
5. Serverul trimite confirmarea finală. Clientul afișează succesul numai după confirmare.

`recv()` poate primi doar o parte din date, de aceea citirea se repetă într-o buclă.
Fișierul rezultat nu este suprascris dacă există deja. O copie incompletă este ștearsă.

## Parametri utili

```bash
python3 -m tema2_transfer.server --help
python3 -m tema2_transfer.client --help
```

`--host` și `--port` aleg adresa și portul. La server, `--director` alege folderul rezultat.
La client, `--nume` permite alegerea unui nume diferit la destinație.
Repornește serverul pentru fiecare transfer nou și folosește un director nou dacă păstrezi copia precedentă.
