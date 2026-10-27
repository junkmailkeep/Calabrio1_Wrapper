"""Exercise schema input boundaries using deliberately synthetic schemas."""

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "generator",
    Path(__file__).parents[1] / "tools/generate_endpoints.py",
)
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


@pytest.fixture
def output(tmp_path):
    (tmp_path / "src/calabrio_one").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    return tmp_path


def schema(node):
    return {
        "paths": {
            "/query/Synthetic/Records": {
                "post": {
                    "requestBody": {
                        "content": {"application/json": {"schema": node}},
                    }
                }
            }
        },
        "components": {"schemas": {}},
    }


def test_inheritance_aliases_and_private_fields_not_copied(output):
    data = schema(
        {
            "allOf": [
                {"$ref": "#/components/schemas/Base"},
                {
                    "properties": {
                        "From": {},
                        "Payload": {},
                        "IncludeIDs": {},
                    }
                },
            ]
        }
    )
    data["components"]["schemas"]["Base"] = {"properties": {"BusinessUnitId": {}}}
    data["servers"] = [{"url": "https://synthetic-secret.example.com"}]
    data["description"] = "synthetic-secret-description"
    generator.generate(data, output)
    source = (output / "src/calabrio_one/endpoints.py").read_text()
    docs = (output / "docs/endpoints.md").read_text()
    assert "synthetic-secret" not in source + docs
    scope = {}
    exec(compile(source, "<generated>", "exec"), scope)

    class Client(scope["WFMEndpoints"]):
        def _operation(self, path, names, payload, kwargs):
            return {names[k]: v for k, v in kwargs.items()}

    assert Client().records(business_unit_id="unit", from_="start", payload_={}) == {
        "BusinessUnitId": "unit",
        "From": "start",
        "Payload": {},
    }


@pytest.mark.parametrize("kind", ["alias", "cycle", "external_ref", "route", "field"])
def test_invalid_schema_never_replaces_files(output, kind):
    data = schema({"properties": {"BusinessUnitId": {}}})
    if kind == "alias":
        data = schema({"properties": {"PersonID": {}, "PersonId": {}}})
    elif kind == "cycle":
        data = schema({"$ref": "#/components/schemas/Loop"})
        data["components"]["schemas"]["Loop"] = {"$ref": "#/components/schemas/Loop"}
    elif kind == "external_ref":
        data = schema({"$ref": "https://example.com/schema"})
    elif kind == "route":
        data["paths"]['/query/bad"""'] = data["paths"].pop("/query/Synthetic/Records")
    else:
        data = schema({"properties": {'bad"""': {}}})
    target = output / "src/calabrio_one/endpoints.py"
    target.write_text("keep-existing")
    with pytest.raises(ValueError):
        generator.generate(data, output)
    assert target.read_text() == "keep-existing"
