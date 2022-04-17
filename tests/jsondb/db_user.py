"""Tests for real.jsondb.data (for users)"""
from real.jsondb.data import User, UsersDB


class TestUser:
    """Test User class"""

    serialized = {
        "id": "test",
        "access": ["test", "test2", "test"],
        "solved": {"test": ["first", "first:second"]},
    }

    def test_deserialize(self):
        """Test deserializing"""

        user = User.deserialize(self.serialized)

        assert (
            user.identifier == "test"
        ), f"Invalid id conversion with {user.identifier}"

        assert isinstance(user.access, set)
        assert len(user.access) == 2
        assert "test" in user.access and "test2" in user.access

    def test_serialize(self):
        """Test deserializing"""
        user = User.serialize(User.deserialize(self.serialized))

        assert "id" in user and "access" in user and "solved" in user
        assert user["id"] == "test"
        assert len(user["access"]) == 2
        assert isinstance(user["solved"], dict) and "test" in user["solved"]

        err = f"{user} doesn't match with {self.serialized}"
        assert user != self.serialized and set(user["access"]) == set(
            self.serialized["access"]
        ), err


class TestUsersDB:
    """Test Users class"""

    serialized = {"test": {"id": "test", "solved": {}, "access": []}}
    ser_user = {"id": "test", "solved": {}, "access": []}
    ser_user2 = {"id": "test2", "solved": {}, "access": []}

    def test_serialize(self):
        """Test serializing"""
        des = UsersDB.deserialize(self.serialized)
        ser = des.serialize()
        assert ser == self.serialized

    def test_deserialize(self):
        """Test deserializing"""

        des = UsersDB.deserialize(self.serialized)

        err = f"Deserialized: {des}"

        assert "test" in des.users, err
        assert des.users["test"].serialize() == self.ser_user, err

    def test_add_user(self):
        """Test adding users"""
        des = UsersDB.deserialize(self.serialized)
        usr1 = des.add_user("test2")

        assert usr1.serialize() == self.ser_user2

    def test_remove_user(self):
        """Test removing users"""
        des = UsersDB.deserialize(self.serialized)
        des.remove_user("test")
        assert len(des.users) == 0


__all__ = ["TestUser", "TestUsersDB"]
