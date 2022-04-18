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

    def add_user(self, identifier: str):
        """
        Creates new empty user with specified identifier and returns it.
        If user with such identifier already exists, it will override it.
        """
        user = User(identifier=identifier, solved={}, access=set())
        self.users[identifier] = user
        return user

    def remove_user(self, identifier: str):
        """Removes user from database"""
        if identifier in self.users:
            del self.users[identifier]

    def get_user(self, identifier: str):
        """Returns user with identifier, if no, returns None"""
        if identifier in self.users:
            return self.users[identifier]
        return None


@dataclass
class User:
    """User"""

    identifier: str
    solved: dict[str, set[str]]
    access: set[str]

    @classmethod
    def deserialize(cls, data):
        """Deserialize self from json-able object"""
        solved = {}
        for name in data["solved"]:
            solved[name] = list(data["solved"][name])

        return cls(data["id"], solved, set(data["access"]))

    def serialize(self):
        """Serialize self to json-able object"""
        solved = {}
        for name in self.solved:
            solved[name] = list(self.solved[name])

        return {
            "id": self.identifier,
            "solved": solved,
            "access": list(self.access),
        }

    def extend_access(self, category: str):
        """Extends user's access to othe categories"""
        self.access.add(category)


@dataclass
class ChallengesDB:
    """Database for challenges"""

    categories: dict[str, Challenges]

    @classmethod
    def deserialize(cls, data):
        """Deserialize self from json-able object"""
        categories = {}
        ret = cls(categories)

        for name in data:
            categories[name] = Challenges.deserialize(ret, data[name], name)

        return ret

    def serialize(self):
        """Serialize self to json-able object"""
        ret = {}

        for name in self.categories:
            ret[name] = self.categories[name].serialize()

        return ret

    def add_category(self, name: str):
        """Creates category and returns it"""
        category = Challenges(identifier=name, challenges={}, data_base=self)
        self.categories[name] = category
        return category

    def remove_category(self, name: str):
        """Removes category"""
        if name in self.categories:
            del self.categories[name]

    def get_challenge_trace(self, identifier: str):
        """Creates list of challenges to specified (using identifier)."""
        splt = identifier.split(":")
        data_base_category = splt[0]

        if data_base_category in self.categories:
            return self.categories[data_base_category].get_challenge_trace(
                identifier.split(":")
            )
        return None

    def get_challenge(self, indentifier: str) -> Challenge | None:
        """Searches for challenge from identifier"""
        splt = indentifier.split(":")

        if len(splt) == 1:
            return None

        if splt[0] in self.categories:
            return self.categories[splt[0]].get_challenge(":".join(splt[1:]))
        return None

    def get_category(self, category: str) -> Challenges | None:
        """
        Returns category with specified name, if doesn't exist, returns None
        """
        if category in self.categories:
            return self.categories[category]
        return []

    def can_user_see(self, user, indentifier: str):
        """Check if user can see the challenge"""
        if len(indentifier.split(":")) == 1:
            chal = self.get_category(indentifier)
        else:
            chal = self.get_challenge(indentifier)

        if chal is None:
            return False

        return chal.can_user_see(user)


@dataclass
class Challenges:
    """Multiple challenges"""

    identifier: str
    challenges: dict[str, Challenge]
    data_base: ChallengesDB

    @classmethod
    def deserialize(cls, data_base: ChallengesDB, data, identifier: str):
        """Deserialize self from json-able object"""
        chal = {}
        ret = cls(data_base=data_base, identifier=identifier, challenges=chal)

        for name in data["challenges"]:
            chal[name] = Challenge.deserialize(
                parent=ret, data=data["challenges"][name]
            )

        return ret

    def serialize(self):
        """Serialize self to json-able object"""
        challenges = {}
        for identifier in self.challenges:
            challenges[identifier] = self.challenges[identifier].serialize()
        return {"challenges": challenges}

    def get_challenge_trace_internal(
        self, splt: list[str], appnd: list[Challenges]
    ) -> list[Challenge]:
        """
        Internal function for creating list of challenges from current
        challenge to specified one (using identifier).
        """
        name = splt[0]

        if name in self.challenges:
            chal = self.challenges[name]
        else:
            return appnd

        if len(splt) > 1:
            join = ":".join(splt[1:])
            if chal.sub_challenges:
                chal.sub_challenges.get_challenge_trace_internal(join, appnd)
        return appnd

    def get_challenge_trace(self, identifier: str) -> list[Challenge]:
        """Creates list of challenges from current to specified."""
        return self.get_challenge_trace_internal(identifier.split(":"), [])

    def get_challenge(self, identifier: str) -> Challenge | None:
        """Searches for challenge from identifier"""
        splt = identifier.split(":")
        name = splt[0]

        if name in self.challenges:
            chal = self.challenges[name]
        else:
            return None

        if len(splt) > 1:
            join = ":".join(splt[1:])
            if chal.sub_challenges:
                return chal.sub_challenges.get_challenge(join)
            return None
        return chal

    def add_challenge(
        self,
        name: str,
        flag: str,
        title: str,
        desc: str,
        files: list[str] | None = None,
    ):
        """Creates challenge and returns it"""
        ret = Challenge(
            flag=flag,
            name=name,
            title=title,
            description=desc,
            files=files,
            parent=self,
            sub_challenges=None,
        )

        self.challenges[name] = ret
        return ret

    def can_user_see(self, user: User):
        """Check if category is accessible for user"""
        splt = self.identifier.split(":")

        if splt[0] not in user.access:
            return False

        if len(splt) == 1:
            return True
        return ":".join(splt[1:-1]) in user.solved[splt[0]]


@dataclass
class Challenge:
    """Challenge"""

    flag: str
    name: str
    title: str
    files: list[str]
    description: str
    parent: Challenges
    sub_challenges: Challenges | None

    @classmethod
    def deserialize(cls, parent: Challenges, data):
        """Deserialize self from json-able object"""
        flag = data["flag"]
        name = data["name"]
        title = data["title"]
        description = data["description"]
        files = data["files"] if "files" in data else []
        if "children" in data:
            sub_challenges = Challenges.deserialize(
                data_base=parent.data_base,
                data=data["children"],
                identifier=cls.get_identifier(parent, name),
            )
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

    @staticmethod
    def get_identifier(parent: Challenges, name: str):
        """Create identifier"""
        return f"{parent.identifier}:{name}"

    @property
    def identifier(self):
        """Get identifier"""
        return self.get_identifier(self.parent, self.name)

    @property
    def category(self):
        """Get the main category of the challenge"""
        return self.identifier.split(":")[0]

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

    def add_challenge(
        self,
        name: str,
        flag: str,
        title: str,
        desc: str,
        files: list[str] | None = None,
    ):
        """Creates challenge and returns it"""
        if not self.sub_challenges:
            self._generate_sub_challenges()

        return self.sub_challenges.add_challenge(
            name=name, flag=flag, title=title, desc=desc, files=files
        )

    def _generate_sub_challenges(self):
        """
        Internal function for generating 'sub_challenges'.
        If 'sub_challenges' already exists, it will be overriden.
        """
        data_base = self.parent.data_base
        group = Challenges(
            identifier=self.identifier, challenges={}, data_base=data_base
        )
        self.sub_challenges = group

    def solve(self, user: User):
        """Mark as solved for specified user"""
        if self.category not in user.solved:
            user.solved[self.category] = set()
        user.solved[self.category].add(self.identifier)

    def is_solved(self, user: User):
        """Check if user has solved this challenge"""
        if self.category not in user.solved:
            return False

        return self.identifier in user.solved[self.category]

    def can_user_see(self, user: User):
        """Check if user can see the challenge"""
        return self.parent.can_user_see(user)


__all__ = ["UsersDB", "User", "ChallengesDB", "Challenges", "Challenge"]
