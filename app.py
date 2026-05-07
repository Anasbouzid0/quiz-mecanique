import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Simulation 3D - Électromagnétisme", layout="wide", page_icon="🧭")

MU_0 = 4 * np.pi * 1e-7
B_TERRE = 2e-5  # Composante horizontale du champ terrestre

# En-tête professionnel
st.markdown("""
<div style='background-color: #0A2540; padding: 20px; border-radius: 10px; margin-bottom: 25px;'>
    <h1 style='color: #00D4FF; margin:0;'>🧭 Le champ magnétique créé par un courant continu</h1>
    <h4 style='color: white; margin-top: 5px; font-weight: 300;'>Séquence 1 : Le fil rectiligne infini | 1ère BAC BIOF - Lycée Ibn Batouta</h4>
    <p style='color: #A0B2C6; margin:0; font-style: italic;'>Enseignant : Anas BOUZID</p>
</div>
""", unsafe_allow_html=True)

# --- 2. BARRE DE CONTRÔLES ---
with st.sidebar:
    st.header("⚙️ Paillasse de l'Enseignant")
    
    st.subheader("🔌 Générateur")
    I = st.slider("Intensité du courant I (A)", min_value=-25.0, max_value=25.0, value=15.0, step=0.5)
    st.caption("Si I > 0, le courant monte. Si I < 0, il descend.")
    
    st.divider()
    
    st.subheader("🕹️ Sonde & Boussole (Libre 3D)")
    st.markdown("Déplacez la boussole dans l'espace :")
    pos_x = st.slider("Axe X (Gauche/Droite) [cm]", -15.0, 15.0, 6.0, step=0.5)
    pos_y = st.slider("Axe Y (Avant/Arrière) [cm]", -15.0, 15.0, 0.0, step=0.5)
    pos_z = st.slider("Axe Z (Haut/Bas) [cm]", -10.0, 10.0, 0.0, step=0.5)
    
    # Conversion SI
    x_m, y_m, z_m = pos_x / 100.0, pos_y / 100.0, pos_z / 100.0
    rayon_m = np.sqrt(x_m**2 + y_m**2)
    
    st.divider()
    
    # Moteur Physique : Calcul de B
    if rayon_m < 0.01: # Éviter la singularité (dans le fil)
        Bx, By, Bz = 0, 0, 0
    else:
        # Biot-Savart : Bx et By
        Bx = - (MU_0 * I / (2 * np.pi * rayon_m**2)) * y_m
        By =   (MU_0 * I / (2 * np.pi * rayon_m**2)) * x_m
        Bz = 0 
        
    # Ajout du champ terrestre
    Bx_tot = Bx
    By_tot = By + B_TERRE
    Bz_tot = Bz
    
    valeur_affichee = np.sqrt(Bx_tot**2 + By_tot**2 + Bz_tot**2) * 1e6
    
    st.subheader("📟 Teslamètre")
    st.metric(label="Intensité du champ magnétique total", value=f"{valeur_affichee:.1f} µT")
    st.info(f"Distance à l'axe du fil : **{rayon_m*100:.1f} cm**")

# --- 3. CONTENU PÉDAGOGIQUE ET SIMULATEUR ---
col_texte, col_3d = st.columns([1, 2])

with col_texte:
    st.markdown("### 📝 Démarche Expérimentale")
    
    with st.expander("1️⃣ Situation de départ", expanded=True):
        st.write("*Vous approchez une boussole d'un câble de forte puissance. L'aiguille dévie brusquement sans aucun contact.*")
        st.markdown("**Hypothèse à tester :** Le courant électrique crée une influence magnétique invisible dans l'espace.")
        
    with st.expander("2️⃣ Manipulation (Oersted)", expanded=True):
        st.write("Observez le modèle 3D à droite et déplacez la boussole à l'aide des curseurs.")
        st.markdown("- **Action 1 :** Fermez le circuit (Mettez une valeur de $I$). Que fait l'aiguille ?")
        st.markdown("- **Action 2 :** Inversez les bornes (Mettez $I$ en négatif). Que se passe-t-il ?")
        st.markdown("- **Action 3 :** Déplacez la boussole sur l'axe Z (Haut/Bas). L'intensité du champ change-t-elle ?")
        
    with st.expander("3️⃣ Bilan et Modélisation", expanded=True):
        st.markdown("**Règle de la Main Droite :**")
        st.write("Le pouce indique le courant $I$, l'enroulement des doigts indique le sens de $\\vec{B}$.")
        st.markdown("**Intensité du champ magnétique :**")
        st.latex(r"B = \frac{\mu_0 \cdot I}{2 \pi \cdot d}")
        st.write("L'intensité du champ magnétique est proportionnelle au courant $I$ et inversement proportionnelle à la distance $d$.")

with col_3d:
    st.markdown("### 🔭 Visualisation 3D Interactive")
    st.caption("Faites un clic-gauche pour faire pivoter la caméra, utilisez la molette pour zoomer.")
    
    fig = go.Figure()

    # Plan de référence (Plexiglas)
    fig.add_trace(go.Surface(
        x=[[-20, 20], [-20, 20]], y=[[-20, -20], [20, 20]], z=[[0, 0], [0, 0]],
        colorscale=[[0, 'rgba(236, 240, 241, 0.4)'], [1, 'rgba(236, 240, 241, 0.4)']],
        showscale=False, hoverinfo='skip'
    ))

    # Fil conducteur
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-15, 15],
        mode='lines', line=dict(color='#d35400', width=12),
        name="Fil en cuivre"
    ))
    
    # Indicateur du sens de I
    if I > 0:
        fig.add_trace(go.Cone(x=[0], y=[0], z=[5], u=[0], v=[0], w=[1], sizemode="absolute", sizeref=3, colorscale=[[0, '#2c3e50'], [1, '#2c3e50']], showscale=False, name="Sens de I"))
    elif I < 0:
        fig.add_trace(go.Cone(x=[0], y=[0], z=[5], u=[0], v=[0], w=[-1], sizemode="absolute", sizeref=3, colorscale=[[0, '#2c3e50'], [1, '#2c3e50']], showscale=False, name="Sens de I"))

    # Lignes de champ (Spectre) - Affichées en Z=0
    if I != 0:
        for r_cercle in [4, 8, 12]:
            theta = np.linspace(0, 2*np.pi, 60)
            fig.add_trace(go.Scatter3d(
                x=r_cercle * np.cos(theta), y=r_cercle * np.sin(theta), z=np.zeros_like(theta),
                mode='lines', line=dict(color='#34495e', width=2), showlegend=False, hoverinfo='skip'
            ))

    # Boussole dynamique
    norme_B = np.sqrt(Bx_tot**2 + By_tot**2 + Bz_tot**2)
    if norme_B > 0:
        dir_x, dir_y, dir_z = Bx_tot/norme_B, By_tot/norme_B, Bz_tot/norme_B
    else:
        dir_x, dir_y, dir_z = 0, 1, 0
        
    taille_boussole = 3 
    
    # Pôle Nord (Rouge)
    fig.add_trace(go.Cone(
        x=[pos_x], y=[pos_y], z=[pos_z],
        u=[dir_x], v=[dir_y], w=[dir_z],
        sizemode="absolute", sizeref=taille_boussole,
        colorscale=[[0, '#e74c3c'], [1, '#e74c3c']], showscale=False, name="Pôle Nord"
    ))
    
    # Pôle Sud (Bleu)
    fig.add_trace(go.Cone(
        x=[pos_x], y=[pos_y], z=[pos_z],
        u=[-dir_x], v=[-dir_y], w=[-dir_z],
        sizemode="absolute", sizeref=taille_boussole,
        colorscale=[[0, '#3498db'], [1, '#3498db']], showscale=False, name="Pôle Sud"
    ))

    # Paramètres de la caméra et de la scène
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X (cm)', range=[-20, 20], showbackground=False, zerolinecolor='black'),
            yaxis=dict(title='Y (cm)', range=[-20, 20], showbackground=False, zerolinecolor='black'),
            zaxis=dict(title='Z (cm)', range=[-15, 15], showbackground=False, zerolinecolor='black'),
            aspectratio=dict(x=1, y=1, z=0.8),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)) # Vue isométrique par défaut
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)
