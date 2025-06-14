import asyncio
import logging
from datetime import datetime

from services.osint_sources import nvd_batch_lookup
from services.system_scanner import windows_scan
from services.alerting.eval_vulnerabilities import evaluar_vulnerabilidades_y_notificar

# 📌 Configuración del logger
log_filename = f"logs/daemon_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def daemon():
    logging.info("🛡️  Iniciando ejecución automática del monitor...")

    try:
        logging.info("🔍 Paso 1: Análisis del sistema operativo y software instalado.")
        windows_scan.main()

        logging.info("🌐 Paso 2: Consultando vulnerabilidades en NVD para software detectado.")
        asyncio.run(nvd_batch_lookup.buscar_cves_para_software_instalado())

        logging.info("🔔 Paso 3: Evaluando y notificando vulnerabilidades críticas.")
        evaluar_vulnerabilidades_y_notificar()

        logging.info("✅ Ejecución del monitor completada con éxito.")

    except Exception as e:
        logging.exception(f"❌ Error inesperado durante la ejecución del monitor: {e}")

if __name__ == "__main__":
    daemon()
