import requests
import os
import dbus
from typing import Optional


class ZTService():
    """This class is in charge of talking to the ZeroTier service via
    the ZeroTier API"""
    SERVICE_NOT_RUNNING_CODE = 1
    NO_ZT_ACCESS_CODE = 2
    ZT_NOT_INSTALLED_CODE = 127

    def __init__(self) -> None:
        zt_host = "localhost"
        zt_port = 9993
        self.set_auth_token_path("~/.zeroTierOneAuthToken")
        self.zt_base_url = f"http://{zt_host}:{zt_port}"

    def setup_systemd_dbus_connection(self):
        bus = dbus.SystemBus()
        systemd1 = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.systemd_interface = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    def set_auth_token_path(self, auth_token_path: str) -> None:
        self.auth_token_path = os.path.expanduser(auth_token_path)

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

    def get_networks(self) -> Optional[list[dict]]:
        """Returns a list with the currently joined networks
        information"""
        response = self.make_get_request("network")
        if not response.ok:
            return None
        return response.json()

    def join_network(self, network_id: str) -> int:
        return self.make_post_request(f"network/{network_id}").status_code

    def leave_network(self, network_id: str) -> int:
        return self.make_del_request(f"network/{network_id}").status_code

    def get_peers(self) -> dict:
        return self.make_get_request("peer").json()

    def is_zerotier_service_running(self) -> bool:
        try:
            requests.get(self.zt_base_url)
            return True
        except requests.exceptions.ConnectionError:
            return False

    def turn_zerotier_service_on(self) -> None:
        self.systemd_interface.StartUnit('zerotier-one.service', 'replace')

    def turn_zerotier_service_off(self) -> None:
        self.systemd_interface.StopUnit('zerotier-one.service', 'replace')
