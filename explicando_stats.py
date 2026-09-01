# Arquivo: explicando_stats.py
import streamlit as st

def renderizar_explicando_stats():
    st.title("📊 Explicando Stats (EA FC26)")
    st.markdown("Explore as 7 categorias de atributos dos jogadores. Clique em **Expandir** em cada card para entender como cada stat afeta o desempenho em campo.")
    st.markdown("---")

    categorias = [
        {
            "tag": "01 /",
            "pt": "Ofensivo",
            "en": "Attacking",
            "desc": "Atributos focados na criação de jogadas ofensivas, finalizações e passes curtos.",
            "stats": {
                "Cruzamento": "Precisão e curva nos passes levantados das laterais diretamente para a área.",
                "Finalização": "Precisão dos chutes com o pé quando o jogador está posicionado dentro da área.",
                "Prec. Cabeceio": "Precisão e direcionamento de bolas cabeceadas ao gol ou para companheiros.",
                "Passe Curto": "Precisão e velocidade em passes de curta e média distância rasteiros.",
                "Voleios": "Precisão e técnica ao chutar bolas no ar antes que elas toquem o solo."
            }
        },
        {
            "tag": "02 /",
            "pt": "Mentalidade",
            "en": "Mentality",
            "desc": "Atributos táticos e emocionais que afetam a tomada de decisão e a postura sob pressão.",
            "stats": {
                "Combatividade": "Intensidade, raça e gana em disputas de bola dividida e faltas táticas.",
                "Intercept.": "Capacidade de prever jogadas adversárias e cortar linhas de passe.",
                "Pos. ataque": "Habilidade sem bola de achar espaços vazios e se colocar em posição de gol.",
                "Visão de jogo": "Percepção para enxergar companheiros desmarcados e acertar passes em profundidade.",
                "Pênaltis": "Precisão e controle emocional na cobrança de penalidades máximas.",
                "Compostura": "Resistência à pressão de defensores; evita erros de passe ou chute sob marcação."
            }
        },
        {
            "tag": "03 /",
            "pt": "Habilidade",
            "en": "Skill",
            "desc": "Atributos técnicos de drible, controle de bola e precisão em bolas paradas.",
            "stats": {
                "Dribles": "Velocidade e controle na condução de bola frente a adversários no mano a mano.",
                "Curva": "Capacidade de dar efeito à bola em passes, cruzamentos e chutes colocados.",
                "Prec. faltas": "Precisão em cobranças de faltas diretas ao gol.",
                "Lançamento": "Precisão e alcance em passes longos, lançamentos e inversões de jogo.",
                "Controle bola": "Qualidade do primeiro domínio e proximidade com que a bola fica no pé ao recebê-la."
            }
        },
        {
            "tag": "04 /",
            "pt": "Defesa",
            "en": "Defending",
            "desc": "Atributos de desarme, posicionamento defensivo e recuperação da posse de bola.",
            "stats": {
                "Hab. defensiva": "Noção de posicionamento defensivo e capacidade de manter a linha de marcação.",
                "Dividida pé": "Eficácia e precisão ao roubar a bola do adversário usando o pé, sem cometer falta.",
                "Carrinho": "Alcance e precisão ao executar desarmes deslizando no chão."
            }
        },
        {
            "tag": "05 /",
            "pt": "Movimentação",
            "en": "Movement",
            "desc": "Atributos de velocidade, agilidade e tempo de resposta corporal dos jogadores.",
            "stats": {
                "Aceleração": "Rapidez com que o jogador atinge sua velocidade máxima partindo do zero.",
                "Pique": "Velocidade máxima alcançada pelo jogador correndo em linha reta.",
                "Agilidade": "Rapidez para mudar de direção e fazer giros corporais com ou sem a bola.",
                "Reação": "Tempo de resposta a imprevistos, desvios, rebotes do goleiro e bolas soltas.",
                "Equilíbrio": "Capacidade de se manter em pé e no controle mesmo sofrendo impacto físico."
            }
        },
        {
            "tag": "06 /",
            "pt": "Força",
            "en": "Power",
            "desc": "Atributos de potência física, resistência ao fôlego e disputas no corpo.",
            "stats": {
                "Força chute": "Potência e velocidade com que a bola viaja após a finalização.",
                "Impulsão": "Altura que o jogador alcança ao saltar para disputar bolas aéreas.",
                "Fôlego": "Capacidade de manter alta intensidade física e ritmo durante os 90 minutos.",
                "Força": "Resistência em disputas físicas no ombro a ombro, trancos e proteção de bola.",
                "Chutes longe": "Precisão e perigo nas finalizações efetuadas de fora da grande área."
            }
        },
        {
            "tag": "07 /",
            "pt": "Atributos GL",
            "en": "Goalkeeping",
            "desc": "Atributos específicos para a performance, saídas de gol e tempo de reação dos goleiros.",
            "stats": {
                "Elasticidade GL": "Capacidade de saltar e alcançar bolas difíceis no ar ou nos cantos do gol.",
                "Manejo GL": "Habilidade de segurar a bola firmemente após o chute, evitando dar rebotes.",
                "Chute GL": "Alcance, força e precisão na saída de bola com os pés ou reposto de mão.",
                "Posicion. GL": "Capacidade de se posicionar corretamente no gol para cobrir os ângulos do chutador.",
                "Reflexos GL": "Velocidade de reação em finalizações à queima-roupa e desvios inesperados."
            }
        }
    ]

    # Renderiza em grade de 3 colunas horizontais
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for idx, cat in enumerate(categorias):
        with cols[idx % 3]:
            # Substituído st.container(border=True) pelo container HTML .custom-box
            st.markdown(f"""
            <div class="custom-box">
                <span style='color: #94a3b8; font-family: monospace; font-size: 13px;'>{cat['tag']}</span>
                <h2 style='margin: 0; padding: 2px 0; font-size: 24px; color: #ffffff;'>{cat['pt']}</h2>
                <p style='color: #00ffcc; font-size: 13px; font-weight: bold; margin-top: -5px;'>{cat['en']}</p>
                <p style='color: #ffffff; font-size: 12px; min-height: 48px; opacity: 0.85;'>{cat['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Expandir"):
                items = list(cat["stats"].items())
                for i, (nome_stat, desc_stat) in enumerate(items):
                    st.markdown(f"<span class='var-text'>{nome_stat}</span>", unsafe_allow_html=True)
                    st.caption(desc_stat)
                    
                    if i < len(items) - 1:
                        st.divider()
