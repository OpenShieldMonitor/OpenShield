from services.data_pipeline.storage_local import storage
from services.alerting.notifier import mostrar_alerta_windows

def evaluar_vulnerabilidades_y_notificar():
    criticas = ["High", "Critical"]
    vulnerabilidades = storage.find_documents("vulnerabilidades")

    if not vulnerabilidades:
        print("✅ No hay vulnerabilidades almacenadas.")
        return

    relevantes = [v for v in vulnerabilidades if v.get("severity") in criticas]

    if not relevantes:
        print("✅ No hay vulnerabilidades críticas o altas.")
        return

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃    Iniciando módulo de alertas     ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
    print(f"⚠️ Se han detectado {len(relevantes)} vulnerabilidades alto riesgo [CVSSv3 > 7.0].\n")

    for v in relevantes:
        producto = v.get("producto_detectado", "Desconocido")
        version = v.get("version_detectada", "N/A")
        severity = v.get("severity", "UNKNOWN")
        cve_id = v.get("id")
        enlaces = v.get("references", [])
        enlace_cve = f"https://nvd.nist.gov/vuln/detail/{cve_id}"

        mostrar_alerta_windows(producto, version, severity, cve_id=cve_id, enlace=enlace_cve)
