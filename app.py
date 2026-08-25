import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E CSS PARA ACESSIBILIDADE E CONTRASTE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização focada em acessibilidade (Alto contraste, textos maiores e nítidos)
st.markdown("""
<style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
        font-size: 1.05rem;
    }

    /* Forçar visibilidade e alto contraste de rótulos e textos de formulários */
    label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #f3f4f6 !important;
        font-weight: 500 !important;
    }

    /* Textos secundários / captions com cor clara e legível */
    .stCaption, small, .caption-text {
        color: #cbd5e1 !important;
        font-size: 0.95rem !important;
    }

    /* Radio buttons e Checkboxes com alto contraste */
    div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    /* Cards e Containers */
    .metric-card {
        background-color: #1a1f2c;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #3b82f6;
        text-align: center;
    }

    .similar-card {
        background-color: #1a1f2c;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .similar-score {
        color: #f59e0b;
        font-weight: bold;
        font-size: 1.1rem;
        float: right;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARREGAMENTO DOS DADOS & MAPEAMENTO COMPLETO DE SUB-STATS (Imagem 2)
# -----------------------------------------------------------------------------
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

    df['short_name'] = df['short_name'].fillna('Jogador Sem Nome').astype(str)
    df['club_name'] = df['club_name'].fillna('Sem Clube').astype(str)
    df['positions'] = df['positions'].fillna('N/A').astype(str)
    df['value'] = df['value'].fillna('N/A').astype(str)
    df['wage'] = df['wage'].fillna('N/A').astype(str)
    df['player_face_url'] = df['player_face_url'].fillna('https://cdn.sofifa.net/player_0.png').astype(str)

    df['overall'] = pd.to_numeric(df['overall'], errors='coerce').fillna(50).astype(int)
    df['potential'] = pd.to_numeric(df['potential'], errors='coerce').fillna(50).astype(int)
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # Dicionário com TODAS as opções exatas da imagem de referência (Imagem 2)
    stat_groups = {
        'Ritmo': ['Acceleration', 'Sprint Speed'],
        'Chute': ['Att. Position', 'Finishing', 'Shot Power', 'Long Shots', 'Volleys', 'Penalties'],
        'Passe': ['Vision', 'Crossing', 'FK Acc.', 'Short Pass', 'Long Pass', 'Curve'],
        'Dribles': ['Agility', 'Balance', 'Reactions', 'Ball Control', 'Dribbling', 'Composure'],
        'Defesa': ['Interceptions', 'Heading Acc.', 'Def. Aware', 'Stand Tackle', 'Slide Tackle'],
        'Físico': ['Jumping', 'Stamina', 'Strength', 'Aggression']
    }

    # Garantir que todas as colunas existam no dataframe (fallback para overall se não constar no CSV)
    for group, stats in stat_groups.items():
        for stat in stats:
            if stat not in df.columns:
                df[stat] = df['overall']

    return df, stat_groups

df_raw, STAT_GROUPS = load_data()

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard SoFIFA")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navegação:", ["👤 Perfil", "🛡️ Equipes", "⚽ Jogadores", "⚔️ Comparar"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Customização de Dados")

all_available_columns = list(df_raw.columns)
default_cols = ['short_name', 'club_name', 'positions', 'age', 'overall', 'potential', 'value', 'wage']

selected_columns = st.sidebar.multiselect(
    "Colunas Ativas na Exibição:",
    options=all_available_columns,
    default=[c for c in default_cols if c in all_available_columns]
)

clubs_list = sorted([c for c in df_raw['club_name'].unique() if c != 'Sem Clube'])
selected_club_filter = st.sidebar.selectbox("Filtrar por Clube (Geral):", options=["Todos"] + clubs_list)

df = df_raw.copy()
if selected_club_filter != "Todos":
    df = df[df['club_name'] == selected_club_filter]

# -----------------------------------------------------------------------------
# 4. PÁGINA PERFIL
# -----------------------------------------------------------------------------
if page == "👤 Perfil":
    st.title("👤 Perfil Detalhado")

    # 1. QUEM (Seleção de Perfil)
    st.markdown("### 1 · Quem")
    who_type = st.radio("Selecione a Entidade:", ["Jogador", "Time"], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    if who_type == "Jogador":
        player_list = sorted(df['short_name'].unique().tolist())
        if not player_list:
            st.warning("Nenhum jogador encontrado com os filtros selecionados.")
            st.stop()

        target_player_name = st.selectbox("Buscar Jogador:", options=player_list)
        p = df[df['short_name'] == target_player_name].iloc[0]

        # Cabeçalho do Jogador
        col_img, col_info = st.columns([1, 4])
        with col_img:
            if str(p['player_face_url']).startswith("http"):
                st.image(p['player_face_url'], width=120)
        with col_info:
            st.subheader(f"🏃 {p['short_name']}")
            st.markdown(f"**Clube:** {p['club_name']} | **Posição:** `{p['positions']}` | **Idade:** {p['age']} anos")
            st.markdown(f"**Overall:** `{p['overall']}` | **Potencial:** `{p['potential']}` | **Valor:** `{p['value']}`")

        st.markdown("---")

        # 2. INDICADORES DE PERFORMANCE (Com todas as estatísticas da Imagem 2)
        st.markdown("### 2 · Indicadores de Performance")
        st.markdown("<p style='color: #cbd5e1;'>Selecione o grupo e ative/desative as sub-estatísticas desejadas:</p>", unsafe_allow_html=True)
        
        selected_group = st.radio("Grupo de Atributos:", list(STAT_GROUPS.keys()), horizontal=True)
        available_stats = STAT_GROUPS[selected_group]
        
        selected_stats = st.multiselect(
            f"Estatísticas de {selected_group} exibidas no Radar:",
            options=available_stats,
            default=available_stats
        )

        st.markdown("---")

        # 3. GRÁFICO RADAR DINÂMICO
        if selected_stats:
            values = [p[s] for s in selected_stats]
            
            fig = go.Figure(go.Scatterpolar(
                r=values + [values[0]],
                theta=selected_stats + [selected_stats[0]],
                fill='toself',
                fillcolor='rgba(245, 158, 11, 0.4)',
                line=dict(color='#f59e0b', width=2),
                name=p['short_name']
            ))
            fig.update_layout(
                title=dict(
                    text=f"Análise de {selected_group}: {p['short_name']} (Valor: {p['value']})",
                    font=dict(color='#ffffff', size=18)
                ),
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#ffffff')),
                    angularaxis=dict(tickfont=dict(color='#ffffff', size=13))
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Selecione pelo menos uma estatística acima para gerar o gráfico Radar.")

        st.markdown("---")

        # 4. JOGADORES PARECIDOS
        st.markdown("### 👥 Jogadores Parecidos")
        st.markdown("<p style='color: #cbd5e1;'>Mesma posição principal e perfil estatístico similar</p>", unsafe_allow_html=True)

        all_stats_cols = [stat for stats in STAT_GROUPS.values() for stat in stats]
        same_pos_df = df_raw[(df_raw['positions'] == p['positions']) & (df_raw['short_name'] != p['short_name'])].copy()

        if not same_pos_df.empty:
            target_vector = p[all_stats_cols].values.astype(float)
            compare_vectors = same_pos_df[all_stats_cols].values.astype(float)

            distances = np.linalg.norm(compare_vectors - target_vector, axis=1)
            max_dist = np.max(distances) if np.max(distances) > 0 else 1
            similarity = (1 - (distances / max_dist)) * 100
            
            same_pos_df['similarity'] = similarity.round(1)
            top_similar = same_pos_df.sort_values(by='similarity', ascending=False).head(5)

            cols = st.columns(len(top_similar))
            for idx, (_, sim_player) in enumerate(top_similar.iterrows()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="similar-card">
                        <span class="similar-score">{sim_player['similarity']}%</span>
                        <strong style="color: #ffffff; font-size: 1.05rem;">{sim_player['short_name']}</strong><br>
                        <small style="color: #cbd5e1;">{sim_player['club_name']}</small><br>
                        <small style="color: #cbd5e1;">OVR: {sim_player['overall']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Nenhum jogador similar encontrado com exatamente a mesma posição.")

    else:  # Perfil do Time
        target_club = st.selectbox("Buscar Time:", options=clubs_list)
        club_df = df_raw[df_raw['club_name'] == target_club]

        st.subheader(f"🛡️ {target_club}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Média Overall", f"{club_df['overall'].mean():.1f}")
        c2.metric("Média Potencial", f"{club_df['potential'].mean():.1f}")
        c3.metric("Elenco Total", f"{len(club_df)} Jogadores")

        st.markdown("---")
        st.markdown("### 2 · Indicadores do Elenco")
        selected_group = st.radio("Grupo de Atributos do Elenco:", list(STAT_GROUPS.keys()), horizontal=True)
        available_stats = STAT_GROUPS[selected_group]
        
        selected_stats = st.multiselect("Estatísticas exibidas:", options=available_stats, default=available_stats)

        if selected_stats:
            club_means = [club_df[s].mean() for s in selected_stats]
            fig = go.Figure(go.Scatterpolar(
                r=club_means + [club_means[0]],
                theta=selected_stats + [selected_stats[0]],
                fill='toself',
                fillcolor='rgba(59, 130, 246, 0.4)',
                line=dict(color='#3b82f6', width=2),
                name=target_club
            ))
            fig.update_layout(
                title=dict(text=f"Média de Atributos - {target_club}", font=dict(color='#ffffff')),
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#ffffff')),
                    angularaxis=dict(tickfont=dict(color='#ffffff'))
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# DEMAIS PÁGINAS (MANTIDAS)
# =============================================================================
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
    st.dataframe(df[selected_columns] if selected_columns else df, use_container_width=True, hide_index=True)

elif page == "⚔️ Comparar":
    st.title("⚔️ Comparativo 1vs1")
    all_players = sorted(df_raw['short_name'].unique().tolist())
    p1_name = st.selectbox("Jogador 1:", options=all_players, index=0)
    p2_name = st.selectbox("Jogador 2:", options=all_players, index=1 if len(all_players)>1 else 0)
    p1, p2 = df_raw[df_raw['short_name'] == p1_name].iloc[0], df_raw[df_raw['short_name'] == p2_name].iloc[0]

    cats = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[p1[c] for c in cats] + [p1[cats[0]]], theta=cats + [cats[0]], fill='toself', name=p1['short_name']))
    fig.add_trace(go.Scatterpolar(r=[p2[c] for c in cats] + [p2[cats[0]]], theta=cats + [cats[0]], fill='toself', name=p2['short_name']))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
