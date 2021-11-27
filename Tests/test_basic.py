import time
import pytest
import responses
from Service.app import CurrencyCached
from Service.mock_responce import Mocked


@pytest.fixture
def mock_rsps():
    with responses.RequestsMock() as rsps:
        rsps.add(Mocked.request_callback(url_path='latest'))
        yield rsps


@pytest.fixture
def client():
    client = CurrencyCached()
    yield client
    client.exchange.clear_cache()


def test_check_cache_to_one_url(client, mock_rsps):
    ''' Second call should use cache'''
    response1 = client.get_currency('USD')
    response2 = client.get_currency('USD')
    assert len(mock_rsps.calls) == 1


def test_responses_check(client, mock_rsps):
    ''' Calls returns same responses'''
    response1 = client.get_currency('USD')
    response2 = client.get_currency('USD')
    assert response1.text == response2.text


def test_check_cache_one_url(client, mock_rsps):
    ''' Calls to diff url are cached separately'''
    response1 = client.get_currency('USD')
    response2 = client.get_currency('ERO')
    assert len(mock_rsps.calls) == 2

    response3 = client.get_currency('USD')
    response4 = client.get_currency('ERO')
    assert len(mock_rsps.calls) == 2


def test_check_cache_time(client, mock_rsps):
    ''' Cache expired after timeout'''
    client.set_interval(seconds=5)
    response1 = client.get_currency('USD')
    time.sleep(6)
    response2 = client.get_currency('USD')
    assert len(mock_rsps.calls) == 2


@pytest.mark.parametrize('s_code', [400, 404, 500])
def test_negative_responses(client, mock_rsps, s_code):
    ''' Responses with not 200 status code are not cached'''
    mock_rsps.replace(Mocked.request_callback(url_path='latest', status=s_code))
    response1 = client.get_currency('USD')
    response2 = client.get_currency('USD')
    assert response1.status_code == response2.status_code == s_code
    assert len(mock_rsps.calls) == 2
