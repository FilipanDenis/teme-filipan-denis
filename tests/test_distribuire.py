"""Verifică distribuirea în procese separate și reconstituirea fișierului binar."""

import json
import tempfile
import unittest
from pathlib import Path

from comun.lansare import Procese, porturi_libere
from tema5_distribuire.reconstituire import reconstituie


class TestDistribuire(unittest.TestCase):
    def test_binar_mare_si_impartire_inegala(self):
        self.verifica(bytes(range(256)) * 4000 + b"xyz12")

    def test_mai_putini_octeti_decat_noduri(self):
        self.verifica(b"ab")

    def test_fisier_gol(self):
        self.verifica(b"")

    def verifica(self, continut):
        with tempfile.TemporaryDirectory() as folder, Procese() as procese:
            root = Path(folder)
            sursa = root / "fișier.bin"
            sursa.write_bytes(continut)
            porturi = porturi_libere(3)
            directoare = [root / f"nod{i}" for i in (1, 2, 3)]
            servere = [procese.server("tema5_distribuire.server", "--port", port,
                                      "--director", director)
                       for port, director in zip(porturi, directoare)]
            manifest = root / "manifest.json"
            procese.client("tema5_distribuire.client", sursa, "--manifest", manifest,
                            "--noduri", *[f"127.0.0.1:{port}" for port in porturi])
            for server in servere:
                procese.asteapta(server)
            date = json.loads(manifest.read_text(encoding="utf-8"))
            dimensiuni = [part["marime"] for part in date["parti"]]
            self.assertEqual(sum(dimensiuni), len(continut))
            self.assertLessEqual(max(dimensiuni) - min(dimensiuni), 1)
            rezultat = root / "refacut.bin"
            procese.client("tema5_distribuire.reconstituire", "--manifest", manifest,
                            "--directoare", *directoare, "--iesire", rezultat)
            self.assertEqual(rezultat.read_bytes(), continut)
            # Modificarea unei bucăți trebuie să fie detectată, cu ștergerea ieșirii incomplete.
            prima = directoare[0] / date["parti"][0]["nume"]
            prima.write_bytes(prima.read_bytes() + b"corupt")
            incomplet = root / "incomplet.bin"
            with self.assertRaises(ValueError):
                reconstituie(manifest, directoare, incomplet)
            self.assertFalse(incomplet.exists())
            prima.unlink()
            with self.assertRaises(ValueError):
                reconstituie(manifest, directoare, root / "lipsa.bin")


if __name__ == "__main__":
    unittest.main()
