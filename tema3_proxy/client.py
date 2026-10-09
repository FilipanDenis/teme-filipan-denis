"""Expeditorul folosește același protocol de fișier, dar se conectează la proxy."""

from comun.retea import executa
from tema2_transfer.client import main as trimite


if __name__ == "__main__":
    executa(lambda: trimite(port_implicit=5300))
