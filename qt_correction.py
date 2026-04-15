import streamlit as st
import numpy as np
import pandas as pd
import os
import datetime
import hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="QTc CSAPA MASTER", layout="wide")

# =====================
# UTILS
# =====================

def pseudonymize(text):
    return hashlib.sha256(text.encode()).hexdigest()[:10]


def calculate_qtc(qt_ms, rr_s, method):
    qt = qt_ms / 1000
    if method == "Bazett":
        return (qt / np.sqrt(rr_s)) * 1000
    elif method == "Fridericia":
        return (qt / (rr_s ** (1/3))) * 1000
    elif method == "Framingham":
        return (qt + 0.154 * (1 - rr_s)) * 1000
    elif method == "Hodges":
        return (qt + (1.75 * (60/rr_s - 60))/1000) * 1000


def interpret(qtc, sexe):
    if (sexe == "Homme" and qtc < 450) or (sexe == "Femme" and qtc < 470):
        return "🟢 QTc normal"
    elif qtc < 480:
        return "🟡 QTc limite"
    elif qtc < 500:
        return "🟠 QTc prolongé"
    else:
        return "🔴 QTc à haut risque (TdP)"

# =====================
# HEADER
# =====================
st.title("🫀 QTc CSAPA – VERSION MASTER")
st.markdown("Outil expert – addictologie cardiovasculaire")

mode = st.radio("Mode", ["Clinique", "Rapide", "Pédagogique"])

# =====================
# INPUT
# =====================
col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Identifiant patient")
    sexe = st.radio("Sexe", ["Homme", "Femme"])
with col2:
    date = st.date_input("Date", datetime.date.today())

qt = st.number_input("QT (ms)", min_value=0.0, help="Mesuré du début QRS à la fin de T")
fc = st.number_input("Fréquence cardiaque", min_value=1.0)
rr = 60 / fc if fc > 0 else 0

method = st.selectbox("Méthode", ["Bazett", "Fridericia", "Framingham", "Hodges"])

# =====================
# CALCUL
# =====================
if st.button("Analyser"):

    patient_id = pseudonymize(patient_name)
    qtc = calculate_qtc(qt, rr, method)
    conclusion = interpret(qtc, sexe)

    st.metric("QTc", f"{qtc:.1f} ms")
    st.subheader("Interprétation")
    st.write(conclusion)

    # =====================
    # PEDAGOGICAL MODE
    # =====================
    if mode == "Pédagogique":
        st.info("Le QTc corrige le QT en fonction de la fréquence cardiaque. Bazett surestime à FC élevée.")

    # =====================
    # FACTEURS
    # =====================
    if mode != "Rapide":
        st.subheader("Facteurs de risque")
        k = st.number_input("K+", value=4.0, help="Objectif ≥ 4.0")
        mg = st.number_input("Mg", value=0.8, help="Objectif ≥ 0.8")
        dfg = st.number_input("DFG", value=90)

        alerts = []
        if k < 3.5: alerts.append("Hypokaliémie")
        if mg < 0.7: alerts.append("Hypomagnésémie")
        if dfg < 30: alerts.append("Insuffisance rénale sévère")

        for a in alerts:
            st.warning(a)

    # =====================
    # DECISION
    # =====================
    st.subheader("Conduite à tenir")
    if qtc >= 500:
        decision = "Urgence : correction ionique + ECG 12 dérivations + avis cardiologique"
        st.error(decision)
    elif qtc >= 480:
        decision = "Corriger facteurs + recontrôle ECG"
        st.warning(decision)
    else:
        decision = "Surveillance"
        st.success(decision)

    # =====================
    # SAVE
    # =====================
    file_path = "patients_master.csv"

    data = {
        "Date": date,
        "Patient": patient_id,
        "QTc": round(qtc,1),
        "Conclusion": conclusion
    }

    df_new = pd.DataFrame([data])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(file_path, index=False)

    # =====================
    # HISTORY
    # =====================
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df_p = df[df["Patient"] == patient_id]
        if not df_p.empty:
            st.line_chart(df_p["QTc"])

    # =====================
    # PDF EXPORT
    # =====================
    if st.button("Générer PDF"):
        doc = SimpleDocTemplate("rapport_master.pdf")
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph("Compte rendu QTc – CSAPA", styles['Title']))
        content.append(Spacer(1,12))
        content.append(Paragraph(f"Date : {date}", styles['Normal']))
        content.append(Paragraph(f"Patient ID : {patient_id}", styles['Normal']))
        content.append(Paragraph(f"QTc : {qtc:.1f} ms", styles['Normal']))
        content.append(Paragraph(f"Conclusion : {conclusion}", styles['Normal']))
        content.append(Paragraph(f"Conduite : {decision}", styles['Normal']))

        doc.build(content)

        with open("rapport_master.pdf", "rb") as f:
            st.download_button("Télécharger PDF", f, file_name="rapport_master.pdf")

st.caption("Version MASTER – outil expert CSAPA")
