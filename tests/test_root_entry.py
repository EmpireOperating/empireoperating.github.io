from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CACHE_KEY = "20260830-two-tone-ivory-v1"
WEB_ANALYTICS_SCRIPT = (
    '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "3c84151dfd63412f802c2cf1a2fbf10e"}\'></script>'
)


class SimplifiedProductionSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.contact = (ROOT / "contact.html").read_text(encoding="utf-8")
        self.css = (ROOT / "site.css").read_text(encoding="utf-8")

    def test_root_remains_the_branded_canonical_landing_page(self) -> None:
        lower = self.index.lower()
        self.assertNotIn('http-equiv="refresh"', lower)
        self.assertIn('class="site-shell"', lower)
        self.assertIn('class="display-title"', lower)
        self.assertIn('id="critical-shell"', lower)
        self.assertIn("background: #040404", lower)
        self.assertIn(
            '<link rel="canonical" href="https://empireoperating.com/">',
            lower,
        )
        self.assertIn("<title>Empire Operating | Practical Operating Systems</title>", self.index)
        self.assertIn(
            "Empire Operating builds practical operating layers that connect a business’s people, tools, and channels—so important work is captured, owned, and moved forward.",
            self.index,
        )
        self.assertNotIn("Business Automation", self.index)
        self.assertNotIn("automates repetitive business tasks", self.index)

    def test_information_rich_about_page_is_preserved_in_git_but_not_shipped(self) -> None:
        self.assertFalse((ROOT / "about.html").exists())
        self.assertNotIn('href="about.html"', self.index)
        self.assertNotIn('href="about.html"', self.contact)

    def test_navigation_contains_only_home_and_contact(self) -> None:
        self.assertIn('<a href="index.html" aria-current="page">Home</a>', self.index)
        self.assertIn('<a href="contact.html">Contact</a>', self.index)
        self.assertIn('<a href="index.html">Home</a>', self.contact)
        self.assertIn('<a href="contact.html" aria-current="page">Contact</a>', self.contact)
        for document in (self.index, self.contact):
            self.assertNotIn('>About</a>', document)

    def test_public_pages_use_the_current_stylesheet_cache_key(self) -> None:
        expected = f'href="site.css?v={CACHE_KEY}"'
        for document in (self.index, self.contact):
            self.assertIn(expected, document)

    def test_public_pages_include_the_cloudflare_web_analytics_beacon(self) -> None:
        for document in (self.index, self.contact):
            self.assertIn(WEB_ANALYTICS_SCRIPT, document)

    def test_home_uses_the_approved_repeatable_task_hero_block(self) -> None:
        protected = (
            "We help businesses",
            "automate repeatable",
            "tasks that are costing",
            "them valuable time.",
            "Even small repeatable tasks can add up to hours each day—and tens of hours each week.",
        )
        for phrase in protected:
            self.assertIn(phrase, self.index)

    def test_home_uses_the_approved_built_for_introduction(self) -> None:
        self.assertIn('<h2 id="team-owned-title">Built for your business.</h2>', self.index)
        self.assertIn(
            "We learn how you run your business, then make the parts causing the most friction easier.",
            self.index,
        )
        self.assertIn(
            "The system should fit your business, not the other way around.",
            self.index,
        )
        self.assertNotIn("Built around your business.", self.index)
        self.assertNotIn("HOW WE HELP.", self.index)

    def test_home_explains_understand_build_and_handoff(self) -> None:
        expected = (
            "01 / UNDERSTAND",
            "MAP THE WORK.",
            "We identify the repeatable tasks still handled manually, who touches them, and where time gets lost.",
            "02 / BUILD",
            "BUILD THE OPERATING LAYER.",
            "We build simple, reliable automations around the tools you already use—so routine tasks move forward with less manual effort.",
            "03 / HANDOFF",
            "KEEP CONTROL.",
            "Your team owns the system. We show you how it works and stay available to maintain or improve it.",
        )
        for phrase in expected:
            self.assertIn(phrase, self.index)

    def test_home_omits_the_rejected_workflow_map_and_dense_duplicate_copy(self) -> None:
        self.assertNotIn('<section class="possibilities"', self.index)
        self.assertNotIn('<div class="system-map"', self.index)
        rejected = (
            "WORK COMES IN",
            "KEEP IT ORGANIZED",
            "WORK GETS DONE",
            "Your business has its own bottleneck.",
            "opportunities that are currently slipping through",
            "whatever form of operational oversight",
        )
        for phrase in rejected:
            self.assertNotIn(phrase, self.index)

    def test_home_flows_from_hero_to_process_to_conversation(self) -> None:
        hero = self.index.index('<section class="about-upper"')
        process = self.index.index('<section class="team-owned-system"')
        conversation = self.index.index('<section class="consultation"')
        self.assertLess(hero, process)
        self.assertLess(process, conversation)

    def test_home_restores_the_warm_email_first_invitation(self) -> None:
        self.assertIn('<h2 id="consultation-title">Start the conversation</h2>', self.index)
        self.assertIn(
            "Tell us about your business. We’d enjoy hearing about what is working well and what you would like to improve. If there is a way we can help, we’d be glad to talk it through.",
            self.index,
        )
        self.assertIn("subject=Start%20the%20conversation", self.index)
        self.assertNotIn("Book a free consultation", self.index)

    def test_contact_page_keeps_the_direct_invitation(self) -> None:
        self.assertIn("Have a question or", self.contact)
        self.assertIn("want to learn more?", self.contact)
        self.assertIn("We’d be glad to hear from you.", self.contact)
        self.assertIn("empireoperating@proton.me", self.contact)

    def test_site_keeps_the_canonical_visual_grammar_and_mobile_layout(self) -> None:
        self.assertIn("--ivory: #c4a77d;", self.css)
        self.assertIn("--ivory-soft: #b89c83;", self.css)
        self.assertIn("--black: #040404;", self.css)
        self.assertIn("--red: #9b1218;", self.css)
        self.assertIn(".team-owned-stages { display: grid; grid-template-columns: repeat(3, 1fr); }", self.css)
        self.assertNotIn("background: #172839;", self.css)
        self.assertNotIn("border-radius: 6px;", self.css)
        mobile = self.css.split("@media (max-width: 700px)", 1)[1].split("@media (max-width: 380px)", 1)[0]
        self.assertIn(".team-owned-stages { grid-template-columns: 1fr; }", mobile)
        self.assertIn(".site-nav", mobile)

    def test_supporting_copy_uses_comfortable_desktop_reading_sizes(self) -> None:
        desktop = self.css.split("@media (max-width: 700px)", 1)[0]
        for selector, declaration in (
            (".about-copy", "font-size: 16px;"),
            (".about-copy", "font-weight: 400;"),
            (".team-owned-intro p", "font-size: 16px;"),
            (".team-owned-stage > p:last-child", "font-size: 15px;"),
            (".team-owned-stage > p:last-child", "font-weight: 400;"),
            (".consultation-copy", "font-size: 16px;"),
            (".contact-copy", "font-size: 16px;"),
        ):
            block = desktop.split(selector, 1)[1].split("}", 1)[0]
            self.assertIn(declaration, block, f"{selector} should include {declaration}")

    def test_supporting_copy_uses_only_the_canonical_soft_ivory(self) -> None:
        for selector in (
            ".about-copy",
            ".team-owned-intro p",
            ".team-owned-stage > p:last-child",
            ".consultation-copy",
            ".contact-copy",
        ):
            block = self.css.split(selector, 1)[1].split("}", 1)[0]
            self.assertIn(
                "color: var(--ivory-soft);",
                block,
                f"{selector} should use the approved copy ivory",
            )
        self.assertNotIn("#b2a198", self.css)


if __name__ == "__main__":
    unittest.main()
