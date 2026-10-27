# Recording and QA exports

`CalabrioClient(url=..., username=..., password=...)` logs into the recording/QM API
automatically. `CalabrioClient(base_url=..., token=...)` supports New WFM. These
API families use different roots and credentials; use separate clients for each.

## Export a call

Set `CALABRIO_CLASSIC_URL` to your HTTPS site origin (without `/api`),
`CALABRIO_USERNAME`, and `CALABRIO_PASSWORD` privately in your environment.

```python
from calabrio_one import CalabrioClient

with CalabrioClient.from_env(api="classic") as client:
    folder = client.export_call(
        123456,                    # fictional ID; supply your own at runtime
        output_dir="exports",
        include_transcript=True,
    )
```

The result is a new `exports/123456/` folder:

- `recording.wav`: streamed recording download.
- `contact.json`: original contact response.
- `metadata.json`: metadata, resolving its local `$ref` when present.
- `evaluation-summary.json`: evaluation object from the contact, when present.
- `evaluation-form.json`: referenced form definition, when present.
- `transcript.json`: included only when requested.
- `manifest.json`: completion marker, saved filenames, absent optional resources,
  and which optional features were requested.

This writes private API results to your selected destination; it does not anonymize
those results. Keep exports outside a source repository. The repository ignores
`exports/`, and release archives include only explicitly selected source paths.

An existing contact folder is never overwritten or merged. A failed export removes
its newly created incomplete folder; previously completed call bundles remain.
Requested-resource errors fail the export rather than silently claiming completeness.
Absent contact metadata/evaluation references are listed in the manifest. Transcripts
are opt-in because availability and permissions vary. Use `include_evaluation=False`
when you only need contact data and media.

## Export calls between dates

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

## Just the recording, or several calls

```python
with CalabrioClient.from_env(api="classic") as client:
    client.export_recording(123456, "exports/call.wav")
    folders = client.export_calls([123457, 123458], "exports")
```

`export_calls` accepts a list, tuple or generator of IDs. It rejects a single ID
and dictionaries; loop over a dictionary explicitly for per-call options. It stops on
the first failure and keeps earlier completed bundles. It is not the server's bulk
export API, and it does not imply that search results contain every historical call.

Supported format choices: `WAV`, `OPUS`, `WEBM`, `WEBM_VP8`, `WEBM_VP9`.
Availability depends on the server. Pass `media_format="WEBM"` for video exports.

Conversion is requested once by POST. Download GETs are polled for pending responses;
POSTs are never automatically repeated. Adjust `wait_timeout=120` and
`poll_interval=2` as needed. HTTP inactivity timeouts also apply; the polling budget
is checked between chunks and is not a strict wall-clock deadline. Interrupted or
invalid downloads leave no destination file. Existing files are never replaced.

After a timeout, resume the already requested download without re-requesting conversion:

```python
with CalabrioClient.from_env(api="classic") as client:
    client.download_recording(123456, "exports/call.wav", wait_timeout=300, prepare=False)
```

## Save individual JSON files

```python
with CalabrioClient.from_env(api="classic") as client:
    client.export_contact(123456, "exports/contact.json")
    client.export_metadata(123456, "exports/metadata.json")
    client.export_transcript(123456, "exports/transcript.json")
    client.export_evaluation(123456, "exports/evaluation.json")
```

Each method accepts an integer or numeric-string contact ID and a string or `Path`
destination. It creates parent directories and returns the saved `Path`. Existing
files are never replaced; failed writes leave no partial destination. Missing
metadata becomes JSON `null`. Evaluation files contain `summary` and `form`, not
completed question-level answers. `export_transcript(..., is_root_recording=True)`
selects the original recording. Use the corresponding `get_...()` method to return
Python data without saving it.

## Search, metadata, transcript and form methods

```python
with CalabrioClient.from_env(api="classic") as client:
    page = client.search_contacts(
        begin_date="2026-01-01", end_date="2026-01-08",
        start=1, count=100, filters={"hasRecording": True},
    )
    contact = client.get_contact(123456)
    transcript = client.get_transcript(123456, is_root_recording=False)
    forms = client.list_evaluation_forms()
    form = client.get_evaluation_form(7)
```

Search returns the server response unchanged. `start` is a one-based Range start;
`count` is limited to 100. Additional `filters` retain exact API spelling; list
values support repeated parameters. Search is one page per call. The server's
`limit`, range behavior, scoping and retention still apply. By default the query
limit covers the last item requested by the Range header, including later pages. Do not assume an empty
or short page proves a complete historical export without checking your deployment.

## Completed evaluation answers and comments

An evaluation summary is not a question-level answer export. A form definition
contains questions/options, not necessarily the selected answers for a contact.
There is no hardcoded, guessed `/answers` or comments endpoint in this package.

Once your deployment's exact GET resource is verified, use `get_resource(path)` or
supply `extra_resources` to include it in the bundle. For example, with
`verified_answer_path` and `verified_comment_path` supplied privately at runtime:

```python
with CalabrioClient.from_env(api="classic") as client:
    folder = client.export_call(
        123456, "exports", include_transcript=True,
        extra_resources={
            "evaluation-answers": verified_answer_path,
            "evaluation-comments": verified_comment_path,
        },
    )
```

Paths must be local `/api/rest/recording/...` or `/api/rest/cas/...` resources.
External URLs, encoded paths, traversal and query strings are rejected. Resource
references from server responses receive the same checks. The client does not probe
for undocumented endpoints. A successful response is preserved without interpreting
it as proof of complete evaluation answers.

## Sessions and private certificate authorities

The `CalabrioClient` username/password constructor logs in immediately; the context
manager logs out the session it created. Call `close()` if you do not use a context manager.
The advanced `ClassicClient.connect()` API is preserved.
`ClassicClient(base_url, session_id=...)` borrows an existing session and only closes
local connections on exit. Credentials are not kept for automatic reauthentication.
A failed logout does not hide an exception already raised inside the context.

For an on-premises server with a private CA, use a verified SSL context:

```python
import ssl
from calabrio_one import CalabrioClient

context = ssl.create_default_context(cafile="/path/to/private-ca.pem")
with CalabrioClient.from_env(api="classic", verify=context) as client:
    contact = client.get_contact(123456)
```

For an explicit bypass, use `CalabrioClient.from_env(api="classic", verify=False)`.
This emits `InsecureTLSWarning` and disables certificate/hostname checks for that
client. HTTPS remains encrypted, but an impersonated server could receive your
credentials and call data. Prefer the trusted-CA context above. The default is
`verify=True`; failed verification never triggers an automatic retry without it.

Redirects are rejected and environment proxies are not inherited. Exceptions omit
response bodies and credentials. Application HTTP logging can still expose sensitive
details, so configure it appropriately.

## Public source and compatibility

Routes and protocol fields were checked against the official
[Cisco Webex WFO API Reference Guide for Classic WFM](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/cust_contact/contact_center/workforce_optimization/Webex_WFO/webex-wfo-api-ref.pdf)
(updated January 17, 2025): authorization, contact search, evaluation forms,
single-contact export, and transcript export sections. The transcript operation
uses PUT `/api/rest/cas/speechtextview` with `ccrid` and `isRootRecording`.

These are reference-backed implementations with synthetic tests, not a guarantee
of compatibility with every Calabrio Classic version. No live tenant calls were made.
Question-level answers, version-specific comments and server bulk reporting still
need independently verified contracts before dedicated methods can be added.

For direct metadata and QA reads, use `client.get_metadata(contact_id)` and
`client.get_evaluation(contact_id)`. The latter returns a dictionary with `summary`
and `form`, resolving the form automatically. Missing values are `None`.
