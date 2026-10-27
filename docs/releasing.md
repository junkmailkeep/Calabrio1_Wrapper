# Release checklist

The initial package is an unpublished alpha. The project uses MIT licensing;
confirm that choice and ownership before the first release.

1. Confirm the proposed name `calabrio-one-wrapper` is available on PyPI.
2. Review Git history, source files, examples, and built archives for private data.
3. Run pytest, Ruff, build, and Twine metadata validation in a clean environment.
4. Install the wheel into another clean environment and smoke-test imports.
5. Validate representative read operations against an authorized environment;
   keep credentials and responses outside the repository. Validate write operations
   only in an approved test environment with synthetic records.
6. Set up PyPI/TestPyPI project ownership and trusted publishing, or use a scoped
   upload token kept outside the repository. Do not put tokens in commands or files.
7. Upload to TestPyPI first, verify installation, then publish the reviewed artifacts.

Push/PR CI tests and builds artifacts only. The separate manually triggered publishing
workflow uploads packages after testing; neither workflow contacts a Calabrio tenant.

## Local audit

Reviewed on 2026-10-27. This is an unpublished alpha; the checks below do not replace
validation against an authorized Calabrio test environment.

### Findings fixed

| Severity / confidence | Location | Finding and fix |
| --- | --- | --- |
| High / confirmed | `src/calabrio_one/classic.py:501`, `export_calls` | A string became individual contact IDs; dictionary settings were silently ignored. Ambiguous batch inputs now fail before any request. |
| High / confirmed | `src/calabrio_one/classic.py:248`, `download_recording` | HTTP 206 could publish a partial recording. Media publication now requires HTTP 200; failed transfers leave no destination file. |
| Medium / confirmed | `src/calabrio_one/classic.py:180`, `search_contacts` | The default result cap did not cover later requested ranges. It now includes the last requested item. |
| Medium / confirmed | `src/calabrio_one/endpoints.py:10`, `_operation` | The typed package had no dispatch contract on its generated base. The generator now declares it explicitly; package, example and generator type checks pass. |
| Medium / confirmed | `src/calabrio_one/classic.py:382`, export validation | Invalid boolean/timing options could make requests before failing; extra filenames could conflict with Windows device names. These inputs now fail early. |
| Medium / confirmed | `src/calabrio_one/classic.py:286`, status polling | A JSON status response could consume unlimited memory. Status buffering is now limited to 1 MiB and checked against the polling budget. |
| Medium / confirmed | `tools/generate_endpoints.py:23` | Conflicting field aliases or cyclic references could generate incorrect code or recurse indefinitely. Invalid schemas now fail before output files are replaced. |

Shared HTTPS/TLS, timeout validation and sanitized HTTP/JSON error handling now live
in `_http.py`. Both clients use these rules; their authentication and API-specific
workflows stay separate. New WFM also accepts a verified private-CA SSL context.

### Verification

- 134 tests passed on macOS for clean wheel installations on Python 3.10, 3.11,
  3.12, 3.13 and 3.14, and on Python 3.12 with the minimum supported HTTPX 0.27.0.
- All 111 generated WFM routes and inherited request-field mappings were checked
  independently against the downloaded public demo schema.
- Ruff and Mypy passed for package, example and generator code.
- The four shipped example modes passed synthetic tests, including multiple IDs
  and error handling. README Python snippets compile.
- A temporary local HTTPS server verified login/session/logout, WFM authorization,
  private-CA trust, rejection of untrusted certificates and redirects, delayed media
  readiness, transcripts, and cleanup after an actual truncated HTTP transfer.
- Source and wheel builds passed Twine checks. Clean installed-wheel tests passed;
  release archives exclude private/export folders, environment files and caches.
- Runtime dependencies installed for this audit had no known advisories reported by
  pip-audit. This is a point-in-time check, not a guarantee about future releases.
- Manual review and targeted scans covered source, documentation, examples, tests,
  the existing Git history and release archive contents. No employer/customer data
  or real credentials were found. Public documentation/demo URLs and synthetic
  credentials in tests are intentional. This does not certify arbitrary future files.

### Still required before publishing

- Verify representative call, transcript and QA exports plus WFM queries on an
  authorized test server; test commands only with approved synthetic records.
- Validate real audio/video playback and the deployment's search range behavior.
  Download checks recognize container headers; they are not a media decoder.
- Confirm any question-level answer/comment resource paths separately. These remain
  configurable verified resources, not promised built-in endpoints.
- Let the configured GitHub CI run on Linux, macOS and Windows. Only macOS was
  executed locally during this audit; configured CI is not evidence of a CI pass.
- Confirm package-name ownership, MIT licensing and publisher configuration. No
  upload, release, push, or live customer API call was performed during this audit.

### Simplified client follow-up

The public `CalabrioClient` now accepts `url`, `username` and `password`, logs in
automatically, and exposes contact, metadata, transcript and evaluation getters.
Its `download_recording` prepares and downloads media in one call. The original
WFM constructor and lower-level Classic client remain supported. The quick-start
script, credential-family checks, automatic metadata/form resolution and download
preparation are covered by the updated 134-test suite. Clean-wheel checks were
repeated across Python 3.10–3.14 and with HTTPX 0.27.0 using cached dependencies.

### Consistent method arguments and exports

All 111 WFM operations now expose typed, named arguments. Nested dictionaries
accept Python-style field names, including objects within lists. Original API
payload dictionaries remain supported unchanged. One-call JSON exports cover
contacts, metadata, transcripts and evaluation summary/forms; batch bundle options
are explicit too. README, the full method reference and three commented example
scripts describe the same interface.

The updated 149-test suite passed in clean wheel installations on Python 3.10,
3.11, 3.12, 3.13 and 3.14, plus Python 3.12 with HTTPX 0.27.0. Independent checks
compared all 111 signatures and field mappings against the public schema. Ruff,
Mypy, documentation snippet compilation, builds and Twine checks passed. Targeted
privacy scans of source and built archives found no employer references or private
keys; archives exclude environment files, caches and exports. Live deployment
validation and the publishing requirements above remain outstanding.

### Public source and certificate-option review

Certificate verification remains enabled by default. An explicit `verify=False`
is now accepted for both API families and emits `InsecureTLSWarning`. It disables
certificate and hostname checks, never HTTPS encryption, and is never used as an
automatic fallback. A verified private-CA SSLContext remains the preferred option.

All 184 tests passed in clean wheel installations on Python 3.10–3.14 and on
Python 3.12 with HTTPX 0.27.0. Real loopback HTTPS tests generated ephemeral
certificates to verify untrusted-certificate rejection before HTTP requests,
trusted-CA connections, explicit bypass and environment-based construction.
These tests require loopback listening; they never connect to a Calabrio tenant.
Trustme is a development-only dependency; no keys/certificates are committed.

Ruff, Mypy, builds and Twine checks passed. The installed runtime dependency
versions had no known advisories reported by pip-audit on 2026-10-27. Source,
Git history and distribution review found no employer/customer information or
real credentials, and no confirmed security defect blocking publication as an
alpha. Security guidance and certificate/key ignore rules were added. This is a
scoped review, not security certification; the live validation and GitHub settings
listed above and in SECURITY.md remain outstanding. Nothing was published.

## Publish with GitHub Trusted Publishing

The manually started `publish.yml` workflow tests and builds `main`, then publishes
using a short-lived identity token. It needs no saved PyPI API token. Ordinary
pushes run CI only and never publish. Choose `testpypi` for a rehearsal or `pypi`
for the public release. An existing version/file cannot be replaced on PyPI.

For the first upload, configure a pending publisher in your PyPI account at
https://pypi.org/manage/account/publishing/ with these exact values:

| Field | Value |
| --- | --- |
| PyPI project name | `calabrio-one-wrapper` |
| Owner | `junkmailkeep` |
| Repository | `Calabrio1_Wrapper` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

For a rehearsal, configure the same values at
https://test.pypi.org/manage/account/publishing/ but use environment `testpypi`.
TestPyPI has separate accounts and publisher settings. Configure the matching
GitHub environments in repository settings; restrict releases to `main` and add
required reviewers if desired. Never paste API tokens into issues or chat.

After CI succeeds, open Actions → Publish package → Run workflow, select `main`
and the chosen index. After a successful PyPI upload, verify installation in a new
virtual environment with `python -m pip install calabrio-one-wrapper==0.1.0a1`.
Update the README's publication status only after the upload is confirmed.
