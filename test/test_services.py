import math

import pytest

from ostrom.domain import UserAddress
from ostrom.services import ProviderPricesService, PriceCalculatorService

from pytest import fixture


@fixture(scope='module')
def provider_prices_service():
    yield ProviderPricesService()


@fixture(scope='module')
def provider_prices_service_populated(location_prices_small_file_path):
    provider = ProviderPricesService()
    provider.load_prices_from_csv_local_file(location_prices_small_file_path)
    yield provider


@fixture(scope='module')
def price_calculator(provider_prices_service_populated):
    yield PriceCalculatorService(provider_prices_service_populated)


class TestProviderPricesService:

    def test_load_prices_from_csv_local_file(self, provider_prices_service, location_prices_small_file_path):
        provider_prices_service.load_prices_from_csv_local_file(location_prices_small_file_path)
        assert len(provider_prices_service.get_providers_prices()) == 18


class TestPriceCalculatorService:

    # 16932,Börgelingstadt,Am Neuenhof,4-10,1.76,4.15,0.67
    # 1.76 + 4.15 + (0.67 * 1500)
    consumer1 = UserAddress(
        postal_code=16932,
        city='Börgelingstadt',
        street='Am Neuenhof',
        house_number=5,
        yearly_kwh_consumption=1500
    )

    # postal_code,city,street,house_number,unit_price,grid_fees,kwh_price
    # 01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.45
    # ((4.79+3.19+(0.45*1000)) + (4.79+3.19+(0.30*1000)))/2 = 382.98
    consumer2 = UserAddress(
        postal_code=int('01847'),
        city='Eliahscheid',
        house_number=816,
        street='Alt Steinbücheler Weg',
        yearly_kwh_consumption=1000
    )

    @pytest.mark.parametrize('consumer, expected_price', [(consumer1, 1010.9100000000001)])
    def test_calculate_price_one_match(self, consumer, expected_price, price_calculator):

        price = price_calculator.calculate_price(consumer)
        assert price.total_price == expected_price, 2

    @pytest.mark.parametrize('consumer, expected_price', [(consumer2, 382.98)])
    def test_calculate_price_two_matches(self,  consumer, expected_price, price_calculator):
        price = price_calculator.calculate_price(consumer)
        assert price.total_price == expected_price


