"""Simple recording API example. Replace the fictional connection settings first.

Install the package, then run: python examples/quickstart.py
No API calls happen when this file is imported.
"""

from calabrio_one import CalabrioClient


def main() -> None:
    # url: your HTTPS server origin, without /api.
    # username/password: your API account credentials. Keep real credentials private.
    # Construction logs in automatically. You can also use environment variables:
    # client = CalabrioClient.from_env(api="classic")
    client = CalabrioClient(
        url="https://your-calabrio-server.example.com",
        username="api_user",
        password="replace-with-your-password",
        # verify=False,  # Explicit bypass: skips server identity checks and warns.
        # Prefer a trusted SSLContext; see the README's certificate example.
    )

    try:
        # ONE contact ID can be an int (123456) or a numeric string ("123456").
        contact_id = 123456

        # Returns the contact information as a Python dictionary.
        contact = client.get_contact(contact_id)

        # Returns the call's metadata, fetching linked data for you.
        # Returns None if this contact has no metadata.
        metadata = client.get_metadata(contact_id)

        # Returns transcript JSON. Requires transcript support and permission.
        transcript = client.get_transcript(contact_id)

        # Returns {"summary": ..., "form": ...}; either value may be None.
        # The form defines questions/options; it is not the selected answers.
        evaluation = client.get_evaluation(contact_id)

        # Prepares the audio, waits for it, and saves the file. No extra setup call.
        # The second argument is a FILE path (str or pathlib.Path).
        # Existing files are never overwritten. Returns the saved file's Path.
        recording = client.download_recording(contact_id, "recording.wav")
        print(f"Recording saved: {recording}")

        # These variables are ready to use in your own program; not saved to disk.
        # For example: contact["id"] or evaluation["summary"].
        # Do not paste real contact data into public issues or source files.
        _ = contact, metadata, transcript, evaluation

        # To save individual JSON files instead of handling the returned data:
        # client.export_contact(contact_id, "contact.json")
        # client.export_metadata(contact_id, "metadata.json")
        # client.export_transcript(contact_id, "transcript.json")
        # client.export_evaluation(contact_id, "evaluation.json")

        # Other direct methods:
        # page = client.search_contacts(begin_date="2026-01-01", end_date="2026-01-08")
        # forms = client.list_evaluation_forms()
        # form = client.get_evaluation_form(7)  # Form ID, not contact ID.

        # To save everything in one folder instead, use:
        # client.export_call(123456, "exports", include_transcript=True)

        # For MULTIPLE calls with the same options, pass a LIST of IDs:
        # client.export_calls([123456, "123457"], "exports", include_transcript=True)

        # For different options per call, loop over a DICTIONARY:
        # jobs = {123456: {"include_transcript": True}, 123457: {"include_transcript": False}}
        # for call_id, options in jobs.items():
        #     client.export_call(call_id, "exports", **options)
    finally:
        # Always log out, including if a call fails.
        # A `with CalabrioClient(...) as client:` block handles this automatically.
        client.close()


if __name__ == "__main__":
    main()
