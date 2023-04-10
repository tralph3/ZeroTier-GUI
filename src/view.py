import tkinter as tk
from tkinter import messagebox
from widgets import Button, Frame, Label, Scrollbar, TreeView


class View(tk.Tk):
    def __init__(self, controller) -> None:
        self.controller = controller
        self.make_main_window()

    def main(self) -> None:
        self.controller.fetch_updated_networks()
        self.mainloop()

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

    def warn_zt_not_installed(self) -> None:
        messagebox.showerror(
            title="Error",
            message="ZeroTier isn't installed!",
            icon="error",
        )

    def make_main_window(self) -> None:
        """Creates, configures and packs all the required widgets for
        the main window"""
        self.configure_main_window()

        top_frame = Frame(self, padx=20, pady=10)
        middle_frame = Frame(self, padx=20)
        bottom_frame = Frame(self, padx=20, pady=10)

        network_label = Label(top_frame, text="Joined Networks:")
        refresh_button = Button(
            top_frame,
            text="Refresh Networks",
            command=self.controller.fetch_updated_networks,
        )
        about_button = Button(
            top_frame, text="About", command=print
        )
        peers_button = Button(
            top_frame, text="Show Peers", command=print
        )
        join_button = Button(
            top_frame,
            text="Join Network",
            command=print
        )

        network_list_scrollbar = Scrollbar(middle_frame)

        self.network_list = TreeView(
            middle_frame, "Network ID", "Name", "Status"
        )
        self.network_list.column("Network ID", width=40)
        self.network_list.column("Status", width=40)

        self.network_list.bind("<Double-Button-1>", print)

        leave_network_button = Button(
            bottom_frame,
            text="Leave Network",
            command=print
        )
        zt_central_button = Button(
            bottom_frame,
            text="ZeroTier Central",
            command=print
        )
        toggle_connection_button = Button(
            bottom_frame,
            text="Disconnect/Connect Interface",
            command=print
        )
        toggle_service_button = Button(
            bottom_frame,
            text="Toggle ZT Service",
            command=print
        )
        service_status_label = Label(bottom_frame)
        infoButton = Button(
            bottom_frame,
            text="Network Info",
            command=print
        )

        network_label.pack(side="left", anchor="sw")
        refresh_button.pack(side="right", anchor="se")
        about_button.pack(side="right", anchor="sw")
        peers_button.pack(side="right", anchor="sw")
        join_button.pack(side="right", anchor="se")

        network_list_scrollbar.pack(side="right", fill="both")
        self.network_list.pack(side="bottom", fill="x")

        leave_network_button.pack(side="left", fill="x")
        toggle_connection_button.pack(side="left", fill="x")
        infoButton.pack(side="right", fill="x")
        zt_central_button.pack(side="right", fill="x")
        toggle_service_button.pack(side="right", fill="x")
        service_status_label.pack(side="right", fill="x", padx=(100, 0))

        top_frame.pack(side="top", fill="x")
        middle_frame.pack(side="top", fill="x")
        bottom_frame.pack(side="top", fill="x")

        self.network_list.config(yscrollcommand=network_list_scrollbar.set)
        network_list_scrollbar.config(command=self.network_list.yview)

    def configure_main_window(self) -> None:
        """Configures the main window itself"""
        super().__init__(className="zerotier-gui")
        self.title("ZeroTier-GUI")
        self.resizable(width=False, height=False)

    def update_network_list(self, networks: list) -> None:
        """Updates the network list widget with the given NETWORKS
        argument. Ideally, these should be more up to date"""
        self.network_list.delete(*self.network_list.get_children())

        for network in networks:
            identifier = network["id"]
            name = network["name"]
            status = network["status"]
            interface_is_down = self.controller.is_network_interface_down(
                network["portDeviceName"])
            if not name:
                name = "Unknown Name"
            self.network_list.insert(
                (identifier, name, status), interface_is_down
            )
