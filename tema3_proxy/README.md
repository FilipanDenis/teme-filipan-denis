# Tema 3 — transfer de fișier printr-un proces proxy

Scop: expeditorul se conectează la proxy, iar proxy-ul se conectează la destinatar.
Există trei procese distincte: expeditor, proxy și serverul destinatar.

## Demonstrație rapidă

```bash
python3 demo.py 3
```

## Rulare manuală

Din rădăcina proiectului, deschide trei terminale.

Terminalul 1 — destinatarul:

```bash
python3 -m tema3_proxy.server
```

Terminalul 2 — proxy-ul, după ce destinatarul afișează `PREGATIT`:

```bash
python3 -m tema3_proxy.proxy
```

Terminalul 3 — expeditorul, după ce proxy-ul afișează `PREGATIT`:

```bash
python3 -m tema3_proxy.client exemple/mesaj.txt
```

Expeditorul se conectează la portul **5300 al proxy-ului**. Proxy-ul deschide o conexiune către
portul **5301 al destinatarului**. Fișierul apare în `rezultate/tema3/mesaj.txt`.

```bash
sha256sum exemple/mesaj.txt rezultate/tema3/mesaj.txt
```

## Cum funcționează

Proxy-ul transmite octeții în ambele direcții. În sensul expeditor → destinatar trec metadatele
și fișierul. În sensul destinatar → expeditor trec confirmările.
Un fir de execuție gestionează un sens, iar firul principal îl gestionează pe celălalt.
Astfel confirmările pot circula fără blocarea transferului.

Proxy-ul nu stochează fișierul pe disc. Clientul și serverul reutilizează protocolul din tema 2;
elementul nou al temei este procesul intermediar `proxy.py`.

## Pe trei calculatoare

Pe destinatar folosește `--host 0.0.0.0`. Pe proxy folosește `--host 0.0.0.0` și
`--destinatie-host IP_DESTINATAR`. La expeditor folosește `--host IP_PROXY`.
Vezi [ghidul de rețea](../ghiduri/noduri_retea.md) pentru exemple complete cu IP-uri de probă.
Aceste IP-uri trebuie înlocuite cu cele reale ale calculatoarelor tale.
