from typing import Dict
from yaml import safe_load

def load_config(config_path: str) -> Dict:
    with open(config_path) as file:
        config = safe_load(file)

    if config["device"] == "gpu":
        config["device"] = "cuda:0"

    return config