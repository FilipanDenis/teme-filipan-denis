"""Un nod primește o bucată de fișier de la distribuitor."""

from comun.retea import executa
from tema2_transfer.server import main as primeste


if __name__ == "__main__":
    executa(lambda: primeste(port_implicit=5501, director_implicit="rezultate/tema5/nod1"))
