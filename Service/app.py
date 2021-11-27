from Data.constants import BASE_URL
from Service.requests_api import RequestsCachedApi
from logging import basicConfig, getLogger

basicConfig(level='INFO')
logger = getLogger('requests_cache')


class CurrencyCached():
    def __init__(self):
        self.exchange = RequestsCachedApi(BASE_URL)  # RequestsApi(BASE_URL, params={'access_key': API_KEY})
        self.exchange.set_up_cached_session()

    def set_interval(self, days=0, hours=0, minutes=0, seconds=0):
        ttl = (((days * 24) + hours) * 60 + minutes) * 60 + seconds
        self.exchange.set_up_cached_session(expire_after=ttl)

    def get_currency(self, parametars=None):
        params = {'symbols': parametars} if parametars else None
        response = self.exchange.get("latest", params=params)
        logger.info(f'Get cached data for {parametars} - {response.text}') if response.from_cache else logger.info(
            f'Make call to {response.url} - response: {response.status_code} - {response.text}')
        return response

    ### TODO add other endpoints here
    