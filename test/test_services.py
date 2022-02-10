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

    def test_calculate_price_one_match(self, consumer1, price_calculator):
        price = price_calculator.calculate_price(consumer1)
        assert price.total_price == 1010.9100000000001

    def test_calculate_price_two_matches(self,  consumer2,  price_calculator):
        price = price_calculator.calculate_price(consumer2)
        assert price.total_price == 382.98


