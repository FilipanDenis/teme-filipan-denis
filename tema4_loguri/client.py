"""Trimite logul unui proces către colectorul de loguri."""

from comun.retea import executa
from tema2_transfer.client import main as trimite


if __name__ == "__main__":
    executa(lambda: trimite(port_implicit=5400))
