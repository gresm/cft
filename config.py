"""Project configs loader"""
import os
import json
from pathlib import Path


convig_path = Path(__file__).parent / "config.json"
with convig_path.open(encoding="UTF-8") as __file:
    config = json.load(__file)

if "CFT_PRODUCTION" in os.environ:
    config["debug"] = False

if "CFT_CUSTOM_DATABASE_USERS" in os.environ:
    config["usersdb"] = os.environ["CFT_CUSTOM_DATABASE_USERS"]

if "CFT_CUSTOM_DATABASE_CHALLENGES" in os.environ:
    config["usersdb"] = os.environ["CFT_CUSTOM_DATABASE_CHALLENGES"]

for __key in config:
    locals()[__key] = config[__key]


__all__ = list(config.keys()) + ["config"]
