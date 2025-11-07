import tkinter as tk
from tkinter import ttk

# La page pour la regression lineaire
class PageRegressionLineaire(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pad_x = 24
        
        tk.Frame(self, height=24).pack()

        label = ttk.Label(self, text="Regression lineaire", font=("Arial", 24))
        label.pack(fill="x", pady=0, padx=pad_x)

        tk.Frame(self, height=12).pack()

        self.objective_container()

        tk.Frame(self, height=16).pack()

    # Widget container pour la fonction Objective a Maximiser ou a Minimiser
    def objective_container(self) :

        container = tk.Frame(self)
        container.pack(fill="x", pady=0, padx=24)
        self.z = {}

        tk.Label(
            container, 
            text="Fonction objective : ", 
            font=("Arial", 12) ).grid(row=0, column=0, sticky="w")

        x = ttk.Entry(container, width=4)
        x.grid(row=0, column=1)

        tk.Label(
            container, 
            text="  x  + ", 
            font=("Arial", 10) ).grid(row=0, column=2)

        y = ttk.Entry(container, width=4)
        y.grid(row=0, column=3)

        tk.Label(container, text=" y", font=("Arial", 10)).grid(row=0, column=4)

        # Selectionner si on veux maximiser ou minimiser(par defaut maximiser)
        self.type_var = tk.StringVar(value="max")

        tk.Radiobutton(
            container, 
            text="Maximiser", 
            variable=self.type_var, value="max", font=("Arial", 10) ).grid(row=1, column=0, sticky="w", pady=8)
        
        tk.Radiobutton(
            container, 
            text="Minimiser", 
            variable=self.type_var, 
            value="min", 
            font=("Arial", 10) ).grid(row=1, column=6, sticky="w", pady=8)

        ttk.Button(
            container, 
            text="Valider", 
            command=self.contrainte_container ).grid(row=2, column=0, sticky="w")

    # Container des contrainte pour ajouter ou enlever des contrainte
    def contrainte_container(self) :
        for widget in getattr(self, "contrainte_container_elements", []):
            widget.destroy()
        self.contrainte_container_elements = []

        container = tk.Frame(self)
        container.pack(fill="x", pady=0, padx=24)
        self.contrainte_container_elements.append(container)

        l_0 = ttk.Label(
            container, 
            text="Les contraintes :",
            font=("Arial", 12) )
        l_0.grid(row=0, column=0, sticky="w")
        self.contrainte_container_elements.append(l_0)

        



