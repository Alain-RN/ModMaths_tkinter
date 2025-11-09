import tkinter as tk
from tkinter import ttk
from core.prog_lineaire import resultat_optimal
from core.prog_lineaire import afficher_graph

# La page pour la regression lineaire
class PageProgrammationLineaire(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pad_x = 24
        
        tk.Frame(self, height=40).pack()

        label = tk.Label(
            self, text="Programmation lineaire", font=("Arial", 18), fg="white",
            background="#2c3e50", padx= 16, pady= 11, anchor="w"
        )
        label.pack(fill="x", pady=0, padx=pad_x)

        tk.Frame(self, height=17).pack()

        self.objective_container()

        ttk.Label(
            self, 
            text="Les contraintes :",
            font=("Arial", 12) ).pack(anchor="w", padx=36, pady=4)

        c_container = self.contrainte_container()

        tk.Frame(self, height=4).pack()

        # Container pour les boutons Resoudre et Ajouter un nouveau contrainte
        btn_container = tk.Frame(self)
        btn_container.pack(fill="x", pady=4, padx=39)
        ttk.Button(
            btn_container, 
            text="Resultat",
            command= self.resultat_opt
        ).grid(row=len(self.contrainte_list) + 2, column=1)

        ttk.Button(
            btn_container, 
            text=" + Nouvelle ligne",
            command=lambda: self.creer_contrainte(container=c_container, index=len(self.contrainte_list) + 1)
        ).grid(row=len(self.contrainte_list) + 2, column=0)

        tk.Frame(self, height=12).pack()

    # Widget container pour la fonction Objective a Maximiser ou a Minimiser
    def objective_container(self) :

        container = tk.Frame(self)
        container.pack(fill="x", pady=8, padx=36)
        self.z = {}

        tk.Label(
            container, 
            text="Fonction objective : ", 
            font=("Arial", 12, "bold") ).grid(row=0, column=0, sticky="w")

        self.coeff_x = ttk.Entry(container, width=5)
        self.coeff_x.grid(row=0, column=1)

        tk.Label(
            container, 
            text=" x +", 
            font=("Arial", 11) ).grid(row=0, column=2)

        self.coeff_y = ttk.Entry(container, width=5)
        self.coeff_y.grid(row=0, column=3)

        tk.Label(container, text=" y", font=("Arial", 11)).grid(row=0, column=4)

        # Selectionner si on veux maximiser ou minimiser(par defaut maximiser)
        self.type_var = tk.StringVar(value="max")

        tk.Radiobutton(
            container, 
            text="Maximiser", 
            variable=self.type_var, 
            value="max", 
            font=("Arial", 10, "bold") ).grid(row=1, column=0, sticky="w", pady=8)
        
        tk.Radiobutton(
            container, 
            text="Minimiser", 
            variable=self.type_var, 
            value="min", 
            font=("Arial", 10, "bold") ).grid(row=1, column=6, sticky="w", pady=8)

    # Container des contrainte pour ajouter ou enlever des contrainte
    def contrainte_container(self) :
        c_principale = ttk.Frame(self)
        c_principale.pack(fill="x", pady=0, padx=36)

        hauteur_max = 100

        self.canvas = tk.Canvas(c_principale, height=hauteur_max, borderwidth=0, background="#f0f0f0")
        self.canvas.pack(side="left", fill="x", expand=True, padx=2, pady=2)
        # Scrollbar verticale attachée au canvas
        scrollbar = ttk.Scrollbar(c_principale, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        container = tk.Frame(self.canvas)
        container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # zone scrollable = taille du contenu
        )

        self.canvas.create_window((0, 0), window=container, anchor="nw")

        self.contrainte_list = []
        
        # Afficher tout les contrainte
        self.creer_contrainte(container=container, index=1)

        return container

    # Creer un widget pour une contrainte
    def creer_contrainte(self, container, index):
        contrainte = []

        # Coefficient de "x" a l'index "0"
        x_in = ttk.Entry(container, width=5)
        x_in.grid(row=index, column=0)
        contrainte.append(x_in)

        l1 = ttk.Label(container, text=" x + ", font=("Arial", 10))
        l1.grid(row=index, column=1)
        contrainte.append(l1)

        # Coefficient de "y" a l'index "2"
        y_in = ttk.Entry(container, width=5)
        y_in.grid(row=index, column=2)
        contrainte.append(y_in)

        l2 = ttk.Label(container, text=" y ", font=("Arial", 10))
        l2.grid(row=index, column=3)
        contrainte.append(l2)

        # Signe d'inegalite pour le contraite a l'index "4"
        signe = ttk.Entry(container, width=5)
        signe.grid(row=index, column=4)
        signe.insert(0, "<=")
        contrainte.append(signe)

        # Le second membre du contrainte a l'index "5"
        second_membre = ttk.Entry(container, width=5)
        second_membre.grid(row=index, column=5, padx=10)
        contrainte.append(second_membre)

        supprimer_contrainte = ttk.Button(
            container,
            text=f"-",
            width=3,
            command=lambda: self.suppr_contrainte(index=index)
        )
        supprimer_contrainte.grid(row=index, column=6, padx=4)
        contrainte.append(supprimer_contrainte)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

        self.contrainte_list.append(contrainte)

    # Supprimer une contrainte dans la liste avec son index
    def suppr_contrainte(self, index):
        # Supprimer la contrainte graphiquement
        contrainte = self.contrainte_list.pop(index - 1)
        for widget in contrainte:
            widget.destroy()

        # Reindexer les autres contraintes pour eviter le decalage
        for i, contrainte in enumerate(self.contrainte_list, start=1):
            btn = contrainte[-1]
            btn.config(text=f"-", command=lambda i=i: self.suppr_contrainte(i))

    # Extraire les coefficients du fonction objective
    def extraire_objective_coeff(self):
        c_x = self.coeff_x.get().strip()
        c_y = self.coeff_y.get().strip()
        if not self.is_number(c_x) or not self.is_number(c_y):
            return None
        return [
            self.to_number(c_x),
            self.to_number(c_y)
        ]

    # Extraire les donnees des inputs de chaque contrainte et verifier en meme temps la validite de chque valeurs
    def extraire_valeur_contrainte(self):
        contrainte_data_list = []
        for contrainte in self.contrainte_list:
            contrainte_data = {}
            coeff_x = contrainte[0].get()
            coeff_y = contrainte[2].get()
            signe = contrainte[4].get()
            second_membre = contrainte[5].get()

            if not self.is_number(coeff_x) or not self.is_number(coeff_y) or not self.is_number(second_membre) or not self.is_signe(signe):
                print("Hello")
                return None
            
            contrainte_data["coefficient"] = [self.to_number(coeff_x), self.to_number(coeff_y)]
            contrainte_data["signe"] = signe.strip()
            contrainte_data["second_membre"] = self.to_number(second_membre)

            contrainte_data_list.append(contrainte_data)
        print(contrainte_data_list)
        return contrainte_data_list

    # Verifier si c'est un nombre
    def is_number(self, val) :
        try:
            float(val.strip())
            return True
        except ValueError:
            print(f"'{val}' n'est pas un nombre valide")
            return False

    # Convertir en nombre
    def to_number(self, val) :
        try:
            return float(val.strip())
        except ValueError:
            print(f"Erreur : '{val}' n'est pas un nombre valide")
            return None

    # Verifier si le signe est un signe d'inegalite
    def is_signe(self, signe):
        signe_valide = ["<=", ">="]
        return signe.strip() in signe_valide
    
    # Afficher le resultat optimal avec le bouton d'affichage graphique
    def resultat_opt(self): 
        for widget in getattr(self, "container_resultat", []):
            widget.destroy()
        self.container_resultat = []       
        
        l_0 = ttk.Label(
            self, 
            text="Resultat numerique :", 
            font=("Arial", 12, "bold")
            )
        l_0.pack(fill="x", padx=36, pady=4)
        self.container_resultat.append(l_0)

        container = tk.Frame(self)   
        container.pack(fill="x", pady=0, padx=36) 
        self.container_resultat.append(container)

        l_1 = tk.Label(
            container, 
            text="  Aucun resultat", 
            font=("Arial", 11)
            )
        l_1.grid(row=0, column=0, columnspan= 10, sticky="w", pady= 4)

        if self.extraire_objective_coeff() == None:
            self.container_resultat.append(l_1)
            return
        if self.extraire_valeur_contrainte() == None:
            self.container_resultat.append(l_1)
            return
        
        l_1.destroy()

        resultat_dict = resultat_optimal(
            self.extraire_objective_coeff(),
            self.extraire_valeur_contrainte(),
            self.type_var.get()
            )

        l_x = tk.Label(
            container, 
            text=f"  X optimal = {resultat_dict["x_max"]}", 
            font=("Arial", 12)
            )
        l_x.grid(row=0, column=0, columnspan= 10, sticky="w", pady= 0)
        self.container_resultat.append(l_x)

        
        l_y = tk.Label(
            container, 
            text=f"  Y optimal = {resultat_dict["y_max"]}", 
            font=("Arial", 12)
            )
        l_y.grid(row=1, column=0, columnspan= 10, sticky="w", pady= 4)
        self.container_resultat.append(l_y)

        l_val_opt = tk.Label(
            container, 
            text=f"  Valeur optimal = {resultat_dict["val_optimal"]}", 
            font=("Arial", 12)
            )
        l_val_opt.grid(row=2, column=0, columnspan= 10, sticky="w", pady= 0)
        self.container_resultat.append(l_val_opt)

        btn_graphique = ttk.Button(
            container, 
            text="Graphique", 
            command=lambda:afficher_graph(
                self.extraire_valeur_contrainte(),
                resultat_dict
            )
        )
        btn_graphique.grid(row=3, column=0, sticky="w",padx=6, pady= 6)
        self.container_resultat.append(btn_graphique)
