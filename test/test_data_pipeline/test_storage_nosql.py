from services.data_pipeline.storage_nosql import *



# Insertar vulnerabilidad
insert_document("vulnerabilidades", {
    "id": "CVE-2024-1234",
    "software": "OpenSSL",
    "version": "1.0.2",
    "cvss": 9.8,
    "estado": "activo"
})

# Buscar
results = find_documents("vulnerabilidades", {"cvss": {"$gte": 7.0}})
for r in results:
    print(r)

# Eliminar por ID
delete_documents("vulnerabilidades", {"id": "CVE-2024-1234"})

# Vaciar colección
delete_all("vulnerabilidades")