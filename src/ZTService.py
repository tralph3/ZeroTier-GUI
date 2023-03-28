import requests
import os


class ZTService():
    """This class is in charge of talking to the ZeroTier service via
    the ZeroTier API"""
    def __init__(self) -> None:
        self.auth_token_path = os.path.expanduser("~/.zeroTierOneAuthToken")
        self.zt_base_url = "http://localhost:9993"

    def make_get_request(self, path: str) -> requests.Response:
        """Makes a get request to the ZeroTier API. PATH is the url
        path to be appended to the base url"""
        return requests.get(
            f"{self.zt_base_url}/{path}",
            headers={"X-ZT1-Auth": self.get_auth_token()}
        )

    def make_post_request(self, path: str, data: dict = None) -> requests.Response:
        """Makes a post request to the ZeroTier API. PATH is the url
        path to be appended to the base url. DATA is the data to send
        to the url"""
        return requests.post(
            f"{self.zt_base_url}/{path}",
            headers={"X-ZT1-Auth": self.get_auth_token()},
            json=data
        )

    def make_del_request(self, path: str) -> requests.Response:
        """Makes a delete request to the ZeroTier API. PATH is the url
        path to be appended to the base url"""
        return requests.delete(
            f"{self.zt_base_url}/{path}",
            headers={"X-ZT1-Auth": self.get_auth_token()},
        )

    def get_auth_token(self) -> str:
        """Retrieves the auth token from disk"""
        with open(self.auth_token_path, "r") as f:
            return f.read()

    def get_networks(self) -> list[dict]:
        """Returns a list with the currently joined networks
        information"""
        return self.make_get_request("network").json()

    def join_network(self, network_id: str) -> None:
        self.make_post_request(f"network/{network_id}")

    def leave_network(self, network_id: str) -> None:
        self.make_del_request(f"network/{network_id}")

    def get_peers(self) -> dict:
        return self.make_get_request("peer").json()

    def is_active(self) -> bool:
        """Determines if the zerotier-one service is currently
        running"""
        try:
            requests.get(self.zt_base_url)
            return True
        except requests.exceptions.ConnectionError:
            return False
