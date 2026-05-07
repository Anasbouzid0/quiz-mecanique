import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ET ESTHÉTIQUE ---
st.set_page_config(page_title="Le Champ Magnétique", page_icon="🧲", layout="wide")

# Constantes physiques
MU_0 = 4 * np.pi * 1e-7
B_TERRE = 2e-5

st.markdown("""
<div style='background-color: #2980b9; padding: 15px; border-radius: 5px;'>
    <h1 style='color: white; margin:0;'>🧲 Le Champ Magnétique créé par un courant électrique</h1>
    <p style='color: white; margin:0; font-size: 18px;'>Physique-Chimie | 1ère BAC BIOF | Lycée Ibn Batouta | Enseignant : Anas BOUZID</p>
</div>
""", unsafe_allow_html=True)
st.write("") # Espace

# --- 2. BARRE LATÉRALE (CONTRÔLES GLOBAUX) ---
with st.sidebar:
    st.header("⚙️ Paillasse Virtuelle")
    st.markdown("Modifiez les paramètres de l'expérience :")
    I = st.slider("Intensité du courant I (A)", min_value=-20.0, max_value=20.0, value=10.0, step=0.5)
    d_cm = st.slider("Distance de la sonde d (cm)", min_value=1.0, max_value=15.0, value=4.0, step=0.5)
    d_m = d_cm / 100.0
    
    st.divider()
    st.subheader("📊 Teslamètre")
    B_calc = (MU_0 * abs(I)) / (2 * np.pi * d_m)
    st.metric(label=f"Valeur théorique à {d_cm} cm", value=f"{B_calc * 1e6:.1f} µT")

# --- 3. MOTEUR PHYSIQUE (Génération des graphiques) ---
def tracer_oersted(I_val, dist_m):
    fig, ax = plt.subplots(figsize=(5, 5))
    # Fil conducteur
    marker, color = ('o', 'red') if I_val > 0 else ('x', 'blue') if I_val < 0 else ('o', 'gray')
    ax.plot(0, 0, marker=marker, color=color, markersize=20, markeredgewidth=2, label="Fil rectiligne")
    
    # Vecteurs B
    Bx_fil, By_fil = 0, (MU_0 * I_val) / (2 * np.pi * dist_m)
    Bx_res, By_res = Bx_fil, By_fil + B_TERRE
    
    norm = np.sqrt(Bx_res**2 + By_res**2)
    dx, dy = (Bx_res/norm, By_res/norm) if norm > 0 else (0, 1)
    
    # Boussole
    ax.quiver(dist_m, 0, dx, dy, color='red', scale=1, scale_units='xy', angles='xy', width=0.015, label="Nord")
    ax.quiver(dist_m, 0, -dx, -dy, color='blue', scale=1, scale_units='xy', angles='xy', width=0.015, label="Sud")
    ax.add_patch(plt.Circle((dist_m, 0), 0.02, color='gray', fill=False, linestyle='--'))
    
    ax.set_xlim(-0.05, max(0.1, dist_m + 0.04))
    ax.set_ylim(-0.05, 0.05)
    ax.set_aspect('equal')
    ax.axis('off') # On cache les axes pour un rendu plus "schéma"
    ax.legend(loc='upper right')
    return fig

def tracer_spectre(I_val):
    fig, ax = plt.subplots(figsize=(5, 5))
    x, y = np.linspace(-0.1, 0.1, 40), np.linspace(-0.1, 0.1, 40)
    X, Y = np.meshgrid(x, y)
    
    r2 = X**2 + Y**2 + 1e-10
    Bx, By = - (MU_0 * I_val / (2 * np.pi)) * (Y / r2), (MU_0 * I_val / (2 * np.pi)) * (X / r2)
    B_norm = np.sqrt(Bx**2 + By**2)
    
    ax.streamplot(X, Y, Bx, By, color=B_norm, cmap='inferno', linewidth=1.5, density=1.2)
    
    marker, color = ('o', 'red') if I_val > 0 else ('x', 'blue') if I_val < 0 else ('o', 'gray')
    ax.plot(0, 0, marker=marker, color=color, markersize=15, markeredgewidth=2)
    
    ax.set_xlim(-0.1, 0.1)
    ax.set_ylim(-0.1, 0.1)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- 4. SCÉNARIO PÉDAGOGIQUE (Onglets) ---
st.markdown("### Étapes de l'activité expérimentale")
tab1, tab2, tab3 = st.tabs(["1️⃣ L'Expérience d'Oersted", "2️⃣ Le Spectre Magnétique", "3️⃣ Loi de Biot et Savart"])

with tab1:
    st.subheader("Mise en évidence de l'influence magnétique")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Protocole :** On place un fil rectiligne au-dessus d'une boussole (alignée sur le méridien Nord-Sud). On ferme le circuit électrique.")
        fig1 = tracer_oersted(I, d_m)
        st.pyplot(fig1)
        plt.close(fig1)
    with col2:
        st.info("💡 **Consigne :** Modifiez l'intensité du courant dans le menu de gauche et observez l'aiguille.")
        st.markdown("**Q1. Que se passe-t-il à la fermeture du circuit ?**")
        st.success("L'aiguille pivote et tend à se placer perpendiculairement au fil.")
        st.markdown("**Q2. Que se passe-t-il si on inverse les bornes du générateur ?**")
        st.success("L'aiguille dévie, mais dans le sens diamétralement opposé. Le sens du champ dépend du sens du courant.")

with tab2:
    st.subheader("Topographie du vecteur champ magnétique")
    col1, col2 = st.columns([1, 1])
    with col1:
        fig2 = tracer_spectre(I)
        st.pyplot(fig2)
        plt.close(fig2)
    with col2:
        st.markdown("**Protocole :** On saupoudre de la limaille de fer sur une plaque en plexiglas traversée par le fil.")
        st.markdown("**Q3. Quelle est la forme des lignes de champ ?**")
        st.success("La limaille dessine des cercles concentriques centrés sur le fil.")
        st.markdown("**Règle de la main droite :**")
        st.write("Le pouce suit le sens du courant $I$, les doigts courbés indiquent le sens de rotation des lignes de champ $\\vec{B}$.")

with tab3:
    st.subheader("Modélisation Mathématique")
    st.markdown("L'utilisation du teslamètre a permis de montrer que l'intensité du champ magnétique est proportionnelle au courant $I$ et inversement proportionnelle à la distance $d$.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.latex(r"B = \frac{\mu_0 \cdot I}{2 \pi \cdot d}")
    with col2:
        st.write("- **$B$** : Intensité en Tesla (T)")
        st.write("- **$I$** : Courant en Ampère (A)")
        st.write("- **$d$** : Distance en mètre (m)")
        st.write("- **$\mu_0$** : Perméabilité du vide ($4\pi \times 10^{-7}$ S.I.)")
