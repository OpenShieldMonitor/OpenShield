import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from services.osint_sources.nvd_client import search_cves_by_keyword
from services.data_pipeline import storage_nosql

def guardar_vulnerabilidades(cves):
    docs = []
    for cve in cves:
        cve_data = cve.get("cve", {})
        docs.append({
            "id": cve_data.get("id"),
            "descriptions": [d["value"] for d in cve_data.get("descriptions", [])],
            "references": [r["url"] for r in cve_data.get("references", [])],
            "cvss": extract_cvss_score(cve),
            "source": "NVD"
        })
    if docs:
        storage_nosql.insert_documents("vulnerabilidades", docs)
        print(f"✅ {len(docs)} CVEs insertados en la base de datos.")
    else:
        print("⚠️ No se insertó nada.")

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

def main(keyword="OpenSSL", max_results=10):
    print(f"🔍 Buscando CVEs relacionados con: {keyword}")
    cves = search_cves_by_keyword(keyword, max_results=max_results)

    if not cves:
        print("❌ No se encontraron resultados.")
        return

    guardar_vulnerabilidades(cves)
