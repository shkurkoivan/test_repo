import requests
from utils.configuration import ConfigParser
import urllib.parse


class HttpClient:
    def __init__(self, auth):
        self.config = ConfigParser.config_parser['server']
        self.host = self.config['host']
        self.port = self.config['port']
        self.base_address = self.host + self.port
        self.auth = auth

    def get(self, path=None, params=None, headers=None):
        url = f"{self.base_address}{path}"
        # Приходится вручную склеивать params, т.к. бэкенд не маппит "%2B%" на "+"
        if params:
            url += "?"
            for i in params.keys():
                params[i] = urllib.parse.quote_plus([params[i]][0])
                url += i + "=" + params[i]
        return requests.get(url=url, headers=headers, auth=self.auth)

    def post(self, path="/", json=None, headers=None):
        if not headers:
            headers = {
                'Content-type': 'application/json'
            }

        url = f"{self.base_address}{path}"
        return requests.post(url=url, json=json, headers=headers, auth=self.auth)

    def put(self, path="/", json=None, headers=None):
        if not headers:
            headers = {
                'Content-type': 'application/json'
            }

        url = f"{self.base_address}{path}"
        return requests.put(url=url, json=json, headers=headers, auth=self.auth)

    def delete(self, path=None, params=None, headers=None):
        url = f"{self.base_address}{path}"
        # Приходится вручную склеивать params, т.к. бэкенд не маппит "%2B%" на "+"
        if params:
            url += "?"
            for i in params.keys():
                params[i] = urllib.parse.quote_plus([params[i]][0])
                url += i + "=" + params[i]
        return requests.delete(url=url, headers=headers, auth=self.auth)
