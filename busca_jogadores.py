# Arquivo: busca_jogadores.py
import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    """Carrega os dados dos jogadores do arquivo CSV do EA FC 26."""
    try:
        return pd.read_csv("EAFC26.csv")
    except FileNotFoundError:
        return None

def renderizar_busca_jogadores():
    st.title("🔎 Busca Avançada de Jogadores (EA FC26)")
    st.markdown("Filtre os atletas por características biológicas, técnicas e estatísticas detalhadas.")

    df = carregar_dados()

    if df is None:
        st.error("O arquivo 'EAFC26.csv' não foi encontrado na raiz do projeto. Por favor, adicione-o para continuar.")
        return

    # Injeção do CSS padrão dos blocos
    st.markdown("""
        <style>
        .custom-box {
            background-color: #161920;
            border: 1px solid #333842;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # BLOCOS DE FILTROS (ORGANIZADOS EM SEÇÕES)
    # ==========================================
    
    # Bloco 1: Bio e Características Gerais
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    st.markdown("### 🧬 Bloco: Bio e Características")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        # Seletor de Nacionalidade
        nacionalidades = ["Todas"] + sorted(df['nationality_name'].dropna().unique().tolist()) if 'nationality_name' in df.columns else ["Todas"]
        filtro_nacionalidade = st.selectbox("Nacionalidade", nacionalidades)
        
        # Seletor de Posição
        posicoes = ["Todas"] + sorted(df['player_positions'].dropna().unique().tolist()) if 'player_positions' in df.columns else ["Todas"]
        filtro_posicao = st.selectbox("Posição", posicoes)
        
        # Filtro de Idade (Mín / Máx)
        min_idade_val = int(df['age'].min()) if 'age' in df.columns else 15
        max_idade_val = int(df['age'].max()) if 'age' in df.columns else 45
        filtro_idade = st.slider("Idade", min_idade_val, max_idade_val, (min_idade_val, max_idade_val))

    with col_f2:
        # Seletor de Liga
        ligas = ["Todas"] + sorted(df['league_name'].dropna().unique().tolist()) if 'league_name' in df.columns else ["Todas"]
        filtro_liga = st.selectbox("Liga", ligas)
        
        # Seletor de Perna Boa
        perna_boa_opts = ["Todas"] + sorted(df['preferred_foot'].dropna().unique().tolist()) if 'preferred_foot' in df.columns else ["Todas"]
        filtro_perna_boa = st.selectbox("Perna Boa", perna_boa_opts)
        
        # Filtro de Altura (Mín / Máx em cm)
        min_alt_val = int(df['height_cm'].min()) if 'height_cm' in df.columns else 150
        max_alt_val = int(df['height_cm'].max()) if 'height_cm' in df.columns else 210
        filtro_altura = st.slider("Altura (cm)", min_alt_val, max_alt_val, (min_alt_val, max_alt_val))

    with col_f3:
        # Nome do Jogador (Busca textual rápida)
        filtro_nome = st.text_input("Nome do Jogador", placeholder="Digite para buscar...")
        
        # Seletor de Fintas (Skill Moves)
        fintas_opts = ["Todas"] + sorted(df['skill_moves'].dropna().unique().tolist()) if 'skill_moves' in df.columns else ["Todas"]
        filtro_fintas = st.selectbox("Nível de Finta", fintas_opts)
        
        # Seletor de Perna Ruim (Weak Foot)
        perna_ruim_opts = ["Todas"] + sorted(df['weak_foot'].dropna().unique().tolist()) if 'weak_foot' in df.columns else ["Todas"]
        filtro_perna_ruim = st.selectbox("Nível com Perna Ruim", perna_ruim_opts)

    st.markdown('</div>', unsafe_allow_html=True)

    # Blocos complementares seguindo a lógica de stats (exemplo: Atributos Gerais de Overall / Potencial)
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Blocos: Atributos e Desempenho")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        min_ovr = int(df['overall'].min()) if 'overall' in df.columns else 0
        max_ovr = int(df['overall'].max()) if 'overall' in df.columns else 99
        filtro_overall = st.slider("Classificação Geral (Overall)", min_ovr, max_ovr, (min_ovr, max_ovr))
    with col_s2:
        min_pot = int(df['potential'].min()) if 'potential' in df.columns else 0
        max_pot = int(df['potential'].max()) if 'potential' in df.columns else 99
        filtro_potencial = st.slider("Potencial", min_pot, max_pot, (min_pot, max_pot))
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # APLICAÇÃO DOS FILTROS NO DATAFRAME
    # ==========================================
    df_filtrado = df.copy()

    if filtro_nome and 'short_name' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['short_name'].str.contains(filtro_nome, case=False, na=False)]
    if filtro_nacionalidade != "Todas" and 'nationality_name' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['nationality_name'] == filtro_nacionalidade]
    if filtro_liga != "Todas" and 'league_name' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['league_name'] == filtro_liga]
    if filtro_posicao != "Todas" and 'player_positions' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['player_positions'].str.contains(filtro_posicao, na=False)]
    if filtro_perna_boa != "Todas" and 'preferred_foot' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['preferred_foot'] == filtro_perna_boa]
    if filtro_fintas != "Todas" and 'skill_moves' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['skill_moves'] == filtro_fintas]
    if filtro_perna_ruim != "Todas" and 'weak_foot' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['weak_foot'] == filtro_perna_ruim]
    
    if 'age' in df_filtrado.columns:
        df_filtrado = df_filtrado[(df_filtrado['age'] >= filtro_idade[0]) & (df_filtrado['age'] <= filtro_idade[1])]
    if 'height_cm' in df_filtrado.columns:
        df_filtrado = df_filtrado[(df_filtrado['height_cm'] >= filtro_altura[0]) & (df_filtrado['height_cm'] <= filtro_altura[1])]
    if 'overall' in df_filtrado.columns:
        df_filtrado = df_filtrado[(df_filtrado['overall'] >= filtro_overall[0]) & (df_filtrado['overall'] <= filtro_overall[1])]
    if 'potential' in df_filtrado.columns:
        df_filtrado = df_filtrado[(df_filtrado['potential'] >= filtro_potencial[0]) & (df_filtrado['potential'] <= filtro_potencial[1])]

    st.markdown("---")
    st.subheader(f"Resultados Encontrados: {len(df_filtrado)} jogadores")

    if df_filtrado.empty:
        st.info("Nenhum jogador encontrado com os filtros selecionados.")
        return

    # ==========================================
    # EXIBIÇÃO DOS RESULTADOS (5 COLUNAS)
    # ==========================================
    # Convertemos o dataframe para lista para renderizar em blocos de 5 colunas
    jogadores_lista = df_filtrado.to_dict('records')
    
    # Divide os jogadores em blocos de 5 colunas por linha
    num_colunas = 5
    linhas = [jogadores_lista[i:i + num_colunas] for i in range(0, len(jogadores_lista), num_colunas)]

    for linha in linhas:
        cols = st.columns(num_colunas)
        for idx, jogador in enumerate(linha):
            with cols[idx]:
                nome_jogador = jogador.get('short_name', jogador.get('long_name', 'Jogador'))
                overall_jog = jogador.get('overall', 'N/A')
                
                # Bloco expansível individual para cada jogador
                with st.expander(f"⭐ {overall_jog} | {nome_jogador}"):
                    # Informações de Bio
                    st.markdown("##### 🧬 Bio")
                    st.write(f"**Nome Completo:** {jogador.get('long_name', nome_jogador)}")
                    st.write(f"**Posição:** {jogador.get('player_positions', 'N/A')}")
                    st.write(f"**Idade:** {jogador.get('age', 'N/A')}")
                    st.write(f"**Altura:** {jogador.get('height_cm', 'N/A')} cm")
                    st.write(f"**Nacionalidade:** {jogador.get('nationality_name', 'N/A')}")
                    st.write(f"**Liga:** {jogador.get('league_name', 'N/A')}")
                    st.write(f"**Perna Boa:** {jogador.get('preferred_foot', 'N/A')} | **Fintas:** {jogador.get('skill_moves', 'N/A')}⭐")

                    # Resumo das Stats (Ofensivo, Mentalidade, Habilidade, etc.)
                    st.markdown("##### 📈 Resumo de Stats")
                    st.write(f"**Ritmo (PAC):** {jogador.get('pace', jogador.get('movement_acceleration', 'N/A'))}")
                    st.write(f"**Finalização (SHO):** {jogador.get('shooting', jogador.get('attacking_finishing', 'N/A'))}")
                    st.write(f"**Passes (PAS):** {jogador.get('passing', jogador.get('passing_vision', 'N/A'))}")
                    st.write(f"**Drible (DRI):** {jogador.get('dribbling', jogador.get('dribbling_agility', 'N/A'))}")
                    st.write(f"**Defesa (DEF):** {jogador.get('defending', jogador.get('defending_sliding_tackle', 'N/A'))}")
                    st.write(f"**Físico (PHY):** {jogador.get('physic', jogador.get('power_stamina', 'N/A'))}")

                    # Checkbox com a opção Comparar
                    id_jogador = jogador.get('sofifa_id', nome_jogador)
                    st.checkbox("Comparar", key=f"comp_{id_jogador}")

# Executa a função caso o arquivo seja chamado diretamente ou importado
if __name__ == "__main__":
    renderizar_busca_jogadores()
