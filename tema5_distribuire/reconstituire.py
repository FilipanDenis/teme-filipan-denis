"""Reunește bucățile în ordinea manifestului și verifică integritatea rezultatului."""

import argparse
import hashlib
import json
from pathlib import Path

from comun.retea import BLOC, executa, nume_sigur


def reconstituie(manifest, directoare, iesire):
    with Path(manifest).open(encoding="utf-8") as fisier:
        date = json.load(fisier)
    parti = date.get("parti")
    if not isinstance(parti, list) or not parti:
        raise ValueError("Manifestul trebuie să conțină lista bucăților.")
    nume = [nume_sigur(part["nume"]) for part in parti]
    if len(set(nume)) != len(nume):
        raise ValueError("Manifestul conține nume de bucăți repetate.")
    surse = []
    for part in parti:
        if type(part.get("marime")) is not int or part["marime"] < 0:
            raise ValueError("Dimensiune de bucată invalidă în manifest.")
        gasite = {str((Path(folder) / part["nume"]).resolve()) for folder in directoare
                  if (Path(folder) / part["nume"]).is_file()}
        if len(gasite) != 1:
            raise ValueError(f"Bucata {part['nume']} lipsește sau apare în mai multe directoare.")
        surse.append(Path(gasite.pop()))
    iesire = Path(iesire)
    iesire.parent.mkdir(parents=True, exist_ok=True)
    creat = False
    try:
        with iesire.open("xb") as rezultat:
            creat = True
            total, calcul_total = 0, hashlib.sha256()
            for part, cale in zip(parti, surse):
                calcul, marime = hashlib.sha256(), 0
                with cale.open("rb") as fisier:
                    for date_binare in iter(lambda: fisier.read(BLOC), b""):
                        rezultat.write(date_binare)
                        calcul.update(date_binare)
                        calcul_total.update(date_binare)
                        marime += len(date_binare)
                if marime != part["marime"] or calcul.hexdigest() != part["sha256"]:
                    raise ValueError(f"Bucata {part['nume']} este modificată sau incompletă.")
                total += marime
        if total != date["marime"] or calcul_total.hexdigest() != date["sha256"]:
            raise ValueError("Fișierul reconstituit nu coincide cu cel descris în manifest.")
    except (OSError, ValueError, KeyError):
        if creat:
            iesire.unlink(missing_ok=True)
        raise
    print(f"RECONSTITUIT: {iesire}; {total} octeți; SHA-256 verificat.", flush=True)
    return iesire


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--directoare", nargs="+", required=True,
                        help="Directoarele locale în care se găsesc bucățile primite.")
    parser.add_argument("--iesire", required=True)
    args = parser.parse_args()
    reconstituie(args.manifest, args.directoare, args.iesire)


if __name__ == "__main__":
    executa(main)
