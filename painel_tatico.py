# Arquivo: painel_tatico.py
import streamlit as st
import matplotlib.pyplot as plt

def desenhar_campo(posicoes):
    """Gera a visualização gráfica do campo de futebol em modo escuro com as posições dos jogadores."""
    fig, ax = plt.subplots(figsize=(7, 8.5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161920')

    # Desenho das linhas do campo
    ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], color="#333842", lw=2)
    ax.plot([0, 100], [50, 50], color="#333842", lw=1.5)
    circulo_central = plt.Circle((50, 50), 12, color="#333842", fill=False, lw=1.5)
    ax.add_patch(circulo_central)
    ax.plot([20, 80, 80, 20, 20], [0, 0, 16, 16, 0], color="#333842", lw=1.5)
    ax.plot([20, 80, 80, 20, 20], [100, 100, 84, 84, 100], color="#333842", lw=1.5)

    # Renderiza os marcadores dos jogadores
    for pos, (x, y) in posicoes.items():
        ax.scatter(x, y, color='#ff4b4b', s=550, zorder=3, edgecolors='white', linewidth=1.5)
        ax.text(x, y, pos, color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=4)

    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off')
    return fig

def renderizar_painel_tatico():
    st.title("📋 Painel de Formações Táticas (EA FC26)")
    st.markdown("Selecione a formação e o preset tático desejado para carregar a análise detalhada.")

    # Mapeamento universal para os 10 Tactical Presets
    preset_labels = {
        "balanced": "Equilibrado (Balanced)",
        "possession": "Posse de Bola (Possession)",
        "short-passing": "Passe Curtos / Construção Paciente",
        "tikitaka": "Tiki-Taka Central",
        "wing-play": "Jogo pelas Pontas (Wing Play)",
        "counter": "Contra-Ataque Rápido (Fast Break)",
        "vertical-counter": "Contra-Ataque Vertical",
        "gegenpress": "Gegenpressing / Pressão Alta",
        "heavy-metal": "Heavy Metal / Pressão Total",
        "park-bus": "Retranca / Bloco Baixo (Park the Bus)"
    }

    # Modelo base com análises genéricas para os 10 presets
    presets_genericos = {
        "balanced": {
            "d": "Estrutura equilibrada com manutenção de posse moderada e linhas defensivas intermediárias.",
            "p": "Alta flexibilidade tática; o time responde bem a qualquer situação de jogo.",
            "c": "Falta de especialização ostensiva em momento específico de ataque ou defesa.",
            "b": "Imponha um ritmo extremo (pressão alta ou contra-ataque rápido) para tirar a formação da zona de conforto."
        },
        "possession": {
            "d": "Foco em manter a posse de bola no campo de ataque com aproximação contínua dos meio-campistas.",
            "p": "Diminui o ritmo do jogo e reduz drasticamente o volume de jogadas do adversário.",
            "c": "Pode se tornar um ataque lento, previsível e suscetível a erros de passe na intermediária.",
            "b": "Monte um bloco médio/baixo compacto e explore transições velozes pelas pontas assim que recuperar a bola."
        },
        "short-passing": {
            "d": "Aproximação intensa entre os setores para troca de passes curtos e triangulações rápidas.",
            "p": "Excelente para atrair a marcação rival e abrir espaços na entrada da grande área.",
            "c": "Dificuldade para vencer defesas muito físicas ou linhas de 5 zagueiros.",
            "b": "Force a marcação física no miolo de zaga e feche os corredores internos de passe."
        },
        "tikitaka": {
            "d": "Troca de passes em ritmo acelerado pelo centro com movimentação constante entre as linhas.",
            "p": "Aceleração mortal no último terço do campo e envolvimento total do setor central.",
            "c": "Falta de amplitude lateral e dependência de alta precisão técnica nos passes de primeira.",
            "b": "Compacte o meio-campo com três homens centrais/volantes e force o jogo para as linhas laterais."
        },
        "wing-play": {
            "d": "Busca constante pelos corredores laterais com alas/pontas bem abertos para dobrar a marcação.",
            "p": "Gera volume maciço de cruzamentos e isola pontas rápidos contra laterais vulneráveis.",
            "c": "Deixa o setor central do meio-campo desguarnecido caso o ataque penda só para os lados.",
            "b": "Utilize dobradinhas na lateral (Lateral + Volante) e garanta zagueiros com bom poder aéreo."
        },
        "counter": {
            "d": "Linhas defensivas recuadas preparadas para roubar a bola e acionar transições letais.",
            "p": "Aproveita instantaneamente qualquer espaço deixado pelas subidas da defesa adversária.",
            "c": "Concede muito controle de bola e campo ao adversário durante a maior parte da partida.",
            "b": "Mantenha o balanço defensivo com ao menos um volante fixo e evite passes arriscados na zona de construção."
        },
        "vertical-counter": {
            "d": "Passe longo e direto rumo aos atacantes assim que a posse de bola é recuperada.",
            "p": "Chegada ultra-rápida ao gol com pouquíssimos toques na bola no meio-campo.",
            "c": "Elevado índice de perda de bola por conta da precipitação dos passes verticais.",
            "b": "Intercepte os passes longos com uma linha defensiva atenta e dominadora na segunda bola."
        },
        "gegenpress": {
            "d": "Pressão sufocante no portador da bola no exato instante em que a posse é perdida.",
            "p": "Força erros na saída de bola do adversário perto do gol e recupera a posse rapidamente.",
            "c": "Desgaste físico acentuado dos atletas e exposição total da defesa se a primeira linha de pressão falhar.",
            "b": "Use passes longos em diagonal para superar a primeira linha de pressão do adversário."
        },
        "heavy-metal": {
            "d": "Ataque em massa e pressão total em todo o campo com ritmo de jogo no limite físico.",
            "p": "Poder ofensivo avassalador que encurrala o adversário na própria grande área.",
            "c": "Linha defensiva extremamente alta e rombo nas costas dos zagueiros e laterais.",
            "b": "Infiltre bolas rasteiras nas costas da zaga adiantada para atacantes rápidos levarem vantagem na corrida."
        },
        "park-bus": {
            "d": "Bloco defensivo baixíssimo com duas linhas muito próximas e compactadas na grande área.",
            "p": "Anula praticamente todas as tentativas de passe e infiltração rasteira pelo centro.",
            "c": "Volume ofensivo quase inexistente e enorme pressão sofrida durante os 90 minutos.",
            "b": "Abuse de chutes colocados da intermediária, jogadas de linha de fundo e cruzamentos para a área."
        }
    }

    # Posições do campo
    posicoes_campo = {
        "3142": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "VOL": (50, 36), "AE": (12, 52), "MC1": (38, 52), "MC2": (62, 52), "AD": (88, 52), "ATA1": (38, 85), "ATA2": (62, 85)},
        "3412": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "ME": (12, 50), "MC1": (38, 45), "MC2": (62, 45), "MD": (88, 50), "MEI": (50, 68), "ATA1": (38, 86), "ATA2": (62, 86)},
        "3421": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "ME": (12, 50), "MC1": (38, 45), "MC2": (62, 45), "MD": (88, 50), "SA1": (35, 72), "SA2": (65, 72), "ATA": (50, 88)},
        "343": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "ME": (12, 50), "MC1": (38, 48), "MC2": (62, 48), "MD": (88, 50), "PE": (20, 82), "ATA": (50, 88), "PD": (80, 82)},
        "3511": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "VOL": (50, 36), "ME": (12, 52), "MC1": (35, 52), "MC2": (65, 52), "MD": (88, 52), "SA": (50, 72), "ATA": (50, 88)},
        "352": {"GOL": (50, 8), "Z1": (25, 20), "Z2": (50, 18), "Z3": (75, 20), "ALA L": (12, 50), "VOL1": (38, 38), "VOL2": (62, 38), "ALA R": (88, 50), "MEI": (50, 68), "ATA1": (38, 86), "ATA2": (62, 86)},
        "41212-n": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 38), "MC1": (35, 54), "MC2": (65, 54), "MEI": (50, 70), "ATA1": (38, 88), "ATA2": (62, 88)},
        "41212-w": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 38), "ME": (18, 56), "MD": (82, 56), "MEI": (50, 70), "ATA1": (38, 88), "ATA2": (62, 88)},
        "4132": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 38), "ME": (20, 62), "MC": (50, 60), "MD": (80, 62), "ATA1": (38, 86), "ATA2": (62, 86)},
        "4141": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 38), "ME": (18, 58), "MC1": (38, 58), "MC2": (62, 58), "MD": (82, 58), "ATA": (50, 86)},
        "4213": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (38, 42), "VOL2": (62, 42), "MEI": (50, 65), "PE": (20, 82), "ATA": (50, 88), "PD": (80, 82)},
        "4222": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (38, 42), "VOL2": (62, 42), "MEI1": (30, 66), "MEI2": (70, 66), "ATA1": (38, 86), "ATA2": (62, 86)},
        "4231-n": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (38, 42), "VOL2": (62, 42), "MSE": (30, 68), "MEI": (50, 70), "MSD": (70, 68), "ATA": (50, 88)},
        "4231-w": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (38, 42), "VOL2": (62, 42), "ME": (18, 68), "MEI": (50, 70), "MD": (82, 68), "ATA": (50, 88)},
        "424": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (38, 48), "VOL2": (62, 48), "PE": (18, 84), "ATA1": (38, 86), "ATA2": (62, 86), "PD": (82, 84)},
        "4312": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "MC1": (28, 48), "MC2": (50, 45), "MC3": (72, 48), "MEI": (50, 68), "ATA1": (38, 86), "ATA2": (62, 86)},
        "4321": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "MC1": (28, 48), "MC2": (50, 45), "MC3": (72, 48), "SA1": (36, 72), "SA2": (64, 72), "ATA": (50, 88)},
        "433-flat": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "MC1": (30, 50), "MC2": (50, 50), "MC3": (70, 50), "PE": (20, 80), "ATA": (50, 88), "PD": (80, 80)},
        "433-holding": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 40), "MC1": (32, 54), "MC2": (68, 54), "PE": (20, 80), "ATA": (50, 88), "PD": (80, 80)},
        "433-defend": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (35, 40), "VOL2": (65, 40), "MC": (50, 56), "PE": (20, 80), "ATA": (50, 88), "PD": (80, 80)},
        "433-attack": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL1": (35, 44), "VOL2": (65, 44), "MEI": (50, 68), "PE": (20, 80), "ATA": (50, 88), "PD": (80, 80)},
        "433-false9": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "VOL": (50, 40), "MC1": (32, 54), "MC2": (68, 54), "PE": (20, 82), "F9": (50, 72), "PD": (80, 82)},
        "4411": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "ME": (18, 55), "MC1": (38, 52), "MC2": (62, 52), "MD": (82, 55), "SA": (50, 72), "ATA": (50, 88)},
        "442-flat": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "ME": (18, 55), "MC1": (38, 52), "MC2": (62, 52), "MD": (82, 55), "ATA1": (38, 85), "ATA2": (62, 85)},
        "442-holding": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "ME": (18, 55), "VOL1": (38, 42), "VOL2": (62, 42), "MD": (82, 55), "ATA1": (38, 85), "ATA2": (62, 85)},
        "451": {"GOL": (50, 8), "LE": (15, 25), "Z1": (38, 22), "Z2": (62, 22), "LD": (85, 25), "ME": (15, 58), "MC1": (32, 52), "MC2": (50, 55), "MC3": (68, 52), "MD": (85, 58), "ATA": (50, 86)},
        "5122": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "VOL": (50, 42), "MC1": (35, 58), "MC2": (65, 58), "ATA1": (38, 86), "ATA2": (62, 86)},
        "5212": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "VOL1": (38, 42), "VOL2": (62, 42), "MEI": (50, 66), "ATA1": (38, 86), "ATA2": (62, 86)},
        "5221": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "VOL1": (38, 45), "VOL2": (62, 45), "SA1": (32, 70), "SA2": (68, 70), "ATA": (50, 88)},
        "523": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "VOL1": (38, 45), "VOL2": (62, 45), "PE": (20, 82), "ATA": (50, 88), "PD": (80, 82)},
        "532": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "MC1": (30, 52), "MC2": (50, 50), "MC3": (70, 52), "ATA1": (38, 85), "ATA2": (62, 85)},
        "541": {"GOL": (50, 8), "AE": (12, 32), "Z1": (30, 22), "Z2": (50, 20), "Z3": (70, 22), "AD": (88, 32), "ME": (18, 55), "MC1": (38, 52), "MC2": (62, 52), "MD": (82, 55), "ATA": (50, 86)}
    }

    # Inicializa a matriz completa com TODOS os 10 presets para TODAS as formações
    matrizMatriz = {formacao: presets_genericos.copy() for formacao in posicoes_campo.keys()}

    # Ajustes finos específicos para as combinações mais populares do meta
    matrizMatriz["4321"]["heavy-metal"] = {
        "d": "Três meio-campistas com dois atacantes flutuantes (CFs) logo atrás de um centroavante em pressão total.",
        "p": "O esquema mais poderoso do meta, unindo infiltrações mortais dos CFs com solidez e abafa defensivo.",
        "c": "Exige ajustes manuais precisos nas instruções para não perder o controle defensivo das laterais.",
        "b": "Utilize um duplo pivô compacto e evite dar espaço para os CFs girarem na entrada da área."
    }
    matrizMatriz["41212-n"]["tikitaka"] = {
        "d": "Losango tradicional no meio-campo focado em troca de passes de primeira pelo centro do campo.",
        "p": "Domínio absoluto do centro do campo, facilitando triangulações curtas e tabelas mortais.",
        "c": "Totalmente nula em amplitude lateral, sofrendo contra equipes que exploram os corredores das pontas.",
        "b": "Utilize formações abertas (como 4-3-3 ou 4-4-2) e force o adversário a atacar exclusivamente pelos lados."
    }
    matrizMatriz["541"]["park-bus"] = {
        "d": "O nível máximo de segurança defensiva: linha de 5 zagueiros e linha de 4 meio-campistas recuados.",
        "p": "Praticamente impossível de ser penetrada por jogadas normais de toque de bola pelo meio.",
        "c": "Zero presença ofensiva natural; o time inteiro abdica de construir jogadas trabalhadas.",
        "b": "Tenha paciência extrema na circulação de bola e explore chutes colocados de longa distância."
    }

    # 1. SELETOR DE FORMAÇÃO
    formacao_selecionada = st.selectbox(
        "1. Escolha a Formação Tática:",
        list(matrizMatriz.keys()),
        index=0
    )

    # Recupera todos os presets disponíveis
    presets_disponiveis = list(matrizMatriz[formacao_selecionada].keys())

    # 2. SELETOR DE TACTICAL PRESET
    preset_selecionado_key = st.selectbox(
        "2. Escolha o Tactical Preset:",
        presets_disponiveis,
        format_func=lambda key: preset_labels.get(key, key),
        index=0
    )

    # Carrega os dados correspondentes
    dados = matrizMatriz[formacao_selecionada][preset_selecionado_key]
    posicoes = posicoes_campo.get(formacao_selecionada, {})

    st.markdown("---")

    # Visualização gráfica do campo
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>Disposição Tática no Campo</h3>", unsafe_allow_html=True)
        fig = desenhar_campo(posicoes)
        st.pyplot(fig)

    st.markdown("---")

    # Exibição dos cards analíticos estruturados em grade de 2 colunas e 2 linhas
    col_a, col_b = st.columns(2)

    with col_a:
        # Linha 1, Coluna 1: Estrutura
        st.markdown(f"""
        <div class="custom-box" style="margin-bottom: 16px;">
            <span style='color: #94a3b8; font-family: monospace; font-size: 13px;'>01 / ESTRUTURA</span>
            <h2 style='margin: 0; padding: 2px 0; font-size: 22px; color: #ffffff;'>{formacao_selecionada}</h2>
            <p style='color: #00ffcc; font-size: 13px; font-weight: bold; margin-top: -5px;'>Preset: {preset_labels.get(preset_selecionado_key, preset_selecionado_key)}</p>
            <p style='color: #ffffff; font-size: 12px; min-height: 48px; opacity: 0.85;'>{dados['d']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Linha 2, Coluna 1: Desvantagens
        st.markdown(f"""
        <div class="custom-box">
            <span style='color: #94a3b8; font-family: monospace; font-size: 13px;'>02.1 / LIMITAÇÕES</span>
            <h2 style='margin: 0; padding: 2px 0; font-size: 20px; color: #ef4444;'>🔴 Desvantagens</h2>
            <p style='color: #ffffff; font-size: 12px; margin-top: 8px; opacity: 0.9;'>{dados['c']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        # Linha 1, Coluna 2: Vantagens
        st.markdown(f"""
        <div class="custom-box" style="margin-bottom: 16px;">
            <span style='color: #94a3b8; font-family: monospace; font-size: 13px;'>02 / DESEMPENHO</span>
            <h2 style='margin: 0; padding: 2px 0; font-size: 20px; color: #22c55e;'>🟢 Vantagens</h2>
            <p style='color: #ffffff; font-size: 12px; margin-top: 8px; opacity: 0.9;'>{dados['p']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Linha 2, Coluna 2: Como Anular
        st.markdown(f"""
        <div class="custom-box">
            <span style='color: #94a3b8; font-family: monospace; font-size: 13px;'>03 / ESTRATÉGIA</span>
            <h2 style='margin: 0; padding: 2px 0; font-size: 22px; color: #ffffff;'>Como Anular</h2>
            <p style='color: #00ffcc; font-size: 13px; font-weight: bold; margin-top: -5px;'>How to Counter</p>
            <p style='color: #ffffff; font-size: 12px; min-height: 48px; opacity: 0.85;'>{dados['b']}</p>
        </div>
        """, unsafe_allow_html=True)
