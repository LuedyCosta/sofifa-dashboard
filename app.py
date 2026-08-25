import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA Stats Dashboard",
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
    .player-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #374151;
    }
    .badge-overall {
        background-color: #10b981;
        color: #ffffff;
        font-weight: bold;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 1.2rem;
        display: inline-block;
    }
    .badge-potential {
        background-color: #3b82f6;
        color: #ffffff;
        font-weight: bold;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 1.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARREGAMENTO E MAPEAMENTO EXATO DO CSV
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sofifa_players.csv")
    except FileNotFoundError:
        st.error("❌ Arquivo 'sofifa_players.csv' não encontrado no repositório.")
        st.stop()

    # Mapeamento com base nas colunas reais do arquivo raspado
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

    # Tratamento de nulos e tipos de dados
    df['short_name'] = df['short_name'].fillna('Jogador Sem Nome').astype(str)
    df['club_name'] = df['club_name'].fillna('Sem Clube').astype(str)
    df['positions'] = df['positions'].fillna('N/A').astype(str)
    df['value'] = df['value'].fillna('N/A').astype(str)
    df['wage'] = df['wage'].fillna('N/A').astype(str)
    df['player_face_url'] = df['player_face_url'].fillna('https://cdn.sofifa.net/player_0.png').astype(str)

    df['overall'] = pd.to_numeric(df['overall'], errors='coerce').fillna(50).astype(int)
    df['potential'] = pd.to_numeric(df['potential'], errors='coerce').fillna(50).astype(int)
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # Como a tabela raspada não contém estatísticas detalhadas (pace, shooting, etc.),
    # definimos valores genéricos baseados no overall para evitar erros no gráfico radar.
    for stat in ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']:
        if stat not in df.columns:
            df[stat] = df['overall']

    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (FILTROS)
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard SoFIFA")
st.sidebar.markdown("---")

all_clubs = sorted([c for c in df['club_name'].unique() if c != 'Sem Clube'])
selected_clubs = st.sidebar.multiselect("Filtrar por Clube(s):", options=all_clubs)

filtered_df = df.copy()
if selected_clubs:
    filtered_df = filtered_df[filtered_df['club_name'].isin(selected_clubs)]

min_ovr = int(df['overall'].min())
max_ovr = int(df['overall'].max())

if min_ovr >= max_ovr:
    min_ovr, max_ovr = 40, 99

selected_ovr = st.sidebar.slider(
    "Faixa de Overall:",
    min_value=min_ovr,
    max_value=max_ovr,
    value=(min_ovr, max_ovr)
)

filtered_df = filtered_df[
    (filtered_df['overall'] >= selected_ovr[0]) & 
    (filtered_df['overall'] <= selected_ovr[1])
]

st.sidebar.markdown("---")
mode = st.sidebar.radio("Navegação:", ["Perfil do Jogador", "Comparador (1 vs 1)", "Visão Geral do Elenco"])

# -----------------------------------------------------------------------------
# 4. EXIBIÇÃO DE CONTEÚDO
# -----------------------------------------------------------------------------
if mode == "Perfil do Jogador":
    player_options = sorted(filtered_df['short_name'].unique().tolist())
    
    if not player_options:
        st.warning("Nenhum jogador encontrado com os filtros selecionados.")
    else:
        selected_player = st.selectbox("Selecione o Jogador:", options=player_options)
        player = filtered_df[filtered_df['short_name'] == selected_player].iloc[0]

        st.markdown(f"## 👤 {player['short_name']}")
        st.markdown(f"**Clube:** {player['club_name']} | **Posição:** `{player['positions']}` | **Idade:** {player['age']} anos")

        col_img, col_metrics, col_radar = st.columns([1, 1.5, 2.5])

        with col_img:
            st.markdown('<div class="player-card" style="text-align: center;">', unsafe_allow_html=True)
            if str(player['player_face_url']).startswith("http"):
                st.image(player['player_face_url'], width=150)
            else:
                st.markdown("📷 *(Foto indisponível)*")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<span class="badge-overall">OVR: {player["overall"]}</span> ', unsafe_allow_html=True)
            st.markdown(f'<span class="badge-potential">POT: {player["potential"]}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_metrics:
            st.markdown("### 📊 Informações Gerais")
            st.metric("Valor Estimado", str(player['value']))
            st.metric("Salário Semanal", str(player['wage']))

        with col_radar:
            categories = ['Ritmo', 'Chute', 'Passe', 'Drible', 'Defesa', 'Físico']
            values = [
                player['pace'], player['shooting'], player['passing'],
                player['dribbling'], player['defending'], player['physic']
            ]
            
            categories_closed = categories + [categories[0]]
            values_closed = values + [values[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(16, 185, 129, 0.4)',
                line=dict(color='#10b981', width=3),
                name=player['short_name']
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                title="Estimativa de Atributos",
                margin=dict(l=40, r=40, t=40, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)

elif mode == "Comparador (1 vs 1)":
    st.markdown("## ⚔️ Comparativo Head-to-Head")
    
    col1, col2 = st.columns(2)
    player_options = sorted(df['short_name'].unique().tolist())

    with col1:
        p1_name = st.selectbox("Selecione o Jogador 1:", options=player_options, index=0)
        p1 = df[df['short_name'] == p1_name].iloc[0]

    with col2:
        idx2 = 1 if len(player_options) > 1 else 0
        p2_name = st.selectbox("Selecione o Jogador 2:", options=player_options, index=idx2)
        p2 = df[df['short_name'] == p2_name].iloc[0]

    categories = ['Ritmo', 'Chute', 'Passe', 'Drible', 'Defesa', 'Físico']
    cats_closed = categories + [categories[0]]

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

elif mode == "Visão Geral do Elenco":
    st.markdown("## 📋 Tabela de Jogadores Filtrados")
    st.markdown(f"Exibindo **{len(filtered_df)}** jogadores.")

    display_cols = ['short_name', 'club_name', 'positions', 'age', 'overall', 'potential', 'value', 'wage']

    st.dataframe(
        filtered_df[display_cols].rename(columns={
            'short_name': 'Nome',
            'club_name': 'Clube',
            'positions': 'Posição',
            'age': 'Idade',
            'overall': 'Overall',
            'potential': 'Potencial',
            'value': 'Valor',
            'wage': 'Salário'
        }),
        use_container_width=True,
        hide_index=True
    )
