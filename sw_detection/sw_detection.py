import platform

def detectar_version_sistema_operativo():
    sistema = platform.system()
    version = platform.version()
    release = platform.release()

    print(f"Sistema operativo: {sistema}")
    print(f"Versión: {version}")
    print(f"Release: {release}")

if __name__ == "__main__":
    detectar_version_sistema_operativo()
