from fastapi import APIRouter, File

from ostrom.domain import UserAddress, LocationPrice
from ostrom.services import provider_prices_service, price_calculator_service

tariff_router = APIRouter()


@tariff_router.post('/prices')
def prices(location_price: LocationPrice):
    provider_prices_service.add_location_price(location_price)


@tariff_router.post('/tariffs')
def tariff(user_consumption: UserAddress):
    return price_calculator_service.calculate_price(user_consumption)

