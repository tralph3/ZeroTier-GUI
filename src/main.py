from zt_service import ZTService
from view import View
from startup import Startup
import os
import json
import subprocess


class Controller():
    def __init__(self) -> None:
        self.startup = Startup()
        self.zt_service = ZTService()
        self.view = View(self)

    def main(self) -> None:
        self.make_preliminary_checks()
        self.view.main()

    def make_preliminary_checks(self) -> None:
        zt_exit_code = self.startup.get_zt_cli_exit_code()
        if zt_exit_code == self.zt_service.SERVICE_NOT_RUNNING_CODE:
            self.handle_service_not_running()
        elif zt_exit_code == self.zt_service.NO_ZT_ACCESS_CODE:
            self.handle_no_access_token()
        elif zt_exit_code == self.zt_service.ZT_NOT_INSTALLED_CODE:
            self.handle_zt_not_installed()

    def handle_service_not_running(self):
        if self.view.ask_to_turn_on_service():
            self.zt_service.turn_on()
        else:
            os._exit(self.zt_service.SERVICE_NOT_RUNNING_CODE)

    def handle_no_access_token(self):
        if self.view.ask_to_run_as_root():
            self.startup.copy_access_token()
        else:
            os._exit(self.zt_service.NO_ZT_ACCESS_CODE)

    def handle_zt_not_installed(self):
        self.view.warn_zt_not_installed()
        os._exit(self.zt_service.ZT_NOT_INSTALLED_CODE)

    def fetch_updated_networks(self):
        networks = self.zt_service.get_networks()
        self.view.update_network_list(networks)

    def is_network_interface_down(self, interface_name: str) -> bool:
        interface_info = json.loads(
            subprocess.check_output(
                ["ip", "--json", "link", "show", interface_name]).decode())[0]
        state = interface_info["operstate"]
        return state.lower() == "down"

if __name__ == "__main__":
    Controller().main()
