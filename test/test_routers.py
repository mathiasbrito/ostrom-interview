import pytest
from fastapi.exceptions import RequestValidationError

from fastapi.testclient import TestClient

from ostrom.routers import tariff_router
from pytest import fixture


@fixture(scope='module')
def api_test_client():
    yield TestClient(tariff_router)


@pytest.mark.parametrize('user_consumption', [
    ({}), ({'zip_code': 12345}), ({'zip_code': '12345'}, {'zip_code': '12345',  'street': 'some'}),
    ({'zip_code': 12345, 'street': 'some', 'city': 'some_city', 'house_number': '34'}),
    ({'zip_code': 12345, 'street': 'some', 'city': 'some_city', 'house_number': '34', 'yearly_kwh_consumption': 'somestr'})
])
def test_location_must_be_ignored_if_schema_do_not_match(user_consumption, api_test_client):
    with pytest.raises(RequestValidationError):
        result = api_test_client.post('/tariffs', json=user_consumption)
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

