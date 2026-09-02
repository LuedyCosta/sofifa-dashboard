import streamlit as st
import pandas as pd

def renderizar_busca_jogadores(df, get_val):
    st.subheader("🔍 Central de Busca SoFifa")
    st.markdown("Filtre atletas detalhadamente por categorias de atributos, posições e biografia.")

    # Botão para limpar filtros
    if st.button("🧹 Limpar Filtros"):
        st.rerun()

    df_filtrado = df.copy()

    # -------------------------------------------------------------
    # BLOCO 1: BIOGRAFIA E INFORMAÇÕES BÁSICAS
    # -------------------------------------------------------------
    with st.expander("👤 Biografia e Informações Básicas", expanded=True):
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

    # Aplicação básica
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
    # BLOCOS EXPANSÍVEIS POR CATEGORIAS DE STATS
    # -------------------------------------------------------------
    with st.expander("⚽ Atributos Ofensivos", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_sho = st.slider("Finalização Mínima", 0, 99, 0)
            min_cross = st.slider("Cruzamento Mínimo", 0, 99, 0) if 'Crossing' in df.columns else 0
        with c2:
            min_head = st.slider("Prec. Cabeceio Mínimo", 0, 99, 0) if 'Heading Accuracy' in df.columns else 0
            min_pass_c = st.slider("Passe Curto Mínimo", 0, 99, 0) if 'Short Passing' in df.columns else 0
        with c3:
            min_vol = st.slider("Voleios Mínimo", 0, 99, 0) if 'Volleys' in df.columns else 0

        df_filtrado = df_filtrado[df_filtrado['SHO'] >= min_sho]
        if 'Crossing' in df.columns and min_cross > 0:
            df_filtrado = df_filtrado[df_filtrado['Crossing'] >= min_cross]
        if 'Heading Accuracy' in df.columns and min_head > 0:
            df_filtrado = df_filtrado[df_filtrado['Heading Accuracy'] >= min_head]
        if 'Short Passing' in df.columns and min_pass_c > 0:
            df_filtrado = df_filtrado[df_filtrado['Short Passing'] >= min_pass_c]
        if 'Volleys' in df.columns and min_vol > 0:
            df_filtrado = df_filtrado[df_filtrado['Volleys'] >= min_vol]

    with st.expander("🎯 Habilidade & Criação", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_dri = st.slider("Dribles Mínimo", 0, 99, 0)
            min_pas = st.slider("Passe Geral (PAS) Mínimo", 0, 99, 0)
        with c2:
            min_long_pass = st.slider("Lançamento Mínimo", 0, 99, 0) if 'Long Passing' in df.columns else 0
            min_ball_ctrl = st.slider("Controle de Bola Mínimo", 0, 99, 0) if 'Ball Control' in df.columns else 0
        with c3:
            min_curve = st.slider("Curva Mínima", 0, 99, 0) if 'Curve' in df.columns else 0

        df_filtrado = df_filtrado[(df_filtrado['DRI'] >= min_dri) & (df_filtrado['PAS'] >= min_pas)]
        if 'Long Passing' in df.columns and min_long_pass > 0:
            df_filtrado = df_filtrado[df_filtrado['Long Passing'] >= min_long_pass]
        if 'Ball Control' in df.columns and min_ball_ctrl > 0:
            df_filtrado = df_filtrado[df_filtrado['Ball Control'] >= min_ball_ctrl]
        if 'Curve' in df.columns and min_curve > 0:
            df_filtrado = df_filtrado[df_filtrado['Curve'] >= min_curve]

    with st.expander("⚡ Movimentação & Ritmo", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_pac = st.slider("Ritmo Geral (PAC) Mínimo", 0, 99, 0)
            min_acc = st.slider("Aceleração Mínima", 0, 99, 0) if 'Acceleration' in df.columns else 0
        with c2:
            min_sprint = st.slider("Pique Mínimo", 0, 99, 0) if 'Sprint Speed' in df.columns else 0
            min_agil = st.slider("Agilidade Mínima", 0, 99, 0) if 'Agility' in df.columns else 0
        with c3:
            min_react = st.slider("Reação Mínima", 0, 99, 0) if 'Reactions' in df.columns else 0
            min_bal = st.slider("Equilíbrio Mínimo", 0, 99, 0) if 'Balance' in df.columns else 0

        df_filtrado = df_filtrado[df_filtrado['PAC'] >= min_pac]
        if 'Acceleration' in df.columns and min_acc > 0:
            df_filtrado = df_filtrado[df_filtrado['Acceleration'] >= min_acc]
        if 'Sprint Speed' in df.columns and min_sprint > 0:
            df_filtrado = df_filtrado[df_filtrado['Sprint Speed'] >= min_sprint]
        if 'Agility' in df.columns and min_agil > 0:
            df_filtrado = df_filtrado[df_filtrado['Agility'] >= min_agil]
        if 'Reactions' in df.columns and min_react > 0:
            df_filtrado = df_filtrado[df_filtrado['Reactions'] >= min_react]
        if 'Balance' in df.columns and min_bal > 0:
            df_filtrado = df_filtrado[df_filtrado['Balance'] >= min_bal]

    with st.expander("💪 Força & Físico", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_phy = st.slider("Físico Geral (PHY) Mínimo", 0, 99, 0)
            min_stam = st.slider("Fôlego (Stamina) Mínimo", 0, 99, 0) if 'Stamina' in df.columns else 0
        with c2:
            min_str = st.slider("Força Mínima", 0, 99, 0) if 'Strength' in df.columns else 0
            min_jump = st.slider("Impulsão Mínima", 0, 99, 0) if 'Jumping' in df.columns else 0
        with c3:
            min_shot_pow = st.slider("Força do Chute Mínima", 0, 99, 0) if 'Shot Power' in df.columns else 0

        df_filtrado = df_filtrado[df_filtrado['PHY'] >= min_phy]
        if 'Stamina' in df.columns and min_stam > 0:
            df_filtrado = df_filtrado[df_filtrado['Stamina'] >= min_stam]
        if 'Strength' in df.columns and min_str > 0:
            df_filtrado = df_filtrado[df_filtrado['Strength'] >= min_str]
        if 'Jumping' in df.columns and min_jump > 0:
            df_filtrado = df_filtrado[df_filtrado['Jumping'] >= min_jump]
        if 'Shot Power' in df.columns and min_shot_pow > 0:
            df_filtrado = df_filtrado[df_filtrado['Shot Power'] >= min_shot_pow]

    with st.expander("🛡️ Defesa", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_def = st.slider("Defesa Geral (DEF) Mínimo", 0, 99, 0)
            min_aware = st.slider("Consciência Defensiva Mínima", 0, 99, 0) if 'Def Awareness' in df.columns else 0
        with c2:
            min_stand = st.slider("Dividida em Pé Mínima", 0, 99, 0) if 'Standing Tackle' in df.columns else 0
        with c3:
            min_slide = st.slider("Carrinho Mínimo", 0, 99, 0) if 'Sliding Tackle' in df.columns else 0

        df_filtrado = df_filtrado[df_filtrado['DEF'] >= min_def]
        if 'Def Awareness' in df.columns and min_aware > 0:
            df_filtrado = df_filtrado[df_filtrado['Def Awareness'] >= min_aware]
        if 'Standing Tackle' in df.columns and min_stand > 0:
            df_filtrado = df_filtrado[df_filtrado['Standing Tackle'] >= min_stand]
        if 'Sliding Tackle' in df.columns and min_slide > 0:
            df_filtrado = df_filtrado[df_filtrado['Sliding Tackle'] >= min_slide]

    with st.expander("🧠 Mentalidade", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            min_pos_at = st.slider("Posicionamento de Ataque Mínimo", 0, 99, 0) if 'Positioning' in df.columns else 0
            min_vision = st.slider("Visão de Jogo Mínima", 0, 99, 0) if 'Vision' in df.columns else 0
        with c2:
            min_compo = st.slider("Compostura Mínima", 0, 99, 0) if 'Composure' in df.columns else 0
            min_aggr = st.slider("Combatividade Mínima", 0, 99, 0) if 'Aggression' in df.columns else 0
        with c3:
            min_inter = st.slider("Interceptações Mínimas", 0, 99, 0) if 'Interceptions' in df.columns else 0

        if 'Positioning' in df.columns and min_pos_at > 0:
            df_filtrado = df_filtrado[df_filtrado['Positioning'] >= min_pos_at]
        if 'Vision' in df.columns and min_vision > 0:
            df_filtrado = df_filtrado[df_filtrado['Vision'] >= min_vision]
        if 'Composure' in df.columns and min_compo > 0:
            df_filtrado = df_filtrado[df_filtrado['Composure'] >= min_compo]
        if 'Aggression' in df.columns and min_aggr > 0:
            df_filtrado = df_filtrado[df_filtrado['Aggression'] >= min_aggr]
        if 'Interceptions' in df.columns and min_inter > 0:
            df_filtrado = df_filtrado[df_filtrado['Interceptions'] >= min_inter]

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
