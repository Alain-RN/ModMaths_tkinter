import csv
import random

# Nom du fichier CSV
nom_fichier = "donnees_xy.csv"

# Creer des données
nb_points = 1000
donnees = []

for _ in range(nb_points):
    x = random.randint(0, 10)
    y = random.randint(0, 10)
    donnees.append([x, y])

# Ecrire le fichier CSV
with open(nom_fichier, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y"])
    writer.writerows(donnees)

print(f"Fichier {nom_fichier} créé avec {nb_points} points.")