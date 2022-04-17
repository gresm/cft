"""Database Loader (Using json)"""
from __future__ import annotations

import json
from pathlib import Path

from .data import UsersDB, ChallengesDB


usersdb_path = Path(__file__).parent / "usersdb.json"
challengesdb_path = Path(__file__).parent / "challengesdb.json"


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

    return UsersDB.deserialize(raw_usersdb), ChallengesDB(raw_challengesdb)


def savedb(anydb: UsersDB | ChallengesDB):
    """Saves given database, doesn't matter if it is user or challenge"""
    if isinstance(anydb, UsersDB):
        with usersdb_path.open("w", encoding="UTF-8") as file:
            file.write(json.dumps(anydb.serialize()))

    elif isinstance(anydb, ChallengesDB):
        with challengesdb_path.open("w", encoding="UTF-8") as file:
            file.write(json.dumps(anydb.serialize()))
