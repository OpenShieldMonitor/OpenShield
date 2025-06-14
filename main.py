import os
import pyfiglet
import asyncio
from config import settings
from services.osint_sources import nvd_get_cves
from services.osint_sources import nvd_batch_lookup
from services.system_scanner import windows_scan
from services.data_pipeline.storage_local import storage
from services.alerting.eval_vulnerabilities import evaluar_vulnerabilidades_y_notificar
from colorama import Fore, Style

def mostrar_banner():
    banner = pyfiglet.figlet_format("OpenShield", font="slant")
    print(Fore.BLUE + banner)
    print(Fore.CYAN + "        Automated OSINT-Based Vulnerability Tracker\n")
    

def mostrar_menu():
    mostrar_banner()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃     0. Salir                                               ┃")
    print("┃     1. Buscar CVEs en NVD y guardar                        ┃")
    print("┃     2. Limpiar la base de datos                            ┃")
    print("┃     3. Analizar sistema y exportar a JSON                  ┃")
    print("┃     4. Buscar CVEs desde software detectado                ┃")
    print("┃     5. Evaluar vulnerabilidades y lanzar notificaciones    ┃")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    storage_str = f"Storage Mode: {Fore.RED}{settings.STORAGE_MODE}"
    print(f"┃ {storage_str}{Fore.CYAN}┃{Style.RESET_ALL}")

def accion_buscar_cves():
    keyword = input("🔎 Introduce palabra clave para buscar CVEs (ej: OpenSSL, Apache, Chrome): ").strip()
    if not keyword:
        print("❌ No se introdujo palabra clave. Cancelando...")
        return
    nvd_get_cves.main(keyword=keyword)

def accion_limpiar_bbdd():
    confirm = input("⚠️  ¿Estás seguro de que quieres eliminar todos los datos? (s/N): ")
    if confirm.lower() == "s":
        deleted_vulb = storage.delete_all("vulnerabilidades")
        deleted_sw = storage.delete_all("software")
        print(f"✅ {deleted_vulb.deleted_count} documentos de vulnerabilidades eliminados.")
        print(f"✅ {deleted_sw.deleted_count} documentos de sw instalado eliminados.")
    else:
        print("❌ Operación cancelada.")

def accion_analizar_sistema():
    windows_scan.main()
  
def accion_buscar_cves_para_sistema():
    asyncio.run(nvd_batch_lookup.buscar_cves_para_software_instalado())

def ejecutar_monitor():
    clear = lambda: os.system('cls')
    clear()
    while True:
        mostrar_menu()
        opcion = input("\n>> Selecciona una opción: ").strip()
        if opcion == "1":
            accion_buscar_cves()
        elif opcion == "2":
            accion_limpiar_bbdd()
        elif opcion == "3":
            accion_analizar_sistema()
        elif opcion == "4":
            accion_buscar_cves_para_sistema()
        elif opcion == "5":
            evaluar_vulnerabilidades_y_notificar()
        elif opcion == "0":
            print("👋 Cerrando monitor. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_monitor()
