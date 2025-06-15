import requests
import time
import sys
import os

# Añadir path raíz para acceder a config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import settings

NVD_API_URL = settings.NVD_API_URL
NVD_API_KEY = settings.NVD_API_KEY
DEFAULT_CVE_RESULTS = settings.DEFAULT_CVE_RESULTS

HEADERS = {
    "apiKey": NVD_API_KEY
} if NVD_API_KEY else {}

def search_cves_by_keyword(keyword, max_results=DEFAULT_CVE_RESULTS):
    """
    Busca CVEs en NVD por palabra clave.
    """
    results = []
    start_index = 0
    total_results = 1

    while start_index < total_results and len(results) < max_results:
        params = {
            "keywordSearch": keyword,
            "startIndex": start_index,
            "resultsPerPage": 200
        }

        response = requests.get(NVD_API_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()
            total_results = data.get("totalResults", 0)
            vulnerabilities = data.get("vulnerabilities", [])
            results.extend(vulnerabilities)
            start_index += len(vulnerabilities)
            time.sleep(1)
        else:
            print(f"[ERROR] {response.status_code} - {response.text}")
            break

    return results[:max_results]
