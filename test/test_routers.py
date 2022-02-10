import pytest

from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from ostrom.routers import tariff_router
from pytest import fixture


@fixture(scope='module')
def api_test_client():
    yield TestClient(tariff_router)


def test_location_must_be_ignored_if_any_field_is_empty(api_test_client):
    with pytest.raises(RequestValidationError):
        api_test_client.get('/tariff', json={'zip_code': 12345})


def test_match_location_with_one_match_house_number():
    pytest.fail()


def test_match_location_with_two_matches():
    pytest.fail()


def test_price_calculation():
    pytest.fail()


def test_multiple_locations_returns_average_for_all_matches():
    pytest.fail()


def test_load_locations_prices():
    pytest.fail()
