import streamlit as st
import pandas as pd

def renderizar_perfil(df, find_similar_players, STAT_GROUPS, jogador_selecionado):
    # Se o quarto argumento passado pelo app for a função get_val em vez do jogador, tratamos isso com segurança:
    if callable(jogador_selecionado):
        get_val = jogador_selecionado
        # Tenta resgatar o jogador selecionado do session_state se existir
        jogador_selecionado = st.session_state.get('jogador_selecionado', df.iloc[0] if not df.empty else {})
    else:
        get_val = lambda row, col: row.get(col, '-')

    if isinstance(jogador_selecionado, pd.Series):
        nome_jogador = jogador_selecionado.get('Name', 'Jogador')
        posicao = jogador_selecionado.get('Position', 'CM')
    else:
        nome_jogador = 'Jogador'
        posicao = 'CM'

    st.subheader(f"👤 Perfil do Atleta: {nome_jogador}")
    
    atrib_sugeridos = {
        'ST': ['SHO', 'PAC', 'DRI', 'Positioning', 'Finishing', 'Shot Power'],
        'CF': ['SHO', 'PAS', 'DRI', 'PAC', 'Vision'],
        'RW': ['PAC', 'DRI', 'Crossing', 'Agility'],
        'LW': ['PAC', 'DRI', 'Crossing', 'Agility'],
        'CAM': ['PAS', 'DRI', 'Vision', 'Short Passing', 'Long Passing'],
        'CM': ['PAS', 'DRI', 'PHY', 'Stamina', 'Short Passing'],
        'CDM': ['DEF', 'PHY', 'Interceptions', 'Standing Tackle', 'Stamina'],
        'CB': ['DEF', 'PHY', 'Strength', 'Def Awareness', 'Standing Tackle', 'Jumping'],
        'RB': ['PAC', 'DEF', 'PHY', 'Stamina', 'Crossing'],
        'LB': ['PAC', 'DEF', 'PHY', 'Stamina', 'Crossing'],
        'GK': ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Reflexes', 'GK Positioning']
    }
    
    sugestoes_posicao = atrib_sugeridos.get(posicao, ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'])

    if st.button("💡 Sugestão para a Posição"):
        st.info(f"Atributos cruciais destacados para a posição **{posicao}**: {', '.join(sugestoes_posicao)}")

    with st.expander("👤 Biografia e Informações Básicas", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall (OVR)", get_val(jogador_selecionado, 'OVR'))
            st.metric("Idade", get_val(jogador_selecionado, 'Age'))
        with col2:
            st.metric("Posição", posicao)
            st.metric("Clube", get_val(jogador_selecionado, 'Team'))
        with col3:
            st.metric("Liga", get_val(jogador_selecionado, 'League'))
            st.metric("Nacionalidade", get_val(jogador_selecionado, 'Nationality') if 'Nationality' in jogador_selecionado else get_val(jogador_selecionado, 'Country'))

    with st.expander("⚽ Atributos Ofensivos", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Finalização (SHO)", get_val(jogador_selecionado, 'SHO'))
            if 'Crossing' in jogador_selecionado:
                st.metric("Cruzamento", get_val(jogador_selecionado, 'Crossing'))
        with c2:
            if 'Heading Accuracy' in jogador_selecionado:
                st.metric("Prec. Cabeceio", get_val(jogador_selecionado, 'Heading Accuracy'))
            if 'Short Passing' in jogador_selecionado:
                st.metric("Passe Curto", get_val(jogador_selecionado, 'Short Passing'))
        with c3:
            if 'Volleys' in jogador_selecionado:
                st.metric("Voleios", get_val(jogador_selecionado, 'Volleys'))

    with st.expander("🎯 Habilidade & Criação", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Dribles (DRI)", get_val(jogador_selecionado, 'DRI'))
            st.metric("Passe Geral (PAS)", get_val(jogador_selecionado, 'PAS'))
        with c2:
            if 'Long Passing' in jogador_selecionado:
                st.metric("Lançamento", get_val(jogador_selecionado, 'Long Passing'))
            if 'Ball Control' in jogador_selecionado:
                st.metric("Controle de Bola", get_val(jogador_selecionado, 'Ball Control'))
        with c3:
            if 'Curve' in jogador_selecionado:
                st.metric("Curva", get_val(jogador_selecionado, 'Curve'))

    with st.expander("⚡ Movimentação & Ritmo", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Ritmo Geral (PAC)", get_val(jogador_selecionado, 'PAC'))
            if 'Acceleration' in jogador_selecionado:
                st.metric("Aceleração", get_val(jogador_selecionado, 'Acceleration'))
        with c2:
            if 'Sprint Speed' in jogador_selecionado:
                st.metric("Pique", get_val(jogador_selecionado, 'Sprint Speed'))
            if 'Agility' in jogador_selecionado:
                st.metric("Agilidade", get_val(jogador_selecionado, 'Agility'))
        with c3:
            if 'Reactions' in jogador_selecionado:
                st.metric("Reação", get_val(jogador_selecionado, 'Reactions'))
            if 'Balance' in jogador_selecionado:
                st.metric("Equilíbrio", get_val(jogador_selecionado, 'Balance'))

    with st.expander("💪 Força & Físico", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Físico Geral (PHY)", get_val(jogador_selecionado, 'PHY'))
            if 'Stamina' in jogador_selecionado:
                st.metric("Fôlego (Stamina)", get_val(jogador_selecionado, 'Stamina'))
        with c2:
            if 'Strength' in jogador_selecionado:
                st.metric("Força", get_val(jogador_selecionado, 'Strength'))
            if 'Jumping' in jogador_selecionado:
                st.metric("Impulsão", get_val(jogador_selecionado, 'Jumping'))
        with c3:
            if 'Shot Power' in jogador_selecionado:
                st.metric("Força do Chute", get_val(jogador_selecionado, 'Shot Power'))

    with st.expander("🛡️ Defesa", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Defesa Geral (DEF)", get_val(jogador_selecionado, 'DEF'))
            if 'Def Awareness' in jogador_selecionado:
                st.metric("Consciência Defensiva", get_val(jogador_selecionado, 'Def Awareness'))
        with c2:
            if 'Standing Tackle' in jogador_selecionado:
                st.metric("Dividida em Pé", get_val(jogador_selecionado, 'Standing Tackle'))
        with c3:
            if 'Sliding Tackle' in jogador_selecionado:
                st.metric("Carrinho", get_val(jogador_selecionado, 'Sliding Tackle'))

    with st.expander("🧠 Mentalidade", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            if 'Positioning' in jogador_selecionado:
                st.metric("Posicionamento Ataque", get_val(jogador_selecionado, 'Positioning'))
            if 'Vision' in jogador_selecionado:
                st.metric("Visão de Jogo", get_val(jogador_selecionado, 'Vision'))
        with c2:
            if 'Composure' in jogador_selecionado:
                st.metric("Compostura", get_val(jogador_selecionado, 'Composure'))
            if 'Aggression' in jogador_selecionado:
                st.metric("Combatividade", get_val(jogador_selecionado, 'Aggression'))
        with c3:
            if 'Interceptions' in jogador_selecionado:
                st.metric("Interceptações", get_val(jogador_selecionado, 'Interceptions'))
