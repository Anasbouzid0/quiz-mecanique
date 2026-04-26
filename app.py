import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Quiz Mécanique Pro - Prof Anas", page_icon="🎓")

# --- INITIALISATION DES VARIABLES (SESSION STATE) ---
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# --- DONNÉES DU QUIZ ---
questions_data = [
    {
        "q": "Quelle est l'expression du vecteur vitesse si $\\vec{OM} = 4t \\cdot \\vec{i} + 2 \\cdot \\vec{j}$ ?",
        "options": ["v = 4 m/s", "v = 2 m/s", "v = 4t m/s"],
        "answer": "v = 4 m/s"
    },
    {
        "q": "Si le mouvement est rectiligne uniforme, l'accélération est :",
        "options": ["Positive", "Nulle", "Négative"],
        "answer": "Nulle"
    },
    {
        "q": "La deuxième loi de Newton s'énonce :",
        "options": ["ΣF = m.v", "ΣF = 0", "ΣF = m.a"],
        "answer": "ΣF = m.a"
    },
    {
        "q": "L'unité de la constante de raideur K d'un ressort est :",
        "options": ["N.m", "N/m", "kg.m/s"],
        "answer": "N/m"
    },
    {
        "q": "Dans le repère de Frénet, l'accélération normale est $a_n = $ :",
        "options": ["dv/dt", "v²/R", "R/v²"],
        "answer": "v²/R"
    },
    {
        "q": "Le travail d'une force constante lors d'un déplacement AB est :",
        "options": ["F.AB.cos(α)", "F.AB.sin(α)", "F/AB"],
        "answer": "F.AB.cos(α)"
    },
    {
        "q": "L'énergie cinétique d'un solide en translation est :",
        "options": ["m.v²", "½.m.v²", "m.g.h"],
        "answer": "½.m.v²"
    },
    {
        "q": "En chute libre, on néglige :",
        "options": ["Le poids", "La poussée d'Archimède et l'air", "La masse"],
        "answer": "La poussée d'Archimède et l'air"
    },
    {
        "q": "Un référentiel lié à la Terre est considéré comme :",
        "options": ["Toujours galiléen", "Approximativement galiléen", "Non-galiléen"],
        "answer": "Approximativement galiléen"
    },
    {
        "q": "La période T d'un pendule pesant dépend de :",
        "options": ["La masse seulement", "La longueur et g", "La vitesse initiale"],
        "answer": "La longueur et g"
    }
]

# --- INTERFACE ---
st.title("🚀 Quiz Interactif : Mécanique 2BAC")
st.sidebar.title(f"👨‍🏫 Prof : Anas Bouzid")
st.sidebar.write("Lycée IBN Batouta")

# Barre de progression
progress = (st.session_state.question_index + 1) / len(questions_data)
st.progress(progress)
st.write(f"**Question {st.session_state.question_index + 1} sur {len(questions_data)}**")

# Affichage de la question actuelle
current_q = questions_data[st.session_state.question_index]
st.markdown(f"### {current_q['q']}")

# Récupérer la réponse déjà donnée si elle existe
default_val = st.session_state.responses.get(st.session_state.question_index, None)

choice = st.radio("Choisis ta réponse :", current_q['options'], index=current_q['options'].index(default_val) if default_val else None, key=f"radio_{st.session_state.question_index}")

# Enregistrer la réponse
if choice:
    st.session_state.responses[st.session_state.question_index] = choice

# --- BOUTONS DE NAVIGATION ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.session_state.question_index > 0:
        if st.button("⬅️ Précédent"):
            st.session_state.question_index -= 1
            st.rerun()

with col2:
    if st.session_state.question_index < len(questions_data) - 1:
        if st.button("Suivant ➡️"):
            st.session_state.question_index += 1
            st.rerun()
    else:
        if st.button("🎯 Terminer le Quiz"):
            st.session_state.finished = True

# --- RÉSULTATS FINAUX ---
if 'finished' in st.session_state:
    st.divider()
    score = 0
    for i, q in enumerate(questions_data):
        if st.session_state.responses.get(i) == q['answer']:
            score += 1
    
    st.balloons()
    st.success(f"### Score Final : {score} / {len(questions_data)}")
    
    if score >= 8:
        st.write("Excellent ! Tu es prêt pour le Bac.")
    elif score >= 5:
        st.write("C'est bien, mais revois tes formules de base.")
    else:
        st.write("Il y a encore du travail. On va reprendre ça ensemble !")
    
    if st.button("Recommencer 🔄"):
        st.session_state.question_index = 0
        st.session_state.responses = {}
        del st.session_state.finished
        st.rerun()
