# Arquivo: explicando_stats.py
import streamlit as st

def renderizar_explicando_stats():
    st.title("📊 Explicando Stats (Atributos FC26)")
    st.markdown("Selecione uma categoria abaixo para entender exatamente como cada atributo afeta a performance dos jogadores em campo.")

    categoria = st.selectbox(
        "Selecione a Categoria de Atributos:",
        ["Ofensivo", "Mentalidade", "Habilidade", "Defesa", "Movimentação", "Atributos GL", "Força"],
        index=0
    )

    st.markdown("---")

    stats = {}

    if categoria == "Ofensivo":
        st.subheader("⚽ Atributos Ofensivos")
        stats = {
            "Cruzamento": "Precisão e curva nos passes levantados das laterais diretamente para a área.",
            "Finalização": "Precisão dos chutes com o pé quando o jogador está posicionado dentro da área.",
            "Prec. Cabeceio": "Precisão e direcionamento de bolas cabeceadas ao gol ou para companheiros.",
            "Passe Curto": "Precisão e velocidade em passes de curta e média distância rasteiros.",
            "Voleios": "Precisão e técnica ao chutar bolas no ar antes que elas toquem o solo."
        }

    elif categoria == "Mentalidade":
        st.subheader("🧠 Atributos de Mentalidade")
        stats = {
            "Combatividade": "Intensidade, raça e gana em disputas de bola dividida e faltas táticas.",
            "Intercept.": "Capacidade de prever jogadas adversárias e cortar linhas de passe.",
            "Pos. ataque": "Habilidade sem bola de achar espaços vazios e se colocar em posição de gol.",
            "Visão de jogo": "Percepção para enxergar companheiros desmarcados e acertar passes em profundidade.",
            "Pênaltis": "Precisão e controle emocional na cobrança de penalidades máximas.",
            "Compostura": "Resistência à pressão de defensores; evita erros de passe ou chute sob marcação."
        }

    elif categoria == "Habilidade":
        st.subheader("🎨 Atributos de Habilidade")
        stats = {
            "Dribles": "Velocidade e controle na condução de bola frente a adversários no mano a mano.",
            "Curva": "Capacidade de dar efeito à bola em passes, cruzamentos e chutes colocados.",
            "Prec. faltas": "Precisão em cobranças de faltas diretas ao gol.",
            "Lançamento": "Precisão e alcance em passes longos, lançamentos e inversões de jogo.",
            "Controle bola": "Qualidade do primeiro domínio e proximidade com que a bola fica no pé ao recebê-la."
        }

    elif categoria == "Defesa":
        st.subheader("🛡️ Atributos Defensivos")
        stats = {
            "Hab. defensiva": "Noção de posicionamento defensivo e capacidade de manter a linha de marcação.",
            "Dividida pé": "Eficácia e precisão ao roubar a bola do adversário usando o pé, sem cometer falta.",
            "Carrinho": "Alcance e precisão ao executar desarmes deslizando no chão."
        }

    elif categoria == "Movimentação":
        st.subheader("🏃 Atributos de Movimentação")
        stats = {
            "Aceleração": "Rapidez com que o jogador atinge sua velocidade máxima partindo do zero.",
            "Pique": "Velocidade máxima alcançada pelo jogador correndo em linha reta.",
            "Agilidade": "Rapidez para mudar de direção e fazer giros corporais com ou sem a bola.",
            "Reação": "Tempo de resposta a imprevistos, desvios, rebotes do goleiro e bolas soltas.",
            "Equilíbrio": "Capacidade de se manter em pé e no controle mesmo sofrendo impacto físico."
        }

    elif categoria == "Atributos GL":
        st.subheader("🧤 Atributos de Goleiro")
        stats = {
            "Elasticidade GL": "Capacidade de saltar e alcançar bolas difíceis no ar ou nos cantos do gol.",
            "Manejo GL": "Habilidade de segurar a bola firmemente após o chute, evitando dar rebotes.",
            "Chute GL": "Alcance, força e precisão na saída de bola com os pés ou reposto de mão.",
            "Posicion. GL": "Capacidade de se posicionar corretamente no gol para cobrir os ângulos do chutador.",
            "Reflexos GL": "Velocidade de reação em finalizações à queima-roupa e desvios inesperados."
        }

    elif categoria == "Força":
        st.subheader("🏋️ Atributos de Força e Físico")
        stats = {
            "Força chute": "Potência e velocidade com que a bola viaja após a finalização.",
            "Impulsão": "Altura que o jogador alcança ao saltar para disputar bolas aéreas.",
            "Fôlego": "Capacidade de manter alta intensidade física e ritmo de corrida durante os 90 minutos.",
            "Força": "Resistência em disputas físicas no ombro a ombro, trancos e proteção de bola.",
            "Chutes longe": "Precisão e perigo nas finalizações efetuadas de fora da grande área."
        }

    # Renderização dos Cards
    for nome_stat, descricao in stats.items():
        with st.container():
            st.markdown(f"### **{nome_stat}**")
            st.info(descricao)
