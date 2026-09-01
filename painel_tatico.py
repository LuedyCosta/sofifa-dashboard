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

    # Mapeamento para nomes exibidos na UI do Streamlit
    preset_labels = {
        "short-passing": "Passe Curtos / Construção Paciente",
        "heavy-metal": "Heavy Metal / Pressão Total",
        "gegenpress": "Gegenpressing / Pressão Alta",
        "wing-play": "Jogo pelas Pontas",
        "possession": "Posse de Bola (Tiki-Taka)",
        "balanced": "Equilibrado",
        "tikitaka": "Tiki-Taka Central",
        "vertical-counter": "Contra-Ataque Vertical",
        "park-bus": "Retranca / Bloco Baixo",
        "counter": "Contra-Ataque Rápido"
    }

    # Posições de cada formação para o renderizador gráfico
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

    # Matriz Matriz exata enviada
    matrizMatriz = {
        "3142": {
            "short-passing": {
                "d": "Utiliza um volante fixo à frente de três zagueiros, uma linha de quatro intermediária com alas e meias centrais, e dois atacantes de referência.",
                "p": "Excelente circulação de bola pelo meio e superioridade numérica imediata na construção ofensiva curta.",
                "c": "Alas sobrecarregados defensivamente; se perdem a bola, o lado do campo fica totalmente exposto.",
                "b": "Explore pontas velozes pelas laterais nas costas dos alas e use triangulações rápidas para isolar os três zagueiros."
            }
        },
        "3412": {
            "heavy-metal": {
                "d": "Estrutura agressiva que une um meia armador (CAM) e dois centroavantes logo acima de quatro meio-campistas/alas.",
                "p": "Poder ofensivo avassalador por dentro, criando tabelas contínuas na entrada da área adversária.",
                "c": "Ausência de um volante fixo de contenção puramente defensivo deixa o miolo vulnerável a infiltrações.",
                "b": "Jogue com um meio-campo compacto (como um 4-2-3-1) para fechar o espaço do CAM e force o jogo para as laterais."
            }
        },
        "3421": {
            "gegenpress": {
                "d": "Dois meias atacantes flutuando por dentro apoiando um único centroavante, com alas cobrindo a largura do campo.",
                "p": "Sufoca o adversário no campo de ataque e gera constante pressão pós-perda com os meias avançados.",
                "c": "Estamina dos alas esgota rapidamente e o ataque pode ficar dependente da inspiração individual do centroavante.",
                "b": "Quebre a primeira linha de pressão com passes longos e certeiros para os pontas ou alas em velocidade."
            }
        },
        "343": {
            "wing-play": {
                "d": "Formação focada em esticar a defesa adversária com pontas abertos colados na linha lateral e forte presença ofensiva.",
                "p": "Criação abundante de jogadas de linha de fundo e cruzamentos venenosos para a grande área.",
                "c": "Fragilidade defensiva extrema nas diagonais defensivas dos zagueiros externos.",
                "b": "Feche a entrada da área com uma linha de quatro zagueiros compactos e anule as opções de cruzamento bloqueando os pontas."
            }
        },
        "3511": {
            "possession": {
                "d": "Meio-campo superpovoado com um segundo atacante (CF) atuando como elemento surpresa atrás do centroavante estático.",
                "p": "Posse de bola segura, controle territorial absoluto e bloqueio eficiente de passes centrais.",
                "c": "Ritmo de jogo lento e previsível se os alas não tiverem ímpeto ofensivo constante.",
                "b": "Adote uma postura de bloco médio, feche as linhas de passe interiores e force erros de troca de bola na intermediária."
            }
        },
        "352": {
            "balanced": {
                "d": "O esquema clássico de três zagueiros com dois volantes de contenção, um armador e dois atacantes.",
                "p": "Equilíbrio perfeito entre solidez defensiva central e volume de jogo ofensivo com a dupla de frente.",
                "c": "Os espaços deixados nas costas dos alas exigem cobertura manual impecável dos zagueiros laterais.",
                "b": "Ataque pelas pontas com pontas rápidos para forçar o ala rival a recuar, transformando a linha de 3 em uma linha defensiva de 5 pressionada."
            }
        },
        "41212-n": {
            "tikitaka": {
                "d": "Losango tradicional no meio-campo com um volante defensivo, dois meias centrais, um CAM e dois atacantes.",
                "p": "Domínio absoluto do centro do campo, facilitando triangulações curtas e tabelas mortais.",
                "c": "Totalmente nula em amplitude lateral, sofrendo contra equipes que exploram os corredores das pontas.",
                "b": "Utilize formações abertas (como 4-3-3 ou 4-4-2) e force o adversário a atacar exclusivamente pelos lados, onde sua defesa está armada."
            }
        },
        "41212-w": {
            "balanced": {
                "d": "Variação do losango que puxa os meias centrais para as posições de LM e RM, garantindo largura.",
                "p": "Corrige a falha crônica de amplitude do losango fechado sem perder o poder de fogo central.",
                "c": "O meio-campo central fica mais desguarnecido, contando apenas com um volante na proteção.",
                "b": "Conquiste o controle do meio-campo com três homens no setor e explore o espaço deixado pelo volante solitário."
            }
        },
        "4132": {
            "vertical-counter": {
                "d": "Linha de três meias avançados logo acima de um único volante, municiando dois centroavantes rápidos.",
                "p": "Transição ofensiva extremamente rápida e vertical rumo ao gol adversário.",
                "c": "O volante central fica totalmente isolado no combate defensivo caso o time perca a bola no campo ofensivo.",
                "b": "Pressione a saída de bola do volante único e mantenha a zaga atenta a bolas longas nas costas."
            }
        },
        "4141": {
            "park-bus": {
                "d": "Linha de quatro meio-campistas compactada com um volante defensivo à frente da zaga e um único atacante isolado.",
                "p": "Linha defensiva extremamente próxima, bloqueando qualquer espaço de infiltração pelo centro.",
                "c": "Extrema dificuldade para gerar perigo ofensivo ou contra-atacar com volume.",
                "b": "Use chutes de longa distância, circule a bola com paciência e explore cruzamentos altos para furar o bloqueio estático."
            }
        },
        "4213": {
            "counter": {
                "d": "Duplo pivô de volantes protegendo a zaga, com um CAM municiando um trio de ataque rápido (PE, PD e centroavante).",
                "p": "Combinação perfeita de segurança defensiva com velocidade letal nas pontas.",
                "c": "O CAM pode se desgastar muito tendo que transitar entre armar o jogo e recompor a linha defensiva.",
                "b": "Feche os corredores internos com um meio-campo em bloco médio e evite perder a bola no ataque para não sofrer contra-ataques."
            }
        },
        "4222": {
            "balanced": {
                "d": "Dois volantes, dois meias ofensivos centralizados/abertos por dentro e dois centroavantes.",
                "p": "Estrutura extremamente simétrica e sólida, excelente para fechar os espaços entrelinhas.",
                "c": "Falta profundidade e largura natural nas pontas, exigindo apoio constante dos laterais.",
                "b": "Explore os espaços deixados pelos laterais quando eles sobem para tentar dar largura ao time."
            }
        },
        "4231-n": {
            "possession": {
                "d": "O clássico esquema de segurança com dois volantes, três meias ofensivos compactos (LAM, CAM, RAM) e um centroavante.",
                "p": "Controle absoluto de jogo, posse de bola segura e intransponibilidade no miolo de zaga.",
                "c": "Jogo pode se tornar engessado e previsível se o adversário fechar bem a entrada da área.",
                "b": "Adote marcação em zona rigorosa e force o adversário a arriscar passes longos inofensivos."
            }
        },
        "4231-w": {
            "gegenpress": {
                "d": "Mantém o duplo pivô e o centroavante, mas abre dois pontas legítimos (LM e RM) nas alas com transição rápida.",
                "p": "Junta a solidez defensiva dos volantes com a amplitude agressiva dos pontas.",
                "c": "Exige extrema dedicação defensiva dos pontas para fechar os espaços junto aos laterais.",
                "b": "Supere o duplo pivô trocando passes rápidos em velocidade pelo centro com meias criativos."
            }
        },
        "424": {
            "gegenpress": {
                "d": "Quatro atacantes fixos apoiados por apenas dois volantes e a linha de defesa.",
                "p": "Pressão sufocante na saída de bola rival e volume ofensivo máximo.",
                "c": "Buraco gigantesco no meio-campo; qualquer erro na pressão resulta em contra-ataque livre para o rival.",
                "b": "Atraia a pressão tocando a bola curto na defesa e lance imediatamente nas costas dos volantes que sobem sozinhos."
            }
        },
        "4312": {
            "short-passing": {
                "d": "Três meio-campistas centrais, um armador central (CAM) e dois centroavantes.",
                "p": "Excelente para reter a bola no campo ofensivo e envolver a zaga com passes curtos.",
                "c": "Totalmente vulnerável a ataques rápidos pelas laterais do campo.",
                "b": "Jogue com pontas rápidos e force o jogo pelas pontas onde o adversário não tem cobertura defensiva natural."
            }
        },
        "4321": {
            "heavy-metal": {
                "d": "Três meio-campistas com dois atacantes flutuantes (CFs) logo atrás de um centroavante.",
                "p": "O esquema mais eficiente do jogo, unindo infiltrações mortais dos CFs com solidez defensiva ajustável.",
                "c": "Exige ajustes manuais precisos nas instruções para não perder o controle das laterais.",
                "b": "Utilize um duplo pivô compacto e evite dar espaço para os CFs girarem na entrada da área."
            }
        },
        "433-flat": {
            "balanced": {
                "d": "O desenho mais universal do futebol: linha de 4, trio de meio-campo plano, pontas abertos e centroavante.",
                "p": "Distribuição homogênea de jogadores por todo o campo, facilitando qualquer estilo de jogo.",
                "c": "Pode se tornar vulnerável se os três meias tiverem apenas funções passivas.",
                "b": "Supere o meio-campo com superioridade numérica temporária vinda de descidas dos alas ou do segundo atacante."
            }
        },
        "433-holding": {
            "possession": {
                "d": "Variação da 4-3-3 com um volante de contenção fixo protegendo a zaga e dois meias à frente.",
                "p": "Maior estabilidade defensiva em transições sem perder a largura dos pontas.",
                "c": "O setor de criação pode ficar lento se o volante for excessivamente defensivo.",
                "b": "Feche os espaços entre o volante fixo e os zagueiros para sufocar a saída de bola curta."
            }
        },
        "433-defend": {
            "park-bus": {
                "d": "Dois volantes mais recuados e um meio-campista central, mantendo os pontas e o centroavante avançados.",
                "p": "Excelente para segurar resultados contra equipes muito técnicas.",
                "c": "Dificuldade acentuada para criar volume de jogo no ataque.",
                "b": "Avance sua linha defensiva até o meio-campo e pressione a saída de bola sem medo."
            }
        },
        "433-attack": {
            "gegenpress": {
                "d": "Um meio-campista avança para se alinhar ao ataque como um armador, deixando dois volantes na base com pressão alta.",
                "p": "Grande presença de jogadores na zona de finalização adversária.",
                "c": "Deixa um buraco perigoso na entrelinhas defensiva.",
                "b": "Infiltra passes rápidos rasteiros no espaço deixado pelo meia que avançou para o ataque."
            }
        },
        "433-false9": {
            "tikitaka": {
                "d": "Centroavante recua para buscar jogo, atraindo zagueiros e abrindo caminho para os pontas.",
                "p": "Posse de bola sufocante e extrema dificuldade de marcação individual para os zagueiros rivais.",
                "c": "Ausência de um centroavante de referência física na grande área.",
                "b": "Mantenha a linha defensiva recuada e por zona, proibindo os zagueiros de saírem da posição para caçar o falso 9."
            }
        },
        "4411": {
            "counter": {
                "d": "Duas linhas de quatro compactas com um segundo atacante flutuando atrás do centroavante.",
                "p": "Solidez defensiva exemplar combinada com transições rápidas pelos lados.",
                "c": "Pouca criatividade central se o segundo atacante for neutralizado.",
                "b": "Use meias criativos entrelinhas para quebrar as duas linhas de quatro do adversário."
            }
        },
        "442-flat": {
            "vertical-counter": {
                "d": "Duas linhas rígidas de quatro jogadores e uma dupla de ataque tradicional.",
                "p": "Simples de executar, extremamente compacta e letal em contra-ataques verticais.",
                "c": "O meio-campo central pode ser dominado por esquemas com três ou mais homens no setor.",
                "b": "Sobrecargue o setor central com um trio de meio-campo móvel para forçar os alas rivais a fecharem o jogo."
            }
        },
        "442-holding": {
            "balanced": {
                "d": "Ajusta os dois meias centrais para funções de volantes de contenção, mantendo as linhas de quatro.",
                "p": "Segurança defensiva máxima sem abrir mão da dupla de ataque.",
                "c": "Pode faltar aproximação rápida para a construção de jogadas no campo ofensivo.",
                "b": "Circule a bola com paciência pelos flancos e explore cruzamentos para vencer a altura dos volantes recuados."
            }
        },
        "451": {
            "possession": {
                "d": "Linha de cinco meio-campistas compactos sufocando o adversário com um único centroavante isolado.",
                "p": "Impossível de perder a posse de bola no meio-campo se bem executada.",
                "c": "Ataque totalmente isolado e dependente de subidas tardias dos meias.",
                "b": "Mantenha a calma na defesa, feche os espaços centrais e utilize bolas longas para surpreender a retarguarda alta."
            }
        },
        "5122": {
            "counter": {
                "d": "Linha defensiva de cinco com um volante central e dois atacantes de referência na frente.",
                "p": "Muralha defensiva intransponível por dentro com duas opções claras de escape no ataque.",
                "c": "Meio-campo defensivo isolado do ataque durante longos períodos do jogo.",
                "b": "Pressione a saída de bola no campo adversário e force os alas a correrem para trás, desgastando-os fisicamente."
            }
        },
        "5212": {
            "vertical-counter": {
                "d": "Três zagueiros e dois alas, protegidos por dois volantes e armados por um CAM para servir dois centroavantes.",
                "p": "Excelente equilíbrio entre fechar a defesa e contra-atacar com velocidade central e lateral.",
                "c": "Espaços consideráveis entre o duplo pivô e o CAM se o time for empurrado para trás.",
                "b": "Mantenha a posse de bola no campo ofensivo e use chutes de longa distância para furar o bloqueio duplo."
            }
        },
        "5221": {
            "wing-play": {
                "d": "Defesa de cinco com dois volantes, dois meias/pontas abertos e um centroavante.",
                "p": "Proteção lateral reforçada combinada com velocidade agigantada nas pontas.",
                "c": "O meio-campo central sofre para conter equipes que tocam a bola rápido por dentro.",
                "b": "Centralize o jogo com meias criativos e evite dar espaço para os pontas dispararem nas costas dos alas."
            }
        },
        "523": {
            "counter": {
                "d": "Trio de zagueiros, dois alas, dois volantes centrais e um trio de ataque rápido (ponta esquerda, ponta direita e centroavante).",
                "p": "Defesa quase intransponível contra investidas centrais e contra-ataques devastadores com três homens na frente.",
                "c": "Meio-campo central reduzido a dois jogadores, facilitando o domínio territorial do rival.",
                "b": "Domine o círculo central com superioridade numérica de meio-campistas e cadastre a posse de bola."
            }
        },
        "532": {
            "park-bus": {
                "d": "Três zagueiros, dois alas, um trio de meio-campo compacto e dois centroavantes.",
                "p": "Fechamento absoluto de todos os espaços centrais e lateral próximos à área.",
                "c": "Ofensivamente pobre, dependendo de lances esporádicos de velocidade da dupla de ataque.",
                "b": "Use cruzamentos venenosos, chutes de fora da área e mantenha uma linha alta para abafar qualquer tentativa de saída rápida."
            }
        },
        "541": {
            "park-bus": {
                "d": "O nível máximo de segurança defensiva do FC 26: linha de 5 defensiva e linha de 4 intermediária.",
                "p": "Praticamente impossível de ser penetrada por jogadas normais de toque de bola.",
                "c": "Zero presença ofensiva; o time inteiro abdica de atacar.",
                "b": "Tenha paciência extrema na circulação de bola, explore chutes colocados de longa distância e o recurso de cruzamentos na área para forçar erros defensivos."
            }
        }
    }

    # 1. SELETOR DE FORMAÇÃO
    formacao_selecionada = st.selectbox(
        "1. Escolha a Formação Tática:",
        list(matrizMatriz.keys()),
        index=0
    )

    # Recupera os presets disponíveis para a formação escolhida
    presets_disponiveis = list(matrizMatriz[formacao_selecionada].keys())

    # 2. SELETOR DE TACTICAL PRESET (Posicionado abaixo do seletor de formação)
    preset_selecionado_key = st.selectbox(
        "2. Escolha o Tactical Preset:",
        presets_disponiveis,
        format_func=lambda key: preset_labels.get(key, key),
        index=0
    )

    # Carrega dados específicos baseados no preset selecionado
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

    # Seção inferior formatada em 3 cards
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>01 / ESTRUTURA</span>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>{formacao_selecionada}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ff4b4b; font-size: 13px; font-weight: bold; margin-top: -5px;'>Preset: {preset_labels.get(preset_selecionado_key, preset_selecionado_key)}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ccc; font-size: 12px; min-height: 48px;'>{dados['d']}</p>", unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>02 / DESEMPENHO</span>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>Prós & Contras</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 13px; font-weight: bold; margin-top: -5px;'>Pontos Chave</p>", unsafe_allow_html=True)
            
            with st.expander("Expandir Vantagens e Desvantagens", expanded=True):
                st.markdown("**🟢 Vantagens:**")
                st.markdown(f"- {dados['p']}")
                
                st.divider()
                
                st.markdown("**🔴 Desvantagens:**")
                st.markdown(f"- {dados['c']}")

    with c3:
        with st.container(border=True):
            st.markdown("<span style='color: #888; font-family: monospace; font-size: 13px;'>03 / ESTRATÉGIA</span>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin: 0; padding: 2px 0; font-size: 22px;'>Como Anular</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888; font-size: 13px; font-weight: bold; margin-top: -5px;'>How to Counter</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #ccc; font-size: 12px; min-height: 48px;'>{dados['b']}</p>", unsafe_allow_html=True)
