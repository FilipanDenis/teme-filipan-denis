# Tema 4 — unirea a două loguri într-un al treilea proces

Două procese client trimit propriile fișiere de log unui server colector.
Colectorul produce un singur log, ordonat cronologic. Se păstrează toate liniile valide,
inclusiv înregistrările cu timestamp egal.

## Formatul de log folosit

Fiecare linie conține trei câmpuri separate prin `;`:

```text
2026-10-09T08:00:01+03:00;P1;Proces pornit
```

Primul câmp este timestampul ISO 8601, al doilea identifică procesul, al treilea este mesajul.
Mesajul poate conține alte caractere `;`. Liniile goale sunt ignorate.
Timestampurile cu fus orar sunt comparate după momentul real în UTC; cele fără fus orar
sunt tratate drept UTC, conform convenției acestei implementări.

## Demonstrație rapidă

```bash
python3 demo.py 4
```

## Rulare manuală

Din rădăcina proiectului, terminalul 1 — colectorul:

```bash
python3 -m tema4_loguri.server
```

După `PREGATIT`, terminalul 2 — primul proces:

```bash
python3 -m tema4_loguri.client exemple/proces1.log
```

Terminalul 3 — al doilea proces:

```bash
python3 -m tema4_loguri.client exemple/proces2.log
```

Rezultatul:

```bash
cat rezultate/tema4/log_comun.log
```

Pentru exemplele incluse trebuie să apară șase linii, cu orele **08:00:01, 08:00:03,
08:00:05, 08:00:07, 08:00:09, 08:00:11**.

## Cum funcționează

1. Serverul acceptă două conexiuni și primește câte un fișier de la fiecare client.
2. Păstrează sursele în directoare temporare separate, inclusiv dacă au același nume.
3. Citește liniile, interpretează timestampurile și sortează înregistrările.
4. Scrie fișierul comun și se închide.

Ordinea sosirii fișierelor nu stabilește ordinea cronologică din rezultat.
La timpi identici se păstrează ordinea surselor și a liniilor din ele. Formatul invalid produce
o eroare, fără un rezultat incomplet. Logurile sunt încărcate în memorie pentru sortare.

În această soluție am interpretat cerința cu timestamp ca unire cronologică. Dacă profesorul cere
strict concatenare, fără sortare, se elimină apelul `inregistrari.sort(...)` din `server.py`.
