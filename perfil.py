import streamlit as st
import pandas as pd
import numpy as np
import ast

from painel_tatico import renderizar_painel_tatico
from explicando_stats import renderizar_explicando_stats
from playstyles import renderizar_playstyles
from busca_jogadores import renderizar_busca_jogadores

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS GLOBAIS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA & FC26 Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .streamlit-expanderHeader { color: #ffffff !important; }
    .stCheckbox label { color: #ffffff !important; }
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
    }
    div[data-testid="stButton"] button:hover {
        background-color: #00ffcc !important;
        border-color: #00ffcc !important;
        color: #0b0f19 !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4) !important;
    }
    .profile-info-box, .similar-card, .tactical-card, .custom-box {
        background-color: #131b2e !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 20px !important;
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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARREGAMENTO DE DADOS E FUNÇÕES AUXILIARES
# -----------------------------------------------------------------------------
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
# 3. BARRA LATERAL E NAVEGAÇÃO MODERNA (st.navigation)
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard FC26")
st.sidebar.markdown("---")

df = df_raw.copy()

# Wrapper function para injetar o dataframe e a função de similares no perfil
def wrapper_perfil():
    renderizar_perfil(df, find_similar_players)

# Definindo as páginas usando st.Page e st.navigation
pagina_perfil = st.Page(wrapper_perfil, title="Perfil Detalhado", icon="👤", default=True)
pagina_formacoes = st.Page(renderizar_painel_tatico, title="Formações", icon="📋")
pagina_playstyles = st.Page(renderizar_playstyles, title="PlayStyles", icon="⚡")
pagina_stats = st.Page(renderizar_explicando_stats, title="Explicando stats", icon="📊")
pagina_busca = st.Page(renderizar_busca_jogadores, title="Busca de Jogadores", icon="🔎")

pg = st.navigation([pagina_perfil, pagina_formacoes, pagina_playstyles, pagina_stats, pagina_busca])

# Executa a navegação
pg.run()
