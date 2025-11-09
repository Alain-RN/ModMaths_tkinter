import csv
import math
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from core.reg_lineaire import regression_lineaire
from core.reg_lineaire import dessiner_regression


class PageRegressionLineaire(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pad_x = 24
        
        tk.Frame(self, height=40).pack()

        label = tk.Label(
            self, text="Regression lineaire", font=("Arial", 18), fg="white",
            background="#2c3e50", padx= 16, pady= 11, anchor="w"
        )
        label.pack(fill="x", pady=0, padx=pad_x)

        tk.Frame(self, height=24).pack()

        self.input_container()

    # Container pour les moyens d'entrer les donnees
    def input_container(self):
        container = ttk.Frame(self)
        container.pack(fill="x", pady=0, padx=24)

        container_impoter_csv = ttk.Frame(container)
        container_impoter_csv.pack(fill="x", pady=0, padx=13)

        # Si l'utilisateur veux importer(fichier CSV) son jeu de donnees
        ttk.Label(
            container_impoter_csv,
            text="Importer le fichier CSV : ",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, sticky="w", padx=0)

        ttk.Button(
            container_impoter_csv, 
            text="Importe",
            command=self.ouvrir_fichier
        ).grid(row=0, column=1, sticky="w")
        
        tk.Frame(container, height=14).pack()

        # Si l'utilisateur veux entrer manuelement son jeu de donnees
        ttk.Label(
            container,
            text="Saisie le jeu de donnees : ",
            font=("Arial", 12)
        ).pack(anchor="w", padx=12, pady=5)

        container_header_list = ttk.Frame(container)
        container_header_list.pack(anchor="w", padx=14, pady=0)

        tk.Label(
            container_header_list,
            text="x",
            font=("Arial", 12),
            fg="white",
            bg="#34495e",
            width=6,
        ).grid(row=1, column=0, sticky="w")
        
        tk.Label(
            container_header_list,
            text="y",
            font=("Arial", 12),
            fg="white",
            bg="#34495e",
            width=6
        ).grid(row=1, column=1, sticky="w", padx=2)

        hauteur_max = 140

        self.canvas = tk.Canvas(container, height=hauteur_max, borderwidth=0, background="#f0f0f0")
        self.canvas.pack(side="left", fill="x", expand=True, padx=12)
        # Scrollbar verticale attachée au canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.container_input_list = ttk.Frame(self.canvas)
        self.container_input_list.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # zone scrollable = taille du contenu
        )

        self.canvas.create_window((0, 0), window=self.container_input_list, anchor="nw")

        # Liste des entrer du couple(x, y) du jeu de donnees
        self.list_input_ligne = []

        # self.creer_ligne(container_input_list, 0)

        # Container des bouton => resulats et l'ajout de nouvelle ligne dans le jeu de donnees
        container_button = ttk.Frame(container)
        container_button.pack(fill="x", pady=0, padx=0)

        ttk.Button(
            container_button, 
            text=" + Nouvelle ligne", 
            command=lambda: self.creer_ligne(self.container_input_list, len(self.list_input_ligne))
            ).grid(row=0, column=0)
        
        ttk.Button(
            container_button, 
            text="Resultat",
            command=self.afficher_resultat
            ).grid(row=0, column=1)
    
    # Affichage du resultat avec le bouton pour affichage graphique
    def afficher_resultat(self):

        for widget in getattr(self, "container_widgets", []):
            widget.destroy()
        self.container_widgets = []

        container = tk.Frame(self)
        container.pack(fill="x", pady=6, padx=37)
        self.container_widgets.append(container)

        l_0 = ttk.Label(
            container,
            text="Resultat numerique :", 
            font=("Arial", 12, "bold")
        )
        l_0.pack(anchor="w", padx=0, pady=0)
        self.container_widgets.append(l_0)

        self.X_list = []
        self.Y_list = []

        aucun_resultat_message = ttk.Label(
            container,
            text="Aucun resultat", 
            font=("Arial", 11)
        )
        aucun_resultat_message.pack(anchor="w", padx=16, pady=6)

        if len(self.list_input_ligne) <= 1 :
            self.container_widgets.append(aucun_resultat_message)
            return
        
        for ligne in self.list_input_ligne:
            x_in = ligne[0].get().strip()
            y_in = ligne[1].get().strip()
            try:
                self.X_list.append(float(x_in))
                self.Y_list.append(float(y_in))
            except ValueError:
                self.X_list = []
                self.Y_list = []
                self.container_widgets.append(aucun_resultat_message)
                return
        # Supprimer le message si l'exraction s'est bien fait
        aucun_resultat_message.destroy()

        # Le resultat
        resultat = regression_lineaire(self.X_list, self.Y_list)
        
        # La fonction modele
        l_modele = ttk.Label(
            container,
            text=f"Modele: {resultat["equation"]}", 
            font=("Arial", 12)
        )
        l_modele.pack(anchor="w", padx=16, pady=8)
        self.container_widgets.append(l_modele)

        # La precion du modele
        acc = resultat['R2'] * 100
        # si le var a predire sont tous les memes(test)
        if math.isnan(acc):
            acc = 100
        l_precison = ttk.Label(
            container,
            text=f"Pecision de la modele: {acc:.4f}%", 
            font=("Arial", 12)
        )
        l_precison.pack(anchor="w", padx=16)
        self.container_widgets.append(l_precison)

        l_err_moyenne = ttk.Label(
            container,
            text=f"Erreur moyenne: {resultat['erreur_moyenne']:.4f}", 
            font=("Arial", 12)
        )
        l_err_moyenne.pack(anchor="w", padx=16, pady=8)
        self.container_widgets.append(l_err_moyenne)

        btn_graphique = ttk.Button(
            container,
            text="Graphique",
            command=lambda:dessiner_regression(resultat)
        )
        btn_graphique.pack(anchor="w", padx=16)

        print(resultat)

    # Creer une ligne a remplire
    def creer_ligne(self, container, index):
        widget_list = []

        x_in = ttk.Entry(container, width=9)
        x_in.grid(
            row=index + 1, 
            column=0, 
            sticky="w",
        )
        widget_list.append(x_in)

        y_in = ttk.Entry(container, width=9)
        y_in.grid(
            row=index + 1, 
            column=1, 
            sticky="w",
            padx=2
        )
        widget_list.append(y_in)

        supp_btn = ttk.Button(
            container,
            text="-",
            width=3,
            command=lambda widgets=widget_list: self.supprimer_ligne(widgets)
        )
        supp_btn.grid(row=index + 1, column=2, sticky="w", padx=4)
        widget_list.append(supp_btn)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

        self.list_input_ligne.append(widget_list)

    # Supprimer une ligne dans le jeu de donnees
    def supprimer_ligne(self, widget_list):
        for widget in widget_list:
            widget.destroy()
        self.list_input_ligne.remove(widget_list)
        
    # Ouvrir un fichier csv pour les jeux de donnnees et lire les donnees et le transformer en donnees manipulable
    def ouvrir_fichier(self):
        chemin_fichier = filedialog.askopenfilename(
            title="Selectionner un fichier",
            filetypes=(("Fichiers csc", "*.csv"), ("Tous les fichiers", "*.*"))
        )

        self.matrice_data = []

        for widget_list in self.list_input_ligne:
            for widget in widget_list:
                widget.destroy()

        self.list_input_ligne = []

        with open(chemin_fichier, "r", encoding="utf-8") as f:
            lecteur = csv.reader(f)
            next(lecteur)

            for ligne in lecteur:
                valeurs = [float(v) for v in ligne]
                self.matrice_data.append(valeurs)
            
        # print(self.matrice_data)

        for i in range(len(self.matrice_data)):
            self.creer_ligne(self.container_input_list, i)
            widget_list = self.list_input_ligne[i]
            widget_list[0].insert(0, self.matrice_data[i][0])
            widget_list[1].insert(0, self.matrice_data[i][1])