import tkinter as tk
from tkinter import ttk, filedialog


class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Notepad")
        self.geometry("800x600")

        self.create_menu()
        self.create_tabs()
        self.bind_shortcuts()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Create", command=self.create_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.add_tab(file_path, content)

    def create_file(self):
        self.add_tab("Untitled", "")

    def save_file(self):
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab).winfo_children()[0]
        content = text_widget.get(1.0, tk.END)
        file_path = self.tab_control.tab(current_tab, "text")
        if file_path == "Untitled":
            self.save_as_file()
        else:
            with open(file_path, 'w') as file:
                file.write(content)

    def save_as_file(self):
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab).winfo_children()[0]
        content = text_widget.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)
            self.tab_control.tab(current_tab, text=file_path)

    def add_tab(self, title, content):
        frame = ttk.Frame(self.tab_control)
        text_widget = tk.Text(frame)
        text_widget.insert(tk.END, content)
        text_widget.pack(expand=1, fill="both")
        self.tab_control.add(frame, text=title)
        self.tab_control.select(frame)

    def bind_shortcuts(self):
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-n>", lambda event: self.create_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-Shift-s>", lambda event: self.save_as_file())


if __name__ == "__main__":
    app = Notepad()
    app.mainloop()
