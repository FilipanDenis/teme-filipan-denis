"""Teste end-to-end: programe separate, conectate prin TCP pe localhost."""

import tempfile
import unittest
from pathlib import Path

from comun.lansare import Procese, porturi_libere


class TestProcese(unittest.TestCase):
    def test_inel_trei_procese(self):
        p1, p2, p3 = porturi_libere(3)
        with Procese() as procese:
            b = procese.server("tema1_inel.nod", "--id", 2, "--port", p2, "--urmator-port", p3)
            c = procese.server("tema1_inel.nod", "--id", 3, "--port", p3, "--urmator-port", p1)
            a = procese.server("tema1_inel.nod", "--id", 1, "--port", p1,
                               "--urmator-port", p2, "--mesaj", "Pădure 🌲")
            iesire = procese.asteapta(a)
            self.assertIn("P1 -> P2 -> P3 -> P1", iesire)
            self.assertIn("Pădure 🌲", iesire)
            self.assertIn("P1 -> P2", procese.asteapta(b))
            self.assertIn("P1 -> P2 -> P3", procese.asteapta(c))

    def test_transfer_direct_doua_procese(self):
        self.transfer(proxy=False)

    def test_transfer_proxy_trei_procese(self):
        self.transfer(proxy=True)

    def transfer(self, proxy):
        with tempfile.TemporaryDirectory() as folder, Procese() as procese:
            root = Path(folder)
            sursa = root / "fișier.bin"
            continut = bytes(range(256)) * 5000
            sursa.write_bytes(continut)
            port_server, port_proxy = porturi_libere(2)
            server = procese.server("tema2_transfer.server", "--port", port_server,
                                    "--director", root / "destinatie")
            if proxy:
                intermediar = procese.server("tema3_proxy.proxy", "--port", port_proxy,
                                             "--destinatie-port", port_server)
            client = "tema3_proxy.client" if proxy else "tema2_transfer.client"
            procese.client(client, sursa, "--port", port_proxy if proxy else port_server)
            self.assertIn("SHA-256 verificat", procese.asteapta(server))
            if proxy:
                self.assertIn("FINAL proxy", procese.asteapta(intermediar))
            self.assertEqual((root / "destinatie" / sursa.name).read_bytes(), continut)


if __name__ == "__main__":
    unittest.main()
