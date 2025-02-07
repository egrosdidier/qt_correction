import numpy as np
import matplotlib.pyplot as plt

def calculate_qtc(qt, rr, method="Bazett"):
    """Calcule le QT corrigé en fonction de la méthode choisie."""
    if method == "Bazett":
        return qt / np.sqrt(rr)
    elif method == "Fridericia":
        return qt / (rr ** (1/3))
    elif method == "Framingham":
        return qt + 0.154 * (1 - rr)
    elif method == "Hodges":
        return qt + 1.75 * (60 / rr - 60)
    else:
        raise ValueError("Méthode non reconnue")

def interpret_qtc(qtc, sexe):
    """Interprétation du QTc en fonction du sexe."""
    seuil_bas = 350
    seuil_haut = 450 if sexe == "Homme" else 460
    
    if qtc < seuil_bas:
        return "QTc court (< 350 ms) - Risque arythmique"
    elif seuil_bas <= qtc <= seuil_haut:
        return "QTc normal"
    else:
        return "QTc allongé (> {} ms) - Risque de torsades de pointes".format(seuil_haut)

def plot_qtc_distribution(qtc):
    """Affiche la courbe de distribution du QTc avec la valeur mesurée."""
    x = np.linspace(300, 550, 100)
    mean_qtc = 400
    std_qtc = 30
    y = (1 / (std_qtc * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_qtc) / std_qtc) ** 2)
    
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label="Distribution normale du QTc")
    plt.axvline(qtc, color='r', linestyle='--', label=f"QTc mesuré: {qtc:.1f} ms")
    plt.fill_between(x, y, where=(x >= 450), color='red', alpha=0.3, label="Risque accru (>450 ms)")
    plt.fill_between(x, y, where=(x <= 350), color='blue', alpha=0.3, label="QTc court (<350 ms)")
    plt.xlabel("QTc (ms)")
    plt.ylabel("Densité de probabilité")
    plt.title("QTc et courbe de distribution du risque")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    print("\nCalcul du QTc et analyse du risque\n")
    
    qt_input = input("Entrez le QT (en ms ou en nombre de petits carreaux à 25mm/s) : ")
    try:
        qt = float(qt_input)
        if qt > 100:  # Supposons qu'une valeur en ms est >100 ms
            pass
        else:
            qt *= 40  # Conversion des petits carreaux en ms (1 carreau = 0.04s * 1000 ms)
    except ValueError:
        print("Entrée non valide.")
        return
    
    fc = float(input("Entrez la fréquence cardiaque (BPM) : "))
    sexe = input("Entrez le sexe (Homme/Femme) : ")
    
    rr = 60 / fc  # Intervalle RR en secondes
    
    print("\nMéthodes disponibles : Bazett, Fridericia, Framingham, Hodges")
    method = input("Choisissez une méthode (par défaut Bazett) : ") or "Bazett"
    
    qtc = calculate_qtc(qt, rr, method) * 1000  # Conversion en ms
    interpretation = interpret_qtc(qtc, sexe)
    
    print(f"\nRésultat:\nQTc ({method}) = {qtc:.1f} ms")
    print("Interprétation :", interpretation)
    
    plot_qtc_distribution(qtc)

if __name__ == "__main__":
    main()
