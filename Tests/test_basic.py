import time
import pytest
import responses
from Service.app import CurrencyCached
from Service.mock_response import Mocked

payload_latest = { "USD": "8.25"}

@pytest.fixture
def mock_rsps():
    """Mocking responses for /latest endpoint"""
    with responses.RequestsMock() as rsps:
        rsps.add(Mocked.request_callback(url_path='latest', payload=payload_latest))
        yield rsps


@pytest.fixture
def client():
    """Start CurrencyCached client"""
    client = CurrencyCached(exp_interval=5)
    yield client
    client.exchange.clear_cache()


def test_check_cache_to_one_url(client, mock_rsps):
    """ Second call should use cache
    Precondition:
        Mock response for /latest endpoint with expire cache interval = 5 sec
    Steps:
        1. Make call to /latest with 'symbols': 'USD'
        2. Make second call to /latest with 'symbols': 'USD'
        3. Check the number of calls made
    Expected result:
        Number of calls = 1
    """
    response1 = client.get_currency('USD')
    response2 = client.get_currency('USD')
    assert len(mock_rsps.calls) == 1


def test_check_cache_one_url(client, mock_rsps):
    """ Calls to diff url are cached separately
    Precondition:
        Mock response for /latest endpoint with expire cache interval = 5 sec
    Steps:
        1. Make call to /latest with 'symbols': 'USD'
        2. Make call to /latest with 'symbols': 'ERO'
        3. Check the number of calls made
        4. Make call to /latest with 'symbols': 'USD'
        5. Make call to /latest with 'symbols': 'ERO'
        6. Check the number of second calls made
    Expected result:
        1. After first two request - number of calls = 2
        2. After next two request - number of calls = 2
    """
    response1 = client.get_currency('USD')
    response2 = client.get_currency('ERO')
    assert len(mock_rsps.calls) == 2

    response3 = client.get_currency('USD')
    response4 = client.get_currency('ERO')
    assert len(mock_rsps.calls) == 2


def test_check_cache_time(client, mock_rsps):
    """ Cache expired after timeout
    Precondition:
        Mock response for /latest endpoint with expire cache interval = 5 sec
    Steps:
        1. Make call to /latest with 'symbols': 'USD'
        2. Wait 6 second
        3. Make call to /latest with 'symbols': 'USD'
        4. Check the number of calls made
    Expected result:
        1. After first two request - number of calls = 2
        2. After next two request -  number of calls = 2
    """
    client.set_interval(seconds=5)
    response1 = client.get_currency('USD')
    time.sleep(6)
    response2 = client.get_currency('USD')
    assert len(mock_rsps.calls) == 2


@pytest.mark.parametrize('s_code', [400, 404, 500])
def test_negative_responses(client, mock_rsps, s_code):
    """ Responses with {s_code} status code are not cached
    Precondition:
        Mock response for /latest endpoint with status code = {s_code}
    Steps:
        1. Make call to /latest with 'symbols': 'USD'
        2. Make call to /latest with 'symbols': 'USD'
        3. Check response status code
        4. Check the number of calls made
    Expected result:
        1. All responses status codes = {s_code}
        2. Number of calls = 2
    """
    mock_rsps.replace(Mocked.request_callback(url_path='latest', status=s_code))
    response1 = client.get_currency('USD')
    response2 = client.get_currency('USD')
    assert response1.status_code == response2.status_code == s_code
    assert len(mock_rsps.calls) == 2
