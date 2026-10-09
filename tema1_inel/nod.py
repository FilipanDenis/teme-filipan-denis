"""Fiecare proces primește pe portul său și trimite către următorul proces."""

import argparse

from comun.retea import (TIMEOUT, asculta, conecteaza, executa,
                         primeste_json, trimite_json)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--urmator-host", default="127.0.0.1")
    parser.add_argument("--urmator-port", type=int, required=True)
    parser.add_argument("--mesaj", default="Salut, Denis! Mesaj trimis în inel.")
    args = parser.parse_args()

    with asculta(args.host, args.port) as server:
        print(f"PREGATIT P{args.id}: {args.host}:{server.getsockname()[1]}", flush=True)
        # P1 inițiază mesajul. P2 și P3 așteaptă să îl primească.
        if args.id == 1:
            mesaj = {"text": args.mesaj, "traseu": [1]}
            with conecteaza(args.urmator_host, args.urmator_port) as iesire:
                trimite_json(iesire, mesaj)
            print(f"P1 a trimis: {args.mesaj}", flush=True)

        conexiune, _ = server.accept()
        with conexiune:
            conexiune.settimeout(TIMEOUT)
            mesaj = primeste_json(conexiune)
        traseu_asteptat = {1: [1, 2, 3], 2: [1], 3: [1, 2]}[args.id]
        if mesaj.get("traseu") != traseu_asteptat or not isinstance(mesaj.get("text"), str):
            raise ValueError("Mesaj invalid sau procesele nu sunt legate în ordinea P1-P2-P3-P1.")

        mesaj["traseu"].append(args.id)
        traseu = " -> ".join(f"P{numar}" for numar in mesaj["traseu"])
        print(f"P{args.id} a primit: {mesaj['text']}", flush=True)
        print(f"TRASEU: {traseu}", flush=True)
        if args.id == 1:
            print("FINAL: mesajul a revenit la P1 după un tur complet.", flush=True)
        else:
            # Același proces este server la primire și client la transmitere.
            with conecteaza(args.urmator_host, args.urmator_port) as iesire:
                trimite_json(iesire, mesaj)


if __name__ == "__main__":
    executa(main)
