import os

# === GENERAL ===
PROJECT_NAME = "OpenShield"
VERSION = "1.0.0"
DEBUG_MODE = True

# === FUENTES OSINT ===
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY", "")  # Mejor cargar desde variables de entorno
DEFAULT_CVE_RESULTS = 50
NVD_REQUEST_DELAY = 6

# === ALMACENAMIENTO ===
STORAGE_MODE = "local"  # local with JSONs
#STORAGE_MODE = "mongo"  # MongoDB with Docker
USE_NOSQL = True
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DB_NAME = "openshield"
MONGODB_COLLECTION_SOFTWARE = "software_instalado"
MONGODB_COLLECTION_VULNS = "vulnerabilidades"
DATA_PATH = "data"  # Carpeta donde se almacenan los JSON



# === ANÁLISIS ===
CVSS_SEVERITY_THRESHOLDS = {
    "CRITICAL": 9.0,
    "HIGH": 7.0,
    "MEDIUM": 4.0,
    "LOW": 0.1
}

# === ALERTAS ===
ALERT_LEVEL_TO_NOTIFY = ["CRITICAL", "HIGH"]  # Solo notificar estos niveles

