"""Trimite un fișier către un server TCP."""

import argparse

from comun.retea import conecteaza, executa, trimite_fisier


def main(port_implicit=5200):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fisier", help="Calea fișierului de trimis.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=port_implicit)
    parser.add_argument("--nume", help="Opțional, numele sub care va fi salvat la destinație.")
    args = parser.parse_args()
    with conecteaza(args.host, args.port) as conexiune:
        raspuns = trimite_fisier(conexiune, args.fisier, args.nume)
    print(f"TRIMIS: {args.fisier}; {raspuns['marime']} octeți; SHA-256 verificat.")


if __name__ == "__main__":
    executa(main)
