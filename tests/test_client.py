import base64
import inspect
import json
from datetime import date
from uuid import UUID

import httpx
import pytest

from calabrio_one import (
    APIError,
    AuthenticationError,
    CalabrioClient,
    OperationError,
    PermissionDeniedError,
    RateLimitError,
    ResponseError,
    TransportError,
)
from calabrio_one.endpoints import WFMEndpoints


@pytest.fixture
def factory():
    clients = []

    def make(handler, **kwargs):
        client = CalabrioClient(
            "https://tenant.example.com/api",
            "synthetic-token",
            transport=httpx.MockTransport(handler),
            **kwargs,
        )
        clients.append(client)
        return client

    yield make
    for client in clients:
        client.close()


def test_simple_call(factory):
    def handler(request):
        assert (
            str(request.url) == "https://tenant.example.com/api/query/BusinessUnit/AllBusinessUnits"
        )
        assert request.headers["Authorization"] == "Bearer synthetic-token"
        assert json.loads(request.content) == {}
        return httpx.Response(200, json={"Result": [{"Id": "synthetic-unit"}], "Errors": []})

    assert factory(handler).all_business_units()["Result"][0]["Id"] == "synthetic-unit"


def test_payload_mapping_and_special_types(factory):
    person = UUID("00000000-0000-0000-0000-000000000001")

    def handler(request):
        assert json.loads(request.content) == {
            "PersonId": str(person),
            "Period": {"StartDate": "2026-01-01", "EndDate": "2026-01-02"},
        }
        return httpx.Response(200, json={"Result": []})

    factory(handler).schedule_by_person_id(
        person_id=person,
        period={"StartDate": date(2026, 1, 1), "EndDate": date(2026, 1, 2)},
    )


def test_inherited_fields_and_explicit_null(factory):
    def handler(request):
        assert json.loads(request.content) == {"BusinessUnitId": "synthetic-unit", "Date": None}
        return httpx.Response(200, json={})

    factory(handler).people_by_business_unit_id(business_unit_id="synthetic-unit", date=None)


def test_raw_payload_and_new_endpoint(factory):
    def handler(request):
        assert json.loads(request.content) == {"NewField": 1}
        return httpx.Response(204)

    client = factory(handler)
    assert client.all_business_units({"NewField": 1}) is None
    assert client.request("query/Future/Operation", {"NewField": 1}) is None


@pytest.mark.parametrize(
    "code,error",
    [
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (429, RateLimitError),
        (400, APIError),
        (500, APIError),
        (302, APIError),
    ],
)
def test_errors_no_retries_or_leaks(factory, code, error):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(
            code,
            text="synthetic-private-response",
            headers={
                "Location": "https://other.example.com/",
            },
        )

    with pytest.raises(error) as caught:
        factory(handler).all_business_units()
    assert len(requests) == 1
    assert caught.value.status_code == code
    assert "synthetic" not in str(caught.value)


def test_transport_error(factory):
    def handler(request):
        raise httpx.ReadTimeout("synthetic-private-value", request=request)

    with pytest.raises(TransportError) as caught:
        factory(handler).all_business_units()
    assert "synthetic" not in str(caught.value)
    assert caught.value.__suppress_context__


@pytest.mark.parametrize(
    "response,error",
    [
        (httpx.Response(200, text="<html>not json</html>"), ResponseError),
        (
            httpx.Response(200, json={"Errors": [{"Message": "synthetic-private-value"}]}),
            OperationError,
        ),
    ],
)
def test_bad_response(factory, response, error):
    with pytest.raises(error) as caught:
        factory(lambda r: response).all_business_units()
    assert "synthetic" not in str(caught.value)


@pytest.mark.parametrize(
    "path",
    [
        "https://other.example.com/api",
        "//other.example.com",
        "../query/Test",
        "query/../command/Test",
        "query/Test?token=x",
        "query/%2e%2e",
        "query/Test#fragment",
    ],
)
def test_path_escape_blocked(factory, path):
    with pytest.raises(ValueError):
        factory(lambda r: pytest.fail("Must not send request")).request(path)


@pytest.mark.parametrize(
    "url",
    [
        "http://tenant.example.com/api",
        "https://user:pass@tenant.example.com/api",
        "https://tenant.example.com/api?token=x",
        "https://tenant.example.com/api#fragment",
        "https://",
        "https://tenant.example.com:bad",
    ],
)
def test_invalid_base_url(url):
    with pytest.raises(ValueError):
        CalabrioClient(url, "synthetic-token")


def test_basic_auth(factory):
    def handler(request):
        expected = base64.b64encode(b"__token__:synthetic-token").decode()
        assert request.headers["Authorization"] == f"Basic {expected}"
        return httpx.Response(200, json={})

    factory(handler, auth_mode="basic").all_business_units()


def test_bad_arguments(factory):
    client = factory(lambda r: pytest.fail("Must not send request"))
    with pytest.raises(TypeError):
        client.all_business_units(typo=True)
    with pytest.raises(TypeError):
        client.people_by_ids({}, ids=[])
    with pytest.raises(TypeError):
        client.all_business_units([])
    with pytest.raises(ValueError):
        client.request("query/Test", {"number": float("nan")})


def test_environment_and_close(monkeypatch):
    monkeypatch.delenv("CALABRIO_BASE_URL", raising=False)
    monkeypatch.delenv("CALABRIO_TOKEN", raising=False)
    with pytest.raises(ValueError):
        CalabrioClient.from_env()
    monkeypatch.setenv("CALABRIO_BASE_URL", "https://tenant.example.com/api")
    monkeypatch.setenv("CALABRIO_TOKEN", "synthetic-token")
    with CalabrioClient.from_env(
        transport=httpx.MockTransport(lambda r: httpx.Response(200, json={}))
    ) as client:
        assert client.all_business_units() == {}
        assert "synthetic-token" not in repr(client)
    assert client._http.is_closed


METHODS = [
    name
    for name, method in inspect.getmembers(WFMEndpoints, inspect.isfunction)
    if not name.startswith("_")
]


def test_expected_coverage():
    assert len(METHODS) == 111


def test_command_routes_without_retries(factory):
    requests = []

    def handler(request):
        requests.append(request)
        assert request.url.path == "/api/command/AddFullDayAbsence"
        assert json.loads(request.content) == {"PersonId": "synthetic-person"}
        return httpx.Response(503)

    with pytest.raises(APIError):
        factory(handler).add_full_day_absence(person_id="synthetic-person")
    assert len(requests) == 1


@pytest.mark.parametrize("timeout", [True, None, "30", -1, float("inf"), float("nan")])
def test_invalid_timeout(timeout):
    with pytest.raises(ValueError):
        CalabrioClient("https://tenant.example.com/api", "synthetic-token", timeout=timeout)


@pytest.mark.parametrize("token", [None, 123, "", "contains space", "line\nbreak"])
def test_invalid_token(token):
    with pytest.raises(ValueError):
        CalabrioClient("https://tenant.example.com/api", token)


def test_wfm_private_ca_context_and_close():
    import ssl

    with CalabrioClient(
        "https://tenant.example.com/api", "synthetic-token", verify=ssl.create_default_context()
    ) as client:
        assert not client._http.is_closed
    assert "Authorization" not in client._http.headers


def test_classic_style_error_body_is_sanitized(factory):
    with pytest.raises(OperationError) as caught:
        factory(
            lambda r: httpx.Response(200, json={"errorMessage": "synthetic-private-value"})
        ).all_business_units()
    assert "synthetic" not in str(caught.value)


def test_nested_python_fields_are_converted_without_mutating_input(factory):
    period = {"start_date": date(2026, 1, 1), "end_date": None}

    def handler(request):
        assert json.loads(request.content) == {
            "PersonId": "synthetic-person",
            "Period": {"StartDate": "2026-01-01", "EndDate": None},
        }
        return httpx.Response(200, json={"Result": []})

    factory(handler).schedule_by_person_id(person_id="synthetic-person", period=period)
    assert period == {"start_date": date(2026, 1, 1), "end_date": None}


@pytest.mark.parametrize(
    "period",
    [
        {"start_date": "2026-01-01", "StartDate": "2026-01-02"},
        {"unknown_field": "2026-01-01"},
    ],
)
def test_invalid_nested_fields_fail_before_request(factory, period):
    with pytest.raises(TypeError):
        factory(lambda r: pytest.fail("Must not send")).schedule_by_person_id(period=period)


def test_raw_payload_retains_original_nested_spelling(factory):
    payload = {"PersonId": "synthetic-person", "Period": {"custom_future_field": True}}

    def handler(request):
        assert json.loads(request.content) == payload
        return httpx.Response(200, json={})

    factory(handler).schedule_by_person_id(payload=payload)


def test_all_wfm_arguments_visible_in_signature():
    for name, method in inspect.getmembers(WFMEndpoints, inspect.isfunction):
        if name.startswith("_"):
            continue
        params = inspect.signature(method).parameters
        assert not any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()), name
    assert "person_id" in inspect.signature(WFMEndpoints.schedule_by_person_id).parameters
    assert "period" in inspect.signature(WFMEndpoints.schedule_by_person_id).parameters
