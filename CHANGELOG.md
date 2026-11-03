# Changelog

Versions follow semantic versioning. The repository contains source; it does not
publish generated executable artifacts.

## 0.1.0 - 2026-11-03

Initial documented local prototype release:

- Record and view insights through FastAPI and SQLite.
- Configure a writable database location using ANDROMEDA_DB_PATH while retaining
  the legacy default when the variable is unset.
- Bound list queries to 1-100 records.
- Render insight source text safely instead of interpreting it as HTML.
- Add regression tests, lint, CodeQL, pinned dependencies, and weekly update checks.
- Add installation/API documentation, contribution instructions, a security policy,
  and MIT licensing.

Compatibility: negative, zero, and greater-than-100 list limits are now rejected
with HTTP 422. Existing valid API calls and the legacy database default remain
supported. Existing deployments must stay on trusted loopback access; this release
does not add authentication. No CVE-assigned vulnerability fixes are claimed.
