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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MAPEAMENTO DOS GRUPOS BASEADO EXATAMENTE NA IMAGEM 2
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
# 3. LEITURA DOS DADOS
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
        player_list = sorted(df['Name'].unique().tolist())
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list)
        p = df[df['Name'] == target_player_name].iloc[0]

        # Estilo de jogo
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

        # PAINEL DE PERFIL
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

        # 2. INDICADORES DE PERFORMANCE (SELETOR VIA CHECKBOX MULTIGRUPO)
        st.markdown("### 2 · Indicadores de Performance")
        st.write("Selecione as estatísticas desejadas para exibir no gráfico Radar (permite mesclar grupos diferentes):")

        # Dicionário dinâmico para armazenar quais checkboxes foram marcados
        selected_stats_map = {}

        # Interface com expansor para manter o visual limpo
        with st.expander("📌 Clique para expandir e selecionar as Estatísticas por Grupo", expanded=True):
            cols = st.columns(4)
            group_keys = list(STAT_GROUPS.keys())
            
            for idx, group_name in enumerate(group_keys):
                col_target = cols[idx % 4]
                with col_target:
                    st.markdown(f"**{group_name}**")
                    # Define defaults para 'Aceleração' e 'Pique' da Movimentação
                    for stat_label, csv_col in STAT_GROUPS[group_name].items():
                        is_default = stat_label in ['Aceleração', 'Pique']
                        checked = st.checkbox(stat_label, value=is_default, key=f"chk_{group_name}_{stat_label}")
                        if checked:
                            selected_stats_map[stat_label] = csv_col

        # GRÁFICO RADAR APENAS OUTLINE (SEM FUNDO BRANCO)
        if selected_stats_map:
            radar_labels = list(selected_stats_map.keys())
            radar_values = [get_val(p, csv_col) for csv_col in selected_stats_map.values()]

            # Fechar a geometria do radar
            r_vals = radar_values + [radar_values[0]]
            theta_labs = radar_labels + [radar_labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=theta_labs,
                mode='lines+markers',
                fill='none',  # OUTLINE PURA
                line=dict(color='#ef4444', width=3),
                marker=dict(size=8, color='#ef4444'),
                name=p['Name']
            ))

            fig.update_layout(
                title=dict(
                    text=f"Análise Personalizada: {p['Name']} (OVR: {p['OVR']})",
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
                margin=dict(l=40, r=40, t=50, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Marque pelo menos uma estatística na lista acima para exibir o gráfico.")

        st.markdown("---")

        # 3. ESTATÍSTICAS DETALHADAS DINÂMICAS DO JOGADOR (IMAGEM 2)
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
