"""This file contains database structures needed for the website"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UsersDB:
    """Multiple Users"""

    users: dict[str, User]

    @classmethod
    def deserialize(cls, data):
        """Deserialize self from json-able object"""
        users = {}
        for identifier in data:
            users[identifier] = User.deserialize(data[identifier])
        return cls(users)

    def serialize(self):
        """Serialize self to json-able object"""
        ret = {}
        for identifier in self.users:
            ret[identifier] = self.users[identifier].serialize()

        return ret


@dataclass
class User:
    """User"""

    identifier: str
    solved: dict[str, list[str]]
    access: set[str]

    @classmethod
    def deserialize(cls, data):
        """Deserialize self from json-able object"""
        return cls(data["id"], data["solved"], set(data["access"]))

    def serialize(self):
        """Serialize self to json-able object"""
        return {
            "id": self.identifier,
            "solved": self.solved,
            "access": list(self.access),
        }


__all__ = ["UsersDB", "User"]
