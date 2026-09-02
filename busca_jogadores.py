import streamlit as st
import pandas as pd

def renderizar_busca_jogadores(df, get_val):
    st.subheader("🔍 Central de Busca SoFifa")
    st.markdown("Filtre atletas detalhadamente por todas as características, posições, ligas e atributos do jogo.")

    df_filtrado = df.copy()

    with st.expander("🛠️ Filtros de Biografia e Informações Básicas", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            positions = ["Todas"] + sorted(df['Position'].dropna().unique().tolist())
            pos_escolhida = st.selectbox("Posição", positions)
            
            col_nac = 'Nationality' if 'Nationality' in df.columns else ('Country' if 'Country' in df.columns else None)
            if col_nac:
                nacionalidades = ["Todas"] + sorted(df[col_nac].dropna().unique().tolist())
                nac_escolhida = st.selectbox("Nacionalidade", nacionalidades)
            else:
                nac_escolhida = "Todas"

        with col2:
            ligas = ["Todas"] + sorted(df['League'].dropna().unique().tolist())
            liga_escolhida = st.selectbox("Liga", ligas)
            
            times = ["Todos"] + sorted(df['Team'].dropna().unique().tolist())
            time_escolhido = st.selectbox("Clube", times)

        with col3:
            min_ovr, max_ovr = int(df['OVR'].min()), int(df['OVR'].max())
            ovr_range = st.slider("Overall (OVR)", min_ovr, max_ovr, (75, max_ovr))
            
            pes = ["Todos"] + sorted(df['Preferred foot'].dropna().unique().tolist())
            pe_escolhido = st.selectbox("Pé Preferido", pes)

        with col4:
            min_idade, max_idade = int(df['Age'].min()), int(df['Age'].max())
            idade_range = st.slider("Idade", min_idade, max_idade, (16, 40))
            
            weak_foot = st.slider("Perna Ruim (Mínima)", 1, 5, 1)
            skill_moves = st.slider("Fintas / Skill Moves (Mínima)", 1, 5, 1)

    # Aplicação dos filtros básicos
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
    # FILTROS AVANÇADOS DE ATRIBUTOS (PAC, SHO, PAS, DRI, DEF, PHY, ETC)
    # -------------------------------------------------------------
    with st.expander("⚡ Filtros por Atributos Detalhados do Atleta", expanded=False):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            min_pac = st.slider("Ritmo (PAC Mínimo)", 0, 99, 0)
            min_sho = st.slider("Finalização (SHO Mínimo)", 0, 99, 0)
            min_pas = st.slider("Passe (PAS Mínimo)", 0, 99, 0)
        with c2:
            min_dri = st.slider("Drible (DRI Mínimo)", 0, 99, 0)
            min_def = st.slider("Defesa (DEF Mínimo)", 0, 99, 0)
            min_phy = st.slider("Físico (PHY Mínimo)", 0, 99, 0)
        with c3:
            # Filtros específicos extras se as colunas existirem no dataset
            min_acc = st.slider("Aceleração Mínima", 0, 99, 0) if 'Acceleration' in df.columns else None
            min_sta = st.slider("Fôlego (Stamina) Mínimo", 0, 99, 0) if 'Stamina' in df.columns else None
            min_str = st.slider("Força (Strength) Mínima", 0, 99, 0) if 'Strength' in df.columns else None

        # Aplicando filtros de atributos principais
        df_filtrado = df_filtrado[
            (df_filtrado['PAC'] >= min_pac) &
            (df_filtrado['SHO'] >= min_sho) &
            (df_filtrado['PAS'] >= min_pas) &
            (df_filtrado['DRI'] >= min_dri) &
            (df_filtrado['DEF'] >= min_def) &
            (df_filtrado['PHY'] >= min_phy)
        ]

        # Aplicando opcionais caso existam
        if min_acc is not None and 'Acceleration' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Acceleration'] >= min_acc]
        if min_sta is not None and 'Stamina' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Stamina'] >= min_sta]
        if min_str is not None and 'Strength' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Strength'] >= min_str]

    st.markdown("---")
    st.markdown(f"### 📋 Resultados encontrados ({len(df_filtrado)} jogadores)")

    if df_filtrado.empty:
        st.warning("Nenhum jogador encontrado com esses critérios de filtro.")
    else:
        colunas_exibir = ['Name', 'Position', 'OVR', 'Age', 'Team', 'League', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        colunas_disponiveis = [c for c in colunas_exibir if c in df_filtrado.columns]
        
        st.dataframe(
            df_filtrado[colunas_disponiveis].head(100),
            use_container_width=True,
            hide_index=True
        )
