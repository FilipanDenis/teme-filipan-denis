"""Verifică ordonarea reală după timp, formatul și primirea de la două procese."""

import tempfile
import unittest
from pathlib import Path

from comun.lansare import Procese, porturi_libere
from tema4_loguri.server import uneste_loguri


class TestLoguri(unittest.TestCase):
    def test_sorteaza_dupa_timp_si_fus_orar(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            a, b = root / "a.log", root / "b.log"
            a.write_text("2026-10-09T08:00:00+03:00;P1;primul\n"
                         "2026-10-09T07:00:00+00:00;P1;ultimul\n", encoding="utf-8")
            b.write_text("2026-10-09T06:00:00+00:00;P2;al doilea\n"
                         "2026-10-09T06:00:00+00:00;P2;al treilea\n", encoding="utf-8")
            iesire = root / "comun.log"
            self.assertEqual(uneste_loguri([a, b], iesire), 4)
            mesaje = [linie.split(";", 2)[2] for linie in iesire.read_text().splitlines()]
            self.assertEqual(mesaje, ["primul", "al doilea", "al treilea", "ultimul"])

    def test_timestamp_invalid_nu_creeaza_rezultatul(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sursa = root / "invalid.log"
            sursa.write_text("nu-e-timestamp;P1;mesaj\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                uneste_loguri([sursa], root / "comun.log")
            self.assertFalse((root / "comun.log").exists())

    def test_doua_loguri_cu_acelasi_nume_in_trei_procese(self):
        with tempfile.TemporaryDirectory() as folder, Procese() as procese:
            root = Path(folder)
            a, b = root / "a" / "log.log", root / "b" / "log.log"
            a.parent.mkdir()
            b.parent.mkdir()
            a.write_text("2026-10-09T08:00:02+03:00;P1;al doilea\n", encoding="utf-8")
            b.write_text("2026-10-09T08:00:01+03:00;P2;primul\n", encoding="utf-8")
            port = porturi_libere(1)[0]
            iesire = root / "comun.log"
            server = procese.server("tema4_loguri.server", "--port", port, "--iesire", iesire)
            procese.client("tema4_loguri.client", a, "--port", port)
            procese.client("tema4_loguri.client", b, "--port", port)
            self.assertIn("2 înregistrări", procese.asteapta(server))
            self.assertEqual([linie.split(";", 2)[1] for linie in iesire.read_text().splitlines()],
                             ["P2", "P1"])


if __name__ == "__main__":
    unittest.main()
