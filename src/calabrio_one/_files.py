"""Private, atomic, no-overwrite JSON exports."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def destination_path(destination: str | Path) -> Path:
    path = Path(destination)
    if path.exists() or path.is_symlink():
        raise FileExistsError("Destination already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_json(value: Any, destination: Path) -> Path:
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent, prefix=".calabrio-", delete=False
        ) as output:
            temp_path = Path(output.name)
            json.dump(value, output, ensure_ascii=False, indent=2, allow_nan=False)
            output.write("\n")
        os.link(temp_path, destination)
        return destination
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
