"""Database Loader (Using json)"""
from __future__ import annotations

import json
from pathlib import Path

from config import config
from .data import UsersDB, ChallengesDB


usersdb_path = Path(__file__).parent / config["usersdb"]
challengesdb_path = Path(__file__).parent / config["challengesdb"]


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

    users = UsersDB.deserialize(raw_usersdb)
    challenges = ChallengesDB.deserialize(raw_challengesdb)

    return users, challenges


def savedb(anydb: UsersDB | ChallengesDB):
    """Saves given database, doesn't matter if it is user or challenge"""
    if isinstance(anydb, UsersDB):
        with usersdb_path.open(encoding="UTF-8") as file:
            content = file.read()

        with usersdb_path.open("w", encoding="UTF-8") as file:
            try:
                file.write(json.dumps(anydb.serialize()))
            except Exception as exce:
                file.write(content)
                raise exce

    elif isinstance(anydb, ChallengesDB):
        with challengesdb_path.open(encoding="UTF-8") as file:
            content = file.read()

        with challengesdb_path.open("w", encoding="UTF-8") as file:
            try:
                file.write(json.dumps(anydb.serialize()))
            except Exception as exce:
                file.write(content)
                raise exce
