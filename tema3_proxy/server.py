"""Destinatarul primește conexiunea făcută de proxy."""

from comun.retea import executa
from tema2_transfer.server import main as primeste


if __name__ == "__main__":
    executa(lambda: primeste(port_implicit=5301, director_implicit="rezultate/tema3"))
