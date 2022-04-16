"""Database Loader (Using json)"""
import json

from pathlib import Path


usersdb_path = Path("usersdb.json")
challengesdb_path = Path("challengesdb.json")


def load():
    """Loads Databases from files"""
    if not usersdb_path.exists():
        with usersdb_path.open("w", encoding="UTF-8") as _f:
            _f.write("{}")

    with usersdb_path.open("r", encoding="UTF-8") as _f:
        raw_usersdb = json.load(_f)

    if not challengesdb_path.exists():
        with challengesdb_path.open("w", encoding="UTF-8") as _f:
            _f.write("{}")

    with challengesdb_path.open("r", encoding="UTF-8") as _f:
        raw_challengesdb = json.load(_f)
    return raw_usersdb, raw_challengesdb


def savedb(users, challenges):
    """Saves Databases to files"""
    with usersdb_path.open("w", encoding="UTF-8") as file:
        file.write(json.dumps(users))

    with challengesdb_path.open("w", encoding="UTF-8") as file:
        file.write(json.dumps(challenges))
