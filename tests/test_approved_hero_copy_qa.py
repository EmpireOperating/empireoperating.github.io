from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ApprovedHeroCopyQATests(unittest.TestCase):
    def test_home_uses_the_exact_approved_hero_copy(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        for phrase in (
            "We help businesses",
            "automate repeatable tasks",
            "that are costing them",
            "valuable time.",
            "Even small repeatable tasks can add up to hours each day—and tens of hours each week.",
        ):
            self.assertIn(phrase, index)

        self.assertNotIn("We build systems", index)
        self.assertNotIn("Most businesses already have many of the tools they need.", index)


if __name__ == "__main__":
    unittest.main()
