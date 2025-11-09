import numpy as np

def regression_lineaire(X_list, Y_list):
    X = np.array(X_list, dtype=float)
    Y = np.array(Y_list, dtype=float)

    if len(X) != len(Y):
        raise ValueError("Les listes X et Y doivent avoir la meme taille.")
    if len(X) < 2:
        raise ValueError("Il faut au moins 2 points pour une regression.")

    # Moyennes
    mean_x = np.mean(X)
    mean_y = np.mean(Y)

    # Coefficient directeur a
    numerateur = np.sum((X - mean_x) * (Y - mean_y))
    denominateur = np.sum((X - mean_x) ** 2)
    a = numerateur / denominateur

    # Ordonnee à l’origine b
    b = mean_y - a * mean_x

    # Predictions
    Y_pred = a * X + b

    # Residus
    residus = Y - Y_pred
    somme_residus = np.sum(residus)

    # Coefficient de determination R2
    ss_res = np.sum((Y - Y_pred)**2)
    ss_tot = np.sum((Y - mean_y)**2)
    R2 = 1 - (ss_res / ss_tot)

    return {
        "a": a,
        "b": b,
        "equation": f"y = {a:.4f}x + {b:.4f}",
        "predictions": Y_pred.tolist(),
        "residus": residus.tolist(),
        "somme_residus": float(somme_residus),
        "erreur_moyenne": float(np.mean(np.abs(residus))),
        "R2": float(R2),
        "points": list(zip(X_list, Y_list))
    }

import matplotlib.pyplot as plt
import numpy as np

def dessiner_regression(resultat):

    X = np.array([p[0] for p in resultat['points']])
    Y = np.array([p[1] for p in resultat['points']])
    Y_pred = np.array(resultat['predictions'])
    residus = np.array(resultat['residus'])
    
    # Creer la figure
    plt.figure(figsize=(10, 6))
    
    # Tracer les points originaux
    plt.scatter(X, Y, color='blue', label='Points reels')
    
    # Tracer la droite de regression
    x_line = np.linspace(min(X)-1, max(X)+1, 100)
    y_line = resultat['a'] * x_line + resultat['b']
    plt.plot(x_line, y_line, color='red', label='Droite de regression')
    
    # Tracer les residus (lignes verticales entre points et droite)
    for xi, yi, y_pred_i in zip(X, Y, Y_pred):
        plt.plot([xi, xi], [yi, y_pred_i], color='gray', linestyle='--', linewidth=1)
    
    # Ajouter legende et titres
    plt.title(f"Regression lineaire : {resultat['equation']}\nR² = {resultat['R2']:.4f}, Erreur moyenne = {resultat['erreur_moyenne']:.4f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    plt.show()
