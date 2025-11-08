import tkinter as tk
from tkinter import ttk

class PageRegressionLineaire(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pad_x = 24
        
        tk.Frame(self, height=24).pack()

        label = ttk.Label(self, text="Regression lineaire", font=("Arial", 24))
        label.pack(fill="x", pady=0, padx=pad_x)

        tk.Frame(self, height=12).pack()