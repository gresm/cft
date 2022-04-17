"""Tests for real.jsondb.data (for challenges)"""
from real.jsondb.data import ChallengesDB, Challenges, Challenge


class TestChallengesDB:
    """Tests for ChallengesDB class"""

    serialized = {
        "test": {
            "challenges": {
                "test": {
                    "flag": "CFT{secret-flag}", "name": "test",
                    "title": "The Test", "files": None,
                    "description": "This is the test"
                }
            }
        }
    }

    def test_deserialize(self):
        """Tests for deserialize"""
        des = ChallengesDB.deserialize(self.serialized)

        assert "test" in des.categories

    def test_serialze(self):
        """Tests for serialize"""
        des = ChallengesDB.deserialize(self.serialized)
        ser = des.serialize()

        assert "test" in ser
        assert "challenges" in ser["test"]
        assert "test" in ser["test"]["challenges"]

        chs = ser["test"]["challenges"]["test"]
        cch = self.serialized["test"]["challenges"]["test"]
        desc = "description"

        assert "flag" in chs and chs["flag"] == cch["flag"]
        assert "name" in chs and chs["name"] == cch["name"]
        assert "title" in chs and chs["title"] == cch["title"]
        assert "files" in chs and chs["files"] == cch["files"]
        assert desc in chs and chs[desc] == cch[desc]

    @staticmethod
    def test_add_category():
        """Tests for add_category"""
        des = ChallengesDB({})
        des.add_category("test")

        assert "test" in des.categories

    def test_remove_category(self):
        """Tests for remove_category"""
        des = ChallengesDB.deserialize(self.serialized)

        assert "test" in des.categories

        des.remove_category("test")

        assert "test" not in des.categories

    def test_get_category(self):
        """Tests for get_category"""
        des = ChallengesDB({})
        cat = des.add_category("test")

        assert des.get_category("test") is cat


__all__ = ["TestChallengesDB"]
