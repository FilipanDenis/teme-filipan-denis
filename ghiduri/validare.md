# Verificarea proiectului

Data: **9 octombrie 2026**. Mediu de execuție: **Linux, Python 3.12.14**.
Instrucțiunile de pregătire sunt pentru Fedora; testele nu au fost rulate pe calculatorul utilizatorului.

## Teste automate

Comanda folosită:

```bash
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

Rezultat: **18 teste, toate trecute**.

| Grup | Teste | Ce s-a verificat |
| --- | --- | --- |
| Protocol și fișiere | 9 | JSON fragmentat, lungimi invalide, închidere prematură, fișier binar de 1,28 MB, fișier gol, integritate, întrerupere, nume invalid și refuzul suprascrierii. |
| Procese TCP | 3 | Inel cu trei procese, transfer direct și transfer prin proxy, cu fișiere identice la destinație. |
| Loguri | 3 | Ordine cronologică cu fusuri orare diferite, timestamp invalid și două loguri cu același nume trimise de procese distincte. |
| Distribuire | 3 | Fișier binar de mărime indivizibilă cu trei, fișier mai mic decât numărul de noduri și fișier gol. În fiecare caz s-au verificat și detectarea coruperii și lipsa unei bucăți. |

Procesele din testele de integrare sunt programe Python separate, nu simulări ale comunicației.

## Demonstrație completă

Comanda `python3 demo.py toate` a trecut pentru toate cele cinci teme:

- Mesajul a revenit la P1 pe traseul P1 → P2 → P3 → P1.
- Fișierul de exemplu de 138 de octeți a fost transferat direct, apoi prin proxy.
- Colectorul a produs șase înregistrări în ordine cronologică.
- Distribuitorul a trimis trei bucăți de câte 46 de octeți către trei servere separate.
- Fișierul reconstituit a avut aceeași amprentă SHA-256 ca originalul.

## Limitele verificării

Comunicarea a fost testată pe localhost, pe un singur nod Linux.
Codul acceptă adrese IP de rețea, dar rularea pe calculatoare distincte și regulile lor de firewall
trebuie verificate în laborator. Instrucțiunile sunt în `noduri_retea.md`.
Formatul logurilor este `timestamp;proces;mesaj`; soluția presupune unirea cronologică.
Repository-ul public al proiectului este [FilipanDenis/teme-filipan-denis](https://github.com/FilipanDenis/teme-filipan-denis).
