# Noțiuni de înțeles pentru prezentare

| Noțiune | Explicație în contextul temelor |
| --- | --- |
| Program | Codul Python salvat în fișiere. |
| Proces | O instanță a programului aflată în execuție. Trei porniri înseamnă trei procese. |
| Nod | Un calculator din rețea; pentru exerciții locale, procesele sunt pe același nod. |
| Client | Procesul care inițiază conexiunea. |
| Server | Procesul care ascultă și acceptă conexiuni. |
| IP | Adresa calculatorului pe care trebuie să ajungă conexiunea. |
| Port | Numărul care identifică serviciul de pe acel calculator. |
| TCP | Un flux de octeți care păstrează ordinea datelor. |
| Proxy | Un intermediar care conectează expeditorul cu destinatarul. |
| Timestamp | Data și ora asociate unei înregistrări din log. |
| SHA-256 | O amprentă folosită aici pentru a verifica dacă fișierul primit este identic. |
| Manifest | Fișierul JSON care descrie bucățile și ordinea necesară reconstituirii. |

## Ce fac principalele instrucțiuni

| Instrucțiune | Rol |
| --- | --- |
| `socket.socket(AF_INET, SOCK_STREAM)` | Creează un socket TCP IPv4. |
| `bind((host, port))` | Leagă serverul de adresa și portul local. |
| `listen(...)` | Pregătește serverul să primească conexiuni. |
| `accept()` | Așteaptă și acceptă un client; întoarce socketul conexiunii. |
| `socket.create_connection(...)` | Conectează clientul la server. |
| `sendall(date)` | Trimite toți octeții indicați sau semnalează o eroare. |
| `recv(n)` | Primește cel mult n octeți, posibil mai puțini. |
| `with ...` | Închide fișierul/socketul la ieșire, inclusiv dacă apare o eroare. |

## De ce nu ajunge un singur recv()

TCP transmite un flux, fără să marcheze automat limitele mesajelor din aplicație.
Dacă trimiți 1000 de octeți, un apel `recv(1000)` poate întoarce numai o parte.
Funcția `primeste_exact` repetă citirea până obține lungimea așteptată.

Pentru mesaje JSON, protocolul transmite întâi lungimea pe 4 octeți, apoi textul JSON UTF-8.
Pentru fișiere, metadatele anunță mărimea și SHA-256. Urmează o confirmare de pregătire,
conținutul de exact acea mărime și o confirmare finală după verificare.

## Adresele folosite

`127.0.0.1` înseamnă propriul calculator. Este potrivit pentru demonstrațiile locale.
`0.0.0.0` se folosește la ascultarea serverului pe interfețele IPv4 locale.
Clientul care se conectează de pe alt calculator folosește IP-ul real al serverului.

## Întrebări pe care le poți primi

**În inel, care proces este server și care este client?**
Fiecare proces joacă ambele roluri: primește de la vecinul anterior și se conectează la următorul.

**Ce diferențiază tema 3 de tema 2?**
Tema 3 introduce un al treilea proces și două conexiuni TCP. Expeditorul contactează proxy-ul,
iar proxy-ul contactează destinatarul și transmite și confirmările înapoi.

**De ce logurile nu sunt unite în ordinea sosirii?**
Ora producerii evenimentului este în timestamp. Un log poate ajunge mai târziu, deși conține
evenimente mai vechi. Soluția sortează după momentul real.

**Cum reconstitui fișierul împărțit?**
Citesc bucățile în ordinea manifestului, le verific separat, apoi verific și amprenta fișierului complet.

**Ai testat pe noduri diferite?**
Această versiune a fost verificată cu procese diferite pe același nod Linux. Codul permite IP-uri
diferite; demonstrația pe calculatoare distincte trebuie efectuată separat dacă profesorul o cere.

Sursă pentru semantica TCP și socket-uri:
[Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html).
