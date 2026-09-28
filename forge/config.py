"""AIOS-FORGE - Configuration Manager"""
import json
import os
import subprocess
import requests
from pathlib import Path

CONFIG_FILE = Path.home() / ".aios-master" / "forge-config.json"
OUTPUT_DIR = Path.home() / "Desktop" / "AIOS-OUTPUT"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    # Migrate from free-ai-hub if exists
    old = Path.home() / ".aios-master" / "free-ai-hub.json"
    if old.exists():
        with open(old) as f:
            data = json.load(f)
        save_config(data)
        return data
    return {}

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_key(name, env_var=None):
    config = load_config()
    if env_var and os.environ.get(env_var):
        return os.environ[env_var]
    return config.get(name)

def set_key(name, value):
    config = load_config()
    config[name] = value
    save_config(config)
    print(f"  \033[32m✓\033[0m {name} configurada")

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR

def timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def check_service(name):
    """Check if a service is available"""
    checks = {
        "gemini": lambda: bool(get_key("google_api_key", "GOOGLE_API_KEY")),
        "groq": lambda: bool(get_key("groq_api_key", "GROQ_API_KEY")),
        "hf": lambda: bool(get_key("hf_api_key", "HF_TOKEN")),
        "together": lambda: bool(get_key("together_api_key", "TOGETHER_API_KEY")),
        "twitter": lambda: bool(get_key("twitter_consumer_key")),
        "ollama": lambda: _check_ollama(),
        "ffmpeg": lambda: _check_cmd("ffmpeg"),
        "edge-tts": lambda: _check_module("edge_tts"),
        "whisper": lambda: _check_module("whisper"),
        "rembg": lambda: _check_module("rembg"),
        "playwright": lambda: _check_cmd("npx") and Path(Path.home() / "Library/Caches/ms-playwright").exists(),
    }
    fn = checks.get(name)
    return fn() if fn else False

def _check_ollama():
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
        return True
    except Exception:
        return False

def _check_cmd(cmd):
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except Exception:
        return False

def _check_module(module):
    import importlib
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False
