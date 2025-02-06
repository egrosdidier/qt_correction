{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import tkinter as tk\
from tkinter import messagebox\
import numpy as np\
import matplotlib.pyplot as plt\
\
# Fonction pour calculer QTc selon diff\'e9rentes formules\
def calculate_qtc(qt, rr, formula):\
    if formula == "Bazett":\
        return qt / (rr ** 0.5)\
    elif formula == "Fridericia":\
        return qt / (rr ** (1/3))\
    elif formula == "Framingham":\
        return qt + 0.154 * (1 - rr)\
    elif formula == "Hodges":\
        return qt + 1.75 * (60 / rr - 60)\
    else:\
        return None\
\
# Fonction principale pour r\'e9cup\'e9rer les donn\'e9es et afficher les r\'e9sultats\
def compute_qtc():\
    try:\
        # R\'e9cup\'e9ration des valeurs saisies\
        if qt_type.get() == "ms":\
            qt = float(entry_qt.get())\
        else:\
            qt = float(entry_qt.get()) * 40  # Un petit carr\'e9 = 40 ms\
        \
        hr = float(entry_hr.get())\
        rr = 60 / hr  # Intervalle RR en secondes\
        \
        qtc_values = \{formula: calculate_qtc(qt, rr, formula) for formula in ["Bazett", "Fridericia", "Framingham", "Hodges"]\}\
        \
        # D\'e9termination du risque\
        interpretation = ""\
        qtc_bazett = qtc_values["Bazett"]\
        if qtc_bazett > 500:\
            interpretation = "Tr\'e8s \'e9lev\'e9 (Torsades de Pointes probables)"\
        elif qtc_bazett > 470 and sex_var.get() == "Femme":\
            interpretation = "\'c9lev\'e9 (Torsades de Pointes possibles)"\
        elif qtc_bazett > 450 and sex_var.get() == "Homme":\
            interpretation = "\'c9lev\'e9 (Torsades de Pointes possibles)"\
        else:\
            interpretation = "Risque faible"\
        \
        result_text.set(f"QTc (Bazett): \{qtc_values['Bazett']:.1f\} ms\\n"\
                        f"QTc (Fridericia): \{qtc_values['Fridericia']:.1f\} ms\\n"\
                        f"QTc (Framingham): \{qtc_values['Framingham']:.1f\} ms\\n"\
                        f"QTc (Hodges): \{qtc_values['Hodges']:.1f\} ms\\n"\
                        f"\\nInterpr\'e9tation: \{interpretation\}")\
        \
        plot_qtc_distribution(qtc_bazett)\
    except ValueError:\
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")\
\
# Fonction pour tracer la distribution du risque\
def plot_qtc_distribution(qtc_value):\
    x = np.linspace(350, 550, 1000)\
    y = np.exp(-((x - 450) / 40) ** 2)\
    \
    plt.figure(figsize=(6, 4))\
    plt.plot(x, y, label="Risque de TdP")\
    plt.axvline(qtc_value, color='r', linestyle='--', label=f'QTc: \{qtc_value:.1f\} ms')\
    plt.xlabel("QTc (ms)")\
    plt.ylabel("Risque relatif")\
    plt.title("Distribution du risque de TdP")\
    plt.legend()\
    plt.show()\
\
# Interface graphique avec Tkinter\
root = tk.Tk()\
root.title("Calcul du QT corrig\'e9")\
\
# Variables\
qt_type = tk.StringVar(value="ms")\
sex_var = tk.StringVar(value="Homme")\
result_text = tk.StringVar()\
\
# Widgets\
frame = tk.Frame(root)\
frame.pack(pady=10)\
\
tk.Label(frame, text="QT (ms ou petits carreaux):").grid(row=0, column=0)\
entry_qt = tk.Entry(frame)\
entry_qt.grid(row=0, column=1)\
\
tk.Label(frame, text="Fr\'e9quence cardiaque (bpm):").grid(row=1, column=0)\
entry_hr = tk.Entry(frame)\
entry_hr.grid(row=1, column=1)\
\
# Choix du sexe\
tk.Label(frame, text="Sexe:").grid(row=2, column=0)\
tk.Radiobutton(frame, text="Homme", variable=sex_var, value="Homme").grid(row=2, column=1)\
tk.Radiobutton(frame, text="Femme", variable=sex_var, value="Femme").grid(row=2, column=2)\
\
# Choix de l'unit\'e9 de QT\
tk.Label(frame, text="Unit\'e9 QT:").grid(row=3, column=0)\
tk.Radiobutton(frame, text="ms", variable=qt_type, value="ms").grid(row=3, column=1)\
tk.Radiobutton(frame, text="Petits carreaux", variable=qt_type, value="carreaux").grid(row=3, column=2)\
\
# Bouton de calcul\
tk.Button(root, text="Calculer", command=compute_qtc).pack(pady=5)\
\
# Affichage des r\'e9sultats\
tk.Label(root, textvariable=result_text, justify="left").pack()\
\
# Lancement de l'interface\
tk.mainloop()\
}