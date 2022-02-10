import os
from collections import OrderedDict

from pytest import fixture


@fixture(scope='module')
def location_prices_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices.csv')
    yield file_path


@fixture(scope='module')
def location_prices_small_file_path() -> OrderedDict[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), 'location_prices_small.csv')
    yield file_path
