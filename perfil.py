import streamlit as st
import pandas as pd

def renderizar_perfil(df, find_similar_players, STAT_GROUPS, get_val):
    # Recupera o jogador selecionado armazenado no session_state
    jogador = st.session_state.get('jogador_selecionado')
    
    if jogador is None:
        st.warning("Nenhum jogador selecionado. Por favor, escolha um atleta na aba de busca.")
        return

    nome = get_val(jogador, 'Name')
    posicao = get_val(jogador, 'Position')
    
    st.subheader(f"👤 Perfil do Atleta: {nome}")

    # Mapeamento de atributos essenciais por posição para o botão de sugestão
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

    # Botão de Sugestão Inteligente por Posição
    if st.button("💡 Sugestão para a Posição"):
        st.success(f"Características mais importantes para a posição **{posicao}**: {', '.join(sugestoes_posicao)}")

    # -------------------------------------------------------------
    # BLOCOS EXPANSÍVEIS DE INDICADORES DE PERFORMANCE
    # -------------------------------------------------------------
    with st.expander("👤 Biografia e Informações Básicas", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall (OVR)", get_val(jogador, 'OVR'))
            st.metric("Idade", get_val(jogador, 'Age'))
        with col2:
            st.metric("Posição", posicao)
            st.metric("Clube", get_val(jogador, 'Team'))
        with col3:
            st.metric("Liga", get_val(jogador, 'League'))
            nac_col = 'Nationality' if 'Nationality' in jogador else 'Country'
            st.metric("Nacionalidade", get_val(jogador, nac_col))
        with col4:
            st.metric("Potencial", get_val(jogador, 'POT', '-'))
            st.metric("Pé Preferido", get_val(jogador, 'Preferred foot', '-'))

    with st.expander("⚽ Atributos Ofensivos", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Finalização (SHO)", get_val(jogador, 'SHO'))
            st.metric("Cruzamento", get_val(jogador, 'Crossing', '-'))
        with c2:
            st.metric("Prec. Cabeceio", get_val(jogador, 'Heading Accuracy', '-'))
            st.metric("Passe Curto", get_val(jogador, 'Short Passing', '-'))
        with c3:
            st.metric("Voleios", get_val(jogador, 'Volleys', '-'))

    with st.expander("🎯 Habilidade & Criação", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Dribles (DRI)", get_val(jogador, 'DRI'))
            st.metric("Passe Geral (PAS)", get_val(jogador, 'PAS'))
        with c2:
            st.metric("Lançamento", get_val(jogador, 'Long Passing', '-'))
            st.metric("Controle de Bola", get_val(jogador, 'Ball Control', '-'))
        with c3:
            st.metric("Curva", get_val(jogador, 'Curve', '-'))

    with st.expander("⚡ Movimentação & Ritmo", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Ritmo Geral (PAC)", get_val(jogador, 'PAC'))
            st.metric("Aceleração", get_val(jogador, 'Acceleration', '-'))
        with c2:
            st.metric("Pique", get_val(jogador, 'Sprint Speed', '-'))
            st.metric("Agilidade", get_val(jogador, 'Agility', '-'))
        with c3:
            st.metric("Reação", get_val(jogador, 'Reactions', '-'))
            st.metric("Equilíbrio", get_val(jogador, 'Balance', '-'))

    with st.expander("💪 Força & Físico", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Físico Geral (PHY)", get_val(jogador, 'PHY'))
            st.metric("Fôlego (Stamina)", get_val(jogador, 'Stamina', '-'))
        with c2:
            st.metric("Força", get_val(jogador, 'Strength', '-'))
            st.metric("Impulsão", get_val(jogador, 'Jumping', '-'))
        with c3:
            st.metric("Força do Chute", get_val(jogador, 'Shot Power', '-'))

    with st.expander("🛡️ Defesa", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Defesa Geral (DEF)", get_val(jogador, 'DEF'))
            st.metric("Consciência Defensiva", get_val(jogador, 'Def Awareness', '-'))
        with c2:
            st.metric("Dividida em Pé", get_val(jogador, 'Standing Tackle', '-'))
        with c3:
            st.metric("Carrinho", get_val(jogador, 'Sliding Tackle', '-'))

    with st.expander("🧠 Mentalidade", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Posicionamento Ataque", get_val(jogador, 'Positioning', '-'))
            st.metric("Visão de Jogo", get_val(jogador, 'Vision', '-'))
        with c2:
            st.metric("Compostura", get_val(jogador, 'Composure', '-'))
            st.metric("Combatividade", get_val(jogador, 'Aggression', '-'))
        with c3:
            st.metric("Interceptações", get_val(jogador, 'Interceptions', '-'))

    # Seção de jogadores similares original do layout
    if find_similar_players is not None:
        st.markdown("---")
        try:
            find_similar_players(df, jogador)
        except Exception:
            pass
