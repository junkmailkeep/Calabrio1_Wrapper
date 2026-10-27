"""Export recordings, transcripts and evaluation summaries/forms for a date range.

Install the package, set CALABRIO_CLASSIC_URL, CALABRIO_USERNAME and
CALABRIO_PASSWORD privately, then run: python examples/export_by_date.py
"""

from calabrio_one import CalabrioClient


def main() -> None:
    with CalabrioClient.from_env(api="classic") as client:
        folders = client.export_by_date(
            # YYYY-MM-DD strings or datetime.date objects. Start is included;
            # end is excluded: this exports calls starting during January.
            begin_date="2026-01-01",
            end_date="2026-02-01",
            # Each matching contact gets its own folder. Existing folders fail.
            output_dir="exports/january",
            # All three default to True. Set False to omit a resource type.
            include_recording=True,
            include_transcript=True,
            include_evaluation=True,
            # Optional time bounds must be supplied together. Server timezone
            # semantics apply; the wrapper does not convert local time to UTC.
            # begin_time="09:00",  # HH:MM, on begin_date
            # end_time="17:00:00",  # HH:MM:SS, on end_date
            # agent_id=7,  # One numeric agent ID, not a list or dictionary.
            # filters={"scored": True},  # Additional documented search filters.
        )
        # Returns a list of pathlib.Path objects; [] means no matches returned.
        print(f"Exported {len(folders)} calls")


if __name__ == "__main__":
    main()
