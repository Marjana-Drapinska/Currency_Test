from Data.constants import BASE_URL
from Service.requests_api import RequestsCachedApi
from logging import basicConfig, getLogger

basicConfig(level='INFO')
logger = getLogger('requests_cache')


class CurrencyCached():
    """Client to get currency value from the server using cached api client with expired interval"""
    def __init__(self, exp_interval=5):
        self.exchange = RequestsCachedApi(BASE_URL)  # RequestsApi(BASE_URL, params={'access_key': API_KEY})
        self.exchange.set_up_cached_session(expire_after=exp_interval)

    def set_interval(self, days=0, hours=0, minutes=0, seconds=0):
        """Set cache entry expiration interval"""
        ttl = (((days * 24) + hours) * 60 + minutes) * 60 + seconds
        self.exchange.set_up_cached_session(expire_after=ttl)

    def get_currency(self, parameters=None):
        """Make call to /latest
        parameters - 'symbols' parameter currency codes to limit output currencies (GBP,JPY,EUR etc.)
        """
        params = {'symbols': parameters} if parameters else None
        response = self.exchange.get("latest", params=params)
        logger.info(f'Get cached data for {parameters} - {response.text}') if response.from_cache else logger.info(
            f'Make call to {response.url} - response: {response.status_code} - {response.text}')
        return response

    ### TODO add other endpoints here
