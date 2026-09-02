import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def renderizar_busca_jogadores(df, get_val):
    st.subheader("🔍 Central de Busca SoFifa")
    st.markdown("Busque atletas por filtros avançados ou descreva livremente o que você procura.")

    aba_filtro, aba_texto = st.tabs(["🎛️ Filtros Tradicionais (SoFifa)", "🤖 Busca por Descrição em Texto"])

    df_filtrado = df.copy()

    # -------------------------------------------------------------
    # ABA 1: FILTROS ESTILO SOFIFA (COM BIOGRAFIA COMPLETA)
    # -------------------------------------------------------------
    with aba_filtro:
        with st.expander("🛠️ Filtros Avançados & Biografia", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                positions = ["Todas"] + sorted(df['Position'].dropna().unique().tolist())
                pos_escolhida = st.selectbox("Posição", positions)
                
                # Novo filtro de Nacionalidade (se a coluna existir)
                col_nac = 'Nationality' if 'Nationality' in df.columns else ('Country' if 'Country' in df.columns else None)
                if col_nac:
                    nacionalidades = ["Todas"] + sorted(df[col_nac].dropna().unique().tolist())
                    nac_escolhida = st.selectbox("Nacionalidade", nacionalidades)
                else:
                    nac_escolhida = "Todas"

            with col2:
                ligas = ["Todas"] + sorted(df['League'].dropna().unique().tolist())
                liga_escolhida = st.selectbox("Liga", ligas)
                
                # Novo filtro de Clube/Time
                times = ["Todos"] + sorted(df['Team'].dropna().unique().tolist())
                time_escolhido = st.selectbox("Clube", times)

            with col3:
                min_ovr, max_ovr = int(df['OVR'].min()), int(df['OVR'].max())
                ovr_range = st.slider("Overall (OVR)", min_ovr, max_ovr, (75, max_ovr))
                
                # Novo filtro de Pé Preferido
                pes = ["Todos"] + sorted(df['Preferred foot'].dropna().unique().tolist())
                pe_escolhido = st.selectbox("Pé Preferido", pes)

            with col4:
                min_idade, max_idade = int(df['Age'].min()), int(df['Age'].max())
                idade_range = st.slider("Idade", min_idade, max_idade, (16, 40))
                
                # Filtros de Estrelas (Perna Ruim e Fintas) se existirem
                weak_foot = st.slider("Perna Ruim (Mínima)", 1, 5, 1)
                skill_moves = st.slider("Fintas / Skill Moves (Mínima)", 1, 5, 1)

            # Aplicação dos filtros tradicionais e de biografia
            if pos_escolhida != "Todas":
                df_filtrado = df_filtrado[df_filtrado['Position'] == pos_escolhida]
            if liga_escolhida != "Todas":
                df_filtrado = df_filtrado[df_filtrado['League'] == liga_escolhida]
            if time_escolhido != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Team'] == time_escolhido]
            if nac_escolhida != "Todas" and col_nac:
                df_filtrado = df_filtrado[df_filtrado[col_nac] == nac_escolhida]
            if pe_escolhido != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Preferred foot'] == pe_escolhido]

            df_filtrado = df_filtrado[
                (df_filtrado['OVR'] >= ovr_range[0]) & (df_filtrado['OVR'] <= ovr_range[1]) &
                (df_filtrado['Age'] >= idade_range[0]) & (df_filtrado['Age'] <= idade_range[1]) &
                (df_filtrado['Weak foot'] >= weak_foot) & (df_filtrado['Skill moves'] >= skill_moves)
            ]

    # -------------------------------------------------------------
    # ABA 2: BUSCA POR DESCRIÇÃO EM TEXTO (SEM API)
    # -------------------------------------------------------------
    with aba_texto:
        st.markdown("Descreva o jogador ideal (Ex: *ponta esquerdo rápido com bom chute*, *volante forte e marcador*).")
        query_texto = st.text_input("O que você procura?", placeholder="Ex: ponta rápido que dribla muito e chuta forte")

        if query_texto.strip():
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
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
            tfidf_matrix = vectorizer.fit_transform(corpus_jogadores)
            
            query_vec = vectorizer.transform([query_texto])
            similaridades = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            df_filtrado = df_filtrado.copy()
            df_filtrado['score_busca'] = similaridades[df_filtrado.index]
            df_filtrado = df_filtrado.sort_values(by='score_busca', ascending=False)

    st.markdown("---")
    st.markdown(f"### 📋 Resultados encontrados ({len(df_filtrado)} jogadores)")

    if df_filtrado.empty:
        st.warning("Nenhum jogador encontrado com esses critérios.")
    else:
        colunas_exibir = ['Name', 'Position', 'OVR', 'Age', 'Team', 'League', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        colunas_disponiveis = [c for c in colunas_exibir if c in df_filtrado.columns]
        
        st.dataframe(
            df_filtrado[colunas_disponiveis].head(50),
            use_container_width=True,
            hide_index=True
        )
