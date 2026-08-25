import streamlit as st
import pandas as pd
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
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .metric-card {
        background-color: #1a1f2c;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2d3748;
        text-align: center;
    }
    .badge-ovr {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    .badge-pot {
        background-color: #3b82f6;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
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

    for stat in ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']:
        if stat not in df.columns:
            df[stat] = df['overall']

    return df

df_raw = load_data()

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard SoFIFA")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegação:",
    ["👤 Perfil", "🛡️ Equipes", "⚽ Jogadores", "⚔️ Comparar"]
)

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
# 4. PÁGINAS
# -----------------------------------------------------------------------------

# =============================================================================
# PÁGINA 1: PERFIL (JOGADOR OU TIME)
# =============================================================================
if page == "👤 Perfil":
    st.title("👤 Perfil Detalhado")
    
    # Alternador de tipo de perfil
    profile_type = st.radio("Visualizar Perfil de:", ["Jogador", "Time"], horizontal=True)
    st.markdown("---")

    if profile_type == "Jogador":
        player_list = sorted(df['short_name'].unique().tolist())
        if not player_list:
            st.warning("Nenhum jogador disponível para os filtros selecionados.")
        else:
            player_name = st.selectbox("Selecione o Jogador:", options=player_list)
            p = df[df['short_name'] == player_name].iloc[0]

            st.markdown(f"### 🏃 {p['short_name']}")
            st.markdown(f"**Clube:** {p['club_name']} | **Posição:** `{p['positions']}` | **Idade:** {p['age']} anos")

            c1, c2, c3 = st.columns([1, 1.5, 2.5])

            with c1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                if str(p['player_face_url']).startswith("http"):
                    st.image(p['player_face_url'], width=140)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<span class="badge-ovr">OVR: {p["overall"]}</span> ', unsafe_allow_html=True)
                st.markdown(f'<span class="badge-pot">POT: {p["potential"]}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown("#### 📊 Métricas Financeiras")
                st.metric("Valor de Mercado", str(p['value']))
                st.metric("Salário Semanal", str(p['wage']))

            with c3:
                st.markdown("#### 🎯 Atributos Principais")
                cats = ['Ritmo', 'Chute', 'Passe', 'Drible', 'Defesa', 'Físico']
                vals = [p['pace'], p['shooting'], p['passing'], p['dribbling'], p['defending'], p['physic']]
                
                fig = go.Figure(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=cats + [cats[0]],
                    fill='toself',
                    fillcolor='rgba(16, 185, 129, 0.4)',
                    line=dict(color='#10b981', width=2)
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=30, r=30, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

    else:  # Perfil do Time
        target_club = st.selectbox("Selecione o Time:", options=clubs_list)
        club_df = df_raw[df_raw['club_name'] == target_club]

        st.markdown(f"### 🛡️ {target_club}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total no Elenco", f"{len(club_df)} jogadores")
        c2.metric("Média de OVR", f"{club_df['overall'].mean():.1f}")
        c3.metric("Média de Potencial", f"{club_df['potential'].mean():.1f}")
        c4.metric("Idade Média", f"{club_df['age'].mean():.1f} anos")

        st.markdown("---")
        col_left, col_right = st.columns([1.5, 1])

        with col_left:
            st.markdown("#### 📊 Desempenho Geral do Elenco")
            fig_bar = px.bar(
                club_df.sort_values(by="overall", ascending=False),
                x='short_name',
                y='overall',
                color='overall',
                labels={'short_name': 'Jogador', 'overall': 'Overall'},
                color_continuous_scale="Greens"
            )
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_right:
            st.markdown("#### ⚽ Distribuição por Posição")
            pos_counts = club_df['positions'].value_counts().reset_index()
            pos_counts.columns = ['Posição', 'Quantidade']
            
            fig_pie = px.pie(
                pos_counts,
                names='Posição',
                values='Quantidade',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

# =============================================================================
# PÁGINA 2: EQUIPES
# =============================================================================
elif page == "🛡️ Equipes":
    st.title("🛡️ Comparação de Equipes")

    club_stats = df_raw.groupby('club_name').agg(
        Total_Jogadores=('short_name', 'count'),
        Media_Overall=('overall', 'mean'),
        Media_Potencial=('potential', 'mean'),
        Media_Idade=('age', 'mean')
    ).reset_index()

    club_stats['Media_Overall'] = club_stats['Media_Overall'].round(1)
    club_stats['Media_Potencial'] = club_stats['Media_Potencial'].round(1)
    club_stats['Media_Idade'] = club_stats['Media_Idade'].round(1)

    st.dataframe(
        club_stats.rename(columns={
            'club_name': 'Equipe',
            'Total_Jogadores': 'Qtd. Jogadores',
            'Media_Overall': 'Média OVR',
            'Media_Potencial': 'Média POT',
            'Media_Idade': 'Média Idade'
        }).sort_values(by="Média OVR", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# =============================================================================
# PÁGINA 3: JOGADORES
# =============================================================================
elif page == "⚽ Jogadores":
    st.title("⚽ Visão Geral dos Jogadores")
    st.markdown(f"Exibindo **{len(df)}** registros.")

    st.dataframe(
        df[selected_columns] if selected_columns else df,
        use_container_width=True,
        hide_index=True
    )

# =============================================================================
# PÁGINA 4: COMPARAR
# =============================================================================
elif page == "⚔️ Comparar":
    st.title("⚔️ Comparativo de Jogadores (1 vs 1)")

    all_players = sorted(df_raw['short_name'].unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        p1_name = st.selectbox("Jogador 1:", options=all_players, index=0)
        p1 = df_raw[df_raw['short_name'] == p1_name].iloc[0]
        st.markdown(f"**Clube:** {p1['club_name']} | **OVR:** `{p1['overall']}` | **POT:** `{p1['potential']}`")

    with col2:
        idx2 = 1 if len(all_players) > 1 else 0
        p2_name = st.selectbox("Jogador 2:", options=all_players, index=idx2)
        p2 = df_raw[df_raw['short_name'] == p2_name].iloc[0]
        st.markdown(f"**Clube:** {p2['club_name']} | **OVR:** `{p2['overall']}` | **POT:** `{p2['potential']}`")

    cats = ['Ritmo', 'Chute', 'Passe', 'Drible', 'Defesa', 'Físico']
    cats_closed = cats + [cats[0]]

    v1 = [p1['pace'], p1['shooting'], p1['passing'], p1['dribbling'], p1['defending'], p1['physic']]
    v2 = [p2['pace'], p2['shooting'], p2['passing'], p2['dribbling'], p2['defending'], p2['physic']]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=v1 + [v1[0]],
        theta=cats_closed,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.3)',
        line=dict(color='#3b82f6', width=2),
        name=p1['short_name']
    ))

    fig.add_trace(go.Scatterpolar(
        r=v2 + [v2[0]],
        theta=cats_closed,
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.3)',
        line=dict(color='#ef4444', width=2),
        name=p2['short_name']
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
