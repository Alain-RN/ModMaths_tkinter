import pulp
import matplotlib.pyplot as plt
import numpy as np

def afficher_graph(contrainte_data_list=None, data_optimal=None):
    if contrainte_data_list is None:
        contrainte_data_list = []
    
    x_vals = np.linspace(0, 10, 400)
    
    plt.figure(figsize=(7, 7))
    
    # Tracer chaque contrainte
    for c in contrainte_data_list:
        a, b = c["coefficient"]
        signe = c["signe"]
        c_val = c["second_membre"]
        
        if b != 0:
            y = (c_val - a * x_vals) / b
            plt.plot(x_vals, y, label=f'{a}x + {b}y {signe} {c_val}')
        else:  # cas vertical x = c_val / a
            x = np.full_like(x_vals, c_val / a)
            plt.plot(x, x_vals, label=f'{a}x + {b}y {signe} {c_val}')
    
    # Définir limites selon contraintes
    plt.xlim(0, max(10, max([c["second_membre"] for c in contrainte_data_list])))
    plt.ylim(0, max(10, max([c["second_membre"] for c in contrainte_data_list])))
    
    # Tracer le point optimal
    if data_optimal:
        plt.scatter(data_optimal["x_max"], data_optimal["y_max"], color='red', s=100, label='Optimum')
        plt.text(data_optimal["x_max"], data_optimal["y_max"]+0.3,
                 f'({data_optimal["x_max"]}, {data_optimal["y_max"]})', color='red')
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graphique des contraintes et point optimal")
    plt.grid(True)
    plt.legend()
    plt.show()



def resultat_optimal(matrice_objective, contrainte_data_list, choix_optimisation):

    prob = pulp.LpProblem("Z", pulp.LpMaximize)

    if choix_optimisation == "min" :
        prob = pulp.LpProblem("Z", pulp.LpMinimize)

    x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

    prob += matrice_objective[0]*x + matrice_objective[1]*y, "z"

    for contraite_data in contrainte_data_list:
        c1 = contraite_data["coefficient"][0]
        c2 = contraite_data["coefficient"][1]
        signe = contraite_data["signe"]
        second_membre = contraite_data["second_membre"]

        if signe == "<=":
            prob += c1*x + c2*y <= second_membre
            continue
        
        prob += c1*x + c2*y >= second_membre

        # print(f"{c1}----{c2} {signe} {second_membre}")
    prob.solve()
    return {
        "x_max" : x.varValue,
        "y_max" : y.varValue,
        "val_optimal" : pulp.value(prob.objective)
    }

    

