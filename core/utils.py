import re
import pyfiglet
from colorama import Fore, Style


def normalizar_nombre_producto(nombre):
    nombre = nombre.lower()

    # Palabras comunes a excluir
    palabras_excluir = [
        "microsoft", "visual", "runtime", "redistributable", "x86", "x64",
        "minimum", "maximum", "required", "setup", "package", "component"
    ]

    # Reemplazar símbolos
    nombre = nombre.replace("++", "pp")
    nombre = nombre.replace("c++", "cpp")
    nombre = nombre.replace(" - ", " ")
    nombre = re.sub(r"[^a-z0-9 .]", "", nombre)  # solo letras, números, punto, espacio

    # Eliminar palabras irrelevantes
    nombre_filtrado = " ".join([palabra for palabra in nombre.split() if palabra not in palabras_excluir])

    return nombre_filtrado.strip()

def mostrar_banner():
    banner = pyfiglet.figlet_format("OpenShield", font="slant")
    print(Fore.BLUE + banner)
    print(Fore.CYAN + "Automated OSINT-Based Vulnerability Tracker\n")
