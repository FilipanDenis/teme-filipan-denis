"""Verifică mesajele fragmentate și fișierele binare, goale sau întrerupte."""

import hashlib
import json
import socket
import struct
import tempfile
import threading
import unittest
from pathlib import Path

from comun.retea import (primeste_exact, primeste_fisier, primeste_json,
                         sha256_fisier, trimite_fisier, trimite_json)


class TestRetea(unittest.TestCase):
    def test_mesaj_json_fragmentat(self):
        a, b = socket.socketpair()
        mesaj = {"text": "Salut, pădure! 🌲"}
        date = json.dumps(mesaj, ensure_ascii=False).encode("utf-8")
        cadru = struct.pack("!I", len(date)) + date
        def trimite():
            with a:
                for octet in cadru:
                    a.sendall(bytes([octet]))
        fir = threading.Thread(target=trimite)
        fir.start()
        with b:
            b.settimeout(5)
            self.assertEqual(primeste_json(b), mesaj)
        fir.join(5)
        self.assertFalse(fir.is_alive())

    def test_lungime_json_invalida(self):
        for lungime in (0, 65537):
            with self.subTest(lungime=lungime):
                a, b = socket.socketpair()
                with a, b:
                    a.sendall(struct.pack("!I", lungime))
                    with self.assertRaises(ValueError):
                        primeste_json(b)

    def test_inchidere_inainte_de_final(self):
        a, b = socket.socketpair()
        with a, b:
            a.sendall(b"abc")
            a.shutdown(socket.SHUT_WR)
            with self.assertRaises(EOFError):
                primeste_exact(b, 10)

    def transfer(self, continut):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sursa = root / "fișier.bin"
            sursa.write_bytes(continut)
            a, b = socket.socketpair()
            erori = []
            def primitor():
                with b:
                    b.settimeout(5)
                    try:
                        primeste_fisier(b, root / "primit")
                    except Exception as eroare:
                        erori.append(eroare)
            fir = threading.Thread(target=primitor)
            fir.start()
            with a:
                a.settimeout(5)
                raspuns = trimite_fisier(a, sursa)
            fir.join(5)
            self.assertFalse(fir.is_alive())
            self.assertEqual(erori, [])
            self.assertEqual((root / "primit" / sursa.name).read_bytes(), continut)
            self.assertEqual(raspuns["sha256"], sha256_fisier(sursa))

    def test_transfer_binar_mare(self):
        self.transfer(bytes(range(256)) * 5000)

    def test_transfer_gol(self):
        self.transfer(b"")

    def test_transfer_corupt_sterge_copia(self):
        self.transfer_invalid("a.bin", 3, "0" * 64, b"abc", ValueError)

    def test_transfer_intrerupt_sterge_copia(self):
        self.transfer_invalid("a.bin", 10, hashlib.sha256(b"abc").hexdigest(), b"abc", EOFError)

    def test_nume_cu_cale_refuzat(self):
        self.transfer_invalid("../a.bin", 0, hashlib.sha256(b"").hexdigest(), b"", ValueError)

    def transfer_invalid(self, nume, marime, amprenta, continut, tip_eroare):
        with tempfile.TemporaryDirectory() as folder:
            a, b = socket.socketpair()
            with a, b:
                trimite_json(a, {"nume": nume, "marime": marime, "sha256": amprenta})
                a.sendall(continut)
                a.shutdown(socket.SHUT_WR)
                with self.assertRaises(tip_eroare):
                    primeste_fisier(b, folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_nu_suprascrie_fisier_existent(self):
        with tempfile.TemporaryDirectory() as folder:
            existent = Path(folder) / "a.bin"
            existent.write_bytes(b"original")
            a, b = socket.socketpair()
            with a, b:
                trimite_json(a, {"nume": "a.bin", "marime": 0,
                                "sha256": hashlib.sha256(b"").hexdigest()})
                with self.assertRaises(FileExistsError):
                    primeste_fisier(b, folder)
                self.assertFalse(primeste_json(a)["ok"])
            self.assertEqual(existent.read_bytes(), b"original")


if __name__ == "__main__":
    unittest.main()
