import requests
import requests_cache


class RequestsApi:
    def __init__(self, base_url, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def get_session(self):
        return self.session

    def request(self, method, url, **kwargs):
        return self.session.request(method, self.base_url + url, **kwargs)

    def get(self, url, **kwargs):
        return self.session.get(self.base_url + url, **kwargs)

    ###TODO add all methods here

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsApi.__deep_merge(value, node)
            else:
                destination[key] = value
        return destination


class RequestsCachedApi(RequestsApi):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.session = requests_cache.CachedSession()

    def set_up_cached_session(self, cache_name='cache', backend=None, expire_after=5, allowable_methods=('GET')):
        self.session = requests_cache.CachedSession(cache_name=cache_name, backend=backend, expire_after=expire_after,
                                                    allowable_methods=allowable_methods, old_data_on_error=False)
        self.clear_cache()

    def read_cache(self):
        self.expire_after = self.session.expire_after
        self.cached_urls = list(self.session.cache.urls)
        return (self.expire_after, self.cached_url)

    def clear_cache(self):
        self.session.cache.clear()
