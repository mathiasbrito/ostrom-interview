from fastapi import APIRouter, File

from ostrom.domain import UserAddress
from ostrom.services import provider_prices_service, price_calculator_service

tariff_router = APIRouter()


@tariff_router.post('/prices')
def prices(file: bytes = File(...)):
    provider_prices_service.load_prices_from_csv(file)


@tariff_router.post('/tariff')
def tariff(user_consumption: UserAddress):
    return price_calculator_service.calculate_price(user_consumption)

