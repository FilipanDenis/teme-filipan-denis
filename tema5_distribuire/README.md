# Tema 5 — împărțirea și distribuirea unui fișier

Distribuitorul împarte fișierul în N bucăți, unde N este numărul de noduri indicat.
Trimite câte o bucată fiecărui nod și salvează un manifest JSON cu ordinea, dimensiunile
și amprentele SHA-256. Mărimile bucăților diferă cu cel mult un octet.

Reconstituirea este adăugată pentru a verifica faptul că distribuirea păstrează fișierul original.

## Demonstrație rapidă

```bash
python3 demo.py 5
```

## Rulare manuală

Din rădăcina proiectului, deschide patru terminale.

Terminalul 1 — nodul 1:

```bash
python3 -m tema5_distribuire.server --port 5501 --director rezultate/tema5/nod1
```

Terminalul 2 — nodul 2:

```bash
python3 -m tema5_distribuire.server --port 5502 --director rezultate/tema5/nod2
```

Terminalul 3 — nodul 3:

```bash
python3 -m tema5_distribuire.server --port 5503 --director rezultate/tema5/nod3
```

După ce toate cele trei servere afișează `PREGATIT`, terminalul 4 — distribuitorul:

```bash
python3 -m tema5_distribuire.client exemple/mesaj.txt --noduri 127.0.0.1:5501 127.0.0.1:5502 127.0.0.1:5503
```

În directoarele nodurilor apar `mesaj.txt.part001`, `mesaj.txt.part002` și `mesaj.txt.part003`.
Manifestul apare în `rezultate/tema5/manifest.json`.

După distribuire, în terminalul 4:

```bash
python3 -m tema5_distribuire.reconstituire --manifest rezultate/tema5/manifest.json --directoare rezultate/tema5/nod1 rezultate/tema5/nod2 rezultate/tema5/nod3 --iesire rezultate/tema5/mesaj_reconstituit.txt
sha256sum exemple/mesaj.txt rezultate/tema5/mesaj_reconstituit.txt
```

Cele două amprente trebuie să fie identice. O bucată lipsă sau modificată produce o eroare.

## Cum funcționează

Pentru un fișier de 10 octeți și trei noduri, împărțirea este **4 + 3 + 3**.
Nu contează dacă fișierul este text sau binar: împărțirea se face după octeți.
Chiar dacă o bucată taie un caracter UTF-8 la mijloc, reconstituirea binară îl păstrează corect.

Clientul creează temporar câte o bucată, o trimite, apoi trece la următoarea.
Un nod primește o singură bucată și se închide. Manifestul se scrie după confirmarea tuturor
transferurilor. Un transfer parțial eșuat nu anulează bucățile deja primite de celelalte noduri.

## Pe calculatoare diferite

Fiecare nod rulează serverul cu `--host 0.0.0.0`. În lista `--noduri` scrie IP-urile reale.
Pentru reconstituire adună mai întâi copiile bucăților într-un director de pe un singur calculator,
apoi indică acel director prin `--directoare`. Programul de reconstituire citește bucăți locale;
nu le descarcă automat de pe noduri.
