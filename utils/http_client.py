import requests
from utils.configuration import ConfigParser


class HttpClient:
    def __init__(self, auth):
        self.config = ConfigParser.config_parser['server']
        self.host = self.config['host']
        self.port = self.config['port']
        self.base_address = self.host + self.port
        self.auth = auth

    def get(self, path="/", params=None, headers=None):
        print (self.auth)
        url = f"{self.base_address}{path}"
        return requests.get(url=url, params=params, headers=headers, auth=self.auth)

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        return requests.post(url=url, params=params, data=data, json=json, headers=headers, auth=self.auth)