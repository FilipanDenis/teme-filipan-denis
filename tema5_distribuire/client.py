"""Împarte fișierul în N bucăți apropiate ca mărime și trimite câte una fiecărui nod."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from comun.retea import BLOC, conecteaza, executa, sha256_fisier, trimite_fisier


def adresa_nod(text):
    try:
        host, port = text.rsplit(":", 1)
        port = int(port)
        if not host or not 1 <= port <= 65535:
            raise ValueError
        return host, port
    except ValueError:
        raise argparse.ArgumentTypeError("Nodul se scrie HOST:PORT, de exemplu 127.0.0.1:5501.") from None


def distribuie(cale, noduri, manifest):
    cale, manifest = Path(cale), Path(manifest)
    if not noduri:
        raise ValueError("Este necesar cel puțin un nod.")
    if manifest.exists():
        raise FileExistsError(f"{manifest} există deja; alege alt manifest.")
    parti = []
    calcul_total = hashlib.sha256()
    with cale.open("rb") as sursa, tempfile.TemporaryDirectory() as folder:
        sursa.seek(0, 2)
        marime = sursa.tell()
        sursa.seek(0)
        cat, rest = divmod(marime, len(noduri))
        for index, (host, port) in enumerate(noduri, start=1):
            nume = f"{cale.name}.part{index:03d}"
            bucata = Path(folder) / nume
            dimensiune = cat + (1 if index <= rest else 0)
            # Scriem și trimitem o singură bucată odată, fără a încărca tot fișierul în RAM.
            with bucata.open("wb") as destinatie:
                ramasi = dimensiune
                while ramasi:
                    date = sursa.read(min(BLOC, ramasi))
                    if not date:
                        raise EOFError("Fișierul s-a micșorat în timpul împărțirii.")
                    destinatie.write(date)
                    calcul_total.update(date)
                    ramasi -= len(date)
            with conecteaza(host, port) as conexiune:
                trimite_fisier(conexiune, bucata)
            parti.append({"nume": nume, "marime": dimensiune,
                          "sha256": sha256_fisier(bucata), "nod": f"{host}:{port}"})
            print(f"DISTRIBUIT {index}/{len(noduri)}: {nume}, {dimensiune} octeți -> {host}:{port}", flush=True)
        if sursa.read(1):
            raise ValueError("Fișierul s-a mărit în timpul împărțirii; repetă pe o sursă stabilă.")
    date = {"original": cale.name, "marime": marime, "sha256": calcul_total.hexdigest(), "parti": parti}
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("x", encoding="utf-8") as fisier:
        json.dump(date, fisier, ensure_ascii=False, indent=2)
        fisier.write("\n")
    print(f"MANIFEST: {manifest}", flush=True)
    return date


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fisier")
    parser.add_argument("--noduri", nargs="+", type=adresa_nod, required=True)
    parser.add_argument("--manifest", default="rezultate/tema5/manifest.json")
    args = parser.parse_args()
    distribuie(args.fisier, args.noduri, args.manifest)


if __name__ == "__main__":
    executa(main)
