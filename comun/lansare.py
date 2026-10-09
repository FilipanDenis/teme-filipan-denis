"""Pornește procese reale pentru demonstrații și teste; nu implementează protocolul."""

import queue
import socket
import subprocess
import sys
import threading
from pathlib import Path

RADACINA = Path(__file__).resolve().parents[1]


def porturi_libere(numar):
    servere = []
    try:
        for _ in range(numar):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servere.append(server)
            server.bind(("127.0.0.1", 0))
        return [server.getsockname()[1] for server in servere]
    finally:
        for server in servere:
            server.close()


class Procese:
    def __init__(self, afiseaza=False):
        self.afiseaza = afiseaza
        self.servere = []

    def comanda(self, modul, argumente):
        return [sys.executable, "-u", "-m", modul, *map(str, argumente)]

    def server(self, modul, *argumente):
        proces = subprocess.Popen(self.comanda(modul, argumente), cwd=RADACINA,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, encoding="utf-8")
        info = {"proces": proces, "modul": modul, "prima": ""}
        self.servere.append(info)
        raspuns = queue.Queue()
        cititor = threading.Thread(target=lambda: raspuns.put(proces.stdout.readline()), daemon=True)
        cititor.start()
        try:
            prima = raspuns.get(timeout=10)
        except queue.Empty:
            raise RuntimeError(f"{modul} nu a pornit în 10 secunde.") from None
        info["prima"] = prima
        if not prima.startswith("PREGATIT"):
            raise RuntimeError(f"{modul} nu a pornit: {prima.strip()}")
        return proces

    def client(self, modul, *argumente):
        rezultat = subprocess.run(self.comanda(modul, argumente), cwd=RADACINA,
                                  capture_output=True, text=True, encoding="utf-8", timeout=20)
        iesire = rezultat.stdout + rezultat.stderr
        if self.afiseaza:
            print(f"\n[{modul}]\n{iesire}", end="", flush=True)
        if rezultat.returncode:
            raise RuntimeError(f"{modul} a eșuat:\n{iesire}")
        return iesire

    def asteapta(self, proces):
        info = next(info for info in self.servere if info["proces"] is proces)
        rest, _ = proces.communicate(timeout=20)
        iesire = info["prima"] + rest
        if self.afiseaza:
            print(f"\n[{info['modul']}]\n{iesire}", end="", flush=True)
        if proces.returncode:
            raise RuntimeError(f"{info['modul']} a eșuat:\n{iesire}")
        return iesire

    def __enter__(self):
        return self

    def __exit__(self, *_):
        for info in self.servere:
            proces = info["proces"]
            if proces.poll() is None:
                proces.terminate()
            try:
                proces.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proces.kill()
                proces.communicate()
