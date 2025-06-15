# 🛡 OpenShield - Automated OSINT-Based Vulnerability Tracker

> Monitor de vulnerabilidades basado en fuentes abiertas (OSINT) que analiza el software instalado en el sistema y consulta CVEs en la base de datos NVD, notificando vulnerabilidades relevantes.

---

## 🚀 Características principales

- Escaneo automático del sistema (Windows, Linux, macOS)
- Búsqueda de CVEs en [NVD (National Vulnerability Database)](https://nvd.nist.gov)
- Validación de versiones afectadas
- Clasificación de severidad con CVSS v2/v3
- Sistema de alertas locales (notificaciones en escritorio Windows)
- Almacenamiento flexible: **JSON local** o **MongoDB con Docker Engine**
- Modo automático `daemon` para uso en segundo plano

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/openshield.git
cd openshield
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuración

### Variables de entorno

Crea un archivo `.env` en la raíz con:

```env
NVD_API_KEY=TU_API_KEY_NVD
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=openshield
```

### Configuración general

En `config/settings.py` puedes definir:

- `STORAGE_MODE`: `"local"` o `"mongo"`
- `NVD_REQUEST_DELAY`: tiempo de espera entre llamadas para evitar sobrecarga a la API

---

## ⚙️ Uso

### Modo manual (CLI)

```bash
python main.py
```

### Modo automático (daemon)

```bash
python daemon.py
```

---

## 🧠 Modo de almacenamiento dual

OpenShield puede almacenar información de CVEs y software detectado en dos modos:

| Modo   | Descripción                                          | Configuración |
|--------|------------------------------------------------------|----------------|
| `local` | Archivos `.json` en la carpeta `/data`              | `STORAGE_MODE = "local"` |
| `mongo` | Base de datos MongoDB (colecciones `software` y `vulnerabilidades`) | `STORAGE_MODE = "mongo"` |

> ⚠️ Cambiar el modo en `settings.py` o a través de variable de entorno.

---

## 📌 Estructura del proyecto

```
openshield/
├── main.py
├── daemon.py
├── config/
│   └── settings.py
├── core/
│   ├── utils.py
│   ├── spinner.py
│   └── config_loader.py
├── services/
│   ├── osint_sources/
│   │   ├── nvd_get_cves.py
│   │   ├── nvd_client.py
│   │   └── nvd_batch_lookup.py
│   ├── system_scanner/
│   │   └── windows_scan.py
│   ├── alerting/
│   │   ├── eval_vulnerabilities.py
│   │   └── notifier.py
│   └── data_pipeline/
│       ├── storage_local.py
│       └── storage_nosql.py
└── data/
    └── software.json, vulnerabilidades.json
```

---

## 🧪 Requisitos y dependencias

**requirements.txt**
```txt
aiohttp>=3.8.0           # Cliente HTTP asíncrono para peticiones a NVD
colorama>=0.4.6          # Colores en terminal (menús, alertas)
packaging>=23.0          # Comparación robusta de versiones
pyfiglet>=0.8            # Banners de texto decorativo en terminal
pymongo>=4.3.3           # Conector de MongoDB
python-dotenv>=1.0.0     # Carga de variables de entorno desde .env
requests>=2.31.0         # Cliente HTTP síncrono
win10toast-click>=0.0.3  # Notificaciones interactivas en Windows

```

---

## 📤 Notificaciones

Actualmente se emiten a través de:

- 💻 Notificación de escritorio en Windows
- Terminal en otros entornos

> En futuras versiones se planea soporte para Telegram o correo electrónico.

---

## 📜 Licencia

MIT License. Uso libre con atribución.
