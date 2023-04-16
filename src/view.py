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

    def join_network(self, network_id: str) -> None:
        self.controller.join_network(network_id)




    # def make_join_network_window(self):
    #     def populate_network_list():
    #         network_history_list.delete(*network_history_list.get_children())
    #         for network_id in self.network_history:
    #             network_name = self.network_history[network_id]["name"]
    #             if network_name == "":
    #                 network_name = "Unknown Name"
    #             network_history_list.insert((network_name, network_id))

    #     def populate_info_sidebar():
    #         selected_item = network_history_list.focus()
    #         if selected_item != "":
    #             item_info = network_history_list.item(selected_item)["values"]
    #             network_id = item_info[1]
    #             join_date = self.network_history[network_id]["join_date"]
    #             network_name = self.network_history[network_id]["name"]
    #             if network_name == "":
    #                 network_name = "Unknown Name"
    #             currently_joined = self.is_on_network(network_id)
    #         else:
    #             network_id = "-"
    #             join_date = "-"
    #             currently_joined = "-"
    #             network_name = "-"
    #         network_id_label.configure(
    #             text="{:20s}{}".format("Network ID:", network_id)
    #         )
    #         network_name_label.configure(
    #             text="{:20s}{}".format("Name:", network_name)
    #         )
    #         last_joined_label.configure(
    #             text="{:20s}{}".format("Last joined date:", join_date)
    #         )
    #         currently_joined_label.configure(
    #             text="{:20s}{}".format("Currently joined:", currently_joined)
    #         )

    #     def on_network_selected(event):
    #         populate_info_sidebar()
    #         selected_item = network_history_list.focus()
    #         item_info = network_history_list.item(selected_item)["values"]
    #         network_id = item_info[1]
    #         network_entry_value.set(network_id)

    #     def delete_history_entry():
    #         selected_item = network_history_list.focus()
    #         item_info = network_history_list.item(selected_item)["values"]
    #         network_id = item_info[1]
    #         self.network_history.pop(network_id)
    #         populate_network_list()

    #     join_window = self.launch_sub_window("Join Network")
    #     join_window.configure(bg=BACKGROUND)

    #     network_entry_value = tk.StringVar()

    #     main_frame = tk.Frame(join_window, padx=20, pady=20, bg=BACKGROUND)
    #     middle_frame = tk.Frame(main_frame, bg=BACKGROUND)
    #     left_frame = tk.LabelFrame(
    #         middle_frame, bg=BACKGROUND, fg=FOREGROUND, text="Network History"
    #     )
    #     right_frame = tk.LabelFrame(
    #         middle_frame,
    #         bg=BACKGROUND,
    #         fg=FOREGROUND,
    #         text="Info",
    #         padx=10,
    #         pady=10,
    #     )
    #     bottom_frame = tk.Frame(main_frame, bg=BACKGROUND)

    #     join_button = self.formatted_buttons(
    #         bottom_frame,
    #         text="Join",
    #         command=lambda: join_network(network_entry_value.get()),
    #     )
    #     delete_history_entry_button = self.formatted_buttons(
    #         bottom_frame,
    #         text="Delete history entry",
    #         command=delete_history_entry,
    #     )

    #     join_title = tk.Label(
    #         main_frame, text="Join Network", font="Monospace"
    #     )
    #     network_history_list = TreeView(left_frame, "Network")
    #     network_history_scrollbar = tk.Scrollbar(
    #         left_frame, bd=2, bg=BACKGROUND
    #     )
    #     network_history_list.config(
    #         yscrollcommand=network_history_scrollbar.set
    #     )
    #     network_history_scrollbar.config(command=network_history_list.yview)

    #     network_history_list.style.configure(
    #         "NoBackground.Treeview", background=BACKGROUND
    #     )
    #     network_history_list.configure(
    #         show="tree", height=20, style="NoBackground.Treeview"
    #     )
    #     network_history_list.column("Network", width=300)
    #     network_history_list.bind("<<TreeviewSelect>>", on_network_selected)
    #     network_history_list.bind(
    #         "<Double-Button-1>", lambda _a: join_button.invoke()
    #     )

    #     join_label = tk.Label(
    #         bottom_frame, text="Network ID:", bg=BACKGROUND, fg=FOREGROUND
    #     )
    #     join_entry = tk.Entry(
    #         bottom_frame,
    #         width=20,
    #         font="Monospace",
    #         textvariable=network_entry_value,
    #     )

    #     network_id_label = tk.Label(
    #         right_frame, font=("Monospace", 11), width=45, anchor="w"
    #     )
    #     network_name_label = tk.Label(
    #         right_frame, font=("Monospace", 11), width=45, anchor="w"
    #     )
    #     last_joined_label = tk.Label(
    #         right_frame,
    #         font=("Monospace", 11),
    #         width=45,
    #         anchor="w",
    #     )
    #     currently_joined_label = tk.Label(
    #         right_frame,
    #         font=("Monospace", 11),
    #         width=45,
    #         anchor="w",
    #     )

    #     populate_network_list()
    #     populate_info_sidebar()

    #     join_title.pack(side="top")
    #     network_history_list.pack(side="left", padx=10, pady=10)
    #     network_history_scrollbar.pack(side="right", fill="y")

    #     network_id_label.pack(side="top", anchor="w")
    #     network_name_label.pack(side="top", anchor="w")
    #     last_joined_label.pack(side="top", anchor="w")
    #     currently_joined_label.pack(side="top", anchor="w")

    #     join_label.pack(side="left", anchor="w", pady=10)
    #     join_entry.pack(side="left", anchor="w", pady=10)
    #     join_button.pack(side="left", pady=10)
    #     delete_history_entry_button.pack(side="left", pady=10)

    #     left_frame.pack(side="left", fill="y", pady=10, padx=5)
    #     right_frame.pack(side="right", fill="y", pady=10, padx=5)
    #     middle_frame.pack(side="top", fill="both")
    #     bottom_frame.pack(side="top", fill="both")
    #     main_frame.pack(side="top", fill="x")
