from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BuildStepQATests(unittest.TestCase):
    def test_build_step_uses_the_approved_reliable_automation_wording(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("AUTOMATE THE TASKS.", index)
        self.assertIn(
            "We build simple, reliable software around the tools your business already uses—so routine tasks move forward with less manual effort.",
            index,
        )
        self.assertNotIn(
            "We build simple, reliable automations around the software your business already uses—so routine tasks move forward with less manual effort.",
            index,
        )
        self.assertNotIn(
            "We connect the tools you already use, cut repetitive work, and give you a clearer view of your business.",
            index,
        )


if __name__ == "__main__":
    unittest.main()
