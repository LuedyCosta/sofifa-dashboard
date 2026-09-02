import streamlit as st
import pandas as pd

def renderizar_perfil(df, jogador_selecionado):
    st.subheader(f"👤 Perfil do Atleta: {jogador_selecionado.get('Name', 'Jogador')}")
    
    posicao = jogador_selecionado.get('Position', 'CM')
    
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
            st.metric("Overall (OVR)", jogador_selecionado.get('OVR', '-'))
            st.metric("Idade", jogador_selecionado.get('Age', '-'))
        with col2:
            st.metric("Posição", posicao)
            st.metric("Clube", jogador_selecionado.get('Team', '-'))
        with col3:
            st.metric("Liga", jogador_selecionado.get('League', '-'))
            st.metric("Nacionalidade", jogador_selecionado.get('Nationality', jogador_selecionado.get('Country', '-')))

    with st.expander("⚽ Atributos Ofensivos", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Finalização (SHO)", jogador_selecionado.get('SHO', '-'))
            if 'Crossing' in jogador_selecionado:
                st.metric("Cruzamento", jogador_selecionado.get('Crossing'))
        with c2:
            if 'Heading Accuracy' in jogador_selecionado:
                st.metric("Prec. Cabeceio", jogador_selecionado.get('Heading Accuracy'))
            if 'Short Passing' in jogador_selecionado:
                st.metric("Passe Curto", jogador_selecionado.get('Short Passing'))
        with c3:
            if 'Volleys' in jogador_selecionado:
                st.metric("Voleios", jogador_selecionado.get('Volleys'))

    with st.expander("🎯 Habilidade & Criação", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Dribles (DRI)", jogador_selecionado.get('DRI', '-'))
            st.metric("Passe Geral (PAS)", jogador_selecionado.get('PAS', '-'))
        with c2:
            if 'Long Passing' in jogador_selecionado:
                st.metric("Lançamento", jogador_selecionado.get('Long Passing'))
            if 'Ball Control' in jogador_selecionado:
                st.metric("Controle de Bola", jogador_selecionado.get('Ball Control'))
        with c3:
            if 'Curve' in jogador_selecionado:
                st.metric("Curva", jogador_selecionado.get('Curve'))

    with st.expander("⚡ Movimentação & Ritmo", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Ritmo Geral (PAC)", jogador_selecionado.get('PAC', '-'))
            if 'Acceleration' in jogador_selecionado:
                st.metric("Aceleração", jogador_selecionado.get('Acceleration'))
        with c2:
            if 'Sprint Speed' in jogador_selecionado:
                st.metric("Pique", jogador_selecionado.get('Sprint Speed'))
            if 'Agility' in jogador_selecionado:
                st.metric("Agilidade", jogador_selecionado.get('Agility'))
        with c3:
            if 'Reactions' in jogador_selecionado:
                st.metric("Reação", jogador_selecionado.get('Reactions'))
            if 'Balance' in jogador_selecionado:
                st.metric("Equilíbrio", jogador_selecionado.get('Balance'))

    with st.expander("💪 Força & Físico", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Físico Geral (PHY)", jogador_selecionado.get('PHY', '-'))
            if 'Stamina' in jogador_selecionado:
                st.metric("Fôlego (Stamina)", jogador_selecionado.get('Stamina'))
        with c2:
            if 'Strength' in jogador_selecionado:
                st.metric("Força", jogador_selecionado.get('Strength'))
            if 'Jumping' in jogador_selecionado:
                st.metric("Impulsão", jogador_selecionado.get('Jumping'))
        with c3:
            if 'Shot Power' in jogador_selecionado:
                st.metric("Força do Chute", jogador_selecionado.get('Shot Power'))

    with st.expander("🛡️ Defesa", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Defesa Geral (DEF)", jogador_selecionado.get('DEF', '-'))
            if 'Def Awareness' in jogador_selecionado:
                st.metric("Consciência Defensiva", jogador_selecionado.get('Def Awareness'))
        with c2:
            if 'Standing Tackle' in jogador_selecionado:
                st.metric("Dividida em Pé", jogador_selecionado.get('Standing Tackle'))
        with c3:
            if 'Sliding Tackle' in jogador_selecionado:
                st.metric("Carrinho", jogador_selecionado.get('Sliding Tackle'))

    with st.expander("🧠 Mentalidade", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            if 'Positioning' in jogador_selecionado:
                st.metric("Posicionamento Ataque", jogador_selecionado.get('Positioning'))
            if 'Vision' in jogador_selecionado:
                st.metric("Visão de Jogo", jogador_selecionado.get('Vision'))
        with c2:
            if 'Composure' in jogador_selecionado:
                st.metric("Compostura", jogador_selecionado.get('Composure'))
            if 'Aggression' in jogador_selecionado:
                st.metric("Combatividade", jogador_selecionado.get('Aggression'))
        with c3:
            if 'Interceptions' in jogador_selecionado:
                st.metric("Interceptações", jogador_selecionado.get('Interceptions'))
