# Security policy

## Supported versions and scope

Security work targets the latest main branch and the latest 0.1.x release once
published. Older snapshots are unsupported. Use the latest supported source and
review CHANGELOG.md before updating.

This is a local prototype without authentication or encrypted database storage.
Bind to loopback (127.0.0.1). It is not suitable for direct Internet exposure or
storage of sensitive information. Supply valid numeric timestamp/confidence values
and unique IDs; reusing an ID overwrites its record. Resource quotas and full
payload validation are not implemented. Review SECURITY-DESIGN.md for details.

## Reporting a vulnerability

Report non-sensitive security concerns through the repository's GitHub Issues:
https://github.com/cypherpunknakamoto/andromeda-dashboard/issues

Include affected version/commit, reproduction steps using synthetic data, impact,
and any proposed remediation. Do not post secrets or personal information. If
GitHub displays a "Report a vulnerability" button in the Security tab, use that
private reporting channel for sensitive details; otherwise open an issue asking
the maintainer to arrange a private channel before sending sensitive details.

The maintainer aims to acknowledge reports within 14 days, assess reproducibility
and impact, and coordinate remediation and disclosure. This is a response target,
not a promise that every issue will be fixed within 14 days. Public reports and
non-sensitive status updates remain searchable through GitHub.
