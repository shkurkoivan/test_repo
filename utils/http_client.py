import requests
from utils.configuration import ConfigParser


class HttpClient:
    def __init__(self, auth):
        self.config = ConfigParser.config_parser['server']
        self.host = self.config['host']
        self.port = self.config['port']
        self.base_address = self.host + self.port
        self.auth = auth

    def get(self, path="/", headers=None):
        url = f"{self.base_address}{path}"
        return requests.get(url=url, headers=headers, auth=self.auth)

    def post(self, path="/", json=None, headers=None):
        if not headers:
            headers = {
                'Content-type': 'application/json'
            }

        url = f"{self.base_address}{path}"
        return requests.post(url=url, json=json, headers=headers, auth=self.auth)
