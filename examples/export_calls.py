"""Export only what you need, using credentials from environment variables.

Run from the repository after installing the package:
    python examples/export_calls.py --kind call --ids 123456 123457 --transcript
    python examples/export_calls.py --kind recording --ids 123456
    python examples/export_calls.py --kind transcript --ids 123456 123457
    python examples/export_calls.py --kind evaluation --ids 123456

All IDs above are fictional. Replace them with your contact IDs.
Set CALABRIO_CLASSIC_URL, CALABRIO_USERNAME and CALABRIO_PASSWORD first.
Existing files/folders are never overwritten. No API calls happen on import.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from calabrio_one import CalabrioClient, CalabrioError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--kind",
        choices=["call", "recording", "transcript", "evaluation"],
        required=True,
        help="Which data to export",
    )
    # nargs='+' accepts one OR several IDs, always returning a list of strings.
    # Python callers can instead use a list of ints: [123456, 123457].
    parser.add_argument("--ids", nargs="+", required=True, help="One or more numeric contact IDs")
    parser.add_argument("--output", type=Path, default=Path("exports"), help="Output directory")
    parser.add_argument(
        "--transcript",
        action="store_true",
        help="Include transcripts in a full call bundle (--kind call only)",
    )
    parser.add_argument(
        "--format",
        choices=["WAV", "OPUS", "WEBM", "WEBM_VP8", "WEBM_VP9"],
        default="WAV",
        help="Recording format (call/recording only)",
    )
    args = parser.parse_args(argv)
    if any(not contact_id.isascii() or not contact_id.isdecimal() for contact_id in args.ids):
        parser.error("Each contact ID must contain decimal digits only")
    if args.transcript and args.kind != "call":
        parser.error("--transcript is only used with --kind call")
    if args.format != "WAV" and args.kind not in {"call", "recording"}:
        parser.error("--format is only used with --kind call or recording")

    try:
        # from_env logs in using the three environment variables listed above.
        # timeout=30 is the HTTP inactivity timeout, in seconds.
        # Leaving this block logs out and closes connections, even after an error.
        with CalabrioClient.from_env(api="classic", timeout=30) as client:
            for contact_id in args.ids:
                if args.kind == "call":
                    # export_call takes ONE int/numeric str plus an output DIRECTORY.
                    # Creates output/contact_id/ with media, metadata and QA files.
                    # include_transcript: bool, default False; requires transcript access.
                    # include_evaluation: bool, default True; includes summary/form.
                    # media_format: one of the --format choices above.
                    # wait_timeout: conversion/download polling budget in seconds.
                    # poll_interval: seconds between pending download checks.
                    result = client.export_call(
                        contact_id,
                        args.output,
                        include_transcript=args.transcript,
                        include_evaluation=True,
                        media_format=args.format,
                        wait_timeout=120,
                        poll_interval=2,
                    )
                elif args.kind == "recording":
                    # download_recording takes ONE ID and a destination FILE path.
                    # Downloads media only; metadata/transcripts/QA are not requested.
                    extension = "webm" if args.format.startswith("WEBM") else args.format.lower()
                    result = client.download_recording(
                        contact_id,
                        args.output / f"{contact_id}.{extension}",
                        media_format=args.format,
                    )
                elif args.kind == "transcript":
                    # export_transcript fetches and saves JSON in ONE method call.
                    # is_root_recording=False selects the agent-associated recording.
                    result = client.export_transcript(
                        contact_id,
                        args.output / f"{contact_id}-transcript.json",
                    )
                else:
                    # export_evaluation saves a QA summary/form without downloading audio.
                    result = client.export_evaluation(
                        contact_id,
                        args.output / f"{contact_id}-evaluation.json",
                    )
                print(f"Saved: {result}")
    except (CalabrioError, OSError, ValueError) as error:
        # Stop at the first failure. Earlier successful exports are kept.
        # Do not print raw API responses or credentials in shared logs.
        print(f"Export stopped: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
