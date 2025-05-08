import os

# === GENERAL ===
PROJECT_NAME = "OpenShield"
VERSION = "1.0.0"
DEBUG_MODE = True

# === FUENTES ABIERTAS ===
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY", "")  # Mejor cargar desde variables de entorno

CCN_CERT_FEED_URL = "https://www.ccn-cert.cni.es/feeds/avisos.xml"
EXPLOIT_DB_SEARCH_URL = "https://www.exploit-db.com/search"

# === SISTEMA LOCAL ===
OSQUERY_PATH = "/usr/bin/osqueryi"  # o ruta en Windows: "C:\\Program Files\\osquery\\osqueryi.exe"

# === ALMACENAMIENTO ===
USE_NOSQL = True
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB_NAME = "monitor_seguridad"
MONGODB_COLLECTION_SOFTWARE = "software_instalado"
MONGODB_COLLECTION_VULNS = "vulnerabilidades"

LOCAL_STORAGE_PATH = "./data/"

# === ANÁLISIS ===
CVSS_SEVERITY_THRESHOLDS = {
    "CRITICAL": 9.0,
    "HIGH": 7.0,
    "MEDIUM": 4.0,
    "LOW": 0.1
}

# === ALERTAS ===
ENABLE_TELEGRAM_ALERTS = True
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ENABLE_WINDOWS_POPUPS = True
ALERT_LEVEL_TO_NOTIFY = ["CRITICAL", "HIGH"]  # Solo notificar estos niveles

# === OTROS ===
LOG_PATH = "./logs/monitor.log"
CACHE_EXPIRATION_HOURS = 24  # Tiempo para reutilizar resultados de fuentes abiertas

