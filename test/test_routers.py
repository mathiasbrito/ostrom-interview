import pytest
from fastapi.exceptions import RequestValidationError

from fastapi.testclient import TestClient

from ostrom.domain import Tariff
from ostrom.routers import tariff_router
from pytest import fixture


@fixture(scope='module')
def api_test_client():
    yield TestClient(tariff_router)


def test_location_must_be_ignored_if_any_field_is_empty(api_test_client):
    with pytest.raises(RequestValidationError):
        result = api_test_client.post('/tariffs', json={'zip_code': 12345})
        assert result.status_code == 422


def test_match_location_with_one_match_house_number(api_test_client, consumer_with_one_match):
    result = api_test_client.post('/tariffs', json=consumer_with_one_match.dict())
    assert result.status_code == 200


def test_match_location_with_two_matches_house_number(api_test_client, consumer_with_two_matches):
    result = api_test_client.post('/tariffs', json=consumer_with_two_matches.dict())
    assert result.status_code == 200


def test_match_location_with_no_matches(api_test_client, consumer_with_no_matches):
    result = api_test_client.post('/tariffs', json=consumer_with_no_matches.dict())
    assert result.status_code == 422

