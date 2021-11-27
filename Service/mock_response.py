import responses
import re


class Mocked():

    def request_callback(method='GET', url_path=None, status=200, payload=None, content_type=None,
                         match_querystring=False):
        """Payload for mocked responses"""
        payload = payload if payload else {
            "Any": "text"
        }
        content_type = content_type if content_type else 'application/json'

        return responses.Response(
            method=method,
            status=status,
            url=re.compile(rf"(.*){url_path}"),
            json=payload,
            content_type=content_type,
            match_querystring=match_querystring)
