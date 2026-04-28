import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms

# --- Configuration ---
st.set_page_config(page_title="Mécanique de Newton", layout="wide")
st.title("📐 Dynamique d'un Solide : 2ème Loi de Newton")

# --- Interface Utilisateur (Sidebar) ---
st.sidebar.header("Configuration de l'Étude")

# 1. Choix du plan
mode_plan = st.sidebar.radio("Type de mouvement", ["Plan Horizontal", "Plan Incliné"])

# 2. Choix des frottements
mode_frottement = st.sidebar.radio("Contact", ["Sans frottement", "Avec frottement"])

st.sidebar.markdown("---")
st.sidebar.header("Paramètres Physiques")

m = st.sidebar.slider("Masse m (kg)", 1.0, 10.0, 2.0)

# Paramètres conditionnels selon le plan
if mode_plan == "Plan Incliné":
    alpha_deg = st.sidebar.slider("Angle d'inclinaison α (°)", 10, 60, 30)
    F_ext = 0.0 # C'est le poids qui fait descendre le solide
else:
    alpha_deg = 0
    F_ext = st.sidebar.slider("Force de traction F_ext (N)", 0.0, 50.0, 15.0)

# Paramètres conditionnels selon les frottements
if mode_frottement == "Avec frottement":
    mu = st.sidebar.slider("Coefficient de frottement μ", 0.05, 0.8, 0.2)
else:
    mu = 0.0

t = st.sidebar.slider("Temps de simulation t (s)", 0.0, 5.0, 1.5, step=0.1)

# --- Moteur Physique ---
g = 9.81
alpha_rad = np.radians(alpha_deg)

# Composantes du Poids
P_mag = m * g
P_x = P_mag * np.sin(alpha_rad)
P_y = P_mag * np.cos(alpha_rad)

# Calcul des forces selon le cas
if mode_plan == "Plan Horizontal":
    Force_motrice = F_ext
    Rn_mag = P_mag # Sur un plan horizontal, Rn compense P exactement
else:
    Force_motrice = P_x
    Rn_mag = P_y   # Sur un plan incliné, Rn compense Py

# Calcul du frottement cinétique
f_mag = mu * Rn_mag

# Application de la 2ème loi de Newton : Somme(Fx) = m * a
F_res = Force_motrice - f_mag

if F_res > 0:
    a = F_res / m
else:
    a = 0
    F_res = 0
    f_mag = Force_motrice # En l'absence de mouvement, le frottement statique bloque le solide

# Équation horaire (vitesse initiale nulle)
distance = 0.5 * a * (t**2)

# --- Affichage des Résultats ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Bilan et Équations")
    st.markdown(f"**Cas étudié :** {mode_plan}, {mode_frottement.lower()}")
    
    st.latex(r"\sum \vec{F} = m \cdot \vec{a}_{G}")
    
    if mode_plan == "Plan Horizontal":
        if mode_frottement == "Sans frottement":
            st.latex(r"\vec{P} + \vec{R}_n + \vec{F}_{ext} = m \cdot \vec{a}")
            st.latex(r"a = \frac{F_{ext}}{m}")
        else:
            st.latex(r"\vec{P} + \vec{R}_n + \vec{f} + \vec{F}_{ext} = m \cdot \vec{a}")
            st.latex(r"a = \frac{F_{ext} - f}{m}")
    else:
        if mode_frottement == "Sans frottement":
            st.latex(r"\vec{P} + \vec{R}_n = m \cdot \vec{a}")
            st.latex(r"a = g \cdot \sin(\alpha)")
        else:
            st.latex(r"\vec{P} + \vec{R}_n + \vec{f} = m \cdot \vec{a}")
            st.latex(r"a = g \cdot \sin(\alpha) - \mu \cdot g \cdot \cos(\alpha)")

    st.markdown("---")
    st.write(f"**Accélération :** {a:.2f} m/s²")
    st.write(f"**Distance parcourue :** {distance:.2f} m")

# --- Visualisation Graphique Rigoureuse ---
with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    longueur_plan = 25.0
    cote_bloc = 2.0
    
    # Géométrie du plan (départ à x=0 en haut)
    y_haut = longueur_plan * np.sin(alpha_rad)
    
    # Tracer la surface
    x_surface = [0, longueur_plan * np.cos(alpha_rad)]
    y_surface = [y_haut, 0]
    ax.plot(x_surface, y_surface, 'k-', lw=4, label="Support")
    
    # Position exacte du Centre de Masse (G) pour que le bloc soit posé SUR la surface
    x_c = distance * np.cos(alpha_rad) + (cote_bloc / 2) * np.sin(alpha_rad)
    y_c = y_haut - distance * np.sin(alpha_rad) + (cote_bloc / 2) * np.cos(alpha_rad)
    
    # Vérification de fin de piste
    if distance > longueur_plan:
        st.warning("Le solide a quitté le plan étudié.")
        distance = longueur_plan
        x_c = longueur_plan * np.cos(alpha_rad) + (cote_bloc / 2) * np.sin(alpha_rad)
        y_c = 0 + (cote_bloc / 2) * np.cos(alpha_rad)

    # Tracer le solide
    rect = patches.Rectangle(
        (x_c - cote_bloc/2, y_c - cote_bloc/2), cote_bloc, cote_bloc,
        angle=np.degrees(-alpha_rad),
        color='cornflowerblue', alpha=0.8
    )
    
    t_start = ax.transData
    t_rot = transforms.Affine2D().rotate_deg_around(x_c, y_c, -alpha_deg)
    rect.set_transform(t_rot + t_start)
    ax.add_patch(rect)
    
    # Centre d'inertie (G)
    ax.plot(x_c, y_c, 'ro', markersize=6, label="Centre de masse (G)")
    
    # --- Vecteurs depuis G ---
    ech = 0.1 # Échelle des vecteurs
    
    # 1. Poids (P) - Toujours vertical vers le bas
    ax.quiver(x_c, y_c, 0, -P_mag * ech, angles='xy', scale_units='xy', scale=1, color='green', width=0.006, label="Poids (P)")
    
    # 2. Réaction Normale (Rn) - Perpendiculaire à la surface
    Rn_dx = Rn_mag * np.sin(alpha_rad) * ech
    Rn_dy = Rn_mag * np.cos(alpha_rad) * ech
    ax.quiver(x_c, y_c, Rn_dx, Rn_dy, angles='xy', scale_units='xy', scale=1, color='red', width=0.006, label="Réaction (Rn)")
    
    # 3. Force de traction (F_ext) - Cas horizontal uniquement
    if mode_plan == "Plan Horizontal" and F_ext > 0:
        ax.quiver(x_c, y_c, F_ext * ech, 0, angles='xy', scale_units='xy', scale=1, color='purple', width=0.006, label="Traction (F_ext)")
        
    # 4. Frottement (f) - Opposé au mouvement
    if mode_frottement == "Avec frottement" and f_mag > 0:
        f_dx = -f_mag * np.cos(alpha_rad) * ech
        f_dy = f_mag * np.sin(alpha_rad) * ech
        ax.quiver(x_c, y_c, f_dx, f_dy, angles='xy', scale_units='xy', scale=1, color='orange', width=0.006, label="Frottements (f)")

    # Formatage de la figure
    ax.set_aspect('equal')
    ax.set_xlim(-2, longueur_plan * np.cos(alpha_rad) + 5)
    ax.set_ylim(-2, y_haut + 5)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    ax.axis('off')
    
    st.pyplot(fig)
