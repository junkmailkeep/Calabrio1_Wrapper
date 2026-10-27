# Security

This package is an unpublished alpha. Automated tests and code review do not
establish compatibility with every Calabrio deployment or guarantee security.

## Connection settings

Certificate and hostname verification are enabled by default. For a private CA,
pass an SSLContext created with `ssl.create_default_context(cafile=...)`.
Explicit `verify=False` disables those identity checks and emits
`InsecureTLSWarning`. HTTPS encryption remains, but credentials and records could
be intercepted by an impersonated server. Verification is never disabled as an
automatic fallback. HTTP URLs and redirects remain rejected.

Use a dedicated API account with only the permissions your task needs. Secrets
belong in your environment or secret manager. The wrapper does not log requests,
send telemetry, or load `.env` files automatically. Application debug logging can
expose credentials and records, even when library exceptions omit them.

## Private data

Do not commit real credentials, tenant URLs, private keys, call recordings,
transcripts, evaluations, API responses, private schemas or employer details.
Examples and tests use synthetic values. Export files are not anonymized.
Use an output directory outside this repository. Ignore rules are a convenience,
not a secret scanner; they cannot remove already tracked files or Git history.
Review source, history and built archives before each publication.

## Reporting a vulnerability

Do not put secrets, call data or an exploitable vulnerability in a public issue.
Use the repository's private vulnerability reporting feature if it is enabled.
Otherwise ask the maintainer for a private reporting channel without disclosing
the vulnerability in public. Use synthetic reproduction data. If credentials were
exposed, revoke or rotate them promptly with their owner.

Before enabling public distribution, configure GitHub private vulnerability
reporting, secret scanning/push protection and dependency alerts where available.
Pushes do not publish automatically. A separate manually triggered workflow supports
Trusted Publishing; no live-tenant tests are configured.
