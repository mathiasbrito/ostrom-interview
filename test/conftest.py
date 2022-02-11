import os
from collections import OrderedDict
from typing import List

from pytest import fixture

from ostrom.domain import UserAddress, LocationPrice


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


@fixture()
def entries_for_testing():
    return """postal_code,city,street,house_number,unit_price,grid_fees,kwh_price\n
24446,Enricoburg,Am Weingarten,12-34,3.86,0.64,0.56\n
76648,Lenyascheid,Adolf-Reichwein-Str.,44-56,1.88,1.81,0.50\n
04676,Neu Pepestadt,Dechant-Krey-Str.,34-40,4.10,1.49,0.32\n
42613,Azraland,Esmarchstr.,98-99,2.89,1.61,0.38\n
28030,Bad Wiebkescheid,Nietzschestr.,3-5,2.27,1.30,0.42\n
89868,Weberburg,Völklinger Str.,92-116,3.48,4.21,0.50\n
86799,Bad Annemarie,Müritzstr.,47-60,3.15,1.24,0.68\n
87977,Ost Rosadorf,Baltrumstr.,92-132,1.29,0.42,0.31\n
76693,Neu Liana,Köpenicker Str.,33-37,2.24,0.19,0.45\n
46221,Ost Nataliescheid,Hallesche Str.,55-61,2.82,0.21,0.42\n
49331,Battkescheid,Jenaer Str.,33-66,2.70,4.97,0.49\n
81391,Hartingstadt,Oulustr.,49-71,2.98,4.81,0.70\n
01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.45\n
01847,Eliahscheid,Alt Steinbücheler Weg,814-849,4.79,3.19,0.30\n
16932,Börgelingstadt,Am Neuenhof,4-10,1.76,4.15,0.67\n
19381,West Luca,Jacob-Fröhlen-Str.,4-14,4.02,0.13,0.55\n
37775,Ghoshdorf,Stresemannplatz,90-128,4.73,4.63,0.49\n
20728,Nord Inka,Treuburger Str.,1-8,2.33,3.21,0.52
"""