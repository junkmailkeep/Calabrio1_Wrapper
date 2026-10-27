# Contributing

Keep this repository safe for public distribution. Never commit employer or
customer names, tenant URLs, credentials, employee records, production responses,
private schemas, screenshots, or operational details. Use example.com domains,
synthetic records, and fabricated identifiers in tests and documentation.

Local secrets belong in environment variables or ignored `.env` files. Keep
private scratch data outside this checkout or in the ignored `private/` directory.
Ignoring a file does not remove it from Git history if it was previously tracked.

Before contributing, review both the staged diff and package contents. Run the
tests, lint, build and metadata checks documented in README.md. Endpoint additions
must be supported by public documentation and tested using synthetic responses.
Describe which API version/source was used and any validation limitations.

Do not attach real request/response bodies to public bug reports. Report exposed
credentials privately to their owner and revoke them promptly.
