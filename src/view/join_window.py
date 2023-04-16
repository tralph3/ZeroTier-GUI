


    def make_join_network_window(self):
        def populate_network_list():
            network_history_list.delete(*network_history_list.get_children())
            for network_id in self.network_history:
                network_name = self.network_history[network_id]["name"]
                if network_name == "":
                    network_name = "Unknown Name"
                network_history_list.insert((network_name, network_id))

        def populate_info_sidebar():
            selected_item = network_history_list.focus()
            if selected_item != "":
                item_info = network_history_list.item(selected_item)["values"]
                network_id = item_info[1]
                join_date = self.network_history[network_id]["join_date"]
                network_name = self.network_history[network_id]["name"]
                if network_name == "":
                    network_name = "Unknown Name"
                currently_joined = self.is_on_network(network_id)
            else:
                network_id = "-"
                join_date = "-"
                currently_joined = "-"
                network_name = "-"
            network_id_label.configure(
                text="{:20s}{}".format("Network ID:", network_id)
            )
            network_name_label.configure(
                text="{:20s}{}".format("Name:", network_name)
            )
            last_joined_label.configure(
                text="{:20s}{}".format("Last joined date:", join_date)
            )
            currently_joined_label.configure(
                text="{:20s}{}".format("Currently joined:", currently_joined)
            )

        def on_network_selected(event):
            populate_info_sidebar()
            selected_item = network_history_list.focus()
            item_info = network_history_list.item(selected_item)["values"]
            network_id = item_info[1]
            network_entry_value.set(network_id)

        def delete_history_entry():
            selected_item = network_history_list.focus()
            item_info = network_history_list.item(selected_item)["values"]
            network_id = item_info[1]
            self.network_history.pop(network_id)
            populate_network_list()

        join_window = self.launch_sub_window("Join Network")
        join_window.configure(bg=BACKGROUND)

        network_entry_value = tk.StringVar()

        main_frame = tk.Frame(join_window, padx=20, pady=20, bg=BACKGROUND)
        middle_frame = tk.Frame(main_frame, bg=BACKGROUND)
        left_frame = tk.LabelFrame(
            middle_frame, bg=BACKGROUND, fg=FOREGROUND, text="Network History"
        )
        right_frame = tk.LabelFrame(
            middle_frame,
            bg=BACKGROUND,
            fg=FOREGROUND,
            text="Info",
            padx=10,
            pady=10,
        )
        bottom_frame = tk.Frame(main_frame, bg=BACKGROUND)

        join_button = self.formatted_buttons(
            bottom_frame,
            text="Join",
            command=lambda: join_network(network_entry_value.get()),
        )
        delete_history_entry_button = self.formatted_buttons(
            bottom_frame,
            text="Delete history entry",
            command=delete_history_entry,
        )

        join_title = tk.Label(
            main_frame, text="Join Network", font="Monospace"
        )
        network_history_list = TreeView(left_frame, "Network")
        network_history_scrollbar = tk.Scrollbar(
            left_frame, bd=2, bg=BACKGROUND
        )
        network_history_list.config(
            yscrollcommand=network_history_scrollbar.set
        )
        network_history_scrollbar.config(command=network_history_list.yview)

        network_history_list.style.configure(
            "NoBackground.Treeview", background=BACKGROUND
        )
        network_history_list.configure(
            show="tree", height=20, style="NoBackground.Treeview"
        )
        network_history_list.column("Network", width=300)
        network_history_list.bind("<<TreeviewSelect>>", on_network_selected)
        network_history_list.bind(
            "<Double-Button-1>", lambda _a: join_button.invoke()
        )

        join_label = tk.Label(
            bottom_frame, text="Network ID:", bg=BACKGROUND, fg=FOREGROUND
        )
        join_entry = tk.Entry(
            bottom_frame,
            width=20,
            font="Monospace",
            textvariable=network_entry_value,
        )

        network_id_label = tk.Label(
            right_frame, font=("Monospace", 11), width=45, anchor="w"
        )
        network_name_label = tk.Label(
            right_frame, font=("Monospace", 11), width=45, anchor="w"
        )
        last_joined_label = tk.Label(
            right_frame,
            font=("Monospace", 11),
            width=45,
            anchor="w",
        )
        currently_joined_label = tk.Label(
            right_frame,
            font=("Monospace", 11),
            width=45,
            anchor="w",
        )

        populate_network_list()
        populate_info_sidebar()

        join_title.pack(side="top")
        network_history_list.pack(side="left", padx=10, pady=10)
        network_history_scrollbar.pack(side="right", fill="y")

        network_id_label.pack(side="top", anchor="w")
        network_name_label.pack(side="top", anchor="w")
        last_joined_label.pack(side="top", anchor="w")
        currently_joined_label.pack(side="top", anchor="w")

        join_label.pack(side="left", anchor="w", pady=10)
        join_entry.pack(side="left", anchor="w", pady=10)
        join_button.pack(side="left", pady=10)
        delete_history_entry_button.pack(side="left", pady=10)

        left_frame.pack(side="left", fill="y", pady=10, padx=5)
        right_frame.pack(side="right", fill="y", pady=10, padx=5)
        middle_frame.pack(side="top", fill="both")
        bottom_frame.pack(side="top", fill="both")
        main_frame.pack(side="top", fill="x")
