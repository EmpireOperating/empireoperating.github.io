from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RestoredOriginalHeadlineQATests(unittest.TestCase):
    def test_hero_keeps_the_original_display_headline_and_uses_new_copy_as_support(self) -> None:
        index = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<h1 class="display-title" id="about-title">', index)
        self.assertIn('<span>We build systems</span>', index)
        self.assertIn('<span class="accent">that give you</span>', index)
        self.assertIn('<span class="accent">your time back</span>', index)
        self.assertIn(
            '<p>We help businesses automate repeatable tasks that are costing them valuable time.</p>',
            index,
        )
        self.assertIn(
            '<p>Even small repeatable tasks can add up to hours each day—and tens of hours each week.</p>',
            index,
        )
        self.assertNotIn('hero-task-title', index)


if __name__ == "__main__":
    unittest.main()
