import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Quiz Mécanique 2BAC - Prof Anas", page_icon="🧪")

st.title("🧪 Diagnostic Mécanique : 2ème BAC")
st.write("Ce questionnaire contient 10 questions pour évaluer tes connaissances.")

# --- DÉBUT DU QUIZ ---
questions = []

# Q1
st.markdown("#### 1. Cinématique : Vecteur Vitesse")
st.latex(r"\vec{OM} = 4t \cdot \vec{i} + 2 \cdot \vec{j}")
q1 = st.radio("Quelle est la valeur de la vitesse v ?", ["v = 4 m/s", "v = 2 m/s", "v = 4t m/s"], index=None, key="q1")

# Q2
st.markdown("#### 2. Accélération")
q2 = st.radio("Si la vitesse est constante, l'accélération est :", ["Positive", "Nulle", "Négative"], index=None, key="q2")

# Q3
st.markdown("#### 3. Lois de Newton")
q3 = st.radio("La deuxième loi de Newton s'applique dans un référentiel :", ["Accéléré", "Tournant", "Galiléen"], index=None, key="q3")

# Q4
st.markdown("#### 4. Unités")
q4 = st.radio("Quelle est l'unité de la force dans le Système International ?", ["Joule (J)", "Newton (N)", "Watt (W)"], index=None, key="q4")

# Q5
st.markdown("#### 5. Repère de Frénet")
q5 = st.radio("L'accélération normale a_n est liée à :", ["Le changement de valeur de la vitesse", "Le changement de direction du mouvement", "La masse du corps"], index=None, key="q5")

# Q6
st.markdown("#### 6. Chute libre")
q6 = st.radio("En chute libre sans frottement, l'accélération est égale à :", ["g (intensité de pesanteur)", "0", "La vitesse initiale"], index=None, key="q6")

# Q7
st.markdown("#### 7. Énergie Cinétique")
q7 = st.radio("Si la vitesse est multipliée par 3, l'énergie cinétique est multipliée par :", ["3", "6", "9"], index=None, key="q7")

# Q8
st.markdown("#### 8. Plan incliné")
q8 = st.radio("Sur un plan incliné d'angle α sans frottement, l'accélération est :", ["a = g", "a = g * sin(α)", "a = 0"], index=None, key="q8")

# Q9
st.markdown("#### 9. Ressorts")
q9 = st.radio("La force de rappel d'un ressort est proportionnelle à :", ["Sa masse", "Son allongement ΔL", "Sa vitesse"], index=None, key="q9")

# Q10
st.markdown("#### 10. Travail d'une force")
q10 = st.radio("Le travail d'une force perpendiculaire au déplacement est :", ["Positif", "Nul", "Moteur"], index=None, key="q10")

# --- CORRECTION ET SCORE ---
if st.button("Afficher mon score final"):
    resp = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    if None in resp:
        st.error("Réponds à toutes les questions avant de valider !")
    else:
        score = 0
        if q1 == "v = 4 m/s": score += 1
        if q2 == "Nulle": score += 1
        if q3 == "Galiléen": score += 1
        if q4 == "Newton (N)": score += 1
        if q5 == "Le changement de direction du mouvement": score += 1
        if q6 == "g (intensité de pesanteur)": score += 1
        if q7 == "9": score += 1
        if q8 == "a = g * sin(α)": score += 1
        if q9 == "Son allongement ΔL": score += 1
        if q10 == "Nul": score += 1
        
        st.success(f"### Score : {score}/10")
        if score < 5: st.warning("Besoin d'un gros rappel des bases !")
        elif score < 8: st.info("Bonnes bases, mais attention aux détails.")
        else: st.balloons(); st.write("Bravo ! Niveau excellent.")

st.sidebar.write("Enseignant : **Anas Bouzid**")
