from services.osint_sources import nvd_get_cves
from services.data_pipeline import storage_nosql

def mostrar_menu():
    print("\n🛡️  MONITOR DE SEGURIDAD - MENÚ PRINCIPAL")
    print("1. Buscar CVEs en NVD y guardar en MongoDB")
    print("2. Limpiar la base de datos (colección: vulnerabilidades)")
    print("3. Salir")

def accion_buscar_cves():
    keyword = input("🔎 Introduce palabra clave para buscar CVEs (ej: OpenSSL, Apache, Chrome): ").strip()
    if not keyword:
        print("❌ No se introdujo palabra clave. Cancelando...")
        return
    nvd_get_cves.main(keyword=keyword)

def accion_limpiar_bbdd():
    confirm = input("⚠️  ¿Estás seguro de que quieres eliminar todos los datos? (s/N): ")
    if confirm.lower() == "s":
        deleted = storage_nosql.delete_all("vulnerabilidades")
        print(f"✅ {deleted.deleted_count} documentos eliminados.")
    else:
        print("❌ Operación cancelada.")

def ejecutar_monitor():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            accion_buscar_cves()
        elif opcion == "2":
            accion_limpiar_bbdd()
        elif opcion == "3":
            print("👋 Cerrando monitor. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_monitor()
