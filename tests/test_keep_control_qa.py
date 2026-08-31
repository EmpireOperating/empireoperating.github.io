from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class KeepControlQATests(unittest.TestCase):
    def test_keep_control_step_uses_the_approved_system_ownership_wording(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn(
            "You stay in control. We show you how the system works and remain available to maintain or improve it.",
            index,
        )
        self.assertNotIn(
            "Your team owns the system. We show you how it works and stay available to maintain or improve it.",
            index,
        )


if __name__ == "__main__":
    unittest.main()
