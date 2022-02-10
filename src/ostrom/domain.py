from pydantic import BaseModel


class Tariff(BaseModel):
    unit_price: float
    grid_fees: float
    kwh_price: float
    total_price: float


class UserAddress(BaseModel):
    postal_code: int = ...
    city: str = ...
    street: str = ...
    house_number: int = ...
    yearly_kwh_consumption: int

    def in_range(self, start, end):
        if start <= self.house_number <= end:
            return True
        return False


class LocationPrice(BaseModel):
    postal_code: int = ...
    city: str = ...
    street: str = ...
    house_number: str = ...
    unit_price: float
    grid_fees: float
    kwh_price: float

    def get_range(self) -> (int, int):
        a, b = self.house_number.split('-')
        return int(a), int(b)



