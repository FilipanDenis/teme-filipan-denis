"""Primește un fișier prin TCP și îl salvează în directorul indicat."""

import argparse

from comun.retea import TIMEOUT, asculta, executa, primeste_fisier


def main(port_implicit=5200, director_implicit="rezultate/tema2"):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=port_implicit)
    parser.add_argument("--director", default=director_implicit)
    args = parser.parse_args()
    with asculta(args.host, args.port) as server:
        print(f"PREGATIT server: {args.host}:{server.getsockname()[1]}", flush=True)
        conexiune, adresa = server.accept()
        with conexiune:
            conexiune.settimeout(TIMEOUT)
            print(f"Client conectat: {adresa[0]}:{adresa[1]}", flush=True)
            cale = primeste_fisier(conexiune, args.director)
            print(f"PRIMIT: {cale} ({cale.stat().st_size} octeți); SHA-256 verificat.", flush=True)


if __name__ == "__main__":
    executa(main)
