# Arquivo: painel_tatico.py
import streamlit as st
import matplotlib.pyplot as plt

def desenhar_campo(posicoes):
    """Gera a visualização gráfica do campo de futebol em modo escuro com as posições dos jogadores."""
    fig, ax = plt.subplots(figsize=(7, 9))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161920')

    # Borda do campo
    ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], color="#333842", lw=2)
    # Linha de meio-campo
    ax.plot([0, 100], [50, 50], color="#333842", lw=1.5)
    # Círculo central
    circulo_central = plt.Circle((50, 50), 12, color="#333842", fill=False, lw=1.5)
    ax.add_patch(circulo_central)
    # Áreas
    ax.plot([20, 80, 80, 20, 20], [0, 0, 16, 16, 0], color="#333842", lw=1.5) # Área inferior
    ax.plot([20, 80, 80, 20, 20], [100, 100, 84, 84, 100], color="#333842", lw=1.5) # Área superior

    # Plota os jogadores no campo
    for pos, (x, y) in posicoes.items():
        ax.scatter(x, y, color='#ff4b4b', s=550, zorder=3, edgecolors='white', linewidth=1.5)
        ax.text(x, y, pos, color='white', fontsize=8, fontweight='bold', ha='center', va='center', zorder=4)

    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off')
    return fig

def renderizar_painel_tatico():
    st.title("📋 Painel de Formações Táticas")
    st.markdown("Selecione uma formação para visualizar o desenho tático no campo e a análise detalhada de desempenho abaixo.")

    formacoes_dados = {
        "4-3-3 (Consolidado)": {
            "preset": "Passe Rápido / Pressão no Erro",
            "explicacao": "Uma das formações mais equilibradas do futebol moderno. Oferece amplitude nas pontas e boa ocupação do meio-campo com três meias centrais.",
            "vantagens": [
                "Excelente largura de campo com pontas velozes.",
                "Triângulos de passes naturais pelo meio e laterais.",
                "Fácil transição ofensiva e boa recomposição."
            ],
            "desvantagens": [
                "Pode deixar o volante isolado se os meias avançarem demais.",
                "Exige pontas com alta dedicação defensiva.",
                "Vulnerável a times com 5 meias no controle de posse."
            ],
            "como_jogar_contra": "Explore os espaços deixados entre os pontas e os laterais adversários. Formações em 4-2-3-1 ou 3-5-2 conseguem povoar o meio e anular a criação de jogadas centrais.",
            "posicoes": {
                "GOL": (50, 8),
                "LE": (15, 25), "ZAG1": (38, 22), "ZAG2": (62, 22), "LD": (85, 25),
                "VOL": (50, 40), "MC1": (32, 52), "MC2": (68, 52),
                "PE": (20, 80), "ATA": (50, 88), "PD": (80, 80)
            }
        },
        "4-2-3-1 (Equilibrado)": {
            "preset": "Equilibrado / Construção Lenta",
            "explicacao": "A formação mais popular para controle tático. Utiliza dois volantes para proteção defensiva e um meia armador (MEI) para articular os ataques.",
            "vantagens": [
                "Defesa extremamente sólida com duplo pivô de volantes.",
                "Alta flexibilidade entre atacar e defender.",
                "Oportunidades de infiltração constante com o MEI."
            ],
            "desvantagens": [
                "O centroavante pode ficar isolado contra defesas de 3 zagueiros.",
                "Depende muito da qualidade individual do MEI central.",
                "Exige paciência na construção de jogadas."
            ],
            "como_jogar_contra": "Use pressão alta nos dois volantes para forçar o erro na saída de bola. Formações como 4-4-2 soltam dois atacantes para pressionar diretamente a saída dos zagueiros.",
            "posicoes": {
                "GOL": (50, 8),
                "LE": (15, 24), "ZAG1": (38, 21), "ZAG2": (62, 21), "LD": (85, 24),
                "VOL1": (35, 42), "VOL2": (65, 42),
                "ME": (20, 68), "MEI": (50, 70), "MD": (80, 68),
                "ATA": (50, 88)
            }
        },
        "4-4-2 (Clássico)": {
            "preset": "Contra-Ataque Rápido / Linhas Baixas",
            "explicacao": "A estrutura tradicional com duas linhas de quatro muito bem definidas. Garante cobertura total em toda a largura do campo.",
            "vantagens": [
                "Presença dupla na área com dois centroavantes.",
                "Duas linhas defensivas muito difíceis de serem furadas.",
                "Transições diretas de contra-ataque letais."
            ],
            "desvantagens": [
                "Pode ser superado numericamente no meio por esquemas com 3 meias.",
                "Espaço entre as linhas defensivas e o ataque se o time recuar muito.",
                "Meias centrais ficam sobrecarregados sem bola."
            ],
            "como_jogar_contra": "Ataque pelos espaços entre as linhas (zona do camisa 10). Usar um esquema com 3 meias centrais como o 4-3-3 permite dominar a posse de bola no centro.",
            "posicoes": {
                "GOL": (50, 8),
                "LE": (15, 25), "ZAG1": (38, 22), "ZAG2": (62, 22), "LD": (85, 25),
                "ME": (18, 55), "MC1": (38, 52), "MC2": (62, 52), "MD": (82, 55),
                "ATA1": (38, 85), "ATA2": (62, 85)
            }
        },
        "3-5-2 (Dominante)": {
            "preset": "Posse de Bola / Pressão Alta",
            "explicacao": "Uma formação ofensiva e versátil que utiliza alas para cobrir todo o corredor lateral, mantendo densidade máxima no meio do campo.",
            "vantagens": [
                "Superioridade numérica constante no meio-campo.",
                "Três zagueiros dão segurança contra duplas de ataque.",
                "Alas dão amplitude total ao ataque."
            ],
            "desvantagens": [
                "Espaços enormes nas costas dos alas durante contra-ataques.",
                "Exige alto desgaste físico dos dois alas.",
                "Vulnerável a pontas rápidos jogando no mano a mano."
            ],
            "como_jogar_contra": "Explore as pontas com velocidade (4-3-3 ou 4-2-3-1). Lance bolas nas costas dos alas quando eles estiverem projetados no ataque.",
            "posicoes": {
                "GOL": (50, 8),
                "ZAG1": (25, 22), "ZAG2": (50, 20), "ZAG3": (75, 22),
                "ALA L": (12, 52), "VOL1": (38, 40), "VOL2": (62, 40), "ALA R": (88, 52),
                "MEI": (50, 68),
                "ATA1": (38, 86), "ATA2": (62, 86)
            }
        }
    }

    # Seletor de formação
    formacao_selecionada = st.selectbox(
        "Escolha a Formação Tática:",
        list(formacoes_dados.keys()),
        index=0
    )

    dados = formacoes_dados[formacao_selecionada]

    st.markdown("---")

    # 1. CAMPO NO TOPO
    col_campo_left, col_campo_center, col_campo_right = st.columns([1, 2, 1])
    with col_campo_center:
        st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>Dispensa Tática em Campo</h3>", unsafe_allow_html=True)
        fig = desenhar_campo(dados["posicoes"])
        st.pyplot(fig)

    st.markdown("---")

    # 2. CARDS INFORMATIVOS ABAIXO DO CAMPO
    c1, c2, c3 = st.columns(3)

    # Card 1: Visão Geral e Preset
    with c1:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>01 /</span>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>{formacao_selecionada}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ff4b4b; font-size: 13px; font-weight: bold; margin-top: -5px;'>Preset: {dados['preset']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ccc; font-size: 12px; min-height: 48px;'>{dados['explicacao']}</p>", unsafe_allow_html=True)

    # Card 2: Análise de Vantagens e Desvantagens
    with c2:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>02 /</span>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>Análise de Jogo</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 13px; font-weight: bold; margin-top: -5px;'>Pros & Cons</p>", unsafe_allow_html=True)
            
            with st.expander("Ver Vantagens e Desvantagens", expanded=True):
                st.markdown("**🟢 Vantagens:**")
                for v in dados["vantagens"]:
                    st.markdown(f"- {v}")
                
                st.divider()
                
                st.markdown("**🔴 Desvantagens:**")
                for d in dados["desvantagens"]:
                    st.markdown(f"- {d}")

    # Card 3: Como Jogar Contra
    with c3:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>03 /</span>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>Contramedidas</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 13px; font-weight: bold; margin-top: -5px;'>How to Counter</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ccc; font-size: 12px; min-height: 48px;'>{dados['como_jogar_contra']}</p>", unsafe_allow_html=True)
