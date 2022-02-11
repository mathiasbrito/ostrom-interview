from fastapi import APIRouter, Response, status

from ostrom.domain import UserAddress, LocationPrice
from ostrom.services import provider_prices_service, price_calculator_service, NoLocationPriceError

tariff_router = APIRouter()


@tariff_router.post('/prices')
async def prices(location_price: LocationPrice):
    provider_prices_service.add_location_price(location_price)


@tariff_router.post('/tariffs')
async def tariff(user_consumption: UserAddress, response: Response):
    try:
        return price_calculator_service.calculate_price(user_consumption)
    except NoLocationPriceError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
