#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "index.html",
    "privacy/index.html",
    "support/index.html",
    "licenses/index.html",
    "zh-cn/index.html",
    "zh-cn/privacy/index.html",
    "zh-cn/support/index.html",
    "zh-cn/licenses/index.html",
    "licenses/THIRD_PARTY_NOTICES.txt",
]
FORBIDDEN = ("google-analytics", "googletagmanager", "facebook.com/tr", "hotjar", "doubleclick")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.lang = None
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        if tag in {"a", "link", "img"}:
            value = values.get("href") or values.get("src")
            if value:
                self.links.append(value)

errors = []
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

html_files = list(ROOT.rglob("*.html"))
for path in html_files:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    for marker in FORBIDDEN:
        if marker in lower:
            errors.append(f"{path.relative_to(ROOT)} contains forbidden tracker marker: {marker}")
    parser = LinkParser()
    parser.feed(text)
    if not parser.lang:
        errors.append(f"{path.relative_to(ROOT)} has no html lang attribute")
    for link in parser.links:
        if link.startswith(("#", "mailto:", "tel:", "https://", "http://")):
            continue
        target = unquote(link.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        if target.startswith("/cc-site/"):
            candidate = ROOT / target.removeprefix("/cc-site/")
        elif target.startswith("/"):
            continue
        else:
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)} link escapes site root: {link}")
                continue
        if candidate.is_dir():
            candidate = candidate / "index.html"
        elif candidate.suffix == "":
            candidate = candidate / "index.html"
        if not candidate.exists():
            errors.append(f"{path.relative_to(ROOT)} broken internal link: {link}")

privacy = (ROOT / "privacy/index.html").read_text(encoding="utf-8").lower() if (ROOT / "privacy/index.html").exists() else ""
for phrase in ("does not collect", "chemical structures", "github pages", "data retention"):
    if phrase not in privacy:
        errors.append(f"privacy page missing expected disclosure: {phrase}")

support = (ROOT / "support/index.html").read_text(encoding="utf-8").lower() if (ROOT / "support/index.html").exists() else ""
for phrase in ("support", "github", "confidential"):
    if phrase not in support:
        errors.append(f"support page missing expected content: {phrase}")

if errors:
    print("Site validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Site validation passed: {len(html_files)} HTML files checked.")
