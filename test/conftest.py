import os
from collections import OrderedDict

from pytest import fixture

from ostrom.domain import UserAddress


@fixture(scope='module')
def location_prices_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices.csv')
    yield file_path


@fixture(scope='module')
def location_prices_small_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices_small.csv')
    yield file_path

@fixture
def consumer1():
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
def consumer2():
    # postal_code,city,street,house_number,unit_price,grid_fees,kwh_price
    # 01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.45
    # ((4.79+3.19+(0.45*1000)) + (4.79+3.19+(0.30*1000)))/2 = 382.98
    return UserAddress(
        postal_code=int('01847'),
        city='Eliahscheid',
        house_number=816,
        street='Alt Steinbücheler Weg',
        yearly_kwh_consumption=1000
    )