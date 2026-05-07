import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONFIGURATION ---
st.set_page_config(page_title="Paillasse Virtuelle - Électromagnétisme", layout="wide", page_icon="⚡")

# --- CSS PERSONNALISÉ POUR UN RENDU "LABORATOIRE" ---
st.markdown("""
<style>
    /* Style pour l'écran LCD du teslamètre */
    .lcd-screen {
        background-color: #879a80; /* Vert typique des vieux LCD */
        color: #1a1e18;
        font-family: 'Courier New', Courier, monospace;
        font-size: 36px;
        font-weight: bold;
        padding: 15px;
        border-radius: 8px;
        border: 4px solid #2c3e50;
        text-align: center;
        box-shadow: inset 3px 3px 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .panel-lab {
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #bdc3c7;
    }
</style>
""", unsafe_allow_html=True)

# Constantes physiques
MU_0 = 4 * np.pi * 1e-7
B_TERRE = 2e-5

st.title("⚡ Paillasse Virtuelle : Oersted et Spectre Magnétique")
st.divider()

# --- INTERFACE DE CONTRÔLE (Le Générateur) ---
col_gen, col_sim, col_mesure = st.columns([1, 2, 1])

with col_gen:
    st.markdown("<div class='panel-lab'>", unsafe_allow_html=True)
    st.subheader("🔌 Générateur DC")
    
    # Boutons de contrôle réalistes
    etat_circuit = st.radio(
        "État du circuit :",
        ["🔴 Circuit Ouvert (I = 0)", "🟢 Sens Direct (+ en haut)", "🔵 Sens Inverse (+ en bas)"]
    )
    
    # Valeur absolue du courant généré
    I_base = st.slider("Réglage du courant |I| (A)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
    
    # Détermination du courant réel selon l'état de l'interrupteur
    if etat_circuit == "🔴 Circuit Ouvert (I = 0)":
        I = 0.0
    elif etat_circuit == "🟢 Sens Direct (+ en haut)":
        I = I_base
    else:
        I = -I_base
        
    st.markdown("</div>", unsafe_allow_html=True)

# --- MOTEUR DE DESSIN RÉALISTE ---
def dessiner_paillasse(I_val, dist_m, mode="oersted"):
    """Génère une vue de dessus réaliste de la table d'expérience."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. Le fond de la table (Bois/Gris)
    ax.set_facecolor('#d5d8dc')
    
    # 2. La plaque en plexiglas transparente
    plaque = patches.Rectangle((-0.08, -0.08), 0.16, 0.16, linewidth=2, edgecolor='#7f8c8d', facecolor='#ffffff', alpha=0.9)
    ax.add_patch(plaque)
    
    if mode == "spectre":
        # Génération de la limaille de fer
        x, y = np.linspace(-0.08, 0.08, 50), np.linspace(-0.08, 0.08, 50)
        X, Y = np.meshgrid(x, y)
        r2 = X**2 + Y**2 + 1e-10
        Bx = - (MU_0 * I_val / (2 * np.pi)) * (Y / r2)
        By =   (MU_0 * I_val / (2 * np.pi)) * (X / r2)
        B_norm = np.sqrt(Bx**2 + By**2)
        
        if I_val != 0:
            ax.streamplot(X, Y, Bx, By, color='#2c3e50', linewidth=1.5, density=1.5, arrowsize=2)
        else:
            # Si pas de courant, limaille aléatoire (bruit)
            ax.scatter(X, Y, color='gray', s=1, alpha=0.3)
            
    # 3. Le fil conducteur en cuivre (Gros point central)
    couleur_fil = '#d35400' # Couleur cuivre
    ax.add_patch(plt.Circle((0, 0), 0.005, color=couleur_fil, zorder=5))
    ax.add_patch(plt.Circle((0, 0), 0.005, color='black', fill=False, linewidth=2, zorder=6))
    
    # Indicateur du sens du courant sur le fil
    if I_val > 0:
        ax.plot(0, 0, marker='.', color='black', markersize=10, zorder=7) # Sortant
    elif I_val < 0:
        ax.plot(0, 0, marker='x', color='black', markersize=8, markeredgewidth=2, zorder=7) # Entrant
        
    if mode == "oersted":
        # 4. Modélisation de la vraie boussole
        Bx_fil, By_fil = 0, (MU_0 * I_val) / (2 * np.pi * dist_m)
        Bx_res, By_res = Bx_fil, By_fil + B_TERRE
        
        norm = np.sqrt(Bx_res**2 + By_res**2)
        dx, dy = (Bx_res/norm, By_res/norm) if norm > 0 else (0, 1)
        
        # Dimensions de l'aiguille
        L, l = 0.015, 0.004
        
        # Calcul des sommets du losange pour la boussole (rotation)
        p1 = (dist_m + dx*L, dy*L)           # Pointe Nord
        p2 = (dist_m - dy*l, dx*l)           # Coin gauche
        p3 = (dist_m - dx*L, -dy*L)          # Pointe Sud
        p4 = (dist_m + dy*l, -dx*l)          # Coin droit
        
        # Dessin du pôle Nord (Rouge)
        nord = patches.Polygon([p1, p2, (dist_m,0), p4], closed=True, facecolor='#e74c3c', edgecolor='black', zorder=4)
        # Dessin du pôle Sud (Bleu)
        sud = patches.Polygon([p3, p2, (dist_m,0), p4], closed=True, facecolor='#3498db', edgecolor='black', zorder=4)
        
        ax.add_patch(nord)
        ax.add_patch(sud)
        
        # Socle de la boussole
        ax.add_patch(plt.Circle((dist_m, 0), L*1.2, color='#ecf0f1', fill=True, edgecolor='#bdc3c7', linewidth=2, zorder=3))
        ax.add_patch(plt.Circle((dist_m, 0), 0.002, color='gold', zorder=5)) # Pivot central

    # Nettoyage des axes mathématiques pour un rendu "réel"
    ax.set_xlim(-0.09, 0.09)
    ax.set_ylim(-0.09, 0.09)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

# --- ZONE D'AFFICHAGE CENTRALE ---
with col_sim:
    onglets = st.tabs(["🧭 Plaque & Boussole (Oersted)", "🌌 Plaque & Limaille (Spectre)"])
    
    d_cm = st.slider("Déplacer la boussole/sonde sur la plaque (Distance d en cm)", min_value=1.0, max_value=8.0, value=4.0, step=0.1)
    d_m = d_cm / 100.0
    
    with onglets[0]:
        fig_oersted = dessiner_paillasse(I, d_m, mode="oersted")
        st.pyplot(fig_oersted)
        plt.close(fig_oersted)
        
    with onglets[1]:
        fig_spectre = dessiner_paillasse(I, d_m, mode="spectre")
        st.pyplot(fig_spectre)
        plt.close(fig_spectre)

# --- ZONE TESLAMÈTRE ---
with col_mesure:
    st.markdown("<div class='panel-lab'>", unsafe_allow_html=True)
    st.subheader("📟 Teslamètre")
    st.write("Intensité du champ magnétique mesurée par la sonde de Hall :")
    
    # Calcul de B théorique
    B_calc = (MU_0 * abs(I)) / (2 * np.pi * d_m)
    valeur_affichee = B_calc * 1e6 # en µT
    
    # Si le circuit est ouvert, on n'affiche que le bruit ambiant (ou 0)
    if I == 0:
        valeur_affichee = 0.0
        
    # Écran LCD customisé
    st.markdown(f"<div class='lcd-screen'>{valeur_affichee:05.1f} µT</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Notes de l'enseignant :**")
    st.markdown("L'intensité du champ magnétique dépend de la distance $d$ et du courant $I$.")
    st.markdown("</div>", unsafe_allow_html=True)
