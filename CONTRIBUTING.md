# Contributing

Use GitHub Issues for bugs, enhancements, and project discussion; use pull requests
for proposed changes. English reports and comments are accepted. Search existing
reports before opening a new one. Include expected behavior, actual behavior, your
OS/Python versions, and minimal reproduction steps. Never include secrets or real
private insight records. Follow SECURITY.md for security reports.

## Development process

1. Create a topic branch from main.
2. Keep changes small; explain the problem and resulting behavior.
3. Use readable Python, type hints for new helpers, and parameterized SQL.
4. Add automated tests for major new functionality and regressions. Changes to
   supported behavior must include tests or a clear explanation of why testing
   is not applicable. Test database writes only against disposable databases.
5. Run the following checks and address warnings before opening a pull request.

[Mac]
```sh
python -m pip install --require-hashes -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
```

[Pi]
```sh
python -m pip install --require-hashes -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
```

CI runs tests and lint; CodeQL checks Python for security findings. Workflow actions
are pinned to complete commit hashes and use limited token permissions. Do not
add untrusted pull request code to privileged workflows. When updating dependencies,
keep constraints.txt, requirements.in, and requirements-dev.in consistent. Use
pip-tools 7.6.2 to regenerate both requirements files with --generate-hashes, then
install with --require-hashes and rerun the checks. Do not hand-edit generated hashes.

Main uses pull requests, blocks force pushes and deletion, and requires resolution
of review conversations. This is currently a sole-maintainer project; a second
human approval is not mandatory, and AI review is not represented as human review.
Human review is welcome when another qualified contributor is available.

## Maintenance and releases

The maintainer aims to acknowledge bug reports and enhancement requests within
14 days. Release versions use MAJOR.MINOR.PATCH. Update CHANGELOG.md with a readable
summary, compatibility impact, and any known CVE fixes, then tag the release.
Do not publish credentials, local databases, environment folders, or generated
executables in the source repository. Contributions are under the project's MIT
license. Do not contribute code you lack permission to license.
