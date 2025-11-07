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

        c_container = self.contrainte_container()

        tk.Frame(self, height=4).pack()

        # Container pour les boutons Resoudre et Ajouter un nouveau contrainte
        btn_container = tk.Frame(self)
        btn_container.pack(fill="x", pady=0, padx=24)
        ttk.Button(btn_container, text="Resultat").grid(row=len(self.contrainte_list) + 2, column=0)
        ttk.Button(
            btn_container, 
            text="Nouveau contrainte",
            command=lambda: self.creer_contrainte(container=c_container, index=len(self.contrainte_list) + 1)
        ).grid(row=len(self.contrainte_list) + 2, column=7)


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

    # Container des contrainte pour ajouter ou enlever des contrainte
    def contrainte_container(self) :
        container = tk.Frame(self)
        container.pack(fill="x", pady=0, padx=24)
        self.contrainte_list = []
        

        ttk.Label(
            container, 
            text="Les contraintes :",
            font=("Arial", 12) ).grid(row=0, column=0, sticky="w", columnspan=20)
        
        # Afficher tout les contrainte
        self.creer_contrainte(container=container, index=1)

        return container

    # Creer un widget pour une contrainte
    def creer_contrainte(self, container, index):
        contrainte = []

        space = ttk.Label(container, text="     ")
        space.grid(row=index, column=0, pady=4)
        contrainte.append(space)

        # Coefficient de "x" a l'index "1"
        x_in = ttk.Entry(container, width=4)
        x_in.grid(row=index, column=1)
        contrainte.append(x_in)

        l1 = ttk.Label(container, text=" x + ", font=("Arial", 10))
        l1.grid(row=index, column=2)
        contrainte.append(l1)

        # Coefficient de "y" a l'index "3"
        y_in = ttk.Entry(container, width=4)
        y_in.grid(row=index, column=3)
        contrainte.append(y_in)

        l2 = ttk.Label(container, text=" y ", font=("Arial", 10))
        l2.grid(row=index, column=4)
        contrainte.append(l2)

        # Signe d'inegalite pour le contraite a l'index "5"
        signe = ttk.Entry(container, width=4)
        signe.grid(row=index, column=5)
        signe.insert(0, "<=")
        contrainte.append(signe)

        # Le second membre du contrainte a l'index "6"
        second_membre = ttk.Entry(container, width=4,)
        second_membre.grid(row=index, column=6, padx=10)
        contrainte.append(second_membre)

        supprimer_contrainte = ttk.Button(
            container,
            text=f"-",
            width=3,
            command=lambda: self.suppr_contrainte(index=index)
        )
        supprimer_contrainte.grid(row=index, column=7, padx=4)
        contrainte.append(supprimer_contrainte)

        self.contrainte_list.append(contrainte)

    def suppr_contrainte(self, index):
        # Supprimer la contrainte graphiquement
        contrainte = self.contrainte_list.pop(index - 1)
        for widget in contrainte:
            widget.destroy()

        # Reindexer les autres contraintes pour eviter le decalage
        for i, contrainte in enumerate(self.contrainte_list, start=1):
            btn = contrainte[-1]
            btn.config(text=f"-", command=lambda i=i: self.suppr_contrainte(i))
