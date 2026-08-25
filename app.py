import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .similar-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .similar-score {
        color: #f59e0b;
        font-weight: bold;
        float: right;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARREGAMENTO DOS DADOS
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

    # Atributos padronizados caso não existam todas as sub-stats
    stat_groups = {
        'Ritmo': ['Aceleração', 'Velocidade de Pique'],
        'Chute': ['Finalização', 'Força do Chute', 'Chutes de Longe', 'Pênaltis'],
        'Passe': ['Visão', 'Passe Curtos', 'Passe Longos', 'Cruzamento'],
        'Dribles': ['Drible', 'Controle de Bola', 'Agilidade', 'Reação'],
        'Defesa': ['Intercepção', 'Carrinho', 'Marcacao'],
        'Físico': ['Fôlego', 'Força', 'Impulsão', 'Agressividade']
    }

    # Garantir colunas de stats para o radar e cálculo de similaridade
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
# 4. PÁGINA PERFIL REFINADA
# -----------------------------------------------------------------------------
if page == "👤 Perfil":
    st.title("👤 Perfil Detalhado")

    # 1. QUEM (Seleção / Jogador ou Time) - Imagem 1
    st.markdown("##### 1 · Quem")
    who_type = st.radio("Selecione a Entidade:", ["Jogador", "Time"], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    if who_type == "Jogador":
        player_list = sorted(df['short_name'].unique().tolist())
        if not player_list:
            st.warning("Nenhum jogador encontrado.")
            st.stop()

        target_player_name = st.selectbox("Buscar Jogador:", options=player_list)
        p = df[df['short_name'] == target_player_name].iloc[0]

        # Cabeçalho do Jogador
        col_img, col_info = st.columns([1, 4])
        with col_img:
            if str(p['player_face_url']).startswith("http"):
                st.image(p['player_face_url'], width=110)
        with col_info:
            st.subheader(f"{p['short_name']}")
            st.markdown(f"**Clube:** {p['club_name']} | **Posição:** `{p['positions']}` | **Idade:** {p['age']} anos | **OVR:** `{p['overall']}` | **POT:** `{p['potential']}` | **Valor:** `{p['value']}`")

        st.markdown("---")

        # 2. INDICADORES (Filtro agrupado de Stats) - Imagem 2
        st.markdown("##### 2 · Indicadores de Performance")
        
        selected_group = st.radio("Grupo de Atributos:", list(STAT_GROUPS.keys()), horizontal=True)
        available_stats = STAT_GROUPS[selected_group]
        
        selected_stats = st.multiselect(
            f"Selecione as estatísticas de {selected_group} para o Radar:",
            options=available_stats,
            default=available_stats
        )

        st.markdown("---")

        # 3. GRÁFICO RADAR DINÂMICO - Imagem 3
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
                title=f"Atributos Selecionados: {p['short_name']} (Valor: {p['value']})",
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Selecione ao menos um indicador no filtro para exibir o gráfico.")

        st.markdown("---")

        # 4. JOGADORES PARECIDOS - Imagem 4
        st.markdown("### 👥 Jogadores Parecidos")
        st.caption("Mesma posição e atributos estatísticos similares")

        # Algoritmo simples de cálculo de distância de similaridade
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
                        <strong>{sim_player['short_name']}</strong><br>
                        <small>{sim_player['club_name']}</small><br>
                        <small>OVR: {sim_player['overall']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Nenhum jogador similar encontrado para a mesma posição.")

    else:  # Perfil do Time
        target_club = st.selectbox("Buscar Time:", options=clubs_list)
        club_df = df_raw[df_raw['club_name'] == target_club]

        st.subheader(f"🛡️ {target_club}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Média Overall", f"{club_df['overall'].mean():.1f}")
        c2.metric("Média Potencial", f"{club_df['potential'].mean():.1f}")
        c3.metric("Elenco", f"{len(club_df)} Jogadores")

        st.markdown("---")
        st.markdown("##### 2 · Indicadores do Elenco")
        selected_group = st.radio("Grupo de Atributos do Elenco:", list(STAT_GROUPS.keys()), horizontal=True)
        available_stats = STAT_GROUPS[selected_group]
        
        selected_stats = st.multiselect("Selecione as estatísticas:", options=available_stats, default=available_stats)

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
                title=f"Médias de Atributos: {target_club}",
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# OUTRAS PÁGINAS (MANTIDAS)
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
