import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E CSS PARA ACESSIBILIDADE E CONTRASTE ALTO
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

    /* Acessibilidade: Rótulos e Textos Claros */
    label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    .stCaption, small, .caption-text {
        color: #cbd5e1 !important;
    }

    /* Contrastes nos seletores */
    div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 600 !important;
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

    /* Card da Imagem 4 (Info do Perfil) */
    .profile-info-box {
        background-color: #1a1f2c;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ESTRUTURAÇÃO E MAPEAMENTO DE ESTATÍSTICAS (DA IMAGEM 2)
# -----------------------------------------------------------------------------
STAT_GROUPS = {
    'Ritmo': {
        'Aceleração': ['acceleration', 'Acceleration', 'aceleração', 'Aceleração'],
        'Pique': ['sprint_speed', 'Sprint Speed', 'sprintspeed', 'Pique', 'pique']
    },
    'Chute': {
        'Finalização': ['finishing', 'Finishing', 'finalização', 'Finalização'],
        'Força do Chute': ['shot_power', 'Shot Power', 'shotpower', 'Força do Chute'],
        'Chutes de Longe': ['long_shots', 'Long Shots', 'longshots', 'Chutes de Longe'],
        'Pênaltis': ['penalties', 'Penalties', 'pênaltis', 'Pênaltis'],
        'Pos. ataque': ['att_position', 'Att. Position', 'positioning', 'Pos. ataque'],
        'Voleios': ['volleys', 'Volleys', 'voleios', 'Voleios']
    },
    'Passe': {
        'Visão de jogo': ['vision', 'Vision', 'visão', 'Visão de jogo'],
        'Cruzamento': ['crossing', 'Crossing', 'cruzamento', 'Cruzamento'],
        'Precisão nas faltas': ['fk_accuracy', 'FK Acc.', 'fkaccuracy', 'Precisão nas faltas'],
        'Passe curto': ['short_passing', 'Short Pass', 'shortpassing', 'Passe curto'],
        'Lançamento': ['long_passing', 'Long Pass', 'longpassing', 'Lançamento'],
        'Curva': ['curve', 'Curve', 'curva', 'Curva']
    },
    'Dribles': {
        'Agilidade': ['agility', 'Agility', 'agilidade', 'Agilidade'],
        'Equilíbrio': ['balance', 'Balance', 'equilíbrio', 'Equilíbrio'],
        'Reação': ['reactions', 'Reactions', 'reação', 'Reação'],
        'Controle de bola': ['ball_control', 'Ball Control', 'ballcontrol', 'Controle de bola'],
        'Dribles': ['dribbling', 'Dribbles', 'dribles', 'Dribles'],
        'Compostura': ['composure', 'Composure', 'compostura', 'Compostura']
    },
    'Defesa': {
        'Intercept.': ['interceptions', 'Interceptions', 'intercept.', 'Intercept.'],
        'Precisão no Cabeceio': ['heading_accuracy', 'Heading Acc.', 'headingaccuracy', 'Precisão no Cabeceio'],
        'Habilidade defensiva': ['defensive_awareness', 'Def. Aware', 'defensiveawareness', 'Habilidade defensiva'],
        'Dividida em pé': ['standing_tackle', 'Stand Tackle', 'standingtackle', 'Dividida em pé'],
        'Carrinho': ['sliding_tackle', 'Slide Tackle', 'slidingtackle', 'Carrinho']
    },
    'Físico': {
        'Impulsão': ['jumping', 'Jumping', 'impulsão', 'Impulsão'],
        'Fôlego': ['stamina', 'Stamina', 'fôlego', 'Fôlego'],
        'Força': ['strength', 'Strength', 'força', 'Força'],
        'Combatividade': ['aggression', 'Aggression', 'combatividade', 'Combatividade']
    }
}

# -----------------------------------------------------------------------------
# 3. LEITURA E TRATAMENTO DOS DADOS DO CSV
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sofifa_players.csv")
    except FileNotFoundError:
        st.error("❌ O arquivo 'sofifa_players.csv' não foi encontrado no diretório do projeto.")
        st.stop()

    # Mapeamento de colunas principais caso venham com o nome do scrape original
    rename_dict = {
        'is-preload': 'short_name',
        'is-preload (2)': 'club_name',
        'pos': 'positions',
        'd2': 'age',
        'd2 (2)': 'overall',
        'd2 (3)': 'potential',
        'd6': 'value',
        'd6 (2)': 'wage',
        'player-check src': 'player_face_url'
    }
    df.rename(columns=rename_dict, inplace=True)

    # Limpeza básica de texto
    for col in ['short_name', 'club_name', 'positions', 'value', 'wage']:
        if col in df.columns:
            df[col] = df[col].fillna('N/A').astype(str)
        else:
            df[col] = 'N/A'

    df['player_face_url'] = df.get('player_face_url', pd.Series()).fillna('https://cdn.sofifa.net/player_0.png').astype(str)

    # Conversão numérica segura
    for num_col in ['overall', 'potential', 'age']:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors='coerce').fillna(50).astype(int)
        else:
            df[num_col] = 50

    return df

df_raw = load_data()

# Função auxiliar para buscar o valor real da estatística no CSV para um jogador
def get_player_stat(player_row, possible_col_names):
    for col in possible_col_names:
        if col in player_row.index:
            val = pd.to_numeric(player_row[col], errors='coerce')
            if not pd.isna(val):
                return int(val)
    # Se não encontrar a estatística exata, retorna o overall do jogador
    return int(player_row.get('overall', 50))

# Helper para buscar colunas de perfil (Perna boa, Fintas, Perna ruim, etc)
def get_player_info_field(player_row, possible_col_names, default_val):
    for col in possible_col_names:
        if col in player_row.index and pd.notna(player_row[col]):
            return str(player_row[col])
    return str(default_val)

# Helper para renderizar estatísticas coloridas (Estilo Imagem 3)
def render_stat_item(label, value):
    val_int = int(value) if str(value).isdigit() else 50
    badge_class = "stat-green" if val_int >= 70 else ("stat-yellow" if val_int >= 60 else "stat-red")
    return f"""
    <div class="stat-box">
        <span class="stat-badge {badge_class}">{val_int}</span>
        <span class="stat-label">{label}</span>
    </div>
    """

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

    st.markdown("### 1 · Quem")
    who_type = st.radio("Selecione a Entidade:", ["Jogador", "Time"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    if who_type == "Jogador":
        player_list = sorted(df['short_name'].unique().tolist())
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list)
        p = df[df['short_name'] == target_player_name].iloc[0]

        # Extração das informações reais do CSV referentes à Imagem 4
        perna_boa = get_player_info_field(p, ['preferred_foot', 'Perna boa', 'foot', 'preferredfoot'], 'Esq.')
        fintas = get_player_info_field(p, ['skill_moves', 'Fintas', 'skillmoves'], '2')
        perna_ruim = get_player_info_field(p, ['weak_foot', 'Perna ruim', 'weakfoot'], '2')
        rep_int = get_player_info_field(p, ['international_reputation', 'Rep. Internacional', 'reputation'], '1')
        especialidades = get_player_info_field(p, ['player_traits', 'specialities', 'Especialidades', 'traits'], '#Força')

        # CABEÇALHO DO PERFIL & QUADRO DE INFORMAÇÕES DO CSV (Imagem 4)
        c_face, c_info, c_details = st.columns([1.2, 2.5, 3.3])
        
        with c_face:
            if str(p['player_face_url']).startswith("http"):
                st.image(p['player_face_url'], width=130)

        with c_info:
            st.subheader(f"🏃 {p['short_name']}")
            st.markdown(f"**Clube:** {p['club_name']}")
            st.markdown(f"**Posição:** `{p['positions']}` | **Idade:** {p['age']} anos")
            st.markdown(f"**Overall:** `{p['overall']}` | **Potencial:** `{p['potential']}`")
            st.markdown(f"**Valor:** `{p['value']}` | **Salário:** `{p['wage']}`")

        with c_details:
            st.markdown(f"""
            <div class="profile-info-box">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong style="color:#cbd5e1;">Perfil</strong><br>
                        <span>Perna boa: <b>{perna_boa}</b></span><br>
                        <span><b>{fintas} ★</b> Fintas</span><br>
                        <span><b>{perna_ruim} ★</b> Perna ruim</span><br>
                        <span><b>{rep_int} ★</b> Rep. Internacional</span>
                    </div>
                    <div>
                        <strong style="color:#cbd5e1;">Especialidades</strong><br>
                        <span style="color:#f59e0b; font-weight:bold;">{especialidades}</span>
                    </div>
                    <div>
                        <strong style="color:#cbd5e1;">Clube</strong><br>
                        <span><b>{p['club_name']}</b></span><br>
                        <span style="color:#38bdf8;">Posição {p['positions']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 2. INDICADORES DE PERFORMANCE (SELETOR DA IMAGEM 2 + RADAR OUTLINE DINÂMICO)
        st.markdown("### 2 · Indicadores de Performance")
        
        selected_group_name = st.radio("Grupo de Atributos:", list(STAT_GROUPS.keys()), horizontal=True)
        current_group_dict = STAT_GROUPS[selected_group_name]

        # Multiselect das opções pertencentes ao grupo escolhido
        selected_pt_labels = st.multiselect(
            f"Selecione as estatísticas de {selected_group_name} para o Radar:",
            options=list(current_group_dict.keys()),
            default=list(current_group_dict.keys())
        )

        if selected_pt_labels:
            radar_labels = selected_pt_labels
            # Busca o valor numérico REAL do CSV do jogador para cada estatística
            radar_values = [get_player_stat(p, current_group_dict[label]) for label in selected_pt_labels]

            # Fechar o perímetro do gráfico radar
            r_vals = radar_values + [radar_values[0]]
            theta_labs = radar_labels + [radar_labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=theta_labs,
                mode='lines+markers',
                fill='none',  # OUTLINE PURA (SEM FUNDO BRANCO / PREENCHIMENTO TRANSPARENTE)
                line=dict(color='#ef4444', width=3),
                marker=dict(size=8, color='#ef4444'),
                name=p['short_name']
            ))

            fig.update_layout(
                title=dict(
                    text=f"Análise de {selected_group_name}: {p['short_name']} (Valor: {p['value']})",
                    font=dict(color='#ffffff', size=16)
                ),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',  # Transparência total
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
                height=450,
                margin=dict(l=40, r=40, t=50, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Selecione pelo menos uma estatística acima para exibir o gráfico radar.")

        st.markdown("---")

        # 3. PAINEL COMPLETO DE ESTATÍSTICAS REAIS DO JOGADOR (IMAGEM 3)
        st.markdown("### 📊 Estatísticas Detalhadas do Jogador")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("#### Ofensivo")
            st.markdown(render_stat_item("Cruzamento", get_player_stat(p, STAT_GROUPS['Passe']['Cruzamento'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Finalização", get_player_stat(p, STAT_GROUPS['Chute']['Finalização'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Prec. Cabeceio", get_player_stat(p, STAT_GROUPS['Defesa']['Precisão no Cabeceio'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Passe curto", get_player_stat(p, STAT_GROUPS['Passe']['Passe curto'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Voleios", get_player_stat(p, STAT_GROUPS['Chute']['Voleios'])), unsafe_allow_html=True)

            st.markdown("#### Mentalidade")
            st.markdown(render_stat_item("Combatividade", get_player_stat(p, STAT_GROUPS['Físico']['Combatividade'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Intercept.", get_player_stat(p, STAT_GROUPS['Defesa']['Intercept.'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pos. ataque", get_player_stat(p, STAT_GROUPS['Chute']['Pos. ataque'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Visão de jogo", get_player_stat(p, STAT_GROUPS['Passe']['Visão de jogo'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pênaltis", get_player_stat(p, STAT_GROUPS['Chute']['Pênaltis'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Compostura", get_player_stat(p, STAT_GROUPS['Dribles']['Compostura'])), unsafe_allow_html=True)

        with col2:
            st.markdown("#### Habilidade")
            st.markdown(render_stat_item("Dribles", get_player_stat(p, STAT_GROUPS['Dribles']['Dribles'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Curva", get_player_stat(p, STAT_GROUPS['Passe']['Curva'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Prec. faltas", get_player_stat(p, STAT_GROUPS['Passe']['Precisão nas faltas'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Lançamento", get_player_stat(p, STAT_GROUPS['Passe']['Lançamento'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Controle bola", get_player_stat(p, STAT_GROUPS['Dribles']['Controle de bola'])), unsafe_allow_html=True)

            st.markdown("#### Defesa")
            st.markdown(render_stat_item("Hab. defensiva", get_player_stat(p, STAT_GROUPS['Defesa']['Habilidade defensiva'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Dividida pé", get_player_stat(p, STAT_GROUPS['Defesa']['Dividida em pé'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Carrinho", get_player_stat(p, STAT_GROUPS['Defesa']['Carrinho'])), unsafe_allow_html=True)

        with col3:
            st.markdown("#### Movimentação")
            st.markdown(render_stat_item("Aceleração", get_player_stat(p, STAT_GROUPS['Ritmo']['Aceleração'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pique", get_player_stat(p, STAT_GROUPS['Ritmo']['Pique'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Agilidade", get_player_stat(p, STAT_GROUPS['Dribles']['Agilidade'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Reação", get_player_stat(p, STAT_GROUPS['Dribles']['Reação'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Equilíbrio", get_player_stat(p, STAT_GROUPS['Dribles']['Equilíbrio'])), unsafe_allow_html=True)

            st.markdown("#### Atributos GL")
            st.markdown(render_stat_item("Elasticidade GL", get_player_stat(p, ['gk_diving', 'Elasticidade GL'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Manejo GL", get_player_stat(p, ['gk_handling', 'Manejo GL'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Chute GL", get_player_stat(p, ['gk_kicking', 'Chute GL'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Posicion. GL", get_player_stat(p, ['gk_positioning', 'Posicion. GL'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Reflexos GL", get_player_stat(p, ['gk_reflexes', 'Reflexos GL'])), unsafe_allow_html=True)

        with col4:
            st.markdown("#### Força")
            st.markdown(render_stat_item("Força chute", get_player_stat(p, STAT_GROUPS['Chute']['Força do Chute'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Impulsão", get_player_stat(p, STAT_GROUPS['Físico']['Impulsão'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Fôlego", get_player_stat(p, STAT_GROUPS['Físico']['Fôlego'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Força", get_player_stat(p, STAT_GROUPS['Físico']['Força'])), unsafe_allow_html=True)
            st.markdown(render_stat_item("Chutes longe", get_player_stat(p, STAT_GROUPS['Chute']['Chutes de Longe'])), unsafe_allow_html=True)

            st.markdown("#### Estilos de Jogo")
            st.markdown("- **Cabeceio Preciso**")
            st.markdown("- **Solidez**")

    else:
        # Perfil do Time
        clubs_list = sorted([c for c in df_raw['club_name'].unique() if c != 'Sem Clube'])
        target_club = st.selectbox("Buscar Time:", options=clubs_list)
        club_df = df_raw[df_raw['club_name'] == target_club]

        st.subheader(f"🛡️ {target_club}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Média Overall", f"{club_df['overall'].mean():.1f}")
        c2.metric("Média Potencial", f"{club_df['potential'].mean():.1f}")
        c3.metric("Elenco Total", f"{len(club_df)} Jogadores")

# -----------------------------------------------------------------------------
# DEMAIS PÁGINAS MANTIDAS INTEGRALMENTE
# -----------------------------------------------------------------------------
elif page == "🛡️ Equipes":
    st.title("🛡️ Comparação de Equipes")
    club_stats = df_raw.groupby('club_name').agg(
        Total_Jogadores=('short_name', 'count'),
        Media_Overall=('overall', 'mean'),
        Media_Potencial=('potential', 'mean')
    ).reset_index()
    st.dataframe(club_stats, use_container_width=True, hide_index=True)

elif page == "⚽ Jogadores":
    st.title("⚽ Visão Geral dos Jogadores")
    st.dataframe(df_raw, use_container_width=True, hide_index=True)

elif page == "⚔️ Comparar":
    st.title("⚔️ Comparativo 1vs1")
    all_players = sorted(df_raw['short_name'].unique().tolist())
    p1_name = st.selectbox("Jogador 1:", options=all_players, index=0)
    p2_name = st.selectbox("Jogador 2:", options=all_players, index=1 if len(all_players)>1 else 0)
    p1, p2 = df_raw[df_raw['short_name'] == p1_name].iloc[0], df_raw[df_raw['short_name'] == p2_name].iloc[0]

    cats = ['Aceleração', 'Finalização', 'Passe curto', 'Dribles', 'Intercept.', 'Força']
    p1_vals = [get_player_stat(p1, STAT_GROUPS['Ritmo']['Aceleração']), get_player_stat(p1, STAT_GROUPS['Chute']['Finalização']), get_player_stat(p1, STAT_GROUPS['Passe']['Passe curto']), get_player_stat(p1, STAT_GROUPS['Dribles']['Dribles']), get_player_stat(p1, STAT_GROUPS['Defesa']['Intercept.']), get_player_stat(p1, STAT_GROUPS['Físico']['Força'])]
    p2_vals = [get_player_stat(p2, STAT_GROUPS['Ritmo']['Aceleração']), get_player_stat(p2, STAT_GROUPS['Chute']['Finalização']), get_player_stat(p2, STAT_GROUPS['Passe']['Passe curto']), get_player_stat(p2, STAT_GROUPS['Dribles']['Dribles']), get_player_stat(p2, STAT_GROUPS['Defesa']['Intercept.']), get_player_stat(p2, STAT_GROUPS['Físico']['Força'])]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=p1_vals + [p1_vals[0]], theta=cats + [cats[0]], fill='none', name=p1['short_name'], line=dict(color='#ef4444')))
    fig.add_trace(go.Scatterpolar(r=p2_vals + [p2_vals[0]], theta=cats + [cats[0]], fill='none', name=p2['short_name'], line=dict(color='#3b82f6')))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
