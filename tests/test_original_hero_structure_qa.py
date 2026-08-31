from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class OriginalHeroStructureQATests(unittest.TestCase):
    def test_approved_copy_uses_the_original_display_headline_and_support_structure(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<h1 class="display-title hero-task-title" id="about-title">', index)
        self.assertIn('<span>We help businesses</span>', index)
        self.assertIn('<span class="accent">automate repeatable tasks</span>', index)
        self.assertIn('<span class="accent">that are costing them</span>', index)
        self.assertIn('<span class="accent">valuable time.</span>', index)
        self.assertIn(
            '<p>Even small repeatable tasks can add up to hours each day—and tens of hours each week.</p>',
            index,
        )


if __name__ == "__main__":
    unittest.main()
