"""Tests for real.jsondb.data"""
from real.jsondb.data import User


class TestUser:
    """Test User class"""

    __test__ = True

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


__all__ = ["TestUser"]
