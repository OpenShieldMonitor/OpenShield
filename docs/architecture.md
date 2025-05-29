Ejemplo de uso del config_loader.py
```python
from core.config_loader import get_setting

if get_setting("ENABLE_TELEGRAM_ALERTS"):
    token = get_setting("TELEGRAM_BOT_TOKEN")
    # Lógica de envío
```