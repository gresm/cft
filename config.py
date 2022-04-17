"""Project configs loader"""
import os
import json
from pathlib import Path


convig_path = Path(__file__).parent / "config.json"
with convig_path.open(encoding="UTF-8") as __file:
    config = json.load(__file)

if "CFT_PRODUCTION" in os.environ:
    config["debug"] = False

for __key in config:
    locals()[__key] = config[__key]


__all__ = list(config.keys()) + ["config"]
