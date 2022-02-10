from pytest import fixture

from ostrom.services import ProviderPricesService, PriceCalculatorService, LocationAddressMatchMaker, \
    ProviderPricesStore


@fixture(scope='function')
def provider_prices_service():
    yield ProviderPricesService()


@fixture(scope='function')
def provider_prices_service_populated(location_prices_small_file_path):
    provider = ProviderPricesService()
    provider.load_prices_from_csv_local_file(location_prices_small_file_path)
    yield provider


@fixture(scope='function')
def price_calculator(provider_prices_service_populated):
    yield PriceCalculatorService(provider_prices_service_populated)


@fixture(scope='function')
def provider_price_store():
    yield ProviderPricesStore()


class TestProviderPricesService:

    def test_load_prices_from_csv_local_file(self, provider_prices_service, location_prices_small_file_path):
        provider_prices_service.load_prices_from_csv_local_file(location_prices_small_file_path)
        assert provider_prices_service.get_providers_prices().number_of_entries() == 18


class TestPriceCalculatorService:

    def test_calculate_price_one_match(self, consumer_with_one_match, price_calculator):
        price = price_calculator.calculate_price(consumer_with_one_match)
        assert price.total_price == 1010.9100000000001

    def test_calculate_price_two_matches(self,  consumer_with_two_matches,  price_calculator):
        price = price_calculator.calculate_price(consumer_with_two_matches)
        assert price.total_price == 382.98

    def test_calculate_per_location_price(self, price_calculator, location_prices, consumer_with_one_match):
        location_price = location_prices[0]
        consumer_consumption = consumer_with_one_match.yearly_kwh_consumption
        expected_from_formula = (location_price.unit_price + location_price.grid_fees +
                                (consumer_consumption * location_price.kwh_price))

        price = price_calculator.calculate_per_location_price(location_price, consumer_consumption)
        assert price == expected_from_formula


class TestLocationAddressMatchMaker:

    def test_does_match(self, consumer_with_one_match,
                        location_price_matching_user_with_one_match):
        result = LocationAddressMatchMaker.does_match(location_price_matching_user_with_one_match,
                                                      consumer_with_one_match)
        assert result is True

    def test_match_all(self, consumer_with_two_matches,
                       location_prices_matches_for_user_with_two_matches):
        matches = LocationAddressMatchMaker.all_matches(location_prices_matches_for_user_with_two_matches,
                                                        consumer_with_two_matches)
        assert len(matches) == 2


class TestProviderPricesStore:

    def test_add_location_price_first_entry_for_postal_code(self, location_prices, provider_price_store):
        location_price = location_prices[0]
        provider_price_store.add(location_price)

        registries_for_given_postal_code = provider_price_store._provider_prices.get(location_price.postal_code)
        assert len(registries_for_given_postal_code) == 1

    def test_add_multiple_location_prices_for_same_postal_code(self, location_prices_with_same_postal_code,
                                                               provider_price_store):
        postal_code = location_prices_with_same_postal_code[1].postal_code
        provider_price_store.add(location_prices_with_same_postal_code[0])
        provider_price_store.add(location_prices_with_same_postal_code[1])

        registries_for_given_postal_code = provider_price_store._provider_prices.get(postal_code)
        assert len(registries_for_given_postal_code) == 2

    def test_number_of_entries(self, location_prices, provider_price_store):
        expected_number_of_entries = len(location_prices)
        for location in location_prices:
            provider_price_store.add(location)

        number_of_entries = provider_price_store.number_of_entries()
        assert number_of_entries == expected_number_of_entries






