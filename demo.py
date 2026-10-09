"""Demonstrații locale: python3 demo.py 1 sau python3 demo.py toate."""

import argparse
from datetime import datetime

from comun.lansare import RADACINA, Procese, porturi_libere
from comun.retea import executa, sha256_fisier


def verifica_fisier(sursa, copie):
    if sha256_fisier(sursa) != sha256_fisier(copie):
        raise RuntimeError("Fișierul rezultat diferă de original.")
    print("VERIFICAT: copia și originalul au aceeași amprentă SHA-256.", flush=True)


def demonstreaza(tema, folder):
    folder.mkdir(parents=True, exist_ok=True)
    sursa = RADACINA / "exemple" / "mesaj.txt"
    print(f"\nTEMA {tema} — procese Python separate, conectate prin TCP", flush=True)
    with Procese(afiseaza=True) as procese:
        if tema == 1:
            p1, p2, p3 = porturi_libere(3)
            b = procese.server("tema1_inel.nod", "--id", 2, "--port", p2, "--urmator-port", p3)
            c = procese.server("tema1_inel.nod", "--id", 3, "--port", p3, "--urmator-port", p1)
            a = procese.server("tema1_inel.nod", "--id", 1, "--port", p1, "--urmator-port", p2)
            iesire = procese.asteapta(a)
            procese.asteapta(b)
            procese.asteapta(c)
            if "P1 -> P2 -> P3 -> P1" not in iesire:
                raise RuntimeError("Mesajul nu a parcurs tot inelul.")
            (folder / "traseu.txt").write_text(iesire, encoding="utf-8")
        elif tema in (2, 3):
            port_server, port_proxy = porturi_libere(2)
            modul = "tema2_transfer" if tema == 2 else "tema3_proxy"
            server = procese.server(modul + ".server", "--port", port_server, "--director", folder)
            if tema == 3:
                proxy = procese.server("tema3_proxy.proxy", "--port", port_proxy,
                                       "--destinatie-port", port_server)
            procese.client(modul + ".client", sursa, "--port", port_proxy if tema == 3 else port_server)
            procese.asteapta(server)
            if tema == 3:
                procese.asteapta(proxy)
            verifica_fisier(sursa, folder / sursa.name)
        elif tema == 4:
            port = porturi_libere(1)[0]
            iesire = folder / "log_comun.log"
            server = procese.server("tema4_loguri.server", "--port", port, "--iesire", iesire)
            for numar in (1, 2):
                procese.client("tema4_loguri.client", RADACINA / "exemple" / f"proces{numar}.log",
                                "--port", port)
            procese.asteapta(server)
            linii = iesire.read_text(encoding="utf-8").splitlines()
            if len(linii) != 6 or [linie.split(";")[1] for linie in linii] != ["P1", "P2"] * 3:
                raise RuntimeError("Logul comun nu are cele șase linii în ordinea așteptată.")
            print("\nLOG COMUN:\n" + "\n".join(linii), flush=True)
        elif tema == 5:
            porturi = porturi_libere(3)
            directoare = [folder / f"nod{i}" for i in (1, 2, 3)]
            servere = [procese.server("tema5_distribuire.server", "--port", port, "--director", director)
                       for port, director in zip(porturi, directoare)]
            manifest = folder / "manifest.json"
            procese.client("tema5_distribuire.client", sursa, "--manifest", manifest,
                            "--noduri", *[f"127.0.0.1:{port}" for port in porturi])
            for server in servere:
                procese.asteapta(server)
            iesire = folder / "mesaj_reconstituit.txt"
            procese.client("tema5_distribuire.reconstituire", "--manifest", manifest,
                            "--directoare", *directoare, "--iesire", iesire)
            verifica_fisier(sursa, iesire)
    print(f"\nTEMA {tema}: OK. Rezultate: {folder.relative_to(RADACINA)}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tema", choices=("1", "2", "3", "4", "5", "toate"))
    args = parser.parse_args()
    moment = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder = RADACINA / "rezultate" / f"demo_{moment}"
    teme = range(1, 6) if args.tema == "toate" else [int(args.tema)]
    for tema in teme:
        demonstreaza(tema, folder / f"tema{tema}")
    print("\nDemonstrație încheiată cu succes.", flush=True)


if __name__ == "__main__":
    executa(main)
