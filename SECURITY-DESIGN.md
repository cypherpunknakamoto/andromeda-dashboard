# Security design and review notes

## Intended environment

One trusted local user or trusted local helper writes insights to a SQLite
database. The browser reads them through a loopback-bound FastAPI service.
No external API, account, telemetry, cryptographic protocol implementation,
password store, or random security token is part of the application.

## Threats, controls, and limitations

| Threat | Control and remaining limitation |
| --- | --- |
| SQL injection through insight text | SQLite placeholders bind values separately from SQL. A regression test stores a SQL-looking title without executing it. |
| Stored cross-site scripting in source values | Build DOM elements and assign textContent; do not interpolate insight data into innerHTML. Other displayed text also uses textContent. |
| Unbounded result reads | API limits are validated as integers from 1 to 100; invalid values return 422. This is not a complete denial-of-service defense. |
| Unauthorized reads or writes | Bind to loopback; no application authentication exists. All local clients with access to the service are trusted. Remote deployment needs reviewed authentication/authorization and TLS. |
| Data loss and collisions | Reusing an ID deliberately replaces the record. Supply unique IDs; default IDs can collide within a second. Back up important data. |
| Malformed or oversized write requests | Known limitation: full input schema, request-size quotas, and numeric validation are incomplete. Use trusted clients and synthetic/non-sensitive data. |
| Local data theft | Use restrictive filesystem permissions. The SQLite file is not encrypted; no confidential data should be stored. |
| Dependency or workflow compromise | Pin versions/hashes, review updates, run tests, use CodeQL, and use read-only workflow defaults. Dependabot proposes updates; it does not merge them. |
| Destructive repository changes | Rules protect main from deletion and force pushes and require pull requests. Independent human approval is not mandatory for this sole-maintainer project. |

## Design principles to understand

Keep the service small; deny remote exposure by default; check authorization at
every restricted entry point when an authentication layer is introduced; keep
design public while protecting credentials; use multiple independent conditions
for sensitive actions; grant minimum privileges; avoid unnecessary shared state;
make safe use straightforward; limit exposed routes; and validate known-good
inputs rather than trying to enumerate every malicious input.

Common relevant errors include SQL injection, script injection, missing
authentication/authorization, overly broad permissions, and dependency flaws.
Their controls above should be reviewed by the human maintainer. These notes
are study material and evidence of design choices, not proof of a person's
security knowledge or of an independently completed security audit.
