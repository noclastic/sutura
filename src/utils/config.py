import json
import os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".genpdf_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception:
        pass

def get_last_folder():
    return load_config().get("last_folder", os.path.expanduser("~"))

def set_last_folder(path):
    config = load_config()
    config["last_folder"] = path
    save_config(config)
