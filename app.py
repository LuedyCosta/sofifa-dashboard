import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ast

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }

    label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    .stCaption, small, .caption-text {
        color: #cbd5e1 !important;
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
        color: #ffffff;
        margin-right: 8px;
    }
    .stat-green { background-color: #10b981; }
    .stat-yellow { background-color: #f59e0b; }
    .stat-red { background-color: #ef4444; }
    .stat-label {
        color: #f1f5f9 !important;
        font-size: 0.95rem;
    }

    /* Card do Perfil do Jogador */
    .profile-info-box {
        background-color: #1a1f2c;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    /* Container de Jogadores Parecidos */
    .similar-container {
        background-color: #161b26;
        border: 1px dashed #3b82f6;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: -15px;
        margin-bottom: 15px;
    }
    .similar-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        height: 100%;
    }
    .similar-name {
        color: #38bdf8 !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        margin-bottom: 2px;
    }
    .similar-meta {
        font-size: 0.8rem;
        color: #cbd5e1 !important;
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
        df = pd.read_csv("sofifa_players_2.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("sofifa_players.csv")
        except FileNotFoundError:
            st.error("❌ Arquivo de dados não encontrado.")
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

def find_similar_players(df, target_player, top_n=3):
    gender = target_player.get('GENDER', 'M')
    candidates = df[(df['GENDER'] == gender) & (df['Name'] != target_player['Name'])].copy()
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
# 4. BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard SoFIFA")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navegação:", ["👤 Perfil", "🛡️ Equipes", "⚽ Jogadores", "⚔️ Comparar"])

df = df_raw.copy()

# -----------------------------------------------------------------------------
# 5. PÁGINA PERFIL
# -----------------------------------------------------------------------------
if page == "👤 Perfil":
    st.title("👤 Perfil Detalhado")

    col_quem, col_similar = st.columns([1, 2.3])

    with col_quem:
        st.markdown("### 1 · Quem")
        who_type = st.radio("Selecione a Entidade:", ["Jogador", "Time"], horizontal=True, label_visibility="collapsed")

    if who_type == "Jogador":
        player_list = sorted(df['Name'].unique().tolist())

        default_index = player_list.index("Bradley Barcola") if "Bradley Barcola" in player_list else 0
        
        with col_quem:
            target_player_name = st.selectbox("Buscar Jogador:", options=player_list, index=default_index)

        p = df[df['Name'] == target_player_name].iloc[0]
        similar_df = find_similar_players(df, p, top_n=3)

        # PAINEL DE JOGADORES PARECIDOS
        with col_similar:
            st.markdown("### 👥 Jogadores Parecidos")
            sim_cols = st.columns(3)
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
                            <b>Pos:</b> {sim_p['Position']} | <b>Idade:</b> {sim_p['Age']} yrs<br>
                            <b>OVR:</b> {sim_p['OVR']} | <b>Clube:</b> {sim_p['Team']}<br>
                            <span style="color:#94a3b8; font-size:0.75rem;">Estilo: {styles_txt}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        # Estilo de jogo do jogador selecionado
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

        # PAINEL DE PERFIL DO JOGADOR
        c_face, c_info, c_details = st.columns([1.2, 2.5, 3.3])
        
        with c_face:
            card_img = p.get('card', '')
            if pd.notna(card_img) and str(card_img).startswith("http"):
                st.image(card_img, width=140)
            else:
                st.image("https://cdn.sofifa.net/player_0.png", width=130)

        with c_info:
            st.subheader(f"🏃 {p['Name']}")
            st.markdown(f"**Clube:** {p['Team']} ({p['League']})")
            st.markdown(f"**Posição:** `{p['Position']}` | **Nacionalidade:** {p.get('Nation', 'N/A')}")
            st.markdown(f"**Overall:** `{p['OVR']}` | **Idade:** {p['Age']} anos")

        with c_details:
            st.markdown(f"""
            <div class="profile-info-box">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong style="color:#cbd5e1;">Perfil</strong><br>
                        <span>Perna boa: <b>{perna_boa}</b></span><br>
                        <span><b>{fintas} ★</b> Fintas</span><br>
                        <span><b>{perna_ruim} ★</b> Perna ruim</span><br>
                        <span>Rank: <b>#{rep_int}</b></span>
                    </div>
                    <div>
                        <strong style="color:#cbd5e1;">Atributos Globais</strong><br>
                        <span style="color:#10b981;">PAC: {p.get('PAC', 0)}</span> | 
                        <span style="color:#f59e0b;">SHO: {p.get('SHO', 0)}</span><br>
                        <span style="color:#3b82f6;">PAS: {p.get('PAS', 0)}</span> | 
                        <span style="color:#8b5cf6;">DRI: {p.get('DRI', 0)}</span><br>
                        <span style="color:#ef4444;">DEF: {p.get('DEF', 0)}</span> | 
                        <span style="color:#ec4899;">PHY: {p.get('PHY', 0)}</span>
                    </div>
                    <div>
                        <strong style="color:#cbd5e1;">Clube</strong><br>
                        <span><b>{p['Team']}</b></span><br>
                        <span style="color:#38bdf8;">Posição {p['Position']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 2. INDICADORES DE PERFORMANCE E COMPARAÇÃO
        st.markdown("### 2 · Indicadores de Performance")

        selected_stats_map = {}

        with st.expander("📌 Clique para expandir e selecionar as Estatísticas por Grupo", expanded=True):
            cols = st.columns(4)
            group_keys = list(STAT_GROUPS.keys())
            
            for idx, group_name in enumerate(group_keys):
                col_target = cols[idx % 4]
                with col_target:
                    st.markdown(f"**{group_name}**")
                    for stat_label, csv_col in STAT_GROUPS[group_name].items():
                        is_default = stat_label in ['Aceleração', 'Pique', 'Dribles', 'Curva']
                        checked = st.checkbox(stat_label, value=is_default, key=f"chk_{group_name}_{stat_label}")
                        if checked:
                            selected_stats_map[stat_label] = csv_col

        # ÁREA DE COMPARAÇÃO NO LADO ESQUERDO DO GRÁFICO (ÁREA AMARELA)
        col_comp_left, col_chart_right = st.columns([1, 2.5])

        with col_comp_left:
            st.markdown("#### ⚔️ Comparar Jogadores")
            st.caption("Adicione até 3 jogadores para comparar com o selecionado:")

            # Lista de opções excluindo o jogador atual
            other_players = [name for name in player_list if name != target_player_name]
            
            compared_players = st.multiselect(
                "Adicionar Jogadores:",
                options=other_players,
                max_selections=3,
                placeholder="Busque e selecione..."
            )

        with col_chart_right:
            if selected_stats_map:
                radar_labels = list(selected_stats_map.keys())
                theta_labs = radar_labels + [radar_labels[0]]

                fig = go.Figure()

                # 1. Jogador Principal (Vermelho)
                radar_values = [get_val(p, csv_col) for csv_col in selected_stats_map.values()]
                r_vals = radar_values + [radar_values[0]]

                fig.add_trace(go.Scatterpolar(
                    r=r_vals,
                    theta=theta_labs,
                    mode='lines+markers',
                    fill='none',
                    line=dict(color='#ef4444', width=3),
                    marker=dict(size=8, color='#ef4444'),
                    name=f"{p['Name']} (Principal)"
                ))

                # Cores contrastantes para os até 3 jogadores comparados
                comp_colors = ['#3b82f6', '#10b981', '#f59e0b']  # Azul, Verde, Amarelo

                # 2. Jogadores Selecionados para Comparação
                for idx, comp_name in enumerate(compared_players):
                    comp_row = df[df['Name'] == comp_name].iloc[0]
                    comp_radar_values = [get_val(comp_row, csv_col) for csv_col in selected_stats_map.values()]
                    comp_r_vals = comp_radar_values + [comp_radar_values[0]]
                    color = comp_colors[idx % len(comp_colors)]

                    fig.add_trace(go.Scatterpolar(
                        r=comp_r_vals,
                        theta=theta_labs,
                        mode='lines+markers',
                        fill='none',
                        line=dict(color=color, width=2.5, dash='solid'),
                        marker=dict(size=7, color=color),
                        name=f"{comp_row['Name']} ({comp_row['OVR']})"
                    ))

                fig.update_layout(
                    title=dict(
                        text=f"Análise Comparativa Radar: {p['Name']} (OVR: {p['OVR']})",
                        font=dict(color='#ffffff', size=16)
                    ),
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            tickfont=dict(color='#cbd5e1'),
                            gridcolor='#334155'
                        ),
                        angularaxis=dict(
                            tickfont=dict(color='#ffffff', size=13),
                            gridcolor='#334155'
                        )
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=480,
                    margin=dict(l=30, r=30, t=50, b=40),
                    legend=dict(
                        font=dict(color='#f8fafc'),
                        orientation="h",
                        yanchor="bottom",
                        y=-0.18,
                        xanchor="center",
                        x=0.5
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Marque pelo menos uma estatística para exibir o gráfico.")

        st.markdown("---")

        # 3. ESTATÍSTICAS DETALHADAS DINÂMICAS DO JOGADOR
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
                    st.markdown(f"- **{style}**")
            else:
                st.markdown("- *Nenhum estilo de jogo específico*")

    else:
        # Perfil do Time
        clubs_list = sorted([c for c in df_raw['Team'].unique() if c != 'Sem Clube'])
        target_club = st.selectbox("Buscar Time:", options=clubs_list)
        club_df = df_raw[df_raw['Team'] == target_club]

        st.subheader(f"🛡️ {target_club}")
        c1, c2 = st.columns(2)
        c1.metric("Média Overall", f"{club_df['OVR'].mean():.1f}")
        c2.metric("Elenco Total", f"{len(club_df)} Jogadores")

# -----------------------------------------------------------------------------
# DEMAIS PÁGINAS
# -----------------------------------------------------------------------------
elif page == "🛡️ Equipes":
    st.title("🛡️ Comparação de Equipes")
    club_stats = df_raw.groupby('Team').agg(
        Total_Jogadores=('Name', 'count'),
        Media_Overall=('OVR', 'mean')
    ).reset_index()
    st.dataframe(club_stats, use_container_width=True, hide_index=True)

elif page == "⚽ Jogadores":
    st.title("⚽ Visão Geral dos Jogadores")
    st.dataframe(df_raw, use_container_width=True, hide_index=True)

elif page == "⚔️ Comparar":
    st.title("⚔️ Comparativo 1vs1")
    all_players = sorted(df_raw['Name'].unique().tolist())
    p1_name = st.selectbox("Jogador 1:", options=all_players, index=0)
    p2_name = st.selectbox("Jogador 2:", options=all_players, index=1 if len(all_players)>1 else 0)
    p1, p2 = df_raw[df_raw['Name'] == p1_name].iloc[0], df_raw[df_raw['Name'] == p2_name].iloc[0]

    cats = ['Aceleração', 'Finalização', 'Passe curto', 'Dribles', 'Intercept.', 'Força']
    p1_vals = [get_val(p1, 'Acceleration'), get_val(p1, 'Finishing'), get_val(p1, 'Short Passing'), get_val(p1, 'Dribbling'), get_val(p1, 'Interceptions'), get_val(p1, 'Strength')]
    p2_vals = [get_val(p2, 'Acceleration'), get_val(p2, 'Finishing'), get_val(p2, 'Short Passing'), get_val(p2, 'Dribbling'), get_val(p2, 'Interceptions'), get_val(p2, 'Strength')]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=p1_vals + [p1_vals[0]], theta=cats + [cats[0]], fill='none', name=p1['Name'], line=dict(color='#ef4444')))
    fig.add_trace(go.Scatterpolar(r=p2_vals + [p2_vals[0]], theta=cats + [cats[0]], fill='none', name=p2['Name'], line=dict(color='#3b82f6')))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
