import os
import requests
from pymemcache.client import base

class RootClient:
    def __init__(self):
#REMPLAZAR LOS []
        self.host = "https://algocerca.cl/"
        self.client = base.Client(('localhost', 11211))
        self.client.set('token', "12345")
        self.client.set('username', "[USERNAME_ADMIN]")
        self.client.set('password', "[PASSWORD_ADMIN]")
        self.token = self.client.get('token').decode("utf-8")
        self.username = self.client.get("username").decode("utf-8")
        self.password = self.client.get("password").decode("utf-8")

    def _test_token(self):
        token = self.client.get('token').decode("utf-8")
        host = self.host
        endpoint = "wp-json/wp/v2/users/me"
        header = {"Authorization": "Bearer " + token}
        get_req_me = requests.get(url=host + endpoint, headers=header)
        if (get_req_me.status_code == 200):
            return True
        else:
            refresh = self._refresh_token()
            if (refresh.status_code == 200):
                return True
            else:
                return False

    def _refresh_token(self):
        user_pass = {"username": self.username, "password": self.password}
        endpoint = "wp-json/jwt-auth/v1/token"
        post_request = requests.post(url=self.host + endpoint, json=user_pass)
        print("STATUS CODE REFRESH " + str(post_request.status_code))
        if (post_request.status_code == 200):
            data_body = post_request.json()
            print(data_body)
            self.client.set('token', data_body["token"])
            self.token = self.client.get("token").decode("utf-8")
        return post_request

    def get_valid_token(self):
        test = self._test_token()
        if (test == True):
            print("This is token: " + self.token)
            bearer = {"Authorization": "Bearer " + self.token}
            return bearer
        else:
            print("Error token: " + self.token)
            print("Error token_refresh: " + self.refresh_token)
            return "ERROR!! Al obtener el token"