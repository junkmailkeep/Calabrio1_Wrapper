"""WFM queries with explicit Python arguments. Replace fictional settings/IDs first.

Run: python examples/wfm.py
WFM uses an API token, not the recording API's username/password login.
"""

from calabrio_one import CalabrioClient


def main() -> dict:
    client = CalabrioClient(
        url="https://your-calabrio-server.example.com/api",
        token="replace-with-your-personal-access-token",
    )
    try:
        # No arguments needed. Returns server JSON, including its Result envelope.
        business_units = client.all_business_units()

        # WFM IDs are GUID strings or uuid.UUID objects (not numeric contact IDs).
        business_unit_id = "00000000-0000-0000-0000-000000000001"
        person_id = "00000000-0000-0000-0000-000000000002"

        # Each argument is visible in autocomplete/help. Integers stay integers.
        people = client.people_by_business_unit_id(
            business_unit_id=business_unit_id,
            page=1,
            page_size=50,
        )

        # For an API field that takes several IDs, pass a list, even for one ID.
        selected_people = client.people_by_ids(ids=[person_id])

        # Nested dictionaries use the same snake_case style as top-level arguments.
        # Dates accept ISO strings or datetime.date objects.
        schedule = client.schedule_by_person_id(
            person_id=person_id,
            period={"start_date": "2026-01-01", "end_date": "2026-01-07"},
        )

        # Write operations use the same named-argument style. Example only: do not
        # uncomment unless you intend to change data in an authorized test system.
        # client.add_team(
        #     business_unit_id=business_unit_id,
        #     team_name="Example team",
        #     site_id="00000000-0000-0000-0000-000000000003",
        # )

        # Optional arguments can simply be omitted. None means JSON null; it does
        # not mean "leave this field out". No custom payload builder is necessary.
        return {
            "business_units": business_units,
            "people": people,
            "selected_people": selected_people,
            "schedule": schedule,
        }
    finally:
        client.close()


if __name__ == "__main__":
    main()
