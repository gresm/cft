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


@dataclass()
class ChallengesDB:
    """Multiple challenges"""

    identifier: str
    challenges: dict[str, Challenge]

    @classmethod
    def deserialize(cls, data):
        """Deserialize self from json-able object"""
        challenges = {}

        ret = cls(identifier=data["id"], challenges=challenges)

        for identifier in data["challenges"]:
            challenges[identifier] = Challenge.deserialize(
                parent=ret, data=data["challenges"][identifier]
            )

        return ret

    def serialize(self):
        """Serialize self to json-able object"""
        challenges = {}
        for identifier in self.challenges:
            challenges[identifier] = self.challenges[identifier].serialize()
        return {"id": self.identifier, "challenges": challenges}


@dataclass
class Challenge:
    """Challenge"""

    flag: str
    name: str
    title: str
    files: list[str]
    description: str
    parent: ChallengesDB
    sub_challenges: ChallengesDB | None

    @classmethod
    def deserialize(cls, parent: ChallengesDB, data):
        """Deserialize self from json-able object"""
        flag = data["flag"]
        name = data["name"]
        title = data["title"]
        description = data["description"]
        files = data["files"] if "files" in data else []
        if "children" in data:
            sub_challenges = ChallengesDB.deserialize(data["children"])
        else:
            sub_challenges = None

        return Challenge(
            flag=flag,
            name=name,
            title=title,
            files=files,
            description=description,
            parent=parent,
            sub_challenges=sub_challenges,
        )

    def serialize(self):
        """Serialize self to json-able object"""

        ret = {
            "flag": self.flag,
            "name": self.name,
            "title": self.title,
            "files": self.files,
            "description": self.description,
        }

        if self.sub_challenges:
            ret["children"] = self.sub_challenges.serialize()

        return ret


__all__ = ["UsersDB", "User"]
