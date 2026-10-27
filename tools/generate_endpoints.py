"""Generate typed, named WFM methods from a reviewed public OpenAPI JSON file.

Only structural API identifiers/types are emitted; never servers, descriptions,
examples or defaults. Review identifiers too before publishing.
"""

from __future__ import annotations

import argparse
import keyword
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def snake(value: str) -> str:
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower()


def alias(value: str) -> str:
    result = snake(value)
    return result + "_" if result in {"self", "payload"} or keyword.iskeyword(result) else result


def generate(schema: dict, root: Path = ROOT) -> None:
    definitions = schema.get("components", {}).get("schemas", {})
    registry: dict[str, dict] = {}

    def resolve(node: dict, stack: tuple[str, ...] = ()) -> dict:
        result: dict[str, Any] = {}
        bases = []
        if "$ref" in node:
            ref = node["$ref"]
            if not ref.startswith("#/components/schemas/") or ref in stack:
                raise ValueError("Expected a non-circular local schema reference")
            bases.append(resolve(definitions[ref.rsplit("/", 1)[1]], (*stack, ref)))
        bases.extend(resolve(part, stack) for part in node.get("allOf", []))
        bases.append({key: value for key, value in node.items() if key not in {"$ref", "allOf"}})
        for part in bases:
            for key, value in part.items():
                if key == "properties":
                    result.setdefault(key, {}).update(value)
                elif key == "required":
                    result[key] = sorted(set(result.get(key, [])) | set(value))
                else:
                    result[key] = value
        return result

    def clean(node: dict) -> dict:
        if "$ref" in node:
            ref = node["$ref"]
            if not re.fullmatch(r"#/components/schemas/[A-Za-z0-9_]+", ref):
                raise ValueError("Expected a local schema reference")
            name = ref.rsplit("/", 1)[1]
            if name not in registry:
                registry[name] = {}  # Allow recursive object fields, unlike inheritance cycles.
                registry[name] = clean(resolve(definitions[name]))
            return {"$ref": ref, **({"nullable": True} if node.get("nullable") else {})}
        node = resolve(node)
        result = {
            key: node[key] for key in ("type", "format", "nullable", "required") if key in node
        }
        if "properties" in node:
            fields = node["properties"]
            seen = set()
            for name in fields:
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name) or alias(name) in seen:
                    raise ValueError("Invalid field identifier or conflicting Python field aliases")
                seen.add(alias(name))
            result["properties"] = {name: clean(value) for name, value in fields.items()}
        if "items" in node:
            result["items"] = clean(node["items"])
        if "additionalProperties" in node:
            value = node["additionalProperties"]
            result["additionalProperties"] = clean(value) if isinstance(value, dict) else value
        return result

    def annotation(node: dict) -> str:
        node = resolve(node)
        kind = node.get("type")
        if kind == "string":
            value = {
                "date": "str | date",
                "date-time": "str | datetime",
                "guid": "str | UUID",
                "uuid": "str | UUID",
            }.get(node.get("format", ""), "str")
        elif kind == "integer":
            value = "int"
        elif kind == "number":
            value = "float"
        elif kind == "boolean":
            value = "bool"
        elif kind == "array":
            value = "list[Any]"
        elif kind == "object" or "properties" in node:
            value = "dict[str, Any]"
        else:
            value = "Any"
        return value + (" | None" if node.get("nullable") else "")

    def nested_rows(node: dict, prefix: str, visited: tuple[str, ...] = ()) -> list[str]:
        if "$ref" in node:
            ref = node["$ref"]
            if ref in visited:
                return []
            visited = (*visited, ref)
        node = resolve(node)
        if "items" in node:
            return nested_rows(node["items"], prefix + "[]", visited)
        rows = []
        for name, child in node.get("properties", {}).items():
            field = prefix + "." + alias(name)
            required = "Yes" if name in node.get("required", []) else "No"
            rows.append(f"| `{field}` | `{annotation(child).replace('|', '/')}` | {required} |")
            rows.extend(nested_rows(child, field, visited))
        return rows

    operations = []
    seen = {
        "request",
        "close",
        "from_env",
        "get_contact",
        "get_metadata",
        "get_transcript",
        "get_evaluation",
        "get_evaluation_form",
        "list_evaluation_forms",
        "get_resource",
        "search_contacts",
        "download_recording",
        "export_recording",
        "export_call",
        "export_calls",
        "export_contact",
        "export_metadata",
        "export_transcript",
        "export_evaluation",
        "export_by_date",
    }
    for path, methods in sorted(schema["paths"].items()):
        if not re.fullmatch(r"/(?:query|command)/[A-Za-z0-9_]+(?:/[A-Za-z0-9_]+)*", path):
            raise ValueError("Expected a WFM query/command route")
        if set(methods) != {"post"}:
            raise ValueError("Expected POST-only WFM operations")
        method = snake(path.rsplit("/", 1)[1])
        if method in seen or not method.isidentifier() or keyword.iskeyword(method):
            raise ValueError("Duplicate, reserved or invalid method")
        seen.add(method)
        request = resolve(methods["post"]["requestBody"]["content"]["application/json"]["schema"])
        normalized = clean(request)
        operations.append((path, method, request, normalized))
    if not operations:
        raise ValueError("Schema contains no operations")

    lines = [
        '"""Generated typed WFM methods. See tools/generate_endpoints.py."""',
        "from abc import ABC, abstractmethod",
        "from datetime import date, datetime  # noqa: F401",
        "from typing import Any",
        "from uuid import UUID  # noqa: F401",
        "",
        "from calabrio_one._arguments import UNSET, Unset",
        "",
        "",
        "class WFMEndpoints(ABC):",
        '    """One named method per public WFM operation; no raw payload required."""',
        f"    _wfm_schemas: dict = {registry!r}",
        f"    _wfm_requests: dict = { {path: node for path, _, _, node in operations}!r}",
        "",
        "    @abstractmethod",
        "    def _operation(self, path: str, names: dict, payload: dict | None, kwargs: dict) -> Any:",
        '        """Dispatch supplied API fields through the implementing client."""',
        "        ...",
        "",
    ]
    docs = [
        "# WFM method reference",
        "",
        f"All {len(operations)} operations in the reviewed public schema use named Python arguments.",
        "Use `client.method(field=value)`; autocomplete/help shows every field and type.",
        "Nested dictionaries accept snake_case or original API field names. Omitted values",
        "are not sent; `None` sends JSON null. UNSET is internal: do not pass it yourself.",
        "Required fields below come from the schema; complete server validation still applies.",
        "A raw API dictionary remains available as `payload={...}` (or the first positional argument).",
        "Raw payloads are passed unchanged; do not mix them with named fields.",
        "",
        "Responses preserve the server JSON/envelope. Commands change data and are never retried.",
        "",
        "## Methods",
        "",
        "| Method | Endpoint | Kind |",
        "| --- | --- | --- |",
    ]
    for path, method, _, _ in operations:
        docs.append(
            f"| [{method}](#{method.replace('_', '-')}) | `{path}` | {'Write' if path.startswith('/command/') else 'Read'} |"
        )
    for path, method, request, _ in operations:
        fields = request.get("properties", {})
        names = {alias(name): name for name in fields}
        lines += [
            f"    def {method}(",
            "        self,",
            "        payload: dict[str, Any] | None = None,",
        ]
        if fields:
            lines.append("        *,")
        for name, node in fields.items():
            lines.append(f"        {alias(name)}: {annotation(node)} | Unset = UNSET,")
        lines += [
            "    ) -> Any:",
            f'        """{"Write" if path.startswith("/command/") else "Read"} operation: {path}.',
            "",
            "        Named fields use snake_case, including nested dictionaries.",
            "        Omitted values are not sent; explicit None sends null.",
            "        Returns the server JSON response unchanged.",
            '        """',
        ]
        values = ", ".join(f"{key!r}: {key}" for key in names)
        lines += [
            f"        values: dict[str, Any] = {{{values}}}",
            "        supplied = {key: value for key, value in values.items() if value is not UNSET}",
            f"        return self._operation({path!r}, {names!r}, payload, supplied)",
            "",
        ]
        docs += ["", f"## {method.replace('_', ' ')}", "", f"`{path}`", ""]
        args = ", ".join(f"{name}=..." for name in names)
        docs += ["```python", f"client.{method}({args})", "```", ""]
        if fields:
            docs += ["| Argument | Accepted type | Required by API |", "| --- | --- | --- |"]
            for name, node in fields.items():
                docs.append(
                    f"| `{alias(name)}` | `{annotation(node).replace('|', '/')}` | {'Yes' if name in request.get('required', []) else 'No'} |"
                )
            nested = []
            for name, node in fields.items():
                nested.extend(nested_rows(node, alias(name)))
            if nested:
                docs += [
                    "",
                    "Nested dictionary/list fields (use these snake_case names):",
                    "",
                    "| Field | Accepted type | Required by API |",
                    "| --- | --- | --- |",
                    *nested,
                ]
        else:
            docs.append("No arguments needed.")
    code = "\n".join(lines)
    compile(code, "generated endpoints", "exec")
    (root / "src/calabrio_one/endpoints.py").write_text(code, encoding="utf-8")
    (root / "docs/endpoints.md").write_text("\n".join(docs) + "\n", encoding="utf-8")
    print(f"Generated {len(operations)} typed methods")


if __name__ == "__main__":
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path)
    generate(json.loads(parser.parse_args().schema.read_text(encoding="utf-8")))
