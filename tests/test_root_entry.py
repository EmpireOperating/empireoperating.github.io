from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RootEntryPageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.lower = self.index.lower()

    def test_root_is_the_branded_landing_document(self) -> None:
        self.assertNotIn('http-equiv="refresh"', self.lower)
        self.assertNotIn("enter empire operating", self.lower)
        self.assertIn('rel="stylesheet"', self.lower)
        self.assertIn('class="site-shell"', self.lower)
        self.assertIn('class="display-title"', self.lower)
        self.assertIn(
            '<link rel="canonical" href="https://empireoperating.com/">',
            self.lower,
        )

    def test_root_has_immediate_branded_canvas_before_external_css(self) -> None:
        self.assertIn('id="critical-shell"', self.lower)
        self.assertIn("background: #040404", self.lower)

    def test_about_duplicate_points_to_root_canonical(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8").lower()
        self.assertIn(
            '<link rel="canonical" href="https://empireoperating.com/">',
            about,
        )


if __name__ == "__main__":
    unittest.main()
