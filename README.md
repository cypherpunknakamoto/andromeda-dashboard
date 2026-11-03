# Andromeda Dashboard

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/cypherpunknakamoto/andromeda-dashboard/badge)](https://scorecard.dev/viewer/?uri=github.com/cypherpunknakamoto/andromeda-dashboard)

A small, local-first dashboard for recording and viewing signals from a home mesh.
FastAPI serves a read-only insights page and an API backed by a local SQLite file.
The application requires no cloud account or external API to run.

## Requirements and installation

Python 3.12 or later is recommended; continuous integration currently tests Python 3.12.
Install dependencies while online. Subsequent application use is offline; an offline
installation requires a previously prepared wheel directory for the target platform.

[Mac]
```sh
git clone https://github.com/cypherpunknakamoto/andromeda-dashboard.git
cd andromeda-dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p data
export ANDROMEDA_DB_PATH="$PWD/data/insights.db"
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

[Pi]
```sh
git clone https://github.com/cypherpunknakamoto/andromeda-dashboard.git
cd andromeda-dashboard
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p data
export ANDROMEDA_DB_PATH="$PWD/data/insights.db"
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

On Debian, the OS may require the matching Python venv package before creating the
environment. Confirm that your installed Python satisfies the requirement above.
Visit http://127.0.0.1:8000/insights. Interactive API documentation is at
http://127.0.0.1:8000/docs. Without `ANDROMEDA_DB_PATH`, the legacy location
`/var/lib/andromeda/insights.db` is used; its parent must be writable.

## API reference

| Method and route | Input | Output |
| --- | --- | --- |
| `GET /health` | None | Service name and `ok` |
| `GET /` | None | `static/index.html` if installed; otherwise JSON status |
| `GET /insights` | None | Insights HTML page |
| `GET /api/insights` | Optional integer `limit`, 1-100; default 20 | `items`, newest timestamp first |
| `POST /api/insights` | JSON object described below | `ok` and the stored `id` |

An insight contains `id` (string), `ts` (Unix seconds), `severity` (string), `title`
and `summary` (strings), `evidence` (object), `recommended_actions` (array of
objects with `label` or `action`), `source` (string), and `confidence` (number).
Omitted fields receive defaults. Timestamps must be integer-convertible and
confidence must be numeric. Reusing an ID replaces that record. Automatically
generated IDs currently use second-resolution timestamps, so callers inserting
multiple records per second should supply unique IDs. Malformed numeric fields
are a known validation limitation; callers must supply valid values.

[Mac]
```sh
curl --fail http://127.0.0.1:8000/health
curl --fail -H 'Content-Type: application/json' \
  -d '{"id":"manual-check-1","title":"Local check","evidence":{"host":"pi"}}' \
  http://127.0.0.1:8000/api/insights
curl --fail 'http://127.0.0.1:8000/api/insights?limit=1'
```

The health response should contain `"ok":true`. The final response should include
the submitted insight if it has the latest timestamp. No credentials are needed
for this loopback-only check.

## Tests and code quality

[Mac]
```sh
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
```

[Pi]
```sh
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m unittest discover -s tests -v
```

Tests use a disposable database, covering health, HTML delivery, JSON round trips,
ordering and limits, record replacement, and parameterized SQL handling.
Tests and lint also run in GitHub Actions. CodeQL scans Python separately.
Dependency versions are recorded in requirements and constraints files;
Dependabot proposes weekly Python and GitHub Actions updates. Review updates,
update all affected pins together, and run tests before merging.

## Security and deployment boundary

This prototype has **no authentication**. Bind it to `127.0.0.1`; do not expose it
to an untrusted network or the public Internet. Network access requires a separate,
reviewed authentication and TLS layer. SQLite is stored unencrypted, and API users
can replace records by ID. Store no secrets or sensitive personal information.
Use trusted local callers, valid payloads, and restrictive database-file permissions.
The HTML page renders source values as text to prevent stored script injection.

See [SECURITY.md](SECURITY.md) for reporting and limitations and
[SECURITY-DESIGN.md](SECURITY-DESIGN.md) for the threat model.

## Feedback, contributions, and releases

Report ordinary bugs or feature requests in [GitHub Issues](https://github.com/cypherpunknakamoto/andromeda-dashboard/issues).
English reports are welcome. Search existing reports first and include reproduction
steps without private data. Proposed changes use pull requests; see
[CONTRIBUTING.md](CONTRIBUTING.md). Releases use semantic versions and human-written
[release notes](CHANGELOG.md). See [LICENSE](LICENSE) for MIT license terms.
