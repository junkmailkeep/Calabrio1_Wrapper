from calabrio_one._arguments import normalize


def test_recursive_lists_preserve_arbitrary_dictionary_keys():
    schemas = {
        "Record": {
            "properties": {
                "ChildRecords": {"type": "array", "items": {"$ref": "#/components/schemas/Record"}},
                "CustomFields": {"type": "object", "additionalProperties": True},
                "Enabled": {"type": "boolean"},
            },
            "additionalProperties": False,
        }
    }
    source = {"child_records": [{"enabled": False, "custom_fields": {"my_custom_key": 0}}]}
    actual = normalize(source, {"$ref": "#/components/schemas/Record"}, schemas)
    assert actual == {"ChildRecords": [{"Enabled": False, "CustomFields": {"my_custom_key": 0}}]}
    assert "child_records" in source


def test_dictionary_values_with_declared_schema():
    schema = {
        "type": "object",
        "additionalProperties": {
            "type": "object",
            "properties": {"StartDate": {"type": "string"}},
        },
    }
    assert normalize({"my_key": {"start_date": "2026-01-01"}}, schema, {}) == {
        "my_key": {"StartDate": "2026-01-01"},
    }
