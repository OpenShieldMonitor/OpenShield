import asyncio
import aiohttp
import re
from packaging import version
from services.data_pipeline.storage_local import storage
from config import settings
from urllib.parse import quote
from core.utils import normalizar_nombre_producto
from colorama import Fore, Style

NVD_API_URL = settings.NVD_API_URL
NVD_API_KEY = settings.NVD_API_KEY
HEADERS = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}

# Consulta asíncrona individual
async def fetch_cves(session, product_name):
    print(f"┣━┳━ Petición vulnerabilidades de: {product_name}")
    params = {
        "keywordSearch": product_name,
        "resultsPerPage": 10,
        "hasKev": "true"
    }

    url = f"{NVD_API_URL}?keywordSearch={product_name}&resultsPerPage=10&hasKev"

    async with session.get(url, headers=HEADERS) as resp:
        if resp.status != 200:
            print(f"┃ ┗━ Respuesta ❌ {resp.status} al buscar {product_name}")
            return []
        
        data = await resp.json()
        
        if resp.status == 200:
            count = len(data.get("vulnerabilities", []))
            if count > 0:
                count = f"{Fore.RED}{count}{Style.RESET_ALL}"
            print(f"┃ ┗━ Respuesta ✅ {resp.status} CVEs encontrados: {count}")
        return data.get("vulnerabilities", [])
# Consulta asíncrona individual con espera para evitar HTTP Status Code 429 Too Many Request
async def fetch_con_espera_con_producto(session, nombre_original, version_detectada, delay):
    await asyncio.sleep(delay)
    normalizado = normalizar_nombre_producto(nombre_original)
    cves = await fetch_cves(session, normalizado)
    return (nombre_original, version_detectada, cves)

# Comparar versión de producto con los rangos afectados en NVD
def version_esta_afectada(version_detectada, configurations):
    try:
        ver_detectada = version.parse(version_detectada)
        for config in configurations:
            for nodo in config.get('nodes', []):
                for cpe in nodo.get('cpeMatch', []):
                    if not cpe.get('vulnerable', False):
                        continue

                    v_start_inc = cpe.get("versionStartIncluding")
                    v_start_exc = cpe.get("versionStartExcluding")
                    v_end_inc = cpe.get("versionEndIncluding")
                    v_end_exc = cpe.get("versionEndExcluding")

                    print(f"┣━━ 🧪 Evaluando: {version_detectada} contra {cpe.get('criteria')}")
                    #print(f"    versionStartIncluding={v_start_inc} versionStartExcluding={v_start_exc}, versionEndIncluding={v_end_inc}, versionEndExcluding={v_end_exc}")

                    if v_start_inc and ver_detectada < version.parse(v_start_inc):
                        continue
                    if v_start_exc and ver_detectada <= version.parse(v_start_exc):
                        continue
                    if v_end_inc and ver_detectada > version.parse(v_end_inc):
                        continue
                    if v_end_exc and ver_detectada >= version.parse(v_end_exc):
                        continue

                    # Si pasa todos los filtros → está afectada
                    return True

    except Exception as e:
        print(f"┣━⚠️ Error evaluando versión: {e}")

    return False

# Búsqueda principal
async def buscar_cves_para_software_instalado():
    productos = storage.find_documents("software", projection={"productName": 1, "productVersion": 1, "_id": 0})
    unicos = {(p["productName"], p["productVersion"]) for p in productos if "productName" in p and "productVersion" in p}

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃    Iniciando módulo OSINT    ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"\nEjecutando búsqueda asincrona para {len(unicos)} productos")
    print("Buscando en National Vulnerability Database (NVD)")
    print("Añadimos parámetro hasKev: Known Exploited Vulnerabilities")

    async with aiohttp.ClientSession() as session:
        tareas = []
        delay = 0
        for nombre, version in unicos:
            normalizado = normalizar_nombre_producto(nombre)
            tareas.append(fetch_con_espera_con_producto(session, nombre, version, delay))
            delay += settings.NVD_REQUEST_DELAY

        resultados = await asyncio.gather(*tareas)

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃    Iniciando validación versión afectada    ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    # Unificar y filtrar los CVEs
    cve_docs = []
    for nombre, version_detectada, cves in resultados:
        for cve in cves:
            configurations = cve.get("cve", {}).get("configurations", [])
            if not version_esta_afectada(version_detectada, configurations):
                continue
            
            cvss_score = extract_cvss_score(cve)
            cve_data = cve.get("cve", {})
            cve_docs.append({
                "id": cve_data.get("id"),
                "producto_detectado": nombre,
                "version_detectada": version_detectada,
                "descriptions": [d["value"] for d in cve_data.get("descriptions", [])],
                "references": [r["url"] for r in cve_data.get("references", [])],
                "cvss": cvss_score,
                "severity": clasificar_severidad(cvss_score),
                "source": "NVD-VERIFIED"
            })
            
            print(f"┃ ┗━ ⚠️ Positivo {nombre}{version_detectada}: {cve_data.get("id")} ⚠️")

    if cve_docs:
        storage.delete_all("vulnerabilidades")
        storage.insert_documents("vulnerabilidades", cve_docs)
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Base de datos actualizada con CVEs detectados   ┃")
        print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print(f"┣━ Insertados {len(cve_docs)} CVEs relevantes en la colección 'vulnerabilidades'")
    else:
        print("⚠️ No se encontraron CVEs que afecten a las versiones detectadas")

def extract_cvss_score(cve):
    try:
        metrics = cve.get("cve", {}).get("metrics", {})
        if "cvssMetricV31" in metrics:
            return metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV30" in metrics:
            return metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV2" in metrics:
            return metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
    except Exception:
        pass
    return None

def clasificar_severidad(cvss):
    if cvss is None:
        return "Unknown"
    elif cvss >= 9.0:
        return "Critical"
    elif cvss >= 7.0:
        return "High"
    elif cvss >= 4.0:
        return "Medium"
    elif cvss > 0.0:
        return "Low"
    else:
        return "None"

def normalizar_nombre_producto(nombre):
    """
    Limpia el nombre del producto para mejorar la compatibilidad con NVD.
    Elimina palabras irrelevantes y simplifica.
    """
    nombre = nombre.lower()

    # Palabras comunes a excluir
    palabras_excluir = [
        "microsoft", "visual", "runtime", "redistributable", "x86", "x64",
        "minimum", "maximum", "required", "setup", "package", "component"
    ]

    # Reemplazar símbolos
    nombre = nombre.replace("++", "pp")
    nombre = nombre.replace("c++", "cpp")
    nombre = nombre.replace(" - ", " ")
    nombre = re.sub(r"[^a-z0-9 .]", "", nombre)  # solo letras, números, punto, espacio

    # Eliminar palabras irrelevantes
    nombre_filtrado = " ".join([palabra for palabra in nombre.split() if palabra not in palabras_excluir])

    return nombre_filtrado.strip()


