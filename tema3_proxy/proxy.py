"""Proxy TCP: transmite octeții și confirmările în ambele direcții."""

import argparse
import socket
import threading

from comun.retea import BLOC, TIMEOUT, asculta, conecteaza, executa


def releu(sursa, destinatie, erori):
    try:
        while True:
            date = sursa.recv(BLOC)
            if not date:
                break
            destinatie.sendall(date)
        # EOF într-un sens; sensul opus poate încă transmite confirmarea.
        destinatie.shutdown(socket.SHUT_WR)
    except OSError as eroare:
        erori.append(str(eroare))
        for conexiune in (sursa, destinatie):
            try:
                conexiune.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5300)
    parser.add_argument("--destinatie-host", default="127.0.0.1")
    parser.add_argument("--destinatie-port", type=int, default=5301)
    args = parser.parse_args()
    with asculta(args.host, args.port) as server:
        print(f"PREGATIT proxy: {args.host}:{server.getsockname()[1]}", flush=True)
        expeditor, _ = server.accept()
        with expeditor, conecteaza(args.destinatie_host, args.destinatie_port) as destinatar:
            expeditor.settimeout(TIMEOUT)
            print(f"Proxy conectat la {args.destinatie_host}:{args.destinatie_port}", flush=True)
            erori = []
            # Două sensuri simultane: fișierul înainte, confirmările înapoi.
            fir = threading.Thread(target=releu, args=(destinatar, expeditor, erori), daemon=True)
            fir.start()
            releu(expeditor, destinatar, erori)
            fir.join(TIMEOUT + 1)
            if fir.is_alive() or erori:
                raise RuntimeError("Proxy: " + (erori[0] if erori else "conexiunea nu s-a încheiat"))
    print("FINAL proxy: transferul și confirmările au fost retransmise.", flush=True)


if __name__ == "__main__":
    executa(main)
