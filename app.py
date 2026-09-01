import streamlit as st
import pandas as pd
import numpy as np
import ast

from painel_tatico import renderizar_painel_tatico
from explicando_stats import renderizar_explicando_stats
from playstyles import renderizar_playstyles
from perfil import renderizar_perfil

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS GLOBAIS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp, .stApp > header {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* ESTILIZAÇÃO DA BARRA LATERAL */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(0, 255, 204, 0.2) !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(0, 255, 204, 0.2) !important;
    }

    /* CORREÇÃO DEFINITIVA DA COR DAS ABAS PARA O VERDE/CIANO */
    div[data-baseweb="tab-list"] button {
        color: #94a3b8 !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #00ffcc !important;
        border-bottom-color: #00ffcc !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #00ffcc !important;
        font-weight: bold !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #00ffcc !important;
    }
    
    .var-text {
        color: #00ffcc !important;
        font-weight: bold;
    }
    .stCaption, small, .caption-text {
        color: #94a3b8 !important;
    }
    div[data-testid="stButton"] button {
        background-color: #1a2234 !important;
        color: #00ffcc !important;
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        white-space: nowrap !important;
        height: 38px !important;
        min-height: 38px !important;
        padding: 0px 16px !important;
        margin-top: 5px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #00ffcc !important;
        border-color: #00ffcc !important;
        color: #0b0f19 !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4) !important;
    }
    
    .profile-info-box {
        background-color: #131b2e !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        display: block !important;
        overflow: hidden !important;
    }
    
    .similar-card, .tactical-card, .custom-box {
        background-color: #131b2e !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 16px !important;
        width: 100% !important;
    }
    .similar-card {
        background-color: #0b0f19;
        border: 1px dashed rgba(0, 255, 204, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
    }
    .similar-name {
        color: #00ffcc !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        margin-bottom: 6px;
    }
    .similar-meta {
        font-size: 0.8rem;
        color: #ffffff !important;
    }
    .stat-box {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .stat-badge {
        width: 36px;
        height: 26px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85rem;
        color: #ffffff !important;
        margin-right: 10px;
        flex-shrink: 0;
    }
    .stat-green { background-color: #10b981; }
    .stat-yellow { background-color: #f59e0b; }
    .stat-red { background-color: #ef4444; }
    .stat-label {
        color: #ffffff !important;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MAPEAMENTO E DADOS
# -----------------------------------------------------------------------------
STAT_GROUPS = {
    'Ofensivo': {'Cruzamento': 'Crossing', 'Finalização': 'Finishing', 'Prec. Cabeceio': 'Heading Accuracy', 'Passe curto': 'Short Passing', 'Voleios': 'Volleys'},
    'Habilidade': {'Dribles': 'Dribbling', 'Curva': 'Curve', 'Prec. faltas': 'Free Kick Accuracy', 'Lançamento': 'Long Passing', 'Controle bola': 'Ball Control'},
    'Movimentação': {'Aceleração': 'Acceleration', 'Pique': 'Sprint Speed', 'Agilidade': 'Agility', 'Reação': 'Reactions', 'Equilíbrio': 'Balance'},
    'Força': {'Força chute': 'Shot Power', 'Impulsão': 'Jumping', 'Fôlego': 'Stamina', 'Força': 'Strength', 'Chutes longe': 'Long Shots'},
    'Mentalidade': {'Combatividade': 'Aggression', 'Intercept.': 'Interceptions', 'Pos. ataque': 'Positioning', 'Visão de jogo': 'Vision', 'Pênaltis': 'Penalties', 'Compostura': 'Composure'},
    'Defesa': {'Hab. defensiva': 'Def Awareness', 'Dividida pé': 'Standing Tackle', 'Carrinho': 'Sliding Tackle'},
    'Atributos GL': {'Elasticidade GL': 'GK Diving', 'Manejo GL': 'GK Handling', 'Chute GL': 'GK Kicking', 'Posicion. GL': 'GK Positioning', 'Reflexos GL': 'GK Reflexes'},
    'Playstyles': {}
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("EAFC26.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("sofifa_players_2.csv")
        except FileNotFoundError:
            try:
                df = pd.read_csv("sofifa_players.csv")
            except FileNotFoundError:
                st.error("❌ Arquivo EAFC26.csv não encontrado.")
                st.stop()

    df['Name'] = df['Name'].fillna('Jogador Sem Nome').astype(str)
    df['Team'] = df['Team'].fillna('Sem Clube').astype(str)
    df['Position'] = df['Position'].fillna('N/A').astype(str)
    df['League'] = df['League'].fillna('Desconhecida').astype(str)
    df['GENDER'] = df['GENDER'].fillna('M').astype(str)
    df['Preferred foot'] = df['Preferred foot'].fillna('Right').astype(str)
    
    for col in ['OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Age', 'Weak foot', 'Skill moves']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    return df

df_raw = load_data()

def get_val(player_row, col_name, default=50):
    if col_name in player_row.index and pd.notna(player_row[col_name]):
        val = pd.to_numeric(player_row[col_name], errors='coerce')
        if not pd.isna(val):
            return int(val)
    return int(default)

def find_similar_players(df, target_player, top_n=3, regens_only=False):
    gender = target_player.get('GENDER', 'M')
    cond = (df['GENDER'] == gender) & (df['Name'] != target_player['Name'])
    if regens_only:
        cond = cond & (df['Age'] <= 23)
    candidates = df[cond].copy()
    if candidates.empty:
        return candidates

    stat_cols = ['OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Age']
    target_vec = np.array([get_val(target_player, col, 50) for col in stat_cols], dtype=float)
    cand_vecs = candidates[stat_cols].apply(pd.to_numeric, errors='coerce').fillna(50).to_numpy(dtype=float)
    std_vec = np.array(df[stat_cols].apply(pd.to_numeric, errors='coerce').std().values, dtype=float)
    std_vec = np.where((np.isnan(std_vec)) | (std_vec == 0), 1.0, std_vec)

    dist = np.linalg.norm((cand_vecs - target_vec) / std_vec, axis=1)
    target_pos = str(target_player['Position'])
    pos_penalty = np.where(candidates['Position'] == target_pos, 0.0, 1.2)

    try:
        t_styles = set(ast.literal_eval(str(target_player.get('play style', '[]'))))
    except:
        t_styles = set()

    def style_dist(style_str):
        try:
            s_set = set(ast.literal_eval(str(style_str)))
            if not t_styles and not s_set: return 0.0
            union = len(t_styles.union(s_set))
            return 1.0 - (len(t_styles.intersection(s_set)) / union) if union > 0 else 1.0
        except:
            return 1.0

    style_penalties = candidates['play style'].apply(style_dist).to_numpy(dtype=float) * 1.0
    candidates['similarity_score'] = dist + pos_penalty + style_penalties
    return candidates.sort_values('similarity_score').head(top_n)

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL COM TÍTULO NO TOPO E NAVEGAÇÃO ABAIXO
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Dashboard FC26 by\n### Luedy Costa")
    st.markdown("---")
    
    # Menu de navegação limpo posicionado após o título
    pagina = st.radio(
        "Navegação",
        options=["Perfil Detalhado", "Formações", "PlayStyles", "Explicando stats"],
        format_func=lambda x: {
            "Perfil Detalhado": "👤 Perfil Detalhado",
            "Formações": "📋 Formações",
            "PlayStyles": "⚡ PlayStyles",
            "Explicando stats": "📊 Explicando stats"
        }[x],
        label_visibility="collapsed"
    )

df = df_raw.copy()

# Renderização da página selecionada
if pagina == "Perfil Detalhado":
    renderizar_perfil(df, find_similar_players, STAT_GROUPS, get_val)
elif pagina == "Formações":
    renderizar_painel_tatico()
elif pagina == "PlayStyles":
    renderizar_playstyles()
elif pagina == "Explicando stats":
    renderizar_explicando_stats()
