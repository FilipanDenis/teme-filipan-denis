# Tema 1 — mesaj în inel de trei procese

Scop: un mesaj pleacă din P1, trece prin P2 și P3 și revine la P1. Fiecare proces este server
pentru vecinul anterior și client pentru vecinul următor. Programul face un singur tur.

## Demonstrație rapidă

Din rădăcina proiectului:

```bash
python3 demo.py 1
```

## Rulare manuală pe Fedora

Deschide trei terminale, toate în rădăcina proiectului. Pornește **P2, P3, apoi P1**.
Așteaptă mesajul `PREGATIT` în fiecare terminal înainte să pornești următorul proces.

Terminalul 1 — P2:

```bash
python3 -m tema1_inel.nod --id 2 --port 5102 --urmator-port 5103
```

Terminalul 2 — P3:

```bash
python3 -m tema1_inel.nod --id 3 --port 5103 --urmator-port 5101
```

Terminalul 3 — P1:

```bash
python3 -m tema1_inel.nod --id 1 --port 5101 --urmator-port 5102 --mesaj "Salut de la Denis!"
```

La P1 trebuie să apară:

```text
P1 a primit: Salut de la Denis!
TRASEU: P1 -> P2 -> P3 -> P1
FINAL: mesajul a revenit la P1 după un tur complet.
```

## Cum funcționează

1. Fiecare proces deschide un server pe propriul port.
2. P1 transmite un mesaj JSON cu textul și traseul `[1]`.
3. P2 primește, adaugă `2` în traseu și transmite către P3.
4. P3 adaugă `3` și transmite către P1.
5. P1 adaugă `1`, afișează turul complet și se oprește.

Traseul este verificat la fiecare pas, pentru a detecta o conectare greșită a proceselor.
Pentru un nou tur, repornește toate cele trei procese.

## De explicat la prezentare

- Cele trei procese pot fi trei instanțe ale aceluiași program `nod.py`.
- Porturile identifică serverele locale; IP-ul identifică nodul din rețea.
- P1 inițiază mesajul și este destinația finală după închiderea inelului.
- Nu sunt doar trei apeluri de funcție: sunt trei programe Python aflate în execuție.
