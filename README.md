# Calabrio ONE Python Client

An unofficial Python client for Calabrio ONE **WFM and Classic recording/QM**.
Export call recordings with metadata, optional transcripts and evaluation forms,
or use 111 named WFM operations generated from Calabrio's public demo schema.

This project is not affiliated with or endorsed by Calabrio. It does not yet cover
all Calabrio ONE APIs: question-level QA answers and server bulk reporting are not
implemented as dedicated operations, and historical ingestion is not covered.
No live customer environment has been used to validate this initial version.

## Early testing — feedback welcome

**Version 0.1.0a2 is an early-testing alpha, not a production-ready release.**
Automated tests cover the wrapper, but it has not been validated against a live
Calabrio deployment. API compatibility, permissions and available resources vary
by server version. Test with an authorized non-production environment first.

Found a problem? [Submit a bug report](https://github.com/junkmailkeep/Calabrio1_Wrapper/issues/new?template=bug_report.md).
Include the package/Python versions, your Calabrio version if known, the method
used, expected versus actual behavior, and a minimal example with synthetic data.
**Never include passwords, tokens, real tenant URLs, recordings, transcripts,
evaluations, customer records or employer information.**

[Pull requests are welcome](https://github.com/junkmailkeep/Calabrio1_Wrapper/pulls)
for fixes, clearer examples and API coverage backed by public documentation.
See the [contribution guide](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/CONTRIBUTING.md)
for setup and checks. Report security vulnerabilities privately using the
[security guidance](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/SECURITY.md).

## Install

Python 3.10 or newer. Install the initial alpha from PyPI:

```sh
python -m pip install calabrio-one-wrapper==0.1.0a2
```

For future prereleases, use `python -m pip install --pre --upgrade calabrio-one-wrapper`.
To install from a source checkout instead, use `python -m pip install .`.
The distribution name is `calabrio-one-wrapper`; the Python import is `calabrio_one`.
This is an alpha: verify behavior against an authorized test environment before
using it with production records.

## Quick start

Create a client with your server URL and API account. Login happens automatically.
The URL is the HTTPS site origin, **without `/api`**. All credentials and IDs here
are fictional; replace them privately with yours.

```python
from calabrio_one import CalabrioClient

client = CalabrioClient(
    url="https://your-calabrio-server.example.com",
    username="api_user",
    password="replace-with-your-password",
)

try:
    contact = client.get_contact(123456)
    metadata = client.get_metadata(123456)
    transcript = client.get_transcript(123456)
    evaluation = client.get_evaluation(123456)
    client.download_recording(123456, "recording.wav")
finally:
    client.close()  # Log out, even if a request fails.
```

**That's all the setup.** `download_recording()` prepares the audio, waits for it,
and saves the file. You do not need a separate export request. Existing files are
never overwritten. The getter methods return Python data without writing files.

You can also use `with CalabrioClient(...) as client:` to handle logout automatically.
The [commented quick-start script](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/examples/quickstart.py)
shows the complete flow, including single and multiple call inputs.

### Pick the method you need

| Call | What you get |
| --- | --- |
| `client.get_contact(123456)` | Contact details as a dictionary |
| `client.get_metadata(123456)` | Call metadata, fetching its reference automatically; `None` if absent |
| `client.get_transcript(123456)` | Transcript JSON, if available and permitted |
| `client.get_evaluation(123456)` | `{"summary": ..., "form": ...}`; either value may be `None` |
| `client.list_evaluation_forms()` | Available form definitions |
| `client.search_contacts(begin_date="2026-01-01", end_date="2026-01-08")` | One page of matching contacts |
| `client.export_contact(123456, "contact.json")` | Contact JSON file |
| `client.export_metadata(123456, "metadata.json")` | Metadata JSON file |
| `client.export_transcript(123456, "transcript.json")` | Transcript JSON file |
| `client.export_evaluation(123456, "evaluation.json")` | Evaluation summary/form JSON file |
| `client.get_evaluation_form(7)` | A form definition; `7` is a **form ID**, not a contact ID |
| `client.download_recording(123456, "recording.wav")` | Prepares/downloads audio; returns the saved file's `Path` |
| `client.export_call(123456, "exports", include_transcript=True)` | A folder containing media, metadata, transcript and available QA summary/form |
| `client.export_calls([123456, 123457], "exports")` | A list of exported call-folder paths |

Single-call methods accept an **integer** (`123456`) or a **numeric string**
(`"123456"`). Batch exports accept a **list, tuple or generator** of IDs. Output
paths can be strings or `pathlib.Path` objects.

The evaluation summary and form are **not completed question-level answers**.
To export selected answers or comments, supply independently verified resource
paths using `extra_resources`; see the
[export guide](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/docs/recording-exports.md#completed-evaluation-answers-and-comments).

### Save a transcript or evaluation to JSON

Inside your open client session:

```python
client.export_transcript(123456, "transcript.json")
client.export_evaluation(123456, "evaluation.json")
client.export_contact(123456, "contact.json")
client.export_metadata(123456, "metadata.json")
```

Each method returns the saved file's `Path`, creates parent folders, and refuses
to overwrite existing files. Failed writes leave no partial destination file.
Use `get_...()` when you want Python data; use `export_...()` when you want a file.
These exports contain real API data; keep them outside your source repository.

### Several calls, or different options per call

Inside your open client session:

```python
# Same options for every ID: pass a list.
client.export_calls([123456, "123457"], "exports", include_transcript=True)

# Different options: dictionary keys are IDs, values are export_call arguments.
jobs = {
    123458: {"include_transcript": True},
    123459: {"include_transcript": False, "include_evaluation": False},
}
for contact_id, options in jobs.items():
    client.export_call(contact_id, "exports", **options)
```

Do not pass a dictionary or a single string directly to `export_calls()`; it rejects
those ambiguous inputs. Batch exports stop on the first failure and retain earlier
completed bundles. Call bundles include available evaluations by default; transcripts
are opt-in because availability and permissions vary.

### Export calls between dates

```python
# Inside your open client session: recordings, transcripts and evaluations.
folders = client.export_by_date("2026-01-01", "2026-02-01", "exports/january")

# Or just transcripts, into a separate destination.
folders = client.export_by_date(
    "2026-01-01", "2026-02-01", "exports/transcripts",
    include_recording=False,
    include_evaluation=False,
)
```

Dates accept `YYYY-MM-DD` strings or `datetime.date` objects. Start is inclusive;
end is exclusive, so January 1 to February 1 covers January. For a narrower time
window, supply both `begin_time="09:00"` and `end_time="17:00:00"` (on their
respective dates). Search uses the server's timezone semantics; no local timezone
conversion is performed. Verify these settings on your deployment.

All three `include_...` options default to `True`. Results are a list of saved
contact-folder paths, or `[]` when no matches are returned. Contact/available
metadata JSON and a completion manifest are also included. Evaluations are the
available summary and form, not completed question-level answers.

Pagination is automatic (`page_size=100`); it continues through short pages until
an empty page. Repeated IDs, malformed responses, or reaching `max_pages=10000`
raise an error instead of reporting completion. Existing folders and requested
resource failures stop the job; earlier completed calls remain. Server permissions,
retention, result caps and changing search results can still limit coverage.
Use a closed historical interval and validate coverage on your server.

Optional `agent_id=7` narrows to one agent; `filters={"scored": True}` supplies
additional API filters. Date/time, result-limit and statistics filters are managed
by the helper and cannot be overridden in `filters`. Recording format and polling
options match `export_call()`.

See the [commented date-range example](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/examples/export_by_date.py).

### Optional settings

| Argument | Default | Used by |
| --- | --- | --- |
| `timeout` | `30` seconds | Client HTTP inactivity timeout |
| `media_format` | `"WAV"` | Download / bundle methods; also accepts `OPUS`, `WEBM`, `WEBM_VP8`, `WEBM_VP9` where supported |
| `wait_timeout` | `120` seconds | Download / bundle polling budget; not a strict wall-clock deadline |
| `poll_interval` | `2` seconds | Delay between pending download checks |
| `prepare` | `True` | `download_recording()`; use `False` to resume an already-requested conversion |
| `include_recording` | `True` | Call bundles; disable for JSON-only exports |
| `include_transcript` | `False` | Call bundles |
| `include_evaluation` | `True` | Call bundles; summary/form |
| `is_root_recording` | `False` | Transcript getter / export / bundles; `True` selects the original/root recording |
| `extra_resources` | `None` | Call bundles; dictionary of filename stems to verified local GET paths |

`export_recording()` is also available as an alias for the prepare-and-download
workflow. The lower-level `ClassicClient` remains available for existing integrations;
its `download_recording()` still downloads an already-requested export.

### Prefer environment variables?

Set `CALABRIO_CLASSIC_URL`, `CALABRIO_USERNAME`, and `CALABRIO_PASSWORD`, then use:

```python
from calabrio_one import CalabrioClient

with CalabrioClient.from_env(api="classic") as client:
    client.download_recording(123456, "recording.wav")
```

Environment variables are optional. The package does not automatically read `.env`
files. `from_env()` selects the only configured API family; when both Classic and
WFM settings exist, specify `api="classic"` or `api="wfm"`.

The [batch command-line example](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/examples/export_calls.py)
uses those environment variables. Run it from the checkout after installation:

```sh
python examples/export_calls.py --kind call --ids 123456 123457 --transcript
python examples/export_calls.py --kind recording --ids 123456
python examples/export_calls.py --kind transcript --ids 123456 123457
python examples/export_calls.py --kind evaluation --ids 123456
python examples/export_calls.py --help
```

All example scripts are included in the source distribution. They are example files, not
installed console commands; copy them from the repository when using the wheel.

## Get started with WFM

Create a client with your API URL and token. Use your environment's exact API
root, including `/api` where applicable.

```python
from calabrio_one import CalabrioClient

with CalabrioClient(
    url="https://your-tenant.example.com/api",
    token="replace-with-your-token",
) as client:
    business_units = client.all_business_units()
    people = client.people_by_business_unit_id(
        business_unit_id="00000000-0000-0000-0000-000000000001",
        page=1,
        page_size=50,
    )
    schedule = client.schedule_by_person_id(
        person_id="00000000-0000-0000-0000-000000000002",
        period={"start_date": "2026-01-01", "end_date": "2026-01-07"},
    )
```

All 111 WFM methods expose named, typed arguments for editor autocomplete. Use
Python-style names in both arguments and nested dictionaries; the wrapper converts
them to API field names. Original API names inside nested dictionaries also work.
Unknown nested fields and duplicate aliases raise `TypeError`. Free-form dictionary
keys are preserved where the API schema permits them. Responses are unchanged.

WFM IDs use GUID strings or `UUID` objects, rather than numeric recording contact
IDs. Date fields accept ISO date strings or `datetime.date` values; datetime fields
accept ISO strings or `datetime.datetime` values. Lists take multiple values, for example:

```python
people = client.people_by_ids(ids=[
    "00000000-0000-0000-0000-000000000002",
    "00000000-0000-0000-0000-000000000003",
])
```

Run this inside your open client session. The
[commented WFM example](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/examples/wfm.py)
explains arguments and includes an optional write example. The
[complete method reference](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/docs/endpoints.md)
lists every method's arguments, types, and nested fields.

Recording methods require username/password; WFM methods require a token. Use
separate clients for the two API families. Wrong-family calls fail locally.
The existing positional `CalabrioClient(base_url, token)` form still works.
For environment-based setup, set `CALABRIO_BASE_URL` and `CALABRIO_TOKEN`, then call
`CalabrioClient.from_env(api="wfm")`. The package does not load `.env` files itself.

All identifiers here are fictional. Supply real values privately at runtime.
Responses retain the server's JSON structure, including any `Result` envelope.
There is no automatic pagination: increment `page` where the endpoint supports it.
Required fields and value types are validated by the server; named arguments check
field spelling locally.
Explicit `None` becomes JSON `null`; omitted arguments remain omitted.

Advanced: raw dictionaries bypass field-name normalization. Use them when copying a request from your environment's API docs:

```python
result = client.people_by_ids({"Ids": ["00000000-0000-0000-0000-000000000002"]})
# New endpoint not yet in the generated methods:
result = client.request("query/BusinessUnit/AllBusinessUnits", {})
```

Use these calls inside a client context, before it closes. Do not mix a positional
payload dictionary with keyword fields. See [all 111 methods](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/docs/endpoints.md).
Both query and command methods send POST requests. Command methods can change data.

## Authentication and errors

The public demo schema describes Bearer authorization, which is the default.
For installations that require personal-token Basic authentication, explicitly use
`CalabrioClient.from_env(api="wfm", auth_mode="basic")`; its username is `__token__`.
Use the authentication method required by your own environment.

```python
from calabrio_one import CalabrioClient, AuthenticationError, RateLimitError

try:
    with CalabrioClient.from_env(api="wfm", timeout=30) as client:
        result = client.all_business_units()
except AuthenticationError:
    print("Check the personal access token.")
except RateLimitError:
    print("Rate limit reached. Wait before making another request.")
```

HTTP errors expose `status_code`. Errors omit server bodies, URLs and tokens.
Nonempty top-level `Errors` in a successful JSON response raise `OperationError`.
Transport failures raise `TransportError`; malformed JSON raises `ResponseError`.
There are **no automatic retries**, so commands are not silently repeated. A timeout
does not prove a command failed: check server state before submitting it again.
TLS verification is enabled by default, redirects are rejected, and environment proxies are
not inherited. Avoid HTTP debug logging in applications handling private data.
The clients do not log or send telemetry. Export methods write the requested files;
getter methods return data without saving it.

## Self-signed certificates

For a private CA or self-signed certificate, prefer trusting its PEM certificate:

```python
import ssl
from calabrio_one import CalabrioClient

context = ssl.create_default_context(cafile="/path/to/trusted-ca.pem")
client = CalabrioClient(
    url="https://your-calabrio-server.example.com",
    username="api_user",
    password="replace-with-your-password",
    verify=context,
)
try:
    contact = client.get_contact(123456)
finally:
    client.close()
```

You can explicitly bypass certificate verification when needed:

```python
with CalabrioClient(
    url="https://your-calabrio-server.example.com",
    username="api_user",
    password="replace-with-your-password",
    verify=False,
) as client:
    contact = client.get_contact(123456)
```

`verify=False` keeps HTTPS encryption but disables certificate and hostname checks.
An impersonated server could receive credentials and call data. It emits
`InsecureTLSWarning`; it is never an automatic fallback after a certificate failure.
The same `verify` argument works with token-based WFM, `ClassicClient`, and
`CalabrioClient.from_env(api="classic", verify=False)`. The default remains `True`.
HTTP URLs are still rejected. Keep certificate files and private keys outside the repo.

## Public repository safety

The current source, examples, Git history and release archives have been reviewed
for employer/customer information and credentials; none were found. This is an
alpha with automated tests, not a security certification or live-deployment guarantee.
Exports contain real private data when you run against a real server; they are not
anonymized. Keep credentials, exports and debug logs out of public commits and issues.
See [security guidance](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/SECURITY.md)
and the release checklist before publishing.

## Development

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
ruff check .
python -m mypy src/calabrio_one examples tools
python -m build
python -m twine check dist/*
```

Tests use a synthetic transport, never real credentials or customer records.
See the [release audit](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/docs/releasing.md#local-audit), [contribution and privacy guidance](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/CONTRIBUTING.md) and the
[release checklist](https://github.com/junkmailkeep/Calabrio1_Wrapper/blob/main/docs/releasing.md).

## API provenance

The initial endpoint catalog was generated on 2026-10-27 from the
[public demo OpenAPI schema](https://mtdemousce01.teleopticloud.com/api/swagger/v1/swagger.json)
linked through Calabrio's [HR integration documentation](https://help.calabrio.com/doc/Content/api-getting-started/wfm-hr-integrations-via-swagger-api.htm).
Only routes, field identifiers, and structural type information are retained; the downloaded schema, server URLs,
examples, descriptions and defaults are not bundled.

To regenerate, download the public schema to a temporary location, then run
`python tools/generate_endpoints.py /path/to/public-schema.json` and review the diff.
Never use a private tenant schema without reviewing and sanitizing it first.

Further official references:
[WFM API access](https://help.calabrio.com/doc/Content/api-getting-started/access-wfm-apis.htm)
and [personal access tokens](https://help.calabrio.com/doc/Content/user-guides/wfm-settings/personal-access-token.htm).
Tenant versions and permissions can differ from the public demo.

MIT licensed. Calabrio trademarks belong to their respective owners.
