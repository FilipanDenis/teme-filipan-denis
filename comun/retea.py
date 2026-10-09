"""Protocol TCP simplu: metadate JSON, apoi numărul exact de octeți al fișierului."""

import hashlib
import json
import socket
import struct
import sys
from pathlib import Path

BLOC = 65536
MAX_JSON = 65536
TIMEOUT = 30


def asculta(host, port):
    """Creează serverul; accept() va aștepta conectarea unui client."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
    except OSError:
        server.close()
        raise
    return server


def conecteaza(host, port):
    return socket.create_connection((host, port), timeout=TIMEOUT)


def primeste_exact(conexiune, numar):
    """TCP poate livra un mesaj în mai multe bucăți, deci repetăm recv()."""
    rezultat = bytearray()
    while len(rezultat) < numar:
        bucata = conexiune.recv(min(BLOC, numar - len(rezultat)))
        if not bucata:
            raise EOFError("Conexiunea s-a închis înainte de primirea tuturor datelor.")
        rezultat.extend(bucata)
    return bytes(rezultat)


def trimite_json(conexiune, mesaj):
    date = json.dumps(mesaj, ensure_ascii=False).encode("utf-8")
    if not 0 < len(date) <= MAX_JSON:
        raise ValueError("Metadatele JSON trebuie să aibă între 1 și 65536 octeți.")
    # !I = un număr întreg de 4 octeți, în ordinea de octeți folosită în rețea.
    conexiune.sendall(struct.pack("!I", len(date)) + date)


def primeste_json(conexiune):
    lungime = struct.unpack("!I", primeste_exact(conexiune, 4))[0]
    if not 0 < lungime <= MAX_JSON:
        raise ValueError("Lungime JSON invalidă.")
    mesaj = json.loads(primeste_exact(conexiune, lungime).decode("utf-8"))
    if not isinstance(mesaj, dict):
        raise ValueError("Mesajul JSON trebuie să fie un obiect.")
    return mesaj


def verifica_raspuns(raspuns):
    if raspuns.get("ok") is not True:
        raise RuntimeError(raspuns.get("eroare", "Destinatarul a refuzat operația."))


def nume_sigur(nume):
    if (not isinstance(nume, str) or not nume or nume in (".", "..")
            or any(c in nume for c in '/\\:\x00')):
        raise ValueError("Numele fișierului trebuie să fie un nume simplu, fără cale.")
    return nume


def sha256_fisier(cale):
    calcul = hashlib.sha256()
    with Path(cale).open("rb") as fisier:
        for bucata in iter(lambda: fisier.read(BLOC), b""):
            calcul.update(bucata)
    return calcul.hexdigest()


def trimite_fisier(conexiune, cale, nume=None):
    cale = Path(cale)
    nume = nume_sigur(cale.name if nume is None else nume)
    with cale.open("rb") as fisier:
        # Calculăm metadatele din același fișier deschis pe care îl vom trimite.
        calcul = hashlib.sha256()
        marime = 0
        for bucata in iter(lambda: fisier.read(BLOC), b""):
            calcul.update(bucata)
            marime += len(bucata)
        fisier.seek(0)
        trimite_json(conexiune, {
            "nume": nume, "marime": marime, "sha256": calcul.hexdigest(),
        })
        verifica_raspuns(primeste_json(conexiune))  # Destinatarul este pregătit.
        ramasi = marime
        while ramasi:
            bucata = fisier.read(min(BLOC, ramasi))
            if not bucata:
                raise EOFError("Fișierul sursă s-a modificat în timpul transferului.")
            conexiune.sendall(bucata)
            ramasi -= len(bucata)
    raspuns = primeste_json(conexiune)  # Confirmare după scriere și verificare.
    verifica_raspuns(raspuns)
    return raspuns


def primeste_fisier(conexiune, director):
    metadate = primeste_json(conexiune)
    cale = None
    creat = False
    try:
        nume = nume_sigur(metadate.get("nume"))
        marime = metadate.get("marime")
        if type(marime) is not int or marime < 0:
            raise ValueError("Dimensiune de fișier invalidă.")
        amprenta = metadate.get("sha256")
        if (not isinstance(amprenta, str) or len(amprenta) != 64
                or any(c not in "0123456789abcdef" for c in amprenta)):
            raise ValueError("Amprenta SHA-256 este invalidă.")
        director = Path(director)
        director.mkdir(parents=True, exist_ok=True)
        cale = director / nume
        # xb refuză suprascrierea unui fișier existent.
        with cale.open("xb") as fisier:
            creat = True
            trimite_json(conexiune, {"ok": True})
            calcul = hashlib.sha256()
            ramasi = marime
            while ramasi:
                bucata = primeste_exact(conexiune, min(BLOC, ramasi))
                fisier.write(bucata)
                calcul.update(bucata)
                ramasi -= len(bucata)
        if calcul.hexdigest() != amprenta:
            raise ValueError("SHA-256 diferă: fișierul primit nu coincide cu sursa.")
    except (OSError, ValueError, EOFError) as eroare:
        if creat:
            cale.unlink(missing_ok=True)  # Ștergem numai copia incompletă creată acum.
        try:
            trimite_json(conexiune, {"ok": False, "eroare": str(eroare)})
        except OSError:
            pass
        raise
    trimite_json(conexiune, {"ok": True, "marime": marime, "sha256": amprenta})
    return cale


def executa(functie):
    """Afișează erorile uzuale într-un mod ușor de citit în terminal."""
    try:
        functie()
    except KeyboardInterrupt:
        print("\nProgram oprit.", file=sys.stderr)
        sys.exit(130)
    except (OSError, ValueError, EOFError, RuntimeError, KeyError) as eroare:
        print(f"EROARE: {eroare}", file=sys.stderr)
        sys.exit(1)
