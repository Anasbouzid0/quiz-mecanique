import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Étude du Champ Magnétique - Fil Rectiligne",
    page_icon="🧲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTES PHYSIQUES ---
MU_0 = 4 * np.pi * 1e-7  # Perméabilité magnétique du vide (T.m/A)
B_TERRE = 2e-5           # Composante horizontale du champ terrestre (~20 µT)

# --- EN-TÊTE PÉDAGOGIQUE ---
st.title("🧲 Le champ magnétique créé par un courant électrique")
st.markdown("""
**Niveau :** 1ère BAC BIOF | **Séquence :** Le fil conducteur rectiligne
*Application interactive conçue pour l'exploration de la topographie et de l'intensité du champ magnétique $\\vec{B}$.*
""")
st.divider()

# --- BARRE LATÉRALE : PARAMÈTRES GLOBAUX ---
with st.sidebar:
    st.header("⚙️ Paramètres du Système")
    st.markdown("Ajustez les grandeurs physiques du circuit :")
    I = st.slider("Intensité du courant I (A)", min_value=-30.0, max_value=30.0, value=15.0, step=0.5)
    d_cm = st.slider("Distance de mesure d (cm)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    d_m = d_cm / 100.0  # Conversion SI
    
    st.divider()
    st.subheader("📊 Teslamètre Virtuel")
    B_calc = (MU_0 * abs(I)) / (2 * np.pi * d_m)
    st.metric(label=f"Intensité de B à {d_cm} cm", value=f"{B_calc * 1e6:.1f} µT")

# --- FONCTIONS DE SIMULATION ---
def plot_oersted(I_val, distance_m):
    """Génère la visualisation de l'expérience d'Oersted avec la boussole."""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    marker = 'o' if I_val > 0 else 'x'
    color = 'red' if I_val > 0 else 'blue'
    if I_val == 0: marker, color = 'o', 'gray'
    ax.plot(0, 0, marker=marker, color=color, markersize=18, markeredgewidth=2, label="Fil (Axe Z)")
    
    Bx_fil = 0
    By_fil = (MU_0 * I_val) / (2 * np.pi * distance_m)
    
    Bx_res = Bx_fil
    By_res = By_fil + B_TERRE
    
    norm = np.sqrt(Bx_res**2 + By_res**2)
    dir_x, dir_y = (Bx_res/norm, By_res/norm) if norm > 0 else (0, 1)
    
    L = 0.02
    ax.quiver(distance_m, 0, dir_x, dir_y, color='red', scale=1, scale_units='xy', angles='xy', width=0.015, label="Pôle Nord")
    ax.quiver(distance_m, 0, -dir_x, -dir_y, color='blue', scale=1, scale_units='xy', angles='xy', width=0.015, label="Pôle Sud")
    ax.add_patch(plt.Circle((distance_m, 0), L*1.2, color='gray', fill=False, linestyle='--'))
    
    ax.set_xlim(-0.1, max(0.1, distance_m + 0.05))
    ax.set_ylim(-0.1, 0.1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.legend(loc='upper left')
    return fig

def plot_spectre(I_val):
    """Génère la topographie du champ magnétique (Limaille de fer)."""
    fig, ax = plt.subplots(figsize=(6, 6))
    x = np.linspace(-0.1, 0.1, 40)
    y = np.linspace(-0.1, 0.1, 40)
    X, Y = np.meshgrid(x, y)
    
    r_carre = X**2 + Y**2
    r_carre[r_carre == 0] = 1e-10 
    
    Bx = - (MU_0 * I_val / (2 * np.pi)) * (Y / r_carre)
    By =   (MU_0 * I_val / (2 * np.pi)) * (X / r_carre)
    B_norm = np.sqrt(Bx**2 + By**2)
    
    ax.streamplot(X, Y, Bx, By, color=B_norm, cmap='viridis', linewidth=1.5, density=1.5, arrowsize=1.5)
    
    marker = 'o' if I_val > 0 else 'x'
    color = 'red' if I_val > 0 else 'blue'
    if I_val == 0: marker, color = 'o', 'gray'
    ax.plot(0, 0, marker=marker, color=color, markersize=15, markeredgewidth=2)
    
    ax.set_xlim(-0.1, 0.1)
    ax.set_ylim(-0.1, 0.1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    return fig

def plot_quantitative():
    """Génère les courbes d'analyse B=f(I) et B=f(1/d)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    I_vals = np.linspace(0, 30, 100)
    B_I_vals = (MU_0 * I_vals) / (2 * np.pi * 0.05) * 1e6 
    ax1.plot(I_vals, B_I_vals, color='blue', linewidth=2)
    ax1.set_title("Intensité du champ B en fonction de I (d = 5 cm)")
    ax1.set_xlabel("Courant I (A)")
    ax1.set_ylabel("Champ B (µT)")
    ax1.grid(True)
    
    d_vals = np.linspace(0.01, 0.20, 100)
    inv_d = 1 / d_vals
    B_d_vals = (MU_0 * 15.0) / (2 * np.pi * d_vals) * 1e6 
    ax2.plot(inv_d, B_d_vals, color='red', linewidth=2)
    ax2.set_title("Intensité du champ B en fonction de 1/d (I = 15 A)")
    ax2.set_xlabel("1/d (m⁻¹)")
    ax2.set_ylabel("Champ B (µT)")
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

# --- ORGANISATION EN ONGLETS ---
tab1, tab2, tab3 = st.tabs(["🧭 1. Expérience d'Oersted", "🌌 2. Spectre Magnétique", "📈 3. Étude Quantitative"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Observation de l'aiguille aimantée")
        st.markdown("Placez une boussole à proximité d'un fil rectiligne aligné sur le méridien terrestre. Faites varier l'intensité $I$.")
        fig1 = plot_oersted(I, d_m)
        st.pyplot(fig1)
        plt.close(fig1) # <-- CORRECTION DE L'ERREUR ICI
    with col2:
        st.subheader("Exploitation")
        with st.expander("Q1. Que se passe-t-il lorsque le courant circule ?"):
            st.write("L'aiguille pivote et tend à se placer perpendiculairement au fil conducteur.")
        with st.expander("Q2. Quel est l'effet de l'inversion des bornes ?"):
            st.write("Le sens du courant s'inverse ($I$ devient négatif), l'aiguille subit une rotation de 180°. Le sens de $\\vec{B}$ dépend du sens de $I$.")
        st.info("💡 **Règle de la main droite :** Le pouce pointe dans le sens de $I$, les doigts s'enroulent dans le sens des lignes de champ.")

with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Topographie de $\\vec{B}$ (Limaille de fer)")
        st.markdown("Visualisation dans un plan perpendiculaire au fil conducteur.")
        fig2 = plot_spectre(I)
        st.pyplot(fig2)
        plt.close(fig2) # <-- CORRECTION DE L'ERREUR ICI
    with col2:
        st.subheader("Exploitation")
        st.write("L'expérience de la limaille de fer permet de visualiser les lignes de champ.")
        with st.expander("Analyse du spectre :"):
            st.markdown("""
            * **Forme :** Les lignes de champ sont des cercles concentriques centrés sur le fil.
            * **Sens :** Donné par la règle du bonhomme d'Ampère ou du tire-bouchon de Maxwell.
            * **Intensité du champ magnétique :** Plus les lignes sont resserrées, plus la valeur de $B$ est grande.
            """)

with tab3:
    st.subheader("Vérification de la loi de Biot et Savart")
    st.markdown("L'utilisation d'une sonde de Hall permet d'établir les relations de proportionnalité.")
    fig3 = plot_quantitative()
    st.pyplot(fig3)
    plt.close(fig3) # <-- CORRECTION DE L'ERREUR ICI
    
    st.latex(r"B = \frac{\mu_0 \cdot I}{2 \pi \cdot d}")
    st.markdown("""
    L'intensité du champ magnétique est :
    - Strictement proportionnelle à l'intensité du courant $I$.
    - Inversement proportionnelle à la distance $d$ au fil conducteur.
    """)
