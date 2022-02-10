import csv
import os.path
from typing import List

from ostrom.domain import LocationPrice, UserAddress, Tariff


class ProviderPricesService:

    provider_prices: List[LocationPrice]

    def __init__(self):
        self._provider_prices = []

    def load_location_prices_from_csv(self, raw_data):
        entries = csv.DictReader(open(raw_data, 'r'))
        for entry in entries:
            if not self.must_reject_location_price(entry):
                self._provider_prices.append(LocationPrice(
                    postal_code=int(entry['postal_code']),
                    city=entry['city'],
                    street=entry['street'],
                    house_number=entry['house_number'],
                    unit_price=float(entry['unit_price']),
                    grid_fees=float(entry['grid_fees']),
                    kwh_price=float(entry['kwh_price'])
                ))

    @staticmethod
    def must_reject_location_price(entry):
        for value in entry.values():
            if value == '':
                return True
        return False

    def load_prices_from_csv_local_file(self, file_path):
        self.load_location_prices_from_csv(file_path)

    def get_providers_prices(self):
        return self._provider_prices

    def add_location_price(self, location_price: LocationPrice):
        self._provider_prices.append(location_price)


class PriceCalculatorService:

    provider_prices: ProviderPricesService

    def __init__(self, provider_prices: ProviderPricesService):
        self.provider_prices = provider_prices

    def calculate_price(self, consumer_address: UserAddress):
        matches = LocationAddressMatchMaker.all_matches(self.provider_prices.get_providers_prices(),
                                                        consumer_address)

        sum_totals = 0
        sum_unit_price = 0
        sum_grid_fees = 0
        sum_kwh_price = 0
        number_of_matches = len(matches)
        for match in matches:
            sum_unit_price += match.unit_price
            sum_grid_fees += match.grid_fees
            sum_kwh_price += match.kwh_price
            sum_totals += self.calculate_per_location_price(match, consumer_address.yearly_kwh_consumption)

        return Tariff(
            unit_price=sum_unit_price/number_of_matches,
            grid_fees=sum_grid_fees/number_of_matches,
            kwh_price=sum_kwh_price/number_of_matches,
            total_price=sum_totals/len(matches)
        )

    @staticmethod
    def calculate_per_location_price(location_price: LocationPrice, consumer_consumption: int):
        return location_price.unit_price + location_price.grid_fees + \
               (consumer_consumption * location_price.kwh_price)


class LocationAddressMatchMaker:

    @staticmethod
    def does_match(provider_location_price: LocationPrice, consumer_address: UserAddress):
        number_start, number_end = provider_location_price.get_range()
        if number_start <= consumer_address.house_number <= number_end\
                and consumer_address.city == provider_location_price.city\
                and consumer_address.street == provider_location_price.street\
                and consumer_address.postal_code == provider_location_price.postal_code:
            return True
        return False

    @staticmethod
    def all_matches(provider_location_prices: List[LocationPrice],
                    consumer_address: UserAddress):
        matches = []
        for location_price in provider_location_prices:
            if LocationAddressMatchMaker.does_match(location_price, consumer_address):
                matches.append(location_price)

        return matches


csv_file = os.path.join(os.path.dirname(__file__), 'data/location_prices.csv')
if os.environ.get('OSTROM_ENV', 'DEVELOPMENT'):
    csv_file = os.path.join(os.path.dirname(__file__), 'data/location_prices_small.csv')
provider_prices_service = ProviderPricesService()
provider_prices_service.load_location_prices_from_csv(csv_file)
price_calculator_service = PriceCalculatorService(provider_prices_service)
