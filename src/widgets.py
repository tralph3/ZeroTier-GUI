import tkinter as tk
from tkinter import ttk

BACKGROUND = "#d9d9d9"
FOREGROUND = "black"
BUTTON_BACKGROUND = "#ffb253"
BUTTON_ACTIVE_BACKGROUND = "#ffbf71"
FONTSIZE = 40


class Button(tk.Button):
    def __init__(
        self,
        *args,
        bg=BUTTON_BACKGROUND,
        fg=FOREGROUND,
        justify="left",
        activbackground=BUTTON_ACTIVE_BACKGROUND,
        activeforeground=FOREGROUND,
        **kwargs
    ) -> None:
        super().__init__(
            *args,
            bg=bg,
            fg=fg,
            justify=justify,
            activebackground=activbackground,
            activeforeground=activeforeground,
            **kwargs
        )


class Frame(tk.Frame):
    def __init__(self, *args, bg=BACKGROUND, **kwargs) -> None:
        super().__init__(*args, bg=bg, **kwargs)


class Label(tk.Label):
    def __init__(
        self, *args, bg=BACKGROUND, fg=FOREGROUND, font=FONTSIZE, **kwargs
    ) -> None:
        super().__init__(*args, bg=bg, fg=fg, font=font, **kwargs)


class Scrollbar(tk.Scrollbar):
    def __init__(self, *args, bd=2, bg=BACKGROUND, **kwargs) -> None:
        super().__init__(*args, bd=bd, bg=bg, **kwargs)


class TreeView(ttk.Treeview):
    def __init__(self, root, *columns):
        super().__init__(root)

        self["columns"] = tuple(columns)
        self.column("#0", width=0, stretch=tk.NO)

        for label in columns:
            self.heading(label, text=label)
        self.configure_style()

    def configure_style(self):
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Monospace", 11))
        self.style.configure("Treeview", font=("Monospace", 11))
        self.style.layout(
            "Treeview", [("Treeview.treearea", {"sticky": "nswe"})]
        )
        self.tag_configure("odd", background="#fcfcfc")
        self.tag_configure("even", background="#eeeeee")
        self.tag_configure("disabled", background="#d14444")

    def insert(self, values, disabled=False, **kwargs):
        item_count = len(self.get_children())
        tag = "even" if item_count % 2 == 0 else "odd"
        if disabled:
            tag = "disabled"
        super().insert(
            "", tk.END, iid=item_count, values=values, tags=tag, **kwargs
        )
