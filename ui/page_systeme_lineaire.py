import tkinter as tk
from tkinter import ttk
import numpy as np
from core.gauss import resoudre_systeme

class PageSystemeLineaire(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pad_x = 24
        
        tk.Frame(self, height=24).pack()

        label = ttk.Label(self, text="Systeme lineaire", font=("Arial", 24))
        label.pack(fill="x", pady=0, padx=pad_x)

        tk.Frame(self, height=12).pack()

        # Input pour entrer le nombre de variable
        container_input_n = tk.Frame(self)
        container_input_n.pack(fill="x", pady=0, padx=pad_x)

        ttk.Label(container_input_n, text="Nombre de variables (n > 1) :  ", font=("Arial", 11)).grid(row=0, column= 0)
        self.input_n = ttk.Entry(container_input_n, width=12)
        self.input_n.grid(row=0, column=1)
        ttk.Button(container_input_n, text="Valider", command= self.generer_matrice).grid(row=0, column= 2,padx=8)

        tk.Frame(self, height=18).pack()

    # Verifier si tous les matrices sont vraiment remplis
    def verifier_inputs(self):
            # Verifier inputs_A
            for key, entry in self.inputs_A.items():
                if entry.get().strip() == "":
                    print(f"L'entrée {key} dans A est vide !")
                    return False

            # Verifier inputs_b
            for key, entry in self.inputs_b.items():
                if entry.get().strip() == "":
                    print(f"L'entrée {key} dans b est vide !")
                    return False

            print("Toutes les Entry sont remplies !")
            return True
    
    # Extraire la matrice A des coefficients
    def extraire_A(self):
        self.A = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                entry = self.inputs_A[f"x({i},{j})"]
                val = entry.get().strip()
                try:
                    self.A[i, j] = float(val)
                except ValueError:
                    print(f"Erreur : entree A[{i},{j}] invalide")
                    return False
        return True
    
    # Extraire la matrice b des seconds membres
    def extraire_b(self):
        self.b = np.zeros(self.n)
        for i in range(self.n):
            entry = self.inputs_b[i]
            val = entry.get().strip()
            if val == "":
                val = 0
            try:
                self.b[i] = float(val)
            except ValueError:
                print(f"Erreur : entree b[{i}] invalide")
                return False
        return True  

    # Recuper la valeur de n apres validation de l'input correspendant
    def valider_input_n(self):
        val = self.input_n.get().strip()
        if val == "":
            return 0
        try:
            n = int(val)
        except ValueError:
            print("Veuillez entrer un nombre entier !")
            return 0
        
        print(n)
        return n
    
    # Generer et met a jour les widgets la matrice du systeme lineaire 
    def generer_matrice(self):
        # Supprimer les anciens widgets si on reclique sur le botton
        for widget in getattr(self, "container_inputs_widgets", []):
            widget.destroy()

        for widget in getattr(self, "container_solution_widgets", []):
            widget.destroy()
        self.container_inputs_widgets = []

        self.n = self.valider_input_n()
        if self.n < 2:
            return

        # Container pour les inputs des matrices
        container_inputs = tk.Frame(self)
        container_inputs.pack(fill="x", pady=0, padx=24)
        self.container_inputs_widgets.append(container_inputs)

        self.inputs_A = {}
        self.inputs_b = {}

        for i in range(self.n):
            for j in range(self.n):
                entry = ttk.Entry(container_inputs, width=5)
                entry.grid(row=i, column=2*j, padx=2, pady=2)
                self.inputs_A[f"x({i},{j})"] = entry
                self.container_inputs_widgets.append(entry)

                label_text = f"x{j+1}  +" if j + 1 != self.n else f"x{j+1}  ="
                label = ttk.Label(container_inputs, text=label_text)
                label.grid(row=i, column=2*j+1, padx=2, pady=2)
                self.container_inputs_widgets.append(label)

            entry = ttk.Entry(container_inputs, width=5)
            entry.grid(row=i, column=2*self.n, padx=2, pady=2)
            self.inputs_b[i] = entry
            self.container_inputs_widgets.append(entry)

        # Bouton Afficher
        btn = tk.Button(container_inputs, text="Resoudre", command=self.generer_solution, padx=12)
        btn.grid(row=self.n, column=0,columnspan=2, pady=18)
        self.container_inputs_widgets.append(btn)

    # Genere les widgets des solution du Systeme
    def generer_solution(self):
        for widget in getattr(self, "container_solution_widgets", []):
            widget.destroy()
        self.container_solution_widgets = []
        
        if not self.verifier_inputs():
            return
        
        if not self.extraire_A():
            return
        
        if not self.extraire_b():
            return
        
        # Container pour les solutions
        container_solution = tk.Frame(self)
        container_solution.pack(fill="x", pady=0, padx=24)
        self.container_solution_widgets.append(container_solution)
        
        label_title = tk.Label(container_solution, text="Solution :", font=("Arial", 14))
        label_title.grid(row=0, column=0, sticky="w", padx=0, pady= 4)
        self.container_solution_widgets.append(label_title)

        solutions = resoudre_systeme(self.A, self.b)

        if len(solutions) == 0:
            l = tk.Label(container_solution, text="     Pas de solution", font=("Arial", 12))
            l.grid(row=1, column=0, sticky="w", pady=2)
            self.container_solution_widgets.append(l)
            return

        for i, val in enumerate(solutions):
            # Label x1, x2, ...
            x_label = tk.Label(container_solution, text=f"      x{i+1} =", font=("Arial", 11))
            x_label.grid(row=i+1, column=0, sticky="w", pady=2, padx=0)
            self.container_solution_widgets.append(x_label)

            # Valeur de x1, x2, ...
            x_value = tk.Label(container_solution, text=f"{val}", font=("Arial", 12))
            x_value.grid(row=i+1, column=1, sticky="w", pady=2, padx=0)
            self.container_solution_widgets.append(x_value)







    

