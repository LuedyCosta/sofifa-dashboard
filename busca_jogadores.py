import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def renderizar_busca_jogadores(df, get_val):
    st.subheader("🔍 Central de Busca SoFifa")
    st.markdown("Busque atletas por filtros avançados ou descreva livremente o que você procura.")

    # Criar abas para alternar entre Filtros Tradicionais (SoFifa) e Busca por Descrição (IA local)
    aba_filtro, aba_texto = st.tabs(["🎛️ Filtros Tradicionais (SoFifa)", "🤖 Busca por Descrição em Texto"])

    df_filtrado = df.copy()

    # -------------------------------------------------------------
    # ABA 1: FILTROS ESTILO SOFIFA
    # -------------------------------------------------------------
    with aba_filtro:
        with st.expander("🛠️ Filtros Avançados", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                positions = ["Todas"] + sorted(df['Position'].dropna().unique().tolist())
                pos_escolhida = st.selectbox("Posição", positions)
            
            with col2:
                ligas = ["Todas"] + sorted(df['League'].dropna().unique().tolist())
                liga_escolhida = st.selectbox("Liga", ligas)
            
            with col3:
                min_ovr, max_ovr = int(df['OVR'].min()), int(df['OVR'].max())
                ovr_range = st.slider("Overall (OVR)", min_ovr, max_ovr, (75, max_ovr))
            
            with col4:
                min_idade, max_idade = int(df['Age'].min()), int(df['Age'].max())
                idade_range = st.slider("Idade", min_idade, max_idade, (16, 40))

            # Aplicar filtros tradicionais
            if pos_escolhida != "Todas":
                df_filtrado = df_filtrado[df_filtrado['Position'] == pos_escolhida]
            if liga_escolhida != "Todas":
                df_filtrado = df_filtrado[df_filtrado['League'] == liga_escolhida]
            
            df_filtrado = df_filtrado[
                (df_filtrado['OVR'] >= ovr_range[0]) & (df_filtrado['OVR'] <= ovr_range[1]) &
                (df_filtrado['Age'] >= idade_range[0]) & (df_filtrado['Age'] <= idade_range[1])
            ]

    # -------------------------------------------------------------
    # ABA 2: BUSCA POR DESCRIÇÃO EM TEXTO (SEM API)
    # -------------------------------------------------------------
    with aba_texto:
        st.markdown("Descreva o jogador ideal (Ex: *ponta esquerdo rápido com bom chute e fintas*, *volante forte e marcador*, *atacante jovem goleador*).")
        query_texto = st.text_input("O que você procura?", placeholder="Ex: ponta rápido que dribla muito e chuta forte")

        if query_texto.strip():
            # Criamos uma coluna de "perfil textual" para cada jogador juntando suas principais características
            @st.cache_resource
            def preparar_corpus(dataframe):
                corpus = []
                for _, row in dataframe.iterrows():
                    texto = f"posição {row.get('Position', '')} liga {row.get('League', '')} time {row.get('Team', '')} " \
                            f"idade {row.get('Age', '')} overall {row.get('OVR', '')} " \
                            f"ritmo {row.get('PAC', '')} finalização {row.get('SHO', '')} passe {row.get('PAS', '')} " \
                            f"drible {row.get('DRI', '')} defesa {row.get('DEF', '')} fisico {row.get('PHY', '')} " \
                            f"estilo {row.get('play style', '')}"
                    corpus.append(texto)
                return corpus

            corpus_jogadores = preparar_corpus(df)
            
            # Vetoriza o texto usando TF-IDF localmente
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
            tfidf_matrix = vectorizer.fit_transform(corpus_jogadores)
            
            query_vec = vectorizer.transform([query_texto])
            similaridades = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Adiciona a pontuação de similaridade no dataframe e ordena
            df_filtrado = df_filtrado.copy()
            df_filtrado['score_busca'] = similaridades[df_filtrado.index]
            df_filtrado = df_filtrado.sort_values(by='score_busca', ascending=False)

    st.markdown("---")
    st.markdown(f"### 📋 Resultados encontrados ({len(df_filtrado)} jogadores)")

    # Exibição estilo tabela SoFifa limpa e direta
    if df_filtrado.empty:
        st.warning("Nenhum jogador encontrado com esses critérios.")
    else:
        # Seleciona colunas principais para exibição em formato de tabela interativa
        colunas_exibir = ['Name', 'Position', 'OVR', 'Age', 'Team', 'League', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        colunas_disponiveis = [c for c in colunas_exibir if c in df_filtrado.columns]
        
        # Mostra a tabela paginada/ajustada do Streamlit
        st.dataframe(
            df_filtrado[colunas_disponiveis].head(50),
            use_container_width=True,
            hide_index=True
        )
