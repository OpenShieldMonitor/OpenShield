# core/config_loader.py
from config import settings

def get_setting(key, default=None):
    return getattr(settings, key, default)
