# ChemCreate Website

Public website and App Store support pages for ChemCreate.

ChemCreate itself is developed in a private repository. Public product claims in this
repository should be kept aligned with the latest verified release audit, privacy
manifest, and third-party notices from the app repository.

## Purpose

This site is intended to provide stable public URLs for:

- product information;
- App Store privacy policy;
- user support;
- open-source software notices.

The site is deliberately static: no framework, package manager, analytics SDK,
advertising, tracking, third-party fonts, or application cookies are required.

## Pages

- `/` — product overview
- `/privacy/` — Privacy Policy
- `/support/` — Support
- `/licenses/` — Open Source Notices
- `/zh-cn/` — Simplified Chinese site

## Local preview

Serve the repository root with any static web server, for example:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

## Validation

```sh
python3 scripts/check_site.py
```

The checker verifies required App Store-facing pages, internal links, language
alternates, and basic privacy/support content.

## GitHub Pages

Publish the repository root from the `main` branch using GitHub Pages. The expected
default URL is:

`https://quickieee.github.io/cc-site/`

A custom domain can be added later without changing the site architecture.

## Release gates

Before using these URLs in a production App Store submission:

1. verify the published site is reachable over HTTPS;
2. confirm the Privacy Policy still matches the shipping app and App Store Connect
   privacy answers;
3. confirm the support page exposes a current, monitored contact route and add a
   private contact method where required by applicable law or App Store review;
4. set the final legal copyright holder consistently in the app, App Store Connect,
   and site if displayed;
5. update product claims whenever the shipping app's capabilities change;
6. add only Apple's official App Store badges after a public App Store product URL
   exists.

## Apple references

- App privacy:
  https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy/
- Platform version information / Support URL:
  https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- App Review Guidelines:
  https://developer.apple.com/app-store/review/guidelines/

## Source-of-truth policy

For release work, do not infer capabilities from roadmap text. Use the shipping build
and the latest verified release audit. In particular, privacy statements must stay
consistent with the app's `PrivacyInfo.xcprivacy`.
