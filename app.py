import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ast

from painel_tatico import renderizar_painel_tatico
from explicando_stats import renderizar_explicando_stats
from playstyles import renderizar_playstyles

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
    /* Fundo Totalmente Preto e Fontes Globais */
    .stApp, .stApp > header {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Textos Fixos Brancos */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Expander e Checkboxes */
    .streamlit-expanderHeader { color: #ffffff !important; }
    .stCheckbox label { color: #ffffff !important; }

    /* Classe para Textos Variáveis (Dinâmicos) em Verde */
    .var-text {
        color: #00ffcc !important;
        font-weight: bold;
    }

    .stCaption, small, .caption-text {
        color: #94a3b8 !important;
    }

    /* Estilização Customizada de Botões Globais (Padronizado PlayStyles / Similares) */
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
    div[data-testid="stButton"] button p {
        color: inherit !important;
        font-size: 0.95rem !important;
    }

    /* Badges de Atributos do FIFA */
    .stat-box {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
    }
    .stat-badge {
        width: 34px;
        height: 25px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85rem;
        color: #ffffff !important;
        margin-right: 8px;
    }
    .stat-green { background-color: #10b981; }
    .stat-yellow { background-color: #f59e0b; }
    .stat-red { background-color: #ef4444; }
    .stat-label {
        color: #ffffff !important;
        font-size: 0.95rem;
    }

    /* Cards e Containers Padrão (Perfil, Similares e Táticos) */
    .profile-info-box, .similar-card, .tactical-card, .custom-box {
        background-color: #131b2e !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease !important;
    }
    .profile-info-box:hover, .similar-card:hover, .tactical-card:hover, .custom-box:hover {
        border-color: rgba(0, 255, 204, 0.4) !important;
        box-shadow: 0 8px 24px rgba(0, 255, 204, 0.1) !important;
    }

    .similar-container {
        background-color: #0b0f19;
        border: 1px dashed rgba(0, 255, 204, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin-top: -15px;
        margin-bottom: 15px;
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
# 2. MAPEAMENTO E DADOS
# -----------------------------------------------------------------------------
STAT_GROUPS = {
    'Ofensivo': {'Cruzamento': 'Crossing', 'Finalização': 'Finishing', 'Prec. Cabeceio': 'Heading Accuracy', 'Passe curto': 'Short Passing', 'Voleios': 'Volleys'},
    'Habilidade': {'Dribles': 'Dribbling', 'Curva': 'Curve', 'Prec. faltas': 'Free Kick Accuracy', 'Lançamento': 'Long Passing', 'Controle bola': 'Ball Control'},
    'Movimentação': {'Aceleração': 'Acceleration', 'Pique': 'Sprint Speed', 'Agilidade': 'Agility', 'Reação': 'Reactions', 'Equilíbrio': 'Balance'},
    'Força': {'Força chute': 'Shot Power', 'Impulsão': 'Jumping', 'Fôlego': 'Stamina', 'Força': 'Strength', 'Chutes longe': 'Long Shots'},
    'Mentalidade': {'Combatividade': 'Aggression', 'Intercept.': 'Interceptions', 'Pos. ataque': 'Positioning', 'Visão de jogo': 'Vision', 'Pênaltis': 'Penalties', 'Compostura': 'Composure'},
    'Defesa': {'Hab. defensiva': 'Def Awareness', 'Dividida pé': 'Standing Tackle', 'Carrinho': 'Sliding Tackle'},
    'Atributos GL': {'Elasticidade GL': 'GK Diving', 'Manejo GL': 'GK Handling', 'Chute GL': 'GK Kicking', 'Posicion. GL': 'GK Positioning', 'Reflexos GL': 'GK Reflexes'}
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

def render_stat_item(label, value):
    val_int = int(value) if str(value).isdigit() else 50
    badge_class = "stat-green" if val_int >= 70 else ("stat-yellow" if val_int >= 60 else "stat-red")
    return f"""
    <div class="stat-box">
        <span class="stat-badge {badge_class}">{val_int}</span>
        <span class="stat-label">{label}</span>
    </div>
    """

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
# 3. BARRA LATERAL E NAVEGAÇÃO
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard FC26")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")

page_selection = st.sidebar.radio("Ir para:", ["Perfil Detalhado", "Formações", "PlayStyles", "Explicando stats"])
df = df_raw.copy()

# -----------------------------------------------------------------------------
# 4. RENDERIZAÇÃO DAS PÁGINAS
# -----------------------------------------------------------------------------
if page_selection == "Perfil Detalhado":
    st.title("👤 Perfil Detalhado")

    col_quem, _ = st.columns([1, 2])
    player_list = sorted(df['Name'].unique().tolist())
    default_index = player_list.index("Bradley Barcola") if "Bradley Barcola" in player_list else 0

    with col_quem:
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list, index=default_index)

    p = df[df['Name'] == target_player_name].iloc[0]
    play_styles_raw = str(p.get('play style', '[]'))
    try:
        play_styles = ast.literal_eval(play_styles_raw)
        if not isinstance(play_styles, list): play_styles = []
    except:
        play_styles = []

    perna_boa = "Esq." if p.get('Preferred foot', 'Right') == 'Left' else "Dir."
    fintas = p.get('Skill moves', 2)
    perna_ruim = p.get('Weak foot', 2)
    rep_int = p.get('Rank', 1)

    c_face, c_info, c_details = st.columns([1.2, 2.5, 3.3])

    with c_face:
        card_img = p.get('card', '')
        if pd.notna(card_img) and str(card_img).startswith("http"):
            st.image(card_img, width=140)
        else:
            st.image("https://cdn.sofifa.net/player_0.png", width=130)

    with c_info:
        st.markdown(f"<h2>🏃 <span class='var-text'>{p['Name']}</span></h2>", unsafe_allow_html=True)
        st.markdown(f"**Clube:** <span class='var-text'>{p['Team']}</span> ({p['League']})", unsafe_allow_html=True)
        st.markdown(f"**Posição:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['Position']}</span> | **Nacionalidade:** <span class='var-text'>{p.get('Nation', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['OVR']}</span> | **Idade:** <span class='var-text'>{p['Age']} anos</span>", unsafe_allow_html=True)

    with c_details:
        st.markdown(f"""
        <div class="profile-info-box">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong style="color:#ffffff;">Perfil</strong><br>
                    <span>Perna boa: <b class="var-text">{perna_boa}</b></span><br>
                    <span><b class="var-text">{fintas} ★</b> Fintas</span><br>
                    <span><b class="var-text">{perna_ruim} ★</b> Perna ruim</span><br>
                    <span>Rank: <b class="var-text">#{rep_int}</b></span>
                </div>
                <div>
                    <strong style="color:#ffffff;">Atributos Globais</strong><br>
                    <span>PAC: <b class="var-text">{p.get('PAC', 0)}</b></span> | 
                    <span>SHO: <b class="var-text">{p.get('SHO', 0)}</b></span><br>
                    <span>PAS: <b class="var-text">{p.get('PAS', 0)}</b></span> | 
                    <span>DRI: <b class="var-text">{p.get('DRI', 0)}</b></span><br>
                    <span>DEF: <b class="var-text">{p.get('DEF', 0)}</b></span> | 
                    <span>PHY: <b class="var-text">{p.get('PHY', 0)}</b></span>
                </div>
                <div>
                    <strong style="color:#ffffff;">Clube</strong><br>
                    <span><b class="var-text">{p['Team']}</b></span><br>
                    <span>Posição <b class="var-text">{p['Position']}</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_sim_title, col_btn_todos, col_btn_regen = st.columns([1.5, 0.6, 0.6])
    with col_sim_title:
        st.markdown("### 👥 Jogadores Parecidos")

    if "sim_filter_mode" not in st.session_state:
        st.session_state["sim_filter_mode"] = "Todos"

    with col_btn_todos:
        if st.button("Todos", use_container_width=True):
            st.session_state["sim_filter_mode"] = "Todos"
    with col_btn_regen:
        if st.button("Regen", use_container_width=True):
            st.session_state["sim_filter_mode"] = "Regen"

    is_regens = (st.session_state["sim_filter_mode"] == "Regen")
    similar_df = find_similar_players(df, p, top_n=3, regens_only=is_regens)

    sim_cols = st.columns(3)
    if not similar_df.empty:
        for idx, (_, sim_p) in enumerate(similar_df.iterrows()):
            with sim_cols[idx]:
                try:
                    s_list = ast.literal_eval(str(sim_p.get('play style', '[]')))
                    styles_txt = ", ".join(s_list[:2]) if s_list else "Padrão"
                except:
                    styles_txt = "Padrão"

                st.markdown(f"""
                <div class="similar-card">
                    <div class="similar-name">⚽ {sim_p['Name']}</div>
                    <div class="similar-meta">
                        <b>Pos:</b> <span class="var-text">{sim_p['Position']}</span> | <b>Idade:</b> <span class="var-text">{sim_p['Age']} yrs</span><br>
                        <b>OVR:</b> <span class="var-text">{sim_p['OVR']}</span> | <b>Clube:</b> <span class="var-text">{sim_p['Team']}</span><br>
                        <span style="color:#94a3b8; font-size:0.75rem;">Estilo: <span class="var-text">{styles_txt}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum jogador semelhante encontrado com esses critérios.")

    st.markdown("---")
    # Restante da página de Perfil Detalhado (Gráficos e Atributos)...

elif page_selection == "Formações":
    st.title("📋 Painel Tático de Formações")
    renderizar_painel_tatico()

elif page_selection == "PlayStyles":
    renderizar_playstyles()
    
elif page_selection == "Explicando stats":
    renderizar_explicando_stats()
