# Teme Python client–server

Repository public: [FilipanDenis/teme-filipan-denis](https://github.com/FilipanDenis/teme-filipan-denis).

Exerciții de comunicare între procese și noduri, implementate cu socket-uri TCP. Instrucțiunile sunt pentru Fedora și folosesc `python3`.

| Tema | Folder | Comportament |
| --- | --- | --- |
| 1 | [tema1_inel](tema1_inel/README.md) | Un mesaj parcurge P1 → P2 → P3 → P1. |
| 2 | [tema2_transfer](tema2_transfer/README.md) | Un client trimite un fișier către un server. |
| 3 | [tema3_proxy](tema3_proxy/README.md) | Fișierul ajunge la destinatar printr-un proxy. |
| 4 | [tema4_loguri](tema4_loguri/README.md) | Un al treilea proces unește două loguri după timestamp. |
| 5 | [tema5_distribuire](tema5_distribuire/README.md) | Un fișier este împărțit, distribuit și apoi reconstituit pentru verificare. |

## Pregătire pe Fedora

Necesită Python **3.10 sau mai nou**. Nu sunt necesare biblioteci externe sau `pip install`.

```bash
python3 --version
git --version
```

Dacă lipsește unul dintre programe:

```bash
sudo dnf install python3 git
```

Descarcă proiectul prin Git și intră în folderul său:

```bash
git clone https://github.com/FilipanDenis/teme-filipan-denis.git
cd teme-filipan-denis
```

Alternativ, extrage arhiva proiectului și deschide terminalul în folderul care conține `README.md` și `demo.py`.
Toate comenzile de mai jos se rulează **din rădăcina proiectului**.

## Primul lucru de rulat

```bash
python3 demo.py 1
```

Demo-ul pornește trei procese Python reale, pe porturi locale disponibile. Mesajul final trebuie să
conțină `P1 -> P2 -> P3 -> P1`. Ieșirile sunt afișate grupat pe proces, după terminarea lor.

După aceea:

```bash
python3 demo.py 2
python3 demo.py 3
python3 demo.py 4
python3 demo.py 5
```

Pentru toate temele într-o singură rulare:

```bash
python3 demo.py toate
```

Rezultatele sunt salvate într-un folder nou în `rezultate/` la fiecare demonstrație.
Demo-ul nu înlocuiește exercițiile: pornește chiar modulele din folderele temelor, în procese separate.
Pentru prezentare, vezi comenzile manuale din fiecare folder.

## Testare

```bash
python3 -m unittest discover -s tests -v
```

Testele verifică mesaje fragmentate, fișiere binare și goale, transferuri întrerupte,
refuzul suprascrierii, proxy-ul, inelul, timestampuri cu fusuri orare diferite și reconstituirea bucăților.

## Ghiduri

- [Fedora și GitHub, de la zero](ghiduri/fedora_github.md): descărcare, prima rulare, accesul profesorului și actualizări.
- [Noțiunile de explicat la prezentare](ghiduri/notiuni.md): proces, nod, client, server, TCP și protocolul de transfer.
- [Rularea pe calculatoare diferite](ghiduri/noduri_retea.md): adrese IP, porturi și modificarea comenzilor.
- [Rezultatele verificării](ghiduri/validare.md): mediul și verificările efectuate asupra acestei versiuni.

## Organizare

`comun/retea.py` conține protocolul comun de mesaje și fișiere. Temele 3–5 reutilizează transferul
din tema 2, adăugând comportamentul propriu. `comun/lansare.py` este folosit numai de demo și teste.
`exemple/` conține fișierul text și cele două loguri de probă.

Transferul de fișiere are dimensiune explicită și confirmare SHA-256. Un server de transfer primește
**un fișier**, apoi se închide. Colectorul de loguri primește **două fișiere**, apoi se închide.
Inelul face **un tur**, apoi procesele se închid. Repornește serverele înaintea unei noi încercări.

Fișierele existente la destinație sunt păstrate; pentru o nouă rulare manuală alege alte directoare
sau alte fișiere de ieșire. Logurile sunt sortate în memorie, pentru volume de laborator.
În această implementare, „concatenare cu timestamp” este interpretată ca unire cronologică:
confirmă cu profesorul dacă dorește doar alipirea fișierelor, fără sortare.

## Surse tehnice

- [Python — Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Python — socket](https://docs.python.org/3/library/socket.html)
- [Fedora — Python](https://developer.fedoraproject.org/tech/languages/python/python-installation.html)
- [GitHub — crearea unui repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub — încărcarea fișierelor](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
- [GitHub — invitarea unui colaborator](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository)
