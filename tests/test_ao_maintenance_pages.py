from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AOMaintenancePageTests(unittest.TestCase):
    def test_public_pages_use_generic_tool_name_and_workflow(self):
        for name in ("ao-maintenance.html", "ao-maintenance-privacy.html", "ao-maintenance-terms.html"):
            with self.subTest(page=name):
                html = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(html, r"\bAO\s+\w+\s+Maintenance\b")
                for private_workflow_detail in ("member", "legacy cells", "legacy-cell", "initial api acceptance", "initial acceptance"):
                    self.assertNotIn(private_workflow_detail, html.lower())

    def test_overview_describes_private_tool_and_links_to_notices(self):
        page = ROOT / "ao-maintenance.html"
        self.assertTrue(page.is_file(), "AO overview page is missing")
        html = page.read_text(encoding="utf-8")
        for phrase in (
            "AO Maintenance", "Empire Operating", "operator-only",
            "Drive file metadata", "Google Sheets", "Apps Script",
            "account-wide", "separate approval", "not a public sign-up service",
            'href="ao-maintenance-privacy.html"',
            'href="ao-maintenance-terms.html"',
            'href="mailto:empireoperating@proton.me"',
            'rel="canonical" href="https://empireoperating.com/ao-maintenance.html"',
        ):
            self.assertIn(phrase, html)
        for forbidden in ("<form", "<script", "client_secret", "@gmail.com", "script.google.com/macros/"):
            self.assertNotIn(forbidden, html)

    def test_privacy_notice_discloses_scopes_processing_retention_and_revocation(self):
        page = ROOT / "ao-maintenance-privacy.html"
        self.assertTrue(page.is_file(), "Privacy notice is missing")
        html = page.read_text(encoding="utf-8")
        for phrase in (
            "AO Maintenance", "Empire Operating", "OpenAI",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/script.projects",
            "https://www.googleapis.com/auth/script.deployments",
            "account-wide", "local", "retention", "revoke",
            "Google Account", "GitHub Pages", "Google Fonts",
            "general-purpose AI", "advertising", "not sold",
            'href="ao-maintenance.html"',
            'href="ao-maintenance-terms.html"',
            'rel="canonical" href="https://empireoperating.com/ao-maintenance-privacy.html"',
        ):
            self.assertIn(phrase, html)
        for forbidden in (
            "<form", "<script", "client_secret", "@gmail.com",
            "script.google.com/macros/", "everything stays local",
            "never leaves this machine", "deleted after 30 days",
        ):
            self.assertNotIn(forbidden, html)

    def test_terms_keep_authorization_and_exact_task_approval_separate(self):
        page = ROOT / "ao-maintenance-terms.html"
        self.assertTrue(page.is_file(), "Usage terms are missing")
        html = page.read_text(encoding="utf-8")
        for phrase in (
            "AO Maintenance", "operator-only", "not a public service",
            "Google consent", "exact task", "production", "QA", "deletion",
            "permission", "allowlist", "Gmail", "local loopback",
            "does not grant", "security", "OpenAI", "retention",
            'href="ao-maintenance.html"',
            'href="ao-maintenance-privacy.html"',
            'href="mailto:empireoperating@proton.me"',
            'rel="canonical" href="https://empireoperating.com/ao-maintenance-terms.html"',
        ):
            self.assertIn(phrase, html)
        for forbidden in ("<form", "<script", "client_secret", "@gmail.com", "script.google.com/macros/"):
            self.assertNotIn(forbidden, html)


if __name__ == "__main__":
    unittest.main()
