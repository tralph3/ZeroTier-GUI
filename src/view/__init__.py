from tkinter import messagebox
from .main_window import MainWindow
from events import Event, emit_event


class View():
    def main(self) -> None:
        self.main_window = MainWindow()
        emit_event(Event.REFRESH_NETWORKS)
        self.main_window.mainloop()

    def ask_to_turn_on_service(self) -> bool:
        return messagebox.askyesno(
            icon="error",
            title="ZeroTier-One Service Not Running",
            message="The 'zerotier-one' service isn't running.\n\n"
            "Do you wish to grant root access to enable it?",
        )

    def ask_to_run_as_root(self) -> bool:
        messagebox.askyesno(
            icon="info",
            title="Root access needed",
            message="In order to grant your user permission "
            "to use ZeroTier temporary root access is needed to "
            "store the Auth Token in your home folder. "
            "Otherwise, you would need to run this "
            "program as root. Grant access?",
        )

    def warn_no_access_token(self) -> None:
        messagebox.showerror(
            title="Error",
            message="The access token for this user is not present or couldn't be found.",
            icon="error",
        )

    def warn_zt_not_installed(self) -> None:
        messagebox.showerror(
            title="Error",
            message="ZeroTier isn't installed.",
            icon="error",
        )

    def warn_already_joined_to_network(self) -> None:
        messagebox.showerror(
            title="Already joined",
            message="You're already a member of this network.",
            icon="info",
        )

    def set_networks_in_list(self, networks: list) -> None:
        self.main_window.update_network_list(networks)
