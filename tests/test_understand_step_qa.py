from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class UnderstandStepQATests(unittest.TestCase):
    def test_understand_step_uses_the_approved_manual_task_wording(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn(
            "We identify the repeatable tasks still handled manually, who touches them, and where time gets lost.",
            index,
        )
        self.assertNotIn(
            "We find where work comes in, who handles it, and where it slows down or gets missed.",
            index,
        )


if __name__ == "__main__":
    unittest.main()
