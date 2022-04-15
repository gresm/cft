"""Core File For server Database (Using json)"""
import json

from pathlib import Path


usersdb_path = Path("users.json")

if not usersdb_path.exists():
    with usersdb_path.open("w", encoding="UTF-8") as _f:
        _f.write("{}")

with usersdb_path.open("r", encoding="UTF-8") as _f:
    raw_usersdb = json.load(_f)


challengesdb_path = Path("challenges.json")

if not challengesdb_path.exists():
    with challengesdb_path.open("w", encoding="UTF-8") as _f:
        _f.write("{}")

with challengesdb_path.open("r", encoding="UTF-8") as _f:
    raw_challengesdb = json.load(_f)


def savedb():
    """Saves Databases to files"""
    with usersdb_path.open("w", encoding="UTF-8") as file:
        file.write(json.dumps(raw_usersdb))

    with challengesdb_path.open("w", encoding="UTF-8") as file:
        file.write(json.dumps(raw_usersdb))
