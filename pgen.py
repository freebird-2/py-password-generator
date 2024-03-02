import tkinter as tk
import random
import logging
import string
import re
from tkinter import ttk

logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d) :\n%(message)s\n')

WINDOW_TITLE = 'Password Generator'

def random_string(chars: set[str], length: int, repeat: bool) -> str:
    char_list = list(chars)
    result = random.choices(char_list, k=length) if repeat else random.sample(char_list, length)
    return ''.join(result)

def is_integer(value: str) -> bool:
    return re.search(r'^\d+$', value) is not None

class Display(ttk.Frame):

    def __init__(self, parent, result_var: tk.StringVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.text_var = result_var

        self.result_text = ttk.Label(
            self,
            textvariable=result_var,
            width=50,
            relief=tk.SOLID
        )
        self.copy_button = ttk.Button(
            self,
            text='Copy',
            command=lambda: self.copy_result(),
        )

        self.copy_button.grid(row=0, column=0, padx=(0, 5))
        self.result_text.grid(row=0, column=1)

    def copy_result(self):
        self.clipboard_clear()
        self.clipboard_append(self.text_var.get())

class Generator(ttk.Frame):

    DEFAULT_PASSWORD_LENGTH = 20

    def __init__(self, parent, result_var: tk.StringVar, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.result_var = result_var
        self.length_var = tk.StringVar()
        self.uppercase_var = tk.IntVar(value=1)
        self.lowercase_var = tk.IntVar(value=1)
        self.digits_var = tk.IntVar(value=1)
        self.symbols_var = tk.IntVar(value=1)
        self.repeat_var = tk.IntVar(value=1)

        self.include_label = ttk.Label(
            self,
            text='Include',
        )
        self.include_label_frame = ttk.LabelFrame(
            self,
            labelwidget=self.include_label
        )
        self.length_frame = ttk.Frame(self)
        self.generate_button = ttk.Button(
            self,
            text='Generate',
            command=self.generate_password
        )
        self.increment_button = ttk.Button(
            self.length_frame,
            text='+',
            width=2,
            command=lambda: self.change_length_input(1)
        )
        self.decrement_button = ttk.Button(
            self.length_frame,
            text='-',
            width=2,
            command=lambda: self.change_length_input(-1)

        )
        self.length_label = ttk.Label(
            self.length_frame,
            text='Length:',
        )
        self.length_entry = ttk.Entry(
            self.length_frame,
            width=5,
            validate='key',
            validatecommand=(self.register(self.validate_length_input), '%P'),
            textvariable=self.length_var
        )
        self.length_entry.insert(tk.END, str(self.DEFAULT_PASSWORD_LENGTH))
        self.uppercase_checkbox = ttk.Checkbutton(
            self.include_label_frame,
            text='Uppercase letters',
            variable=self.uppercase_var
        )
        self.lowercase_checkbox = ttk.Checkbutton(
            self.include_label_frame,
            text='Lowercase letters',
            variable=self.lowercase_var
        )
        self.digits_checkbox = ttk.Checkbutton(
            self.include_label_frame,
            text='Digits',
            variable=self.digits_var
        )
        self.symbols_checkbox = ttk.Checkbutton(
            self.include_label_frame,
            text='Symbols',
            variable=self.symbols_var
        )
        self.repeat_checkbox = ttk.Checkbutton(
            self,
            text='Allow repeated characters',
            variable=self.repeat_var
        )


        self.length_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.length_entry.grid(row=0, column=1, padx=(0, 5))
        self.increment_button.grid(row=0, column=2)
        self.decrement_button.grid(row=0, column=3)

        self.uppercase_checkbox.grid(row=0, column=0, sticky=tk.W)
        self.lowercase_checkbox.grid(row=1, column=0, sticky=tk.W)
        self.digits_checkbox.grid(row=2, column=0, sticky=tk.W)
        self.symbols_checkbox.grid(row=3, column=0, sticky=tk.W)


        self.include_label_frame.grid(row=0, column=0, sticky=tk.W)
        self.repeat_checkbox.grid(row=5, column=0, sticky=tk.W, pady=(15, 0))
        self.length_frame.grid(row=6, column=0, sticky=tk.W, pady=(15, 0))
        self.generate_button.grid(row=7, column=0, sticky=tk.W, pady=(15, 0))

    def get_current_length(self) -> int:
        length_str = self.length_entry.get()
        return 0 if length_str == "" else int(length_str)

    def change_length_input(self, change: int) -> None:
        length = self.get_current_length()
        length += change
        if length >= 0:
            self.length_var.set(str(length))

    def validate_length_input(self, length_input: str) -> bool:
        return length_input == "" or is_integer(length_input)

    def generate_password(self) -> None:
        characters = set()
        if self.uppercase_var.get():
            characters.update(string.ascii_uppercase)
        if self.lowercase_var.get():
            characters.update(string.ascii_lowercase)
        if self.digits_var.get():
            characters.update(string.digits)
        if self.symbols_var.get():
            characters.update(string.punctuation)
        if len(characters) > 0:
            password = random_string(characters, self.get_current_length(), bool(self.repeat_var.get()))
            self.result_var.set(password)

class PasswordGenerator(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.result_var = tk.StringVar()

        font1 = ('Cascadia Code', 10)
        style = ttk.Style()
        style.configure('TButton', font=font1)
        style.configure('TCheckbutton', font=font1)
        style.configure('TLabel', font=font1)

        self.settings = Generator(self, self.result_var)
        self.sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.result = Display(self, self.result_var)

        self.settings.grid(row=0, column=0, sticky=tk.W)
        self.sep.grid(row=1, column=0, sticky=tk.W + tk.E, pady=20)
        self.result.grid(row=2, column=0, sticky=tk.W)

if __name__ == '__main__':
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.resizable(False, False)
    PasswordGenerator(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)
    root.mainloop()
