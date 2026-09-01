# Arquivo: playstyles.py
import streamlit as st

def renderizar_playstyles():
    st.title("🎭 PlayStyles (EA FC26)")
    st.markdown("Explore as 6 categorias oficiais de PlayStyles. Clique em **Expandir** em cada card para visualizar a lista completa e seus impactos em campo.")
    st.markdown("---")

    categorias = [
        {
            "tag": "01 /",
            "pt": "Finalização",
            "en": "Scoring",
            "desc": "Habilidades voltadas para chutes, cavadas, cabeceios e cobranças de bola parada.",
            "styles": {
                "Chute Colocado (Finesse Shot)": "Executa chutes colocados com maior curva, precisão e velocidade, reduzindo a chance de defesa do goleiro.",
                "Chute Forte (Power Shot)": "Aumenta drasticamente a velocidade do Chute Forte (L1+R1 / LB+RB) e reduz o tempo de preparação.",
                "Cabeceio Certeiro (Power Header)": "Executa cabeceios com força máxima e alta precisão, além de alcançar bolas altas com facilidade.",
                "Cavada (Chip Shot)": "Realiza chutes por cobertura (cavadinhas) com maior velocidade e trajetória perfeita sobre o goleiro.",
                "Bola Parada (Dead Ball)": "Aumenta a linha de trajetória visível em faltas e escanteios, aplicando mais curva, velocidade e precisão."
            }
        },
        {
            "tag": "02 /",
            "pt": "Passe",
            "en": "Passing",
            "desc": "Habilidades que aprimoram a visão de jogo, assistências, cruzamentos e lançamentos.",
            "styles": {
                "Passe Incisivo (Incisive Pass)": "Passe em profundidade mais preciso, com curva perfeita para desviar dos defensores.",
                "Passe Rápido (Pinged Pass)": "Passes rasteiros viajam em altíssima velocidade sem que o companheiro perca o controle ao receber.",
                "Lançamento (Long Ball Pass)": "Lançamentos e inversões de jogo pelo alto são mais rápidos, precisos e difíceis de interceptar.",
                "Tiki-Taka (Tiki Taka)": "Executa passes de primeira de calcanhar ou de chapa com extrema precisão e velocidade em espaços curtos.",
                "Cruzamento de Precisão (Whipped Pass)": "Cruzamentos viajam com alta velocidade, curva acentuada e caem no espaço ideal para o atacante."
            }
        },
        {
            "tag": "03 /",
            "pt": "Controle de Bola",
            "en": "Ball Control",
            "desc": "Habilidades de drible, condução rápida, recepção/primeiro domínio e proteção de bola.",
            "styles": {
                "Primeiro Domínio (First Touch)": "Minimiza erros ao dominar a bola, permitindo transicionar para a condução ou drible quase instantaneamente.",
                "Driblador (Trickster)": "Libera fintas e fakes exclusivos com o analógico, além de executar drible de corpo mais ágil.",
                "Proteção de Bola (Press Proven)": "Mantém a posse sob forte pressão física dos defensores e protege a bola com o corpo de forma eficaz.",
                "Condução Rápida (Rapid)": "Alcança velocidade mais alta enquanto conduz a bola no pique e reduz a chance de adiantá-la em excesso.",
                "Técnico (Technical)": "Aumenta a velocidade e precisão ao usar a condução controlada (R2/RT), permitindo curvas fechadas com a bola grudada ao pé.",
                "Elegância (Flair)": "Executa passes, letra, calcanhares e finalizações acrobáticas com maior taxa de sucesso."
            }
        },
        {
            "tag": "04 /",
            "pt": "Defesa",
            "en": "Defending",
            "desc": "Habilidades de desarmes em pé, carrinhos, marcação e interceptações de linha de passe.",
            "styles": {
                "Bloqueio (Block)": "Aumenta o alcance de esticada de perna para bloquear chutes e passes, travando a bola com sucesso.",
                "Interceptação (Intercept)": "Aumenta o alcance de leitura de jogadas para cortar passes rasteiros ou aéreos e manter a posse.",
                "Antecipação (Anticipate)": "Melhora a taxa de sucesso no desarme em pé, parando o adversário sem cometer falta e mantendo a bola nos pés.",
                "Muralha (Bruiser)": "Vence disputas físicas de ombro a ombro com facilidade ao desarmar o adversário na força bruta.",
                "Carrinho (Slide Tackle)": "Aumenta o alcance do carrinho defensivo e permite parar a bola nos pés mesmo deslizando no gramado.",
                "Cercar (Jockey)": "Aumenta a velocidade máxima ao cercar (L2/LT) e permite transições rápidas de corrida durante a marcação."
            }
        },
        {
            "tag": "05 /",
            "pt": "Físico",
            "en": "Physical",
            "desc": "Habilidades de explosão física, resistência/fôlego, disputas aéreas e arremessos.",
            "styles": {
                "Arrancada Rápida (Quick Step)": "Aceleração explosiva mais rápida ao iniciar o pique com ou sem a bola.",
                "Incansável (Relentless)": "Reduz drasticamente o consumo de fôlego durante a partida e recupera energia rapidamente no intervalo.",
                "Trivela (Trivela)": "Passes e finalizações de três dedos (extrema do pé) são executados espontaneamente com alta precisão.",
                "Aéreo (Aerial)": "Realiza saltos mais altos e possui maior presença física em disputas de bola pelo alto no ataque ou defesa.",
                "Acrobático (Acrobatic)": "Executa voleios, tesouras e finalizações no ar com alcance ampliado e precisão impecável.",
                "Arremesso Longo (Long Throw)": "Executa arremessos laterais com alcance e força equivalente a um cruzamento na área."
            }
        },
        {
            "tag": "06 /",
            "pt": "Goleiro",
            "en": "Goalkeeping",
            "desc": "Habilidades exclusivas para arqueiros (elasticidade, saídas do gol, reflexos e reposição).",
            "styles": {
                "Elasticidade (Far Reach)": "Goleiro alcança chutes mais difíceis nos ângulos e cantos distantes.",
                "Dono da Área (Cross Catcher)": "Sai do gol em escanteios e cruzamentos com tempo de bola perfeito para agarrar a bola no ar.",
                "Saída Agressiva (Rush Out)": "Velocidade ampliada ao sair do gol no mano a mano para fechar o ângulo do atacante.",
                "Jogo de Pés (Footwork)": "Realiza defesas com os pés com mais frequência e eficiência em chutes rasteiros e à queima-roupa.",
                "Espalmada (Deflector)": "Espalma chutes fortes para zonas seguras do campo, longe dos atacantes adversários.",
                "Arremesso Longo GL (Far Throw)": "Arremessa a bola com as mãos até o meio-campo com velocidade e precisão para iniciar contra-ataques."
            }
        }
    ]

    # Renderiza em grade de 3 colunas horizontais
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for idx, cat in enumerate(categorias):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"<span style='color: #888; font-family: monospace; font-size: 13px;'>{cat['tag']}</span>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='margin: 0; padding: 2px 0; font-size: 24px;'>{cat['pt']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #888; font-size: 13px; font-weight: bold; margin-top: -5px;'>{cat['en']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #ccc; font-size: 12px; min-height: 48px;'>{cat['desc']}</p>", unsafe_allow_html=True)
                
                with st.expander("Expandir"):
                    for nome_style, desc_style in cat["styles"].items():
                        st.markdown(f"**{nome_style}**")
                        st.caption(desc_style)
