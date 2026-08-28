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

    def test_about_duplicate_uses_the_current_message(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        self.assertNotIn("Free consultation", about)
        self.assertNotIn("Book a free consultation", about)
        self.assertIn("Built around your business.", about)
        self.assertIn("Tell me what keeps repeating", about)

    def test_existing_hero_message_is_preserved(self) -> None:
        for expected in (
            "We build systems",
            "that give you",
            "your time back",
            "We automate your most repetitive business tasks",
            "Your family, your hobbies, or growing your business.",
        ):
            self.assertIn(expected, self.index)

    def test_root_explains_one_workflow_and_three_starting_points(self) -> None:
        self.assertIn('class="possibilities"', self.lower)
        self.assertIn("What this can look like", self.index)
        self.assertIn("Things coming in", self.index)
        self.assertIn("What happens next", self.index)
        self.assertIn("Useful things coming out", self.index)
        self.assertIn("Inquiry follow-up", self.index)
        self.assertIn("Client intake", self.index)
        self.assertIn("Recurring reports", self.index)

    def test_root_says_the_system_is_tailored_to_the_business(self) -> None:
        self.assertIn("Built around your business.", self.index)
        self.assertIn("Your business has its own bottleneck.", self.index)
        self.assertIn(
            "The system should fit your business, not the other way around.",
            self.index,
        )

    def test_contact_invitation_is_direct_not_a_consultation_label(self) -> None:
        self.assertNotIn("Free consultation", self.index)
        self.assertNotIn("Book a free consultation", self.index)
        self.assertIn("Let's find the part worth fixing.", self.index)
        self.assertIn("Tell me what keeps repeating", self.index)
        self.assertIn("subject=What%20keeps%20repeating", self.index)


if __name__ == "__main__":
    unittest.main()
