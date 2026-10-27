"""Schema-aware argument conversion for generated WFM methods."""

from __future__ import annotations

import keyword
import re
from enum import Enum
from typing import Any


class Unset(Enum):
    VALUE = "unset"

    def __repr__(self) -> str:
        return "UNSET"


UNSET = Unset.VALUE


def python_name(value: str) -> str:
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower()
    if value in {"self", "payload"} or keyword.iskeyword(value):
        value += "_"
    return value


def normalize(value: Any, schema: dict, schemas: dict) -> Any:
    """Translate declared fields only; arbitrary dictionary keys are preserved.

    Explicit null stays null. This translates names, not a full schema validator.
    Unknown properties and duplicate aliases fail before a request is sent.
    """
    if value is None:
        return None
    if "$ref" in schema:
        schema = schemas[schema["$ref"].rsplit("/", 1)[1]]
    if isinstance(value, (list, tuple)) and "items" in schema:
        return [normalize(item, schema["items"], schemas) for item in value]
    if not isinstance(value, dict):
        return value
    properties = schema.get("properties", {})
    aliases = {python_name(name): name for name in properties}
    result = {}
    for key, item in value.items():
        canonical = key if key in properties else aliases.get(key)
        if canonical is None:
            additional = schema.get("additionalProperties", True)
            if additional is False:
                raise TypeError("Unknown nested API field; see the method reference")
            result[key] = (
                normalize(item, additional, schemas) if isinstance(additional, dict) else item
            )
            continue
        if canonical in result:
            raise TypeError("Field supplied twice using different spellings")
        result[canonical] = normalize(item, properties[canonical], schemas)
    return result
