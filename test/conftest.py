import os
from collections import OrderedDict
from typing import List

from pytest import fixture

from ostrom.domain import UserAddress, Tariff, LocationPrice


@fixture(scope='module')
def location_prices_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices.csv')
    yield file_path


@fixture(scope='module')
def location_prices_small_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices_small.csv')
    yield file_path

@fixture
def consumer_with_one_match():
    # 16932,Börgelingstadt,Am Neuenhof,4-10,1.76,4.15,0.67
    # 1.76 + 4.15 + (0.67 * 1500)
    return UserAddress(
        postal_code=16932,
        city='Börgelingstadt',
        street='Am Neuenhof',
        house_number=5,
        yearly_kwh_consumption=1500
    )


@fixture
def consumer_with_two_matches():
    # postal_code,city,street,house_number,unit_price,grid_fees,kwh_price
    # 01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.45
    # ((4.79+3.19+(0.45*1000)) + (4.79+3.19+(0.30*1000)))/2 = 382.98
    return UserAddress(
        postal_code=1847,
        city='Eliahscheid',
        house_number=816,
        street='Alt Steinbücheler Weg',
        yearly_kwh_consumption=1000
    )


@fixture
def consumer_with_no_matches():
    return UserAddress(
        postal_code=0,
        city='Irgendwo',
        house_number=9999,
        street='Zum Nichts Weg',
        yearly_kwh_consumption=1
    )


@fixture
def location_prices() -> List[LocationPrice]:
    # 01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.45
    # 01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.30
    return [
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.45

        ),
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.30

        ),
        # 16932,Börgelingstadt,Am Neuenhof,4-10,1.76,4.15,0.67
        LocationPrice(
            postal_code=16932,
            city='Börgelingstadt',
            street='Am Neuenhof',
            house_number='4-10',
            unit_price=1.76,
            grid_fees=4.15,
            kwh_price=0.67
        )
    ]


@fixture
def location_price_matching_user_with_one_match():
    return LocationPrice(
            postal_code=16932,
            city='Börgelingstadt',
            street='Am Neuenhof',
            house_number='4-10',
            unit_price=1.76,
            grid_fees=4.15,
            kwh_price=0.67
        )


@fixture
def location_prices_matches_for_user_with_two_matches():
    return [
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.45),
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.30

        )]


@fixture
def location_prices_with_same_postal_code():
    return [
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.45),
        LocationPrice(
            postal_code=1847,
            city='Eliahscheid',
            street='Alt Steinbücheler Weg',
            house_number='814-849',
            unit_price=4.79,
            grid_fees=3.19,
            kwh_price=0.30

        )]
