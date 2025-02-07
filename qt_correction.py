import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_qtc(qt, rr, method="Bazett"):
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

def plot_qtc_distribution(qtc):
    x = np.linspace(300, 550, 100)
    mean_qtc = 400
    std_qtc = 30
    y = (1 / (std_qtc * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_qtc) / std_qtc) ** 2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, label="Distribution normale du QTc")
    ax.axvline(qtc, color='r', linestyle='--', label=f"QTc mesuré: {qtc:.1f} ms")
    ax.fill_between(x, y, where=(x >= 450), color='red', alpha=0.3, label="Risque accru (>450 ms)")
    ax.fill_between(x, y, where=(x <= 350), color='blue', alpha=0.3, label="QTc court (<350 ms)")
    ax.set_xlabel("QTc (ms)")
    ax.set_ylabel("Densité de probabilité")
    ax.set_title("QTc et courbe de distribution du risque")
    ax.legend()
    ax.grid()
    
    return fig

# Interface Streamlit
st.title("Calcul du QT corrigé (QTc)")

qt_input_type = st.radio("Choisir la méthode de saisie du QT", ["Millisecondes", "Petits carreaux"])
qt = st.number_input("QT", min_value=0.0, format="%.1f")
if qt_input_type == "Petits carreaux":
    qt *= 40  # Conversion des petits carreaux en millisecondes

fc = st.number_input("Fréquence cardiaque (BPM)", min_value=1.0, format="%.1f")
sexe = st.radio("Sexe", ["Homme", "Femme"])
method = st.selectbox("Méthode de correction", ["Bazett", "Fridericia", "Framingham", "Hodges"])

if st.button("Calculer QTc"):
    rr = 60 / fc  # Intervalle RR en secondes
    qtc = calculate_qtc(qt, rr, method) * 1000  # Conversion en ms
    
    st.success(f"QTc ({method}) = {qtc:.1f} ms")
    
    fig = plot_qtc_distribution(qtc)
    st.pyplot(fig)
