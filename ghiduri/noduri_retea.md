# Rularea pe calculatoare diferite

Demonstrațiile automate folosesc `127.0.0.1`: procese distincte pe același calculator.
Pentru teme care cer noduri fizice distincte, rulează programele pe calculatoare diferite
conectate la aceeași rețea. Fiecare calculator trebuie să aibă proiectul și Python 3.10 sau mai nou.

În terminalul fiecărui calculator poți vedea adresele disponibile cu:

```bash
hostname -I
```

Alege adresa IPv4 a interfeței conectate la aceeași rețea. Adresele `192.168.1.x` din exemplele
următoare sunt illustrative: înlocuiește-le cu adresele reale. `0.0.0.0` este adresa de ascultare
a serverului; clienții folosesc IP-ul real al destinației.

## Tema 2 — două noduri

Pe destinatarul care are, în acest exemplu, IP-ul `192.168.1.20`:

```bash
python3 -m tema2_transfer.server --host 0.0.0.0 --port 5200 --director rezultate/primite
```

Pe expeditor:

```bash
python3 -m tema2_transfer.client exemple/mesaj.txt --host 192.168.1.20 --port 5200
```

## Tema 3 — trei noduri

| Rol | IP ilustrativ | Port de ascultare |
| --- | --- | --- |
| Expeditor | `192.168.1.10` | Nu are server. |
| Proxy | `192.168.1.20` | `5300` |
| Destinatar | `192.168.1.30` | `5301` |

Mai întâi, pe destinatar:

```bash
python3 -m tema3_proxy.server --host 0.0.0.0
```

Apoi, pe proxy:

```bash
python3 -m tema3_proxy.proxy --host 0.0.0.0 --destinatie-host 192.168.1.30
```

În final, pe expeditor:

```bash
python3 -m tema3_proxy.client exemple/mesaj.txt --host 192.168.1.20
```

## Tema 5 — trei noduri destinatar

Pe fiecare dintre cele trei calculatoare destinatar, de exemplu `192.168.1.21`, `.22` și `.23`:

```bash
python3 -m tema5_distribuire.server --host 0.0.0.0 --port 5501 --director rezultate/bucata
```

Același port poate fi folosit pe calculatoare diferite. Pe calculatorul distribuitor:

```bash
python3 -m tema5_distribuire.client exemple/mesaj.txt --noduri 192.168.1.21:5501 192.168.1.22:5501 192.168.1.23:5501
```

Adună apoi cele trei bucăți de pe noduri într-un director local `rezultate/tema5/toate_bucatile/`,
folosind metoda de copiere disponibilă în laborator. Manifestul este deja pe distribuitor.
Reconstituirea citește fișiere locale:

```bash
python3 -m tema5_distribuire.reconstituire --manifest rezultate/tema5/manifest.json --directoare rezultate/tema5/toate_bucatile --iesire rezultate/tema5/refacut.txt
```

## Temele 1 și 4

La inel, fiecare proces ascultă cu `--host 0.0.0.0`, iar `--urmator-host` este IP-ul
nodului următor. Se păstrează legăturile P1 → P2, P2 → P3, P3 → P1 și ordinea de pornire P2, P3, P1.

La loguri, colectorul ascultă cu `--host 0.0.0.0`. Ambele procese client folosesc `--host IP_COLECTOR`
cu IP-ul real. Formatul logurilor rămâne cel din README-ul temei 4.

## Dacă legătura nu funcționează

Verifică întâi mesajul `PREGATIT`, adresa IP și portul. Poți vedea serverele locale cu:

```bash
ss -ltn
```

Pentru conexiuni între calculatoare, firewall-ul trebuie să permită portul TCP folosit pe server.
Configurează portul necesar în firewalld pentru zona interfeței active. Pentru testele pe
`127.0.0.1` nu este necesară deschiderea acestor porturi către rețea.

Fiecare server de transfer se închide după primirea unui fișier; repornește-l pentru o nouă încercare.
Un timeout de 30 de secunde se aplică după conectare. Serverul poate aștepta clientul înainte de
conectare fără această limită.
