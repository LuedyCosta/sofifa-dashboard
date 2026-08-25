import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E CSS PARA ACESSIBILIDADE E ALTO CONTRASTE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fundo escuro com texto de alto contraste */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }

    /* Correção de Acessibilidade: Rótulos e Textos em Branco/Claro */
    label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    .stCaption, small, .caption-text {
        color: #94a3b8 !important;
    }

    /* Radio buttons com contraste elevado */
    div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Badges de Atributos do FIFA (Estilo Imagem 3) */
    .stat-box {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
    }
    .stat-badge {
        width: 32px;
        height: 24px;
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
        color: #e2e8f0 !important;
        font-size: 0.95rem;
    }

    /* Card para Informações do Perfil (Imagem 4) */
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
# 2. MAPEAMENTO COMPLETO DAS ESTATÍSTICAS (IMAGEM 2)
# -----------------------------------------------------------------------------
# Sub-estatísticas detalhadas mapeadas por grupo do radar
STAT_GROUPS = {
    'Ritmo': {
        'Aceleração': 'Acceleration',
        'Pique': 'Sprint Speed'
    },
    'Chute': {
        'Finalização': 'Finishing',
        'Força do Chute': 'Shot Power',
        'Chutes de Longe': 'Long Shots',
        'Pênaltis': 'Penalties',
        'Pos. ataque': 'Att. Position',
        'Voleios': 'Volleys'
    },
    'Passe': {
        'Visão de jogo': 'Vision',
        'Cruzamento': 'Crossing',
        'Precisão nas faltas': 'FK Acc.',
        'Passe curto': 'Short Pass',
        'Lançamento': 'Long Pass',
        'Curva': 'Curve'
    },
    'Dribles': {
        'Agilidade': 'Agility',
        'Equilíbrio': 'Balance',
        'Reação': 'Reactions',
        'Controle de bola': 'Ball Control',
        'Dribles': 'Dribbling',
        'Compostura': 'Composure'
    },
    'Defesa': {
        'Intercept.': 'Interceptions',
        'Precisão no Cabeceio': 'Heading Acc.',
        'Habilidade defensiva': 'Def. Aware',
        'Dividida em pé': 'Stand Tackle',
        'Carrinho': 'Slide Tackle'
    },
    'Físico': {
        'Impulsão': 'Jumping',
        'Fôlego': 'Stamina',
        'Força': 'Strength',
        'Combatividade': 'Aggression'
    }
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sofifa_players.csv")
    except FileNotFoundError:
        st.error("❌ Arquivo 'sofifa_players.csv' não encontrado.")
        st.stop()

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

    # Tratamento de nulos e tipos
    df['short_name'] = df['short_name'].fillna('Jogador Sem Nome').astype(str)
    df['club_name'] = df['club_name'].fillna('Sem Clube').astype(str)
    df['positions'] = df['positions'].fillna('N/A').astype(str)
    df['value'] = df['value'].fillna('N/A').astype(str)
    df['wage'] = df['wage'].fillna('N/A').astype(str)
    df['player_face_url'] = df['player_face_url'].fillna('https://cdn.sofifa.net/player_0.png').astype(str)

    df['overall'] = pd.to_numeric(df['overall'], errors='coerce').fillna(50).astype(int)
    df['potential'] = pd.to_numeric(df['potential'], errors='coerce').fillna(50).astype(int)
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # Garantir a existência de colunas de atributos
    for grp in STAT_GROUPS.values():
        for pt_name, col_name in grp.items():
            if col_name not in df.columns:
                df[col_name] = df['overall']

    # Atributos adicionais para imagens 3 e 4 (com fallback dinâmico)
    extra_cols = ['Perna boa', 'Fintas', 'Perna ruim', 'Rep. Internacional', 
                  'Elasticidade GL', 'Manejo GL', 'Chute GL', 'Posicion. GL', 'Reflexos GL']
    for col in extra_cols:
        if col not in df.columns:
            if 'Perna' in col:
                df[col] = 'Esq.' if 'boa' in col else 2
            elif 'GL' in col:
                df[col] = 10
            else:
                df[col] = 2

    return df

df_raw = load_data()

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard SoFIFA")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navegação:", ["👤 Perfil", "🛡️ Equipes", "⚽ Jogadores", "⚔️ Comparar"])

df = df_raw.copy()

# Helper para renderizar estatísticas estilo FIFA (Imagem 3)
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
# 4. PÁGINA PERFIL
# -----------------------------------------------------------------------------
if page == "👤 Perfil":
    st.title("👤 Perfil Detalhado")

    # 1. QUEM
    st.markdown("### 1 · Quem")
    who_type = st.radio("Selecione a Entidade:", ["Jogador", "Time"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    if who_type == "Jogador":
        player_list = sorted(df['short_name'].unique().tolist())
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list)
        p = df[df['short_name'] == target_player_name].iloc[0]

        # DETALHES DE PERFIL E CLUBE (Inspirado nas Imagens 3 e 4)
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
                        <strong style="color:#94a3b8;">Perfil</strong><br>
                        <span>Perna boa: <b>{p.get('Perna boa', 'Esq.')}</b></span><br>
                        <span>{p.get('Fintas', 2)} ★ Fintas</span><br>
                        <span>{p.get('Perna ruim', 2)} ★ Perna ruim</span><br>
                        <span>{p.get('Rep. Internacional', 1)} ★ Rep. Internacional</span>
                    </div>
                    <div>
                        <strong style="color:#94a3b8;">Especialidades</strong><br>
                        <span style="color:#f59e0b; font-weight:bold;">#Força</span>
                    </div>
                    <div>
                        <strong style="color:#94a3b8;">Clube</strong><br>
                        <span><b>{p['club_name']}</b></span><br>
                        <span style="color:#38bdf8;">Posição {p['positions']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 2. INDICADORES DE PERFORMANCE (IMAGEM 2 + RADAR OUTLINE)
        st.markdown("### 2 · Indicadores de Performance")
        
        selected_group_name = st.radio("Grupo de Atributos:", list(STAT_GROUPS.keys()), horizontal=True)
        current_group_dict = STAT_GROUPS[selected_group_name]

        # Multi-select com opções do grupo atual
        selected_pt_labels = st.multiselect(
            f"Selecione as estatísticas de {selected_group_name} para o Radar:",
            options=list(current_group_dict.keys()),
            default=list(current_group_dict.keys())
        )

        if selected_pt_labels:
            radar_labels = selected_pt_labels
            radar_values = [p[current_group_dict[label]] for label in selected_pt_labels]

            # Fechar a forma geométrica do radar
            r_vals = radar_values + [radar_values[0]]
            theta_labs = radar_labels + [radar_labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=theta_labs,
                mode='lines+markers',
                fill='none',  # REMOVE O FUNDO BRANCO / APENAS OUTLINE
                line=dict(color='#f59e0b', width=3),
                marker=dict(size=8, color='#f59e0b'),
                name=p['short_name']
            ))

            fig.update_layout(
                title=dict(
                    text=f"Análise de {selected_group_name}: {p['short_name']} (Valor: {p['value']})",
                    font=dict(color='#ffffff', size=16)
                ),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',  # TRANSPARENTE
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(color='#94a3b8'),
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
            st.warning("Selecione ao menos um atributo acima para visualizar o radar.")

        st.markdown("---")

        # 3. PAINEL DE ESTATÍSTICAS DETALHADAS (ESTILO IMAGEM 3)
        st.markdown("### 📊 Estatísticas Detalhadas do Jogador")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("#### Ofensivo")
            st.markdown(render_stat_item("Cruzamento", p[STAT_GROUPS['Passe']['Cruzamento']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Finalização", p[STAT_GROUPS['Chute']['Finalização']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Prec. Cabeceio", p[STAT_GROUPS['Defesa']['Precisão no Cabeceio']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Passe curto", p[STAT_GROUPS['Passe']['Passe curto']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Voleios", p[STAT_GROUPS['Chute']['Voleios']]), unsafe_allow_html=True)

            st.markdown("#### Mentalidade")
            st.markdown(render_stat_item("Combatividade", p[STAT_GROUPS['Físico']['Combatividade']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Intercept.", p[STAT_GROUPS['Defesa']['Intercept.']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pos. ataque", p[STAT_GROUPS['Chute']['Pos. ataque']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Visão de jogo", p[STAT_GROUPS['Passe']['Visão de jogo']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pênaltis", p[STAT_GROUPS['Chute']['Pênaltis']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Compostura", p[STAT_GROUPS['Dribles']['Compostura']]), unsafe_allow_html=True)

        with col2:
            st.markdown("#### Habilidade")
            st.markdown(render_stat_item("Dribles", p[STAT_GROUPS['Dribles']['Dribles']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Curva", p[STAT_GROUPS['Passe']['Curva']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Prec. faltas", p[STAT_GROUPS['Passe']['Precisão nas faltas']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Lançamento", p[STAT_GROUPS['Passe']['Lançamento']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Controle bola", p[STAT_GROUPS['Dribles']['Controle de bola']]), unsafe_allow_html=True)

            st.markdown("#### Defesa")
            st.markdown(render_stat_item("Hab. defensiva", p[STAT_GROUPS['Defesa']['Habilidade defensiva']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Dividida pé", p[STAT_GROUPS['Defesa']['Dividida em pé']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Carrinho", p[STAT_GROUPS['Defesa']['Carrinho']]), unsafe_allow_html=True)

        with col3:
            st.markdown("#### Movimentação")
            st.markdown(render_stat_item("Aceleração", p[STAT_GROUPS['Ritmo']['Aceleração']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Pique", p[STAT_GROUPS['Ritmo']['Pique']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Agilidade", p[STAT_GROUPS['Dribles']['Agilidade']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Reação", p[STAT_GROUPS['Dribles']['Reação']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Equilíbrio", p[STAT_GROUPS['Dribles']['Equilíbrio']]), unsafe_allow_html=True)

            st.markdown("#### Atributos GL")
            st.markdown(render_stat_item("Elasticidade GL", p.get('Elasticidade GL', 10)), unsafe_allow_html=True)
            st.markdown(render_stat_item("Manejo GL", p.get('Manejo GL', 10)), unsafe_allow_html=True)
            st.markdown(render_stat_item("Chute GL", p.get('Chute GL', 10)), unsafe_allow_html=True)
            st.markdown(render_stat_item("Posicion. GL", p.get('Posicion. GL', 10)), unsafe_allow_html=True)
            st.markdown(render_stat_item("Reflexos GL", p.get('Reflexos GL', 10)), unsafe_allow_html=True)

        with col4:
            st.markdown("#### Força")
            st.markdown(render_stat_item("Força chute", p[STAT_GROUPS['Chute']['Força do Chute']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Impulsão", p[STAT_GROUPS['Físico']['Impulsão']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Fôlego", p[STAT_GROUPS['Físico']['Fôlego']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Força", p[STAT_GROUPS['Físico']['Força']]), unsafe_allow_html=True)
            st.markdown(render_stat_item("Chutes longe", p[STAT_GROUPS['Chute']['Chutes de Longe']]), unsafe_allow_html=True)

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

    cats = ['Acceleration', 'Finishing', 'Short Pass', 'Dribbling', 'Interceptions', 'Strength']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[p1[c] for c in cats] + [p1[cats[0]]], theta=cats + [cats[0]], fill='none', name=p1['short_name'], line=dict(color='#f59e0b')))
    fig.add_trace(go.Scatterpolar(r=[p2[c] for c in cats] + [p2[cats[0]]], theta=cats + [cats[0]], fill='none', name=p2['short_name'], line=dict(color='#3b82f6')))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
