import time

import requests
import urllib3
import json
import base64
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Api():
    def __init__(self, lockfile, region, version):
        self.lockfile = lockfile
        self.version = version
        self.pd_url = f"https://pd.{region[0]}.a.pvp.net"
        self.glz_url = f"https://glz-{region[1][0]}.{region[1][1]}.a.pvp.net"
        self.puuid = ""
        self.headers = {}
        self.getHeaders()
        self.tierDict = {
            "0cebb8be-46d7-c12a-d306-e9907bfc5a25": (0, 149, 135),
            "e046854e-406c-37f4-6607-19a9ba8426fc": (241, 184, 45),
            "60bca009-4182-7998-dee7-b8a2558dc369": (209, 84, 141),
            "12683d76-48d7-84a3-4e09-6985794f0445": (90, 159, 226),
            "411e4a55-4e59-7757-41f0-86a53f101bb5": (239, 235, 101),
            None: None
        }


    def getLockfile(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
                data = lockfile.read().split(':')
                keys = ['name', 'PID', 'port', 'password', 'protocol']
                return dict(zip(keys, data))
        except FileNotFoundError:
            return None

    def getHeaders(self):
        global puuid
        if self.headers == {}:

            self.lockfile = self.getLockfile()
            local_headers = {'Authorization': 'Basic ' + base64.b64encode(
                ('riot:' + self.lockfile['password']).encode()).decode()}
            response = requests.get(f"https://127.0.0.1:{self.lockfile['port']}/entitlements/v1/token",
                                    headers=local_headers, verify=False)
            entitlements = response.json()
            self.puuid = entitlements['subject']
            self.headers = {
                'Authorization': f"Bearer {entitlements['accessToken']}",
                'X-Riot-Entitlements-JWT': entitlements['token'],
                'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjog"
                                         "IldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5"
                                         "MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
                'X-Riot-ClientVersion': self.version
            }
        return self.headers


    def api(self, url_type: str, endpoint: str, method: str, j=None):
        global response
        global headers
        try:
            if url_type == "glz":
                response = requests.request(method, self.glz_url + endpoint, headers=self.getHeaders(), verify=False, json=j)
                return response

            elif url_type == "pd":
                response = requests.request(method, self.pd_url + endpoint, headers=self.getHeaders(), verify=False, json=j)
                return response

            elif url_type == "local":
                local_headers = {'Authorization': 'Basic ' + base64.b64encode(
                    ('riot:' + self.lockfile['password']).encode()).decode()}
                response = requests.request(method, f"https://127.0.0.1:{self.lockfile['port']}{endpoint}",
                                            headers=local_headers,
                                            verify=False)
                return response

            elif url_type == "custom":
                response = requests.request(method, f"{endpoint}", headers=self.getHeaders(), verify=False, json=j)
                return response
        except json.decoder.JSONDecodeError:
            print(response)
            print(response.text)
            return None


    def get_presence(self):
        presences = self.api(url_type="local", endpoint="/chat/v4/presences", method="get")
        return presences

    def wait_for_presence(self):
        while True:
            presences = self.get_presence()
            if presences.ok:
                return True
            time.sleep(1)


    def get_inventory(self):
        return self.api(url_type="pd", endpoint=f"/personalization/v2/players/{self.puuid}/playerloadout", method="get")

    def put_inventory(self, inv):
        return self.api(url_type="pd", endpoint=f"/personalization/v2/players/{self.puuid}/playerloadout", method="put", j=inv)



