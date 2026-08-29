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

    def test_all_pages_use_the_current_stylesheet_cache_key(self) -> None:
        for page in ("index.html", "about.html", "contact.html"):
            document = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn(
                'href="site.css?v=20260829-hero-operating-layer-v1"',
                document,
            )

    def test_about_duplicate_points_to_root_canonical(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8").lower()
        self.assertIn(
            '<link rel="canonical" href="https://empireoperating.com/">',
            about,
        )

    def test_about_duplicate_uses_the_current_message(self) -> None:
        about = (ROOT / "about.html").read_text(encoding="utf-8")
        self.assertIn("Built around your business.", about)
        self.assertIn("Start the conversation", about)
        self.assertNotIn("Free consultation", about)
        self.assertNotIn("Book a free consultation", about)
        self.assertNotIn("A few possible starting points", about)

    def test_hero_keeps_the_title_and_uses_the_operating_layer_copy(self) -> None:
        expected_title = (
            "We build systems",
            "that give you",
            "your time back",
        )
        expected_copy = (
            "Most businesses already have many of the tools they need. What they often lack is an operating layer that connects those tools, people, and channels into one coherent system.",
            "The result is less time spent manually coordinating work—and fewer opportunities, follow-ups, and important details falling through the cracks.",
        )
        for page in ("index.html", "about.html"):
            document = (ROOT / page).read_text(encoding="utf-8")
            for expected in (*expected_title, *expected_copy):
                self.assertIn(expected, document)
            self.assertNotIn("We automate your most repetitive business tasks", document)
            self.assertNotIn("Your family, your hobbies, or growing your business.", document)

    def test_workflow_example_has_no_intro_block_on_either_page(self) -> None:
        for page in ("index.html", "about.html"):
            document = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn('class="possibilities"', document.lower())
            self.assertIn("Things coming in", document)
            self.assertIn("What happens next", document)
            self.assertIn("Useful things coming out", document)
            self.assertNotIn("What this can look like", document)
            self.assertNotIn("From repetitive work", document)
            self.assertNotIn("to something ready to use.", document)
            self.assertNotIn(
                "Work comes in, the repeatable steps get handled, and the right person receives something clear and ready to use.",
                document,
            )
            self.assertNotIn("One example", document)
            self.assertNotIn("A few possible starting points", document)
            self.assertNotIn("Inquiry follow-up", document)
            self.assertNotIn("Client intake", document)
            self.assertNotIn("Recurring reports", document)

    def test_tailored_business_block_precedes_the_workflow_example_on_both_pages(self) -> None:
        for page in ("index.html", "about.html"):
            document = (ROOT / page).read_text(encoding="utf-8")
            tailored = document.index('<section class="tailored"')
            example = document.index('<div class="system-map"')
            self.assertLess(tailored, example)
            self.assertIn("Built around your business.", document)
            self.assertIn("Your business has its own bottleneck.", document)
            self.assertIn(
                "The system should fit your business, not the other way around.",
                document,
            )

    def test_tailored_copy_introduces_the_workflow_below(self) -> None:
        for page in ("index.html", "about.html"):
            document = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn(
                "The workflow below is only one example. Your business has its own bottleneck.",
                document,
            )
            self.assertNotIn("This is only one example. Your business has its own bottleneck.", document)

    def test_consultation_starts_an_email_conversation_without_booking(self) -> None:
        self.assertIn('<h2 id="consultation-title">Start the conversation</h2>', self.index)
        self.assertIn("Let's talk about your business and see if we can", self.index)
        self.assertIn("Start the conversation", self.index)
        self.assertIn("subject=Start%20the%20conversation", self.index)
        self.assertNotIn("Free consultation", self.index)
        self.assertNotIn("Book a free consultation", self.index)
        self.assertNotIn("Let's find the part worth fixing.", self.index)
        self.assertNotIn("Tell me what keeps repeating", self.index)

    def test_added_section_uses_the_canonical_brand_red(self) -> None:
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        self.assertIn("--red: #9b1218;", css)
        self.assertIn("--red-readable: #9b1218;", css)
        self.assertNotIn("--red-readable: #cf4b51;", css)

    def test_workflow_transitions_use_map_rules_without_outer_duplicates(self) -> None:
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        tailored = css.split(".tailored {", 1)[1].split("}", 1)[0]
        possibilities = css.split(".possibilities {", 1)[1].split("}", 1)[0]
        system_map = css.split(".system-map {", 1)[1].split("}", 1)[0]
        self.assertNotIn("border-bottom", tailored)
        self.assertNotIn("border-bottom", possibilities)
        self.assertIn("border-top: 1px solid var(--line);", system_map)
        self.assertIn("border-bottom: 1px solid var(--line);", system_map)

    def test_narrow_screens_use_readable_navigation_and_workflow_text(self) -> None:
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        mobile = css.split("@media (max-width: 700px)", 1)[1].split("@media (max-width: 380px)", 1)[0]
        self.assertIn(".site-nav { gap: 18px; margin-top: 14px; font-size: 11px; }", mobile)
        self.assertIn(".map-column small { font-size: 12px; }", mobile)
        self.assertIn(".map-column ul { font-size: 14px; }", mobile)
        self.assertIn(".consultation-copy { width: auto; max-width: 355px; font-size: 13px;", mobile)

    def test_desktop_hero_rule_uses_the_tighter_post_reorder_spacing(self) -> None:
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        desktop = css.split("@media (max-width: 700px)", 1)[0]
        rule = desktop.split(".section-rule", 1)[1].split("}", 1)[0]
        self.assertIn("margin: 128px 0 0;", rule)

    def test_workflow_connectors_use_rules_and_diamonds_not_arrows(self) -> None:
        css = (ROOT / "site.css").read_text(encoding="utf-8")
        connector = css.split(".map-arrow::after", 1)[1].split("}", 1)[0]
        self.assertNotIn("content: '→';", connector)
        self.assertIn("border: 1px solid var(--red-readable);", connector)
        self.assertIn("rotate(45deg)", connector)


if __name__ == "__main__":
    unittest.main()
