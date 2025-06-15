# 📐 Arquitectura del Proyecto OpenShield

---

## 🔰 Objetivo

OpenShield es una herramienta de monitorización de vulnerabilidades basada en el análisis de software instalado localmente y la búsqueda de CVEs en fuentes OSINT como NVD.

---

## 🧱 Componentes principales

### 1. `main.py` / `daemon.py`

- **main.py**: interfaz CLI con menú interactivo
- **daemon.py**: modo automático que realiza escaneo + búsqueda + notificación

### 2. `services/system_scanner`

- Escanea software instalado en función del OS
- Normaliza el nombre y versión del producto
- Inserta los resultados en la capa de almacenamiento (`storage`)

### 3. `services/osint_sources`

- `nvd_client.py`: cliente síncrono a NVD
- `nvd_get_cves.py`: búsqueda simple por palabra clave
- `nvd_batch_lookup.py`: búsqueda asincrónica con verificación de versiones

### 4. `services/alerting`

- `eval_vulnerabilities.py`: evalúa CVSS y filtra por criticidad
- `notifier.py`: lanza notificación local con enlace al CVE

### 5. `services/data_pipeline`

- `storage_local.py`: almacenamiento persistente en JSON
- `storage_nosql.py`: almacenamiento persistente en MongoDB
- Se inicializa con la variable `STORAGE_MODE`

---

## 🗃 Modo dual de almacenamiento

El sistema detecta en tiempo de ejecución si debe guardar los datos en archivos locales o en una base de datos MongoDB:

| Configuración         | Componente usado         | Ubicación      |
|----------------------|--------------------------|----------------|
| `STORAGE_MODE = "local"` | `LocalStorage`             | `/data/*.json` |
| `STORAGE_MODE = "mongo"` | `MongoStorage` o `storage_nosql` | MongoDB        |

Esto permite adaptar OpenShield a entornos sin infraestructura persistente o con Docker/Mongo en producción.

---

## 🔁 Flujo de ejecución (modo automático)

```plaintext
daemon.py
 └── mostrar_banner()
 └── windows_scan.main()
     └── listar_paquetes_instalados() → almacenamiento
 └── nvd_batch_lookup.buscar_cves_para_software_instalado()
     └── fetch async de CVEs → validación de versión → almacenamiento
 └── evaluar_vulnerabilidades_y_notificar()
     └── mostrar_alerta_windows()
```

---

## 🧩 Integración futura

- ✅ Soporte multiplataforma (pendiente notificación multiplataforma)
- 🔄 Integración con sistemas de ticketing (Jira, GitHub Issues)
- 🔔 Notificaciones vía Telegram o email
- 📈 Panel web para visualizar el estado (en versión futura)

---

## 🧪 Seguridad y ética

El sistema solo analiza el software **instalado localmente** y no envía información sensible a terceros. Todo el análisis se realiza con datos públicos (NVD).
