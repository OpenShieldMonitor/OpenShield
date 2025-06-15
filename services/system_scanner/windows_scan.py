import json
import subprocess
import platform
import sys
from services.data_pipeline.storage_local import storage
from core.spinner import Spinner 

# 1. Funciones

# Función para poder ejecutar comandos en el sistema
def ejecutar_comando(comando):
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if resultado.returncode == 0:
        return resultado.stdout.strip()
    else:
        return f"ERROR: {resultado.stderr.strip()}"

# Funcion para poder exportar a JSON
def exportar_a_json(datos, archivo):
    print(f"Exportando datos a '{archivo}'...")
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)
    print("Exportación completada.\n")

# Función para obtener nombre y versión del sistema operativo
def obtener_os():
    so = platform.system()
    version = platform.release()
    print(f"Sistema operativo detectado: {so} {version}\n")
    return so, {
        "Product_Name": so,
        "Product_Version": version
    }

#2.Recogida de datos de la máquina objetivo

# Listar paquetes instalados dependiendo del sistema operativo detectado
def listar_paquetes_instalados(so):
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃    Inicio módulo análisis del sistema    ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
    spinner = Spinner("Escaneando software instalado...")
    spinner.start()
    paquetes = []
    if so == "Linux":
        salida = ejecutar_comando("apt list --installed 2>/dev/null | tail -n +2")
        for linea in salida.split('\n'):
            if not linea.strip():
                continue
            partes = linea.split('/')
            if len(partes) < 2:
                continue
            nombre = partes[0].strip()
            resto = partes[1].strip().split()
            version = resto[1] if len(resto) >= 2 else "N/A"
            paquetes.append({"Product_Name": nombre, "Product_Version": version})

    elif so == "Darwin":  # macOS
        salida = ejecutar_comando("brew list --versions")
        for linea in salida.split('\n'):
            if not linea.strip():
                continue
            partes = linea.strip().split()
            if len(partes) >= 2:
                nombre = partes[0]
                version = partes[1]
                paquetes.append({"Product_Name": nombre, "Product_Version": version})

    elif so == "Windows":
        try:
            salida = ejecutar_comando('powershell "Get-WmiObject -Class Win32_Product | Select-Object Name, Version"')
        finally:
            spinner.stop()
        for linea in salida.split('\n'):
            if not linea.strip() or 'Name' in linea or '---' in linea:
                continue
            partes = linea.strip().rsplit(None, 1)
            if len(partes) == 2:
                nombre, version = partes
                paquetes.append({"Product_Name": nombre, "Product_Version": version})
                print(f"┣━ {nombre} | versión: {version}")

    else:
        print(" ⚠️ Sistema operativo no reconocido ⚠️")

    print(f"\n  📦 {len(paquetes)} paquetes detectados 📦\n")
    return paquetes

# 3.Export de la información
def main():
    print("\n   🔍 Iniciando escaneo del sistema 🔍\n")
    so_nombre, so_info = obtener_os()

    datos_unificados = {
        "OS": so_info,
        "Installed_Packages": listar_paquetes_instalados(so_nombre)
    }

    guardar_scan(datos_unificados)

def guardar_scan(scan):
    docs = []
    installedPackages = scan.get("Installed_Packages")
    os = scan.get("OS")
    docs.append({
        "productName": os.get("Product_Name"),
        "productVersion": os.get("Product_Version")
    })
    for sw in installedPackages:
        
        docs.append({
            "productName": sw.get("Product_Name"),
            "productVersion": sw.get("Product_Version")
        })
    if docs:
        storage.delete_all("software")
        storage.insert_documents("software", docs)
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Base de datos actualizada con el software detectado   ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else:
        print("⚠️ No se insertó nada ⚠️")
