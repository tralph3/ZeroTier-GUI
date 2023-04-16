from modules.zt_service import ZTService
from modules.startup import Startup
from codes.exit_codes import ExitCode
from codes.status_codes import StatusCode
from view import View
import sys
import os
import json
import subprocess


class Controller():
    def __init__(self) -> None:
        self.startup = Startup()
        self.zt_service = ZTService()
        self.view = View()

    def main(self) -> None:
        self.make_preliminary_checks()
        self.view.main()

    def make_preliminary_checks(self) -> None:
        zt_exit_code = self.startup.get_zt_cli_exit_code()
        handler_mappings = {
            ExitCode.ZT_SERVICE_NOT_RUNNING: self.handle_service_not_running,
            ExitCode.ZT_NO_ACCESS_TOKEN: self.handle_no_access_token,
            ExitCode.ZT_NOT_INSTALLED: self.handle_zt_not_installed,
            ExitCode.OK: lambda: None,
        }
        handler_mappings[zt_exit_code]()

    def handle_service_not_running(self):
        if self.view.ask_to_turn_on_service():
            self.zt_service.turn_on()
        else:
            os._exit(ExitCode.ZT_SERVICE_NOT_RUNNING)

    def handle_no_access_token(self):
        self.view.warn_no_access_token()
        if self.view.ask_to_run_as_root():
            self.startup.copy_access_token()
        else:
            os._exit(ExitCode.ZT_NO_ACCESS_TOKEN)

    def handle_zt_not_installed(self):
        self.view.warn_zt_not_installed()
        os._exit(ExitCode.ZT_NOT_INSTALLED)

    def handle_status_codes(self, status_code: int) -> None:
        if status_code == StatusCode.OK:
            return
        elif status_code == StatusCode.AUTHORIZATION_REQUIRED:
            self.view.warn_no_access_token()
        else:
            print(f"Unrecognized status code: {status_code}", file=sys.stderr)

    def fetch_updated_networks(self):
        networks = self.zt_service.get_networks()
        self.view.update_network_list(networks)

    def is_network_interface_down(self, interface_name: str) -> bool:
        interface_info = json.loads(
            subprocess.check_output(
                ["ip", "--json", "link", "show", interface_name]).decode())[0]
        state = interface_info["operstate"]
        return state.lower() == "down"

    def leave_network(self, network_id: str):
        self.zt_service.leave_network(network_id)
        self.view.show_network_left_successfully()
        self.fetch_updated_networks()

    def join_network(self, network_id: str):
        if self.zt_service.is_joined_to_network(network_id):
            self.view.warn_already_joined_to_network()
            return
        self.handle_status_codes(self.zt_service.join_network(network_id))
        self.fetch_updated_networks()


if __name__ == "__main__":
    Controller().main()
