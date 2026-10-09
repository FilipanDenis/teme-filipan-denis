# Fedora și GitHub — de la zero

Repository public: [FilipanDenis/teme-filipan-denis](https://github.com/FilipanDenis/teme-filipan-denis).
Profesorul poate vedea proiectul prin acest link. Pentru vizualizare nu este necesară o invitație.

## 1. Verifică programele pe Fedora

Deschide terminalul:

```bash
python3 --version
git --version
```

Proiectul necesită Python 3.10 sau mai nou. Dacă lipsește unul dintre programe:

```bash
sudo dnf install python3 git
```

Nu sunt necesare biblioteci externe sau un server web. Poți folosi orice editor de text.

## 2. Descarcă proiectul

Din directorul în care vrei să păstrezi proiectele:

```bash
git clone https://github.com/FilipanDenis/teme-filipan-denis.git
cd teme-filipan-denis
```

`git clone` descarcă fișierele și istoricul. `cd` te mută în folderul proiectului.
Toate comenzile temelor se rulează din acest folder, unde se află `demo.py`.
Dacă ai deja o copie clonată a repository-ului, intră în ea și folosește `git pull` pentru actualizare.

## 3. Prima temă: mesajul în inel

```bash
python3 demo.py 1
```

Demo-ul pornește trei procese separate. La sfârșit trebuie să vezi:

```text
TRASEU: P1 -> P2 -> P3 -> P1
FINAL: mesajul a revenit la P1 după un tur complet.
```

Pentru a înțelege fiecare pas, deschide [instrucțiunile temei 1](../tema1_inel/README.md)
și rulează manual cele trei procese în terminale separate.

## 4. Celelalte teme

```bash
python3 demo.py 2
python3 demo.py 3
python3 demo.py 4
python3 demo.py 5
```

Pentru toate odată: `python3 demo.py toate`.
Fiecare demonstrație salvează rezultatele într-un folder nou din `rezultate/`.

| Tema | Instrucțiuni | Ce observi |
| --- | --- | --- |
| 1 | [Inel](../tema1_inel/README.md) | Mesajul revine la P1. |
| 2 | [Transfer direct](../tema2_transfer/README.md) | Serverul salvează copia fișierului. |
| 3 | [Proxy](../tema3_proxy/README.md) | Fișierul și confirmările trec prin intermediar. |
| 4 | [Loguri](../tema4_loguri/README.md) | Șase înregistrări sunt unite cronologic. |
| 5 | [Distribuire](../tema5_distribuire/README.md) | Bucățile sunt trimise și fișierul este reconstituit. |

Pentru testele automate:

```bash
python3 -m unittest discover -s tests -v
```

## 5. Accesul profesorului

Trimite profesorului linkul repository-ului prin canalul cerut la curs:

https://github.com/FilipanDenis/teme-filipan-denis

Poți verifica accesul deschizând linkul într-o fereastră privată, fără autentificare.
Doar dacă profesorul cere și drept de modificare, folosește
**Settings → Collaborators → Add people**, cu username-ul său GitHub exact.

## 6. Modificări și actualizări

Configurează autorul commiturilor în copia clonată. Adresa poate fi cea `noreply` din
**GitHub Settings → Emails**:

```bash
git config user.name "FilipanDenis"
read -r -p "Adresa de e-mail pentru commituri: " autor_email
git config user.email "$autor_email"
```

După ce modifici codul sau explicațiile:

```bash
python3 -m unittest discover -s tests -v
git status
git add .
git commit -m "Explic traseul mesajului din tema 1"
git push
```

Alege un mesaj care descrie modificarea ta. `git add` pregătește fișierele, `git commit`
creează un punct în istoric, iar `git push` îl trimite pe GitHub.
Pentru publicarea prin Git ai nevoie de autentificare configurată separat de browser;
vezi [ghidul oficial](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github).

GitHub permite și editarea fișierelor din browser. După o editare online, folosește `git pull`
în copia locală înainte să continui lucrul. `.gitignore` exclude rezultatele și fișierele temporare.

## Probleme uzuale

- Rulează comenzile din rădăcina proiectului, cu `python3 -m tema...`.
- Pornește serverul înaintea clientului și așteaptă mesajul `PREGATIT`.
- „Connection refused”: verifică serverul, IP-ul și portul.
- „Address already in use”: oprește procesul vechi cu `Ctrl+C` sau alege alt port în ambele comenzi.
- „File exists”: copia veche este păstrată; alege alt director de ieșire.

Pentru calculatoare distincte vezi [ghidul de rețea](noduri_retea.md).

## Surse

- [Python în Fedora](https://developer.fedoraproject.org/tech/languages/python/python-installation.html)
- [GitHub — repository-uri publice](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [GitHub — colaboratori](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository)
