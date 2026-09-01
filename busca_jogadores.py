# Arquivo: busca_jogadores.py
import streamlit as st
import pandas as pd

def renderizar_busca_jogadores(df):
    st.title("🔍 Busca Avançada de Jogadores")

    # Injeção de CSS para responsividade total em dispositivos móveis
    st.markdown("""
    <style>
        div[data-testid="stDataFrame"] {
            width: 100% !important;
            overflow-x: auto !important;
        }
        div[data-testid="stDataFrame"] > div {
            width: 100% !important;
        }
        @media (max-width: 768px) {
            .stTextInput, .stSelectbox, .stMultiSelect {
                margin-bottom: 10px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Bloco de Filtros Responsivos
    with st.container(border=True):
        st.markdown("### 🎛️ Filtros de Pesquisa")
        
        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            nome_busca = st.text_input("Filtrar por Nome:", placeholder="Ex: Mbappé, Rodrygo...")
        with col2:
            posicoes_disponiveis = ["Todas"] + sorted(df['Position'].dropna().unique().tolist())
            posicao_busca = st.selectbox("Posição:", options=posicoes_disponiveis)
        with col3:
            ligas_disponiveis = ["Todas"] + sorted(df['League'].dropna().unique().tolist())
            liga_busca = st.selectbox("Liga:", options=ligas_disponiveis)

        col4, col5, col6 = st.columns(3)
        with col4:
            ovr_min, ovr_max = int(df['OVR'].min()), int(df['OVR'].max())
            faixa_ovr = st.slider("Overall (OVR):", ovr_min, ovr_max, (ovr_min, ovr_max))
        with col5:
            idade_min, idade_max = int(df['Age'].min()), int(df['Age'].max())
            faixa_idade = st.slider("Idade:", idade_min, idade_max, (idade_min, idade_max))
        with col6:
            times_disponiveis = ["Todos"] + sorted(df['Team'].dropna().unique().tolist())
            time_busca = st.selectbox("Clube:", options=times_disponiveis)

    # Filtragem do DataFrame
    df_filtrado = df.copy()

    if nome_busca:
        df_filtrado = df_filtrado[df_filtrado['Name'].str.contains(nome_busca, case=False, na=False)]
    if posicao_busca != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Position'] == posicao_busca]
    if liga_busca != "Todas":
        df_filtrado = df_filtrado[df_filtrado['League'] == liga_busca]
    if time_busca != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Team'] == time_busca]

    df_filtrado = df_filtrado[
        (df_filtrado['OVR'] >= faixa_ovr[0]) & (df_filtrado['OVR'] <= faixa_ovr[1]) &
        (df_filtrado['Age'] >= faixa_idade[0]) & (df_filtrado['Age'] <= faixa_idade[1])
    ]

    st.markdown(f"**Resultados encontrados:** <span class='var-text'>{len(df_filtrado)}</span> jogadores", unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("Nenhum jogador encontrado com os filtros selecionados.")
    else:
        colunas_exibicao = ['Name', 'OVR', 'Position', 'Age', 'Team', 'League', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        colunas_disponiveis = [c for c in colunas_exibicao if c in df_filtrado.columns]

        st.dataframe(
            df_filtrado[colunas_disponiveis],
            hide_index=True
        )

        st.markdown("---")
        st.markdown("### 📋 Ações Rápidas por Jogador")
        
        max_por_pagina = 10
        total_paginas = max(1, (len(df_filtrado) + max_por_pagina - 1) // max_por_pagina)
        
        pagina_atual = st.number_input("Página:", min_value=1, max_value=total_paginas, value=1, step=1)
        inicio = (pagina_atual - 1) * max_por_pagina
        fim = inicio + max_por_pagina

        df_pagina = df_filtrado.iloc[inicio:fim]

       for idx, row in df_pagina.iterrows():
            id_jog = row.get('id', idx)
            
            col_nome, col_info, col_acao = st.columns([2, 2, 1])
            with col_nome:
                st.markdown(f"**{row['Name']}**")
            with col_info:
                st.markdown(f"<span style='color: #94a3b8;'>OVR: {row['OVR']} | Pos: {row['Position']}</span>", unsafe_allow_html=True)
            with col_acao:
                st.checkbox("Comparar", key=f"comp_{id_jog}_{idx}")

# <--- ADICIONE ESTA LINHA NO FINAL DO ARQUIVO BUSCA_JOGADORES.PY --->
renderizar_busca_jogadores()
