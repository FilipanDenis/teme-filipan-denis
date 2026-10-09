"""Primește două loguri și le unește cronologic, păstrând toate înregistrările."""

import argparse
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from comun.retea import TIMEOUT, asculta, executa, primeste_fisier


def uneste_loguri(cai, iesire):
    inregistrari = []
    for cale in cai:
        with Path(cale).open(encoding="utf-8") as fisier:
            for numar, linie in enumerate(fisier, start=1):
                linie = linie.rstrip("\r\n")
                if not linie.strip():
                    continue
                campuri = linie.split(";", 2)
                try:
                    if len(campuri) != 3 or not campuri[1].strip():
                        raise ValueError("Formatul este timestamp;proces;mesaj.")
                    moment = datetime.fromisoformat(campuri[0])
                    # Pentru loguri fără fus orar folosim convenția explicită UTC.
                    if moment.tzinfo is None:
                        moment = moment.replace(tzinfo=timezone.utc)
                    moment = moment.astimezone(timezone.utc)
                except ValueError as eroare:
                    raise ValueError(f"{cale}, linia {numar}: {eroare}") from eroare
                inregistrari.append((moment, linie))
    # Sortarea Python este stabilă: timpii egali păstrează ordinea surselor/liniilor.
    inregistrari.sort(key=lambda inregistrare: inregistrare[0])
    iesire = Path(iesire)
    iesire.parent.mkdir(parents=True, exist_ok=True)
    with iesire.open("x", encoding="utf-8", newline="\n") as rezultat:
        for _, linie in inregistrari:
            rezultat.write(linie + "\n")
    return len(inregistrari)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5400)
    parser.add_argument("--iesire", default="rezultate/tema4/log_comun.log")
    args = parser.parse_args()
    if Path(args.iesire).exists():
        raise FileExistsError(f"{args.iesire} există deja; alege alt fișier de ieșire.")
    with tempfile.TemporaryDirectory() as folder, asculta(args.host, args.port) as server:
        print(f"PREGATIT colector: {args.host}:{server.getsockname()[1]}", flush=True)
        cai = []
        for numar in (1, 2):
            conexiune, _ = server.accept()
            with conexiune:
                conexiune.settimeout(TIMEOUT)
                # Directoare separate permit ca ambele loguri să aibă același nume.
                cale = primeste_fisier(conexiune, Path(folder) / f"proces{numar}")
                cai.append(cale)
            print(f"PRIMIT log {numar}/2: {cale.name}", flush=True)
        numar = uneste_loguri(cai, args.iesire)
    print(f"FINAL: {numar} înregistrări ordonate cronologic în {args.iesire}.", flush=True)


if __name__ == "__main__":
    executa(main)
