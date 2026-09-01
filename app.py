import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ast

# Importação da função do arquivo painel_tatico.py
from painel_tatico import renderizar_painel_tatico
from explicando_stats import renderizar_explicando_stats

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA & FC26 Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fundo Totalmente Preto */
    .stApp, .stApp > header {
        background-color: #000000;
        color: #ffffff;
    }

    /* Textos Fixos Brancos */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Expander e Checkboxes Textos Brancos */
    .streamlit-expanderHeader { color: #ffffff !important; }
    .stCheckbox label { color: #ffffff !important; }

    /* Classe para Textos Variáveis (Dinâmicos) em Verde */
    .var-text {
        color: #10b981 !important; /* Verde 500 */
        font-weight: bold;
    }

    .stCaption, small, .caption-text {
        color: #a3a3a3 !important;
    }

    /* Estilização Customizada de Botões Globais */
    div[data-testid="stButton"] button {
        background-color: #808080 !important; /* Cinza 50% */
        color: #ffffff !important;
        border: none !important;
        white-space: nowrap !important; /* Força 1 linha */
        height: 38px !important;
        min-height: 38px !important;
        padding: 0px 16px !important;
        margin-top: 5px !important;
        border-radius: 6px !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #a3a3a3 !important;
        border: none !important;
        color: #ffffff !important;
    }
    div[data-testid="stButton"] button p {
        color: #ffffff !important;
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

    /* Card do Perfil do Jogador */
    .profile-info-box {
        background-color: #111111;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #333333;
        margin-bottom: 20px;
    }

    /* Container de Jogadores Parecidos */
    .similar-container {
        background-color: #000000;
        border: 1px dashed #333333;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: -15px;
        margin-bottom: 15px;
    }
    .similar-card {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        height: 100%;
    }
    .similar-name {
        color: #10b981 !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        margin-bottom: 2px;
    }
    .similar-meta {
        font-size: 0.8rem;
        color: #ffffff !important;
    }
    
    /* Cards de Conteúdo Tático */
    .tactical-card {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MAPEAMENTO DOS GRUPOS
# -----------------------------------------------------------------------------
STAT_GROUPS = {
    'Ofensivo': {
        'Cruzamento': 'Crossing',
        'Finalização': 'Finishing',
        'Prec. Cabeceio': 'Heading Accuracy',
        'Passe curto': 'Short Passing',
        'Voleios': 'Volleys'
    },
    'Habilidade': {
        'Dribles': 'Dribbling',
        'Curva': 'Curve',
        'Prec. faltas': 'Free Kick Accuracy',
        'Lançamento': 'Long Passing',
        'Controle bola': 'Ball Control'
    },
    'Movimentação': {
        'Aceleração': 'Acceleration',
        'Pique': 'Sprint Speed',
        'Agilidade': 'Agility',
        'Reação': 'Reactions',
        'Equilíbrio': 'Balance'
    },
    'Força': {
        'Força chute': 'Shot Power',
        'Impulsão': 'Jumping',
        'Fôlego': 'Stamina',
        'Força': 'Strength',
        'Chutes longe': 'Long Shots'
    },
    'Mentalidade': {
        'Combatividade': 'Aggression',
        'Intercept.': 'Interceptions',
        'Pos. ataque': 'Positioning',
        'Visão de jogo': 'Vision',
        'Pênaltis': 'Penalties',
        'Compostura': 'Composure'
    },
    'Defesa': {
        'Hab. defensiva': 'Def Awareness',
        'Dividida pé': 'Standing Tackle',
        'Carrinho': 'Sliding Tackle'
    },
    'Atributos GL': {
        'Elasticidade GL': 'GK Diving',
        'Manejo GL': 'GK Handling',
        'Chute GL': 'GK Kicking',
        'Posicion. GL': 'GK Positioning',
        'Reflexos GL': 'GK Reflexes'
    }
}

# -----------------------------------------------------------------------------
# 3. LEITURA DOS DADOS E ALGORITMO DE SIMILARIDADE
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
            if not t_styles and not s_set:
                return 0.0
            union = len(t_styles.union(s_set))
            return 1.0 - (len(t_styles.intersection(s_set)) / union) if union > 0 else 1.0
        except:
            return 1.0

    style_penalties = candidates['play style'].apply(style_dist).to_numpy(dtype=float) * 1.0
    candidates['similarity_score'] = dist + pos_penalty + style_penalties
    return candidates.sort_values('similarity_score').head(top_n)

# -----------------------------------------------------------------------------
# 4. BARRA LATERAL E NAVEGAÇÃO ENTRE PÁGINAS
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard FC26")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")

page_selection = st.sidebar.radio("Ir para:", ["Perfil Detalhado", "Formações"])

df = df_raw.copy()

# -----------------------------------------------------------------------------
# 5. PÁGINA 1: PERFIL DETALHADO
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
        if not isinstance(play_styles, list):
            play_styles = []
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
        st.markdown(f"**Posição:** <span style='background-color: #262626; color: #10b981; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['Position']}</span> | **Nacionalidade:** <span class='var-text'>{p.get('Nation', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall:** <span style='background-color: #262626; color: #10b981; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['OVR']}</span> | **Idade:** <span class='var-text'>{p['Age']} anos</span>", unsafe_allow_html=True)

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
                        <span style="color:#a3a3a3; font-size:0.75rem;">Estilo: <span class="var-text">{styles_txt}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum jogador semelhante encontrado com esses critérios.")

    st.markdown("---")

    all_stat_keys = []
    for g_name, g_stats in STAT_GROUPS.items():
        for stat_label in g_stats.keys():
            all_stat_keys.append(f"chk_{g_name}_{stat_label}")

    def select_all_stats():
        for k in all_stat_keys:
            st.session_state[k] = True

    def deselect_all_stats():
        for k in all_stat_keys:
            st.session_state[k] = False

    POSITION_SUGGESTIONS = {
        'ST': ['Finalização', 'Pos. ataque', 'Aceleração', 'Pique', 'Força chute', 'Compostura'],
        'CF': ['Finalização', 'Dribles', 'Controle bola', 'Visão de jogo', 'Pos. ataque', 'Agilidade'],
        'LW': ['Aceleração', 'Pique', 'Dribles', 'Agilidade', 'Cruzamento', 'Finalização'],
        'RW': ['Aceleração', 'Pique', 'Dribles', 'Agilidade', 'Cruzamento', 'Finalização'],
        'LM': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Passe curto', 'Dribles'],
        'RM': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Passe curto', 'Dribles'],
        'CAM': ['Visão de jogo', 'Passe curto', 'Lançamento', 'Dribles', 'Controle bola', 'Compostura'],
        'CM': ['Passe curto', 'Lançamento', 'Visão de jogo', 'Fôlego', 'Reação', 'Combatividade'],
        'CDM': ['Intercept.', 'Hab. defensiva', 'Dividida pé', 'Combatividade', 'Fôlego', 'Força'],
        'CB': ['Hab. defensiva', 'Dividida pé', 'Prec. Cabeceio', 'Força', 'Combatividade', 'Intercept.'],
        'LB': ['Aceleração', 'Pique', 'Cruzamento', 'Hab. defensiva', 'Dividida pé', 'Fôlego'],
        'RB': ['Aceleração', 'Pique', 'Cruzamento', 'Hab. defensiva', 'Dividida pé', 'Fôlego'],
        'LWB': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Hab. defensiva', 'Dividida pé'],
        'RWB': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Hab. defensiva', 'Dividida pé'],
        'GK': ['Elasticidade GL', 'Manejo GL', 'Chute GL', 'Posicion. GL', 'Reflexos GL', 'Reação']
    }

    def suggest_stats():
        for k in all_stat_keys:
            st.session_state[k] = False
        pos = str(p.get('Position', 'CM')).upper()
        suggested_list = POSITION_SUGGESTIONS.get(pos, POSITION_SUGGESTIONS['CM'])
        for g_name, g_stats in STAT_GROUPS.items():
            for stat_label in g_stats.keys():
                if stat_label in suggested_list:
                    st.session_state[f"chk_{g_name}_{stat_label}"] = True

    c_title, c_btn1, c_btn2, c_btn3 = st.columns([2.2, 1.1, 1.1, 1.1])
    with c_title:
        st.markdown("### 2 · Indicadores de Performance")
    with c_btn1:
        st.button("✅ Marcar Todos", on_click=select_all_stats, use_container_width=True)
    with c_btn2:
        st.button("❌ Desmarcar", on_click=deselect_all_stats, use_container_width=True)
    with c_btn3:
        st.button("💡 Sugestão", on_click=suggest_stats, use_container_width=True)

    selected_stats_map = {}

    with st.expander("📌 Clique para expandir e selecionar as Estatísticas por Grupo", expanded=True):
        cols = st.columns(4)
        group_keys = list(STAT_GROUPS.keys())
        for idx, group_name in enumerate(group_keys):
            col_target = cols[idx % 4]
            with col_target:
                st.markdown(f"**{group_name}**")
                for stat_label, csv_col in STAT_GROUPS[group_name].items():
                    chk_key = f"chk_{group_name}_{stat_label}"
                    if chk_key not in st.session_state:
                        st.session_state[chk_key] = stat_label in ['Aceleração', 'Pique', 'Dribles', 'Curva']
                    checked = st.checkbox(stat_label, key=chk_key)
                    if checked:
                        selected_stats_map[stat_label] = csv_col

    col_comp_left, col_chart_right = st.columns([1, 2.5])

    with col_comp_left:
        st.markdown("#### ⚔️ Comparar Jogadores")
        st.caption("Adicione até 3 jogadores para comparar com o selecionado:")

        other_players = ["Nenhum"] + [name for name in player_list if name != target_player_name]
        comp1 = st.selectbox("🔵 Jogador Comparado 1:", options=other_players, index=0, key="comp_slot_1")
        options_p2 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1]] if comp1 != "Nenhum" else ["Nenhum"]
        comp2 = st.selectbox("🟢 Jogador Comparado 2:", options=options_p2, index=0, key="comp_slot_2", disabled=(comp1 == "Nenhum"))
        options_p3 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1, comp2]] if comp2 != "Nenhum" else ["Nenhum"]
        comp3 = st.selectbox("🟡 Jogador Comparado 3:", options=options_p3, index=0, key="comp_slot_3", disabled=(comp2 == "Nenhum"))

    with col_chart_right:
        if selected_stats_map:
            radar_labels = list(selected_stats_map.keys())
            theta_labs = radar_labels + [radar_labels[0]]

            fig = go.Figure()
            radar_values = [get_val(p, csv_col) for csv_col in selected_stats_map.values()]
            r_vals = radar_values + [radar_values[0]]

            fig.add_trace(go.Scatterpolar(
                r=r_vals, theta=theta_labs, mode='lines+markers', fill='none',
                line=dict(color='#ef4444', width=3), marker=dict(size=8, color='#ef4444'),
                name=f"{p['Name']} (Principal)"
            ))

            slot_colors = {'comp_slot_1': '#3b82f6', 'comp_slot_2': '#10b981', 'comp_slot_3': '#f59e0b'}
            active_slots = [('comp_slot_1', comp1), ('comp_slot_2', comp2), ('comp_slot_3', comp3)]

            for slot_key, comp_name in active_slots:
                if comp_name != "Nenhum":
                    comp_row = df[df['Name'] == comp_name].iloc[0]
                    comp_radar_values = [get_val(comp_row, csv_col) for csv_col in selected_stats_map.values()]
                    comp_r_vals = comp_radar_values + [comp_radar_values[0]]
                    color = slot_colors[slot_key]

                    fig.add_trace(go.Scatterpolar(
                        r=comp_r_vals, theta=theta_labs, mode='lines+markers', fill='none',
                        line=dict(color=color, width=2.5, dash='solid'), marker=dict(size=7, color=color),
                        name=f"{comp_row['Name']} ({comp_row['OVR']})"
                    ))

            fig.update_layout(
                title=dict(text=f"Análise Comparativa Radar: {p['Name']} (OVR: {p['OVR']})", font=dict(color='#ffffff', size=16)),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#cbd5e1'), gridcolor='#333333'),
                    angularaxis=dict(tickfont=dict(color='#ffffff', size=13), gridcolor='#333333')
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=480,
                margin=dict(l=30, r=30, t=50, b=40),
                legend=dict(font=dict(color='#ffffff'), orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Marque pelo menos uma estatística para exibir o gráfico.")

    st.markdown("---")

    st.markdown("### 📊 Estatísticas Detalhadas do Jogador")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### Ofensivo")
        for lbl, col in STAT_GROUPS['Ofensivo'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Mentalidade")
        for lbl, col in STAT_GROUPS['Mentalidade'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)

    with col2:
        st.markdown("#### Habilidade")
        for lbl, col in STAT_GROUPS['Habilidade'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Defesa")
        for lbl, col in STAT_GROUPS['Defesa'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)

    with col3:
        st.markdown("#### Movimentação")
        for lbl, col in STAT_GROUPS['Movimentação'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Atributos GL")
        for lbl, col in STAT_GROUPS['Atributos GL'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col, 10)), unsafe_allow_html=True)

    with col4:
        st.markdown("#### Força")
        for lbl, col in STAT_GROUPS['Força'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Estilos de Jogo")
        if play_styles:
            for style in play_styles:
                st.markdown(f"- **<span class='var-text'>{style}</span>**", unsafe_allow_html=True)
        else:
            st.markdown("- *<span class='var-text'>Nenhum estilo de jogo específico</span>*", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. PÁGINA 2: FORMAÇÕES (CARREGA PAINEL TÁTICO EXTERNO)
# -----------------------------------------------------------------------------
elif page_selection == "Formações":
    st.title("📋 Painel Tático de Formações")
    # Chamada da função que renderiza o componente contido no arquivo painel_tatico.py
    renderizar_painel_tatico()
