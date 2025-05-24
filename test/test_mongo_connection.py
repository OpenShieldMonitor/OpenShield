from services.data_pipeline import storage_nosql

def test_mongo():
    # Insertar un documento de prueba
    test_doc = {
        "nombre": "OpenSSL",
        "version": "1.1.1k",
        "cvss": 7.8,
        "estado": "activo"
    }

    insert_result = storage_nosql.insert_document("vulnerabilidades", test_doc)
    print(f"Documento insertado con ID: {insert_result.inserted_id}")

    # Leer el documento insertado
    results = storage_nosql.find_documents("vulnerabilidades", {"nombre": "OpenSSL"})
    print("Resultados obtenidos:")
    for doc in results:
        print(doc)

    # Eliminar el documento de prueba
    storage_nosql.delete_documents("vulnerabilidades", {"nombre": "OpenSSL"})

if __name__ == "__main__":
    test_mongo()
