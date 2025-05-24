import argparse
from services.data_pipeline import storage_nosql

def limpiar_base_de_datos():
    confirm = input("⚠️ ¿Estás seguro de que quieres eliminar todos los datos de la colección 'vulnerabilidades'? (s/N): ")
    if confirm.lower() == "s":
        deleted = storage_nosql.delete_all("vulnerabilidades")
        print(f"✅ {deleted.deleted_count} documentos eliminados.")
    else:
        print("❌ Operación cancelada.")

def main():
    parser = argparse.ArgumentParser(description="Monitor de Seguridad - Ejecutor")
    parser.add_argument("accion", help="Acción a realizar", choices=["get_nvd_cves", "limpiar_bbdd"])
    args = parser.parse_args()

    if args.accion == "get_nvd_cves":
        from services.osint_sources import nvd_get_cves
        nvd_get_cves.main()
    elif args.accion == "limpiar_bbdd":
        limpiar_base_de_datos()

if __name__ == "__main__":
    main()
