import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms # <-- L'import manquant est ici

# --- Configuration de la page ---
st.set_page_config(page_title="Simulation 2ème Loi de Newton", layout="wide")
st.title("📐 Mouvement sur un Plan Incliné & 2ème Loi de Newton")

st.markdown("""
Cette application illustre le mouvement d'un solide glissant sans vitesse initiale. 
Observez comment le vecteur **Poids** reste dirigé vers le centre de la Terre, indépendamment de l'angle du plan.
""")

# --- Barre latérale : Paramètres ---
st.sidebar.header("Paramètres Physiques")
alpha_deg = st.sidebar.slider("Angle d'inclinaison α (°)", 0, 60, 30)
m = st.sidebar.slider("Masse du solide m (kg)", 1.0, 10.0, 2.0)
mu = st.sidebar.slider("Coefficient de frottement μ", 0.0, 0.8, 0.15)
t = st.sidebar.slider("Temps t (secondes)", 0.0, 5.0, 0.0, step=0.1)

# --- Constantes et Physique ---
g = 9.81
alpha_rad = np.radians(alpha_deg)

# Calcul des composantes des forces
P_mag = m * g
P_x = m * g * np.sin(alpha_rad) # Composante motrice
P_y = m * g * np.cos(alpha_rad) # Composante normale

Rn_mag = P_y                    # Équilibre sur l'axe y
f_mag = mu * Rn_mag             # Intensité de la force de frottement cinétique

# 2ème loi de Newton (Axe x) : P_x - f = m * a
F_res = P_x - f_mag

# L'accélération ne peut pas être négative si le bloc part du repos
if F_res > 0:
    a = F_res / m
else:
    a = 0
    F_res = 0
    f_mag = P_x # Le frottement statique compense exactement P_x

# Équation horaire de la position (x = 1/2 * a * t^2)
distance = 0.5 * a * (t**2)

# --- Affichage des Équations ---
col_eq, col_graph = st.columns([1, 2])

with col_eq:
    st.subheader("Bilan des Forces et Accélération")
    st.latex(r"\sum \vec{F} = m \cdot \vec{a}")
    st.latex(r"\vec{P} + \vec{R}_n + \vec{f} = m \cdot \vec{a}")
    
    st.markdown("**Projection sur l'axe du mouvement (Ox) :**")
    st.latex(r"P_x - f = m \cdot a")
    st.latex(rf"m \cdot g \cdot \sin(\alpha) - \mu \cdot R_n = m \cdot a")
    
    st.markdown("---")
    st.markdown("**Valeurs en temps réel :**")
    st.write(f"- **Poids (P) :** {P_mag:.2f} N")
    st.write(f"- **Réaction (Rn) :** {Rn_mag:.2f} N")
    st.write(f"- **Frottement (f) :** {f_mag:.2f} N")
    st.write(f"- **Accélération (a) :** {a:.2f} m/s²")
    st.write(f"- **Position (x) :** {distance:.2f} m")

# --- Visualisation Matplotlib ---
with col_graph:
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Géométrie du plan
    longueur_plan = 25.0
    x_haut = 0
    y_haut = longueur_plan * np.sin(alpha_rad)
    x_bas = longueur_plan * np.cos(alpha_rad)
    y_bas = 0
    
    # Tracer le plan
    ax.plot([x_haut, x_bas], [y_haut, y_bas], 'k-', lw=3, label="Plan incliné")
    ax.plot([x_haut, x_haut], [y_haut, 0], 'k--', lw=1)
    ax.plot([x_haut, x_bas], [0, 0], 'k--', lw=1)
    
    # Géométrie du solide
    cote_bloc = 2.0
    x_c = distance * np.cos(alpha_rad) + (cote_bloc/2) * np.sin(alpha_rad)
    y_c = y_haut - distance * np.sin(alpha_rad) + (cote_bloc/2) * np.cos(alpha_rad)
    
    # Arrêter le bloc en bas du plan
    if distance > longueur_plan:
        x_c = x_bas + (cote_bloc/2) * np.sin(alpha_rad)
        y_c = y_bas + (cote_bloc/2) * np.cos(alpha_rad)
        st.warning("Le solide a atteint le bas du plan !")

    # Dessiner le solide
    rect = patches.Rectangle(
        (x_c - cote_bloc/2, y_c - cote_bloc/2), cote_bloc, cote_bloc,
        angle=np.degrees(-alpha_rad),
        color='royalblue', alpha=0.7, label="Solide"
    )
    
    # Application de la rotation via la librairie correctement importée
    t_start = ax.transData
    t_rot = transforms.Affine2D().rotate_deg_around(x_c, y_c, -alpha_deg)
    rect.set_transform(t_rot + t_start)
    ax.add_patch(rect)
    
    # Centre d'inertie
    ax.plot(x_c, y_c, 'ro', markersize=5)
    
    # --- Tracé des vecteurs forces ---
    échelle = 0.15 
    
    # Vecteur Poids (P) - strictement vers le bas
    ax.quiver(x_c, y_c, 0, -P_mag * échelle, angles='xy', scale_units='xy', scale=1, color='green', width=0.008, label="Poids (P)")
    
    # Vecteur Réaction Normale (Rn)
    Rn_dx = Rn_mag * np.sin(alpha_rad) * échelle
    Rn_dy = Rn_mag * np.cos(alpha_rad) * échelle
    ax.quiver(x_c, y_c, Rn_dx, Rn_dy, angles='xy', scale_units='xy', scale=1, color='red', width=0.008, label="Réaction (Rn)")
    
    # Vecteur Frottement (f)
    if f_mag > 0:
        f_dx = -f_mag * np.cos(alpha_rad) * échelle
        f_dy = f_mag * np.sin(alpha_rad) * échelle
        ax.quiver(x_c, y_c, f_dx, f_dy, angles='xy', scale_units='xy', scale=1, color='orange', width=0.008, label="Frottements (f)")

    # Paramètres du graphique
    ax.set_aspect('equal')
    ax.set_xlim(-2, longueur_plan + 2)
    ax.set_ylim(-2, longueur_plan + 2)
    ax.set_title(f"Simulation à t = {t:.1f} s")
    ax.legend(loc="upper right")
    ax.axis('off') 
    
    st.pyplot(fig)
