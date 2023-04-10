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

        topFrame = Frame(self, padx=20, pady=10)
        middleFrame = Frame(self, padx=20)
        bottomFrame = Frame(self, padx=20, pady=10)

        networkLabel = Label(topFrame, text="Joined Networks:")
        refreshButton = Button(
            topFrame,
            text="Refresh Networks",
            command=self.controller.fetch_updated_networks,
        )
        aboutButton = Button(
            topFrame, text="About", command=print
        )
        peersButton = Button(
            topFrame, text="Show Peers", command=print
        )
        joinButton = Button(
            topFrame,
            text="Join Network",
            command=print
        )

        networkListScrollbar = Scrollbar(middleFrame)

        self.networkList = TreeView(
            middleFrame, "Network ID", "Name", "Status"
        )
        self.networkList.column("Network ID", width=40)
        self.networkList.column("Status", width=40)

        self.networkList.bind("<Double-Button-1>", print)

        leaveButton = Button(
            bottomFrame,
            text="Leave Network",
            command=print
        )
        ztCentralButton = Button(
            bottomFrame,
            text="ZeroTier Central",
            command=print
        )
        toggleConnectionButton = Button(
            bottomFrame,
            text="Disconnect/Connect Interface",
            command=print
        )
        toggleServiceButton = Button(
            bottomFrame,
            text="Toggle ZT Service",
            command=print
        )
        serviceStatusLabel = Label(bottomFrame)
        infoButton = Button(
            bottomFrame,
            text="Network Info",
            command=print
        )

        networkLabel.pack(side="left", anchor="sw")
        refreshButton.pack(side="right", anchor="se")
        aboutButton.pack(side="right", anchor="sw")
        peersButton.pack(side="right", anchor="sw")
        joinButton.pack(side="right", anchor="se")

        networkListScrollbar.pack(side="right", fill="both")
        self.networkList.pack(side="bottom", fill="x")

        leaveButton.pack(side="left", fill="x")
        toggleConnectionButton.pack(side="left", fill="x")
        infoButton.pack(side="right", fill="x")
        ztCentralButton.pack(side="right", fill="x")
        toggleServiceButton.pack(side="right", fill="x")
        serviceStatusLabel.pack(side="right", fill="x", padx=(100, 0))

        topFrame.pack(side="top", fill="x")
        middleFrame.pack(side="top", fill="x")
        bottomFrame.pack(side="top", fill="x")

        self.networkList.config(yscrollcommand=networkListScrollbar.set)
        networkListScrollbar.config(command=self.networkList.yview)

    def configure_main_window(self) -> None:
        """Configures the main window itself"""
        super().__init__(className="zerotier-gui")
        self.title("ZeroTier-GUI")
        self.resizable(width=False, height=False)

    def update_network_list(self, networks: list) -> None:
        """Updates the network list widget with the given NETWORKS
        argument. Ideally, these should be more up to date"""
        self.networkList.delete(*self.networkList.get_children())

        for network in networks:
            identifier = network["id"]
            name = network["name"]
            status = network["status"]
            interface_is_down = self.controller.is_network_interface_down(
                network["portDeviceName"])
            if not name:
                name = "Unknown Name"
            self.networkList.insert(
                (identifier, name, status), interface_is_down
            )
