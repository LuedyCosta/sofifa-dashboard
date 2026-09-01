# Arquivo: app.py
import streamlit as st
import pandas as pd  # Corrige o NameError da página Perfil Detalhado
import streamlit.components.v1 as components  # Necessário para renderizar o painel tático
from painel_tatico import renderizar_painel_tatico # Importa o seu novo módulo

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SoFIFA & FC26 Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fundo Totalmente Preto */
    .stApp, .stApp > header {
        background-color: #000000;
        color: #ffffff;
    }

    /* Textos Fixos Brancos */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p, .stMarkdown span, div[data-baseweb="typography"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Expander e Checkboxes Textos Brancos */
    .streamlit-expanderHeader { color: #ffffff !important; }
    .stCheckbox label { color: #ffffff !important; }

    /* Classe para Textos Variáveis (Dinâmicos) em Verde */
    .var-text {
        color: #10b981 !important; /* Verde 500 */
        font-weight: bold;
    }

    .stCaption, small, .caption-text {
        color: #a3a3a3 !important;
    }

    /* Estilização Customizada de Botões Globais */
    div[data-testid="stButton"] button {
        background-color: #808080 !important; /* Cinza 50% */
        color: #ffffff !important;
        border: none !important;
        white-space: nowrap !important; /* Força 1 linha */
        height: 38px !important;
        min-height: 38px !important;
        padding: 0px 16px !important;
        margin-top: 5px !important;
        border-radius: 6px !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #a3a3a3 !important;
        border: none !important;
        color: #ffffff !important;
    }
    div[data-testid="stButton"] button p {
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }

    /* Badges de Atributos do FIFA */
    .stat-box {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
    }
    .stat-badge {
        width: 34px;
        height: 25px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85rem;
        color: #ffffff !important;
        margin-right: 8px;
    }
    .stat-green { background-color: #10b981; }
    .stat-yellow { background-color: #f59e0b; }
    .stat-red { background-color: #ef4444; }
    .stat-label {
        color: #ffffff !important;
        font-size: 0.95rem;
    }

    /* Card do Perfil do Jogador */
    .profile-info-box {
        background-color: #111111;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #333333;
        margin-bottom: 20px;
    }

    /* Container de Jogadores Parecidos */
    .similar-container {
        background-color: #000000;
        border: 1px dashed #333333;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: -15px;
        margin-bottom: 15px;
    }
    .similar-card {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        height: 100%;
    }
    .similar-name {
        color: #10b981 !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        margin-bottom: 2px;
    }
    .similar-meta {
        font-size: 0.8rem;
        color: #ffffff !important;
    }
    
    /* Cards de Conteúdo Tático */
    .tactical-card {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MAPEAMENTO DOS GRUPOS E DADOS TÁTICOS
# -----------------------------------------------------------------------------
STAT_GROUPS = {
    'Ofensivo': {
        'Cruzamento': 'Crossing',
        'Finalização': 'Finishing',
        'Prec. Cabeceio': 'Heading Accuracy',
        'Passe curto': 'Short Passing',
        'Voleios': 'Volleys'
    },
    'Habilidade': {
        'Dribles': 'Dribbling',
        'Curva': 'Curve',
        'Prec. faltas': 'Free Kick Accuracy',
        'Lançamento': 'Long Passing',
        'Controle bola': 'Ball Control'
    },
    'Movimentação': {
        'Aceleração': 'Acceleration',
        'Pique': 'Sprint Speed',
        'Agilidade': 'Agility',
        'Reação': 'Reactions',
        'Equilíbrio': 'Balance'
    },
    'Força': {
        'Força chute': 'Shot Power',
        'Impulsão': 'Jumping',
        'Fôlego': 'Stamina',
        'Força': 'Strength',
        'Chutes longe': 'Long Shots'
    },
    'Mentalidade': {
        'Combatividade': 'Aggression',
        'Intercept.': 'Interceptions',
        'Pos. ataque': 'Positioning',
        'Visão de jogo': 'Vision',
        'Pênaltis': 'Penalties',
        'Compostura': 'Composure'
    },
    'Defesa': {
        'Hab. defensiva': 'Def Awareness',
        'Dividida pé': 'Standing Tackle',
        'Carrinho': 'Sliding Tackle'
    },
    'Atributos GL': {
        'Elasticidade GL': 'GK Diving',
        'Manejo GL': 'GK Handling',
        'Chute GL': 'GK Kicking',
        'Posicion. GL': 'GK Positioning',
        'Reflexos GL': 'GK Reflexes'
    }
}

# Base de Conhecimento Tático Baseada no PDF Analítico do FC26
TACTICAL_DATABASE = {
    "3-1-4-2": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "O time usa a superioridade numérica central gerada pelos 4 meias e 2 atacantes para manter a posse curta, atraindo a pressão do adversário para o miolo do campo.",
        "pros": "Triangulações constantes, extrema facilidade para manter a posse e envolver defesas fechadas.",
        "cons": "Vulnerável a pressões sufocantes nas laterais, já que os alas precisam dar toda a largura sozinhos.",
        "counter": "Feche o centro com um 4-2-3-1 compacto e force o adversário a tocar a bola para os alas, anulando a progressão pelo meio.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "CDM", "x": 50, "y": 40},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CM", "x": 38, "y": 52}, {"pos": "CM", "x": 62, "y": 52}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "ST", "x": 40, "y": 85}, {"pos": "ST", "x": 60, "y": 85}
        ]
    },
    "3-4-1-2": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Assim que a bola é recuperada pelos 3 zagueiros ou pelo ala, a equipe dispara em transição vertical fulminante em direção aos dois centroavantes e ao CAM.",
        "pros": "Rapidez impressionante na transição ofensiva, gerando situações de superioridade numérica no ataque antes da defesa voltar.",
        "cons": "Deixa buracos imensos no meio-campo caso o contra-ataque inicial seja interceptado.",
        "counter": "Adote uma postura defensiva equilibrada e recue os volantes para cobrir o espaço vazio deixado nas costas dos alas adversários.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 52}, {"pos": "CM", "x": 38, "y": 48}, {"pos": "CM", "x": 62, "y": 48}, {"pos": "RM", "x": 85, "y": 52},
            {"pos": "CAM", "x": 50, "y": 70},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "3-4-2-1": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Os dois meias ofensivos (CFs) flutuam inteligentemente enquanto a equipe alterna entre manter a posse e buscar o espaço vazio de forma natural.",
        "pros": "Grande imprevisibilidade ofensiva e excelente ocupação da entrelinha adversária.",
        "cons": "Exige alto vigor físico dos alas e pode sofrer defensivamente contra pontas velozes.",
        "counter": "Use laterais e pontas abertos (como em um 4-3-3) para esticar a linha defensiva de 3 zagueiros pelos lados.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 52}, {"pos": "CM", "x": 38, "y": 48}, {"pos": "CM", "x": 62, "y": 48}, {"pos": "RM", "x": 85, "y": 52},
            {"pos": "CF", "x": 35, "y": 78}, {"pos": "CF", "x": 65, "y": 78},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "3-4-3": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Os pontas abertos ficam esticados no campo defensivo rival esperando o lançamento longo ou a enfiada de bola rápida após o roubo.",
        "pros": "Potencial letal em contra-ataques verticais com pontas disparando em velocidade máxima.",
        "cons": "Meio-campo extremamente vulnerável ao controle de posse de adversários organizados.",
        "counter": "Tenha volantes com instruções de cobertura defensiva rigorosa e não suba os dois laterais ao mesmo tempo.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 52}, {"pos": "CM", "x": 38, "y": 48}, {"pos": "CM", "x": 62, "y": 48}, {"pos": "RM", "x": 85, "y": 52},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "3-4-3 Diamond": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Variação do 3-4-3 com meias em formato de losango no centro e pontas agudos no ataque.",
        "pros": "Excelente equilíbrio entre largura nas pontas e transição rápida central.",
        "cons": "Espaço considerável nas costas dos alas quando a pressão é quebrada.",
        "counter": "Domine o meio-campo com superioridade numérica e bloqueie os corredores laterais.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "CDM", "x": 50, "y": 38}, {"pos": "LM", "x": 15, "y": 55}, {"pos": "RM", "x": 85, "y": 55}, {"pos": "CAM", "x": 50, "y": 68},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 92}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "3-4-3 Flat": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Linha tradicional de 4 meias planos com 3 atacantes abertos.",
        "pros": "Amplitude máxima e chegada rápida ao terço final.",
        "cons": "Menor densidade central defensiva.",
        "counter": "Feche as linhas com um bloco compacto e use volantes focados em interceptação.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 52}, {"pos": "CM", "x": 38, "y": 50}, {"pos": "CM", "x": 62, "y": 50}, {"pos": "RM", "x": 85, "y": 52},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "3-5-1-1": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Foco absoluto em dominar o ritmo da partida através da circulação de bola no miolo de campo com 5 meio-campistas.",
        "pros": "Controle territorial impecável e baixa incidência de erros de passe não forçados.",
        "cons": "O único centroavante pode ficar isolado se o adversário fechar bem a entrada da área.",
        "counter": "Mantenha uma linha defensiva compacta e não dê espaço para o segundo atacante (CF/CAM) girar na intermediária.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 52}, {"pos": "CM", "x": 35, "y": 48}, {"pos": "CDM", "x": 50, "y": 38}, {"pos": "CM", "x": 65, "y": 48}, {"pos": "RM", "x": 85, "y": 52},
            {"pos": "CF", "x": 50, "y": 75},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "3-5-2": {
        "default_style": "Balanced (Equilibrado)",
        "info": "O esquema clássico de 3 zagueiros com dupla de ataque que equilibra transições e construção de jogadas de forma orgânica.",
        "pros": "Solidez central e presença constante de gente tanto no meio quanto na área adversária.",
        "cons": "As costas dos alas são corredores livres para pontas rápidos do adversário.",
        "counter": "Explore os flancos com alas ou pontas velozes para forçar os zagueiros laterais a saírem da linha de 3.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "CB", "x": 30, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 70, "y": 22},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CDM", "x": 40, "y": 42}, {"pos": "CDM", "x": 60, "y": 42}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "CAM", "x": 50, "y": 68},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-1-2-1-2 Narrow": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "O famoso 'losango fechado' potencializado pelo toque curto, criando uma teia de passes na zona central do campo.",
        "pros": "Domínio absoluto do centro e tabelas mortais entre o CAM e a dupla de atacantes.",
        "cons": "Totalmente nulo nas extremidades do campo; sofre demais com jogadas de linha de fundo.",
        "counter": "Jogue com uma formação aberta (como 4-3-3 Wide ou 4-4-2) e explore os corredores laterais onde o adversário não tem jogadores de origem.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "CM", "x": 35, "y": 52}, {"pos": "CM", "x": 65, "y": 52},
            {"pos": "CAM", "x": 50, "y": 70},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-1-2-1-2 Wide": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Corrige a falta de largura do losango fechado adicionando meias abertos que participam da construção equilibrada.",
        "pros": "Mantém a força central do losango com maior proteção e opções de cruzamento pelas pontas.",
        "cons": "Exige que os meias laterais tenham estamina infinita para fechar por dentro e cobrir as pontas.",
        "counter": "Asfixie o único volante defensivo do adversário com dois meias centrais, cortando a conexão entre a defesa e o CAM.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "LM", "x": 15, "y": 58}, {"pos": "RM", "x": 85, "y": 58},
            {"pos": "CAM", "x": 50, "y": 70},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-1-3-2": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Uma linha de 3 meias compacta que recupera a bola e aciona imediatamente os dois atacantes em velocidade vertiginosa.",
        "pros": "Transições ofensivas diretas, pegando o adversário desorganizado no campo de ataque.",
        "cons": "O único volante pode ser facilmente superado por tabelas rápidas pelo centro.",
        "counter": "Use um meio-campo com superioridade numérica central (como 4-3-3 Holding) para neutralizar a linha de 3 armadores.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "LM", "x": 20, "y": 58}, {"pos": "CAM", "x": 50, "y": 62}, {"pos": "RM", "x": 80, "y": 58},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-1-4-1": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Bloco defensivo ultra-compacto de 4 homens no meio com foco em posse de bola paciente e segura.",
        "pros": "Impossível de ser infiltrado pelo centro; excelente para segurar resultados.",
        "cons": "Extrema falta de presença de jogadores na área adversária (apenas 1 atacante).",
        "counter": "Avance sua linha defensiva e pressione a saída de bola para forçar o erro do único volante adversário.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "LM", "x": 15, "y": 60}, {"pos": "CM", "x": 38, "y": 55}, {"pos": "CM", "x": 62, "y": 55}, {"pos": "RM", "x": 85, "y": 60},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-2-1-3": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Duplo pivô seguro na base e um trio de frente dinâmico conectado por um CAM criativo.",
        "pros": "Equilíbrio perfeito entre solidez defensiva e poder de fogo nas pontas.",
        "cons": "Se o CAM se desgastar, o time perde o elo de ligação com o centroavante.",
        "counter": "Monitore rigorosamente os movimentos do CAM adversário e feche as diagonais dos pontas com os laterais.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 38, "y": 42}, {"pos": "CDM", "x": 62, "y": 42},
            {"pos": "CAM", "x": 50, "y": 65},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-2-2-2": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Os dois meias ofensivos fechados e os dois atacantes disparam em contra-ataques fulminantes apoiados pelo duplo pivô.",
        "pros": "Perigoso em transições rápidas e muito seguro defensivamente pelo miolo central.",
        "cons": "Jogo previsível e fechado se o adversário optar por se retrancar.",
        "counter": "Jogue com laterais bem postados e evite perder a bola no campo ofensivo sem cobertura na retaguarda.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 38, "y": 42}, {"pos": "CDM", "x": 62, "y": 42},
            {"pos": "CAM", "x": 35, "y": 68}, {"pos": "CAM", "x": 65, "y": 68},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-2-3-1 Narrow": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "O ápice do controle de jogo tático: posse de bola paciente, circulação segura pelo duplo pivô e construção metódica.",
        "pros": "Controle total do ritmo da partida, baixíssimo índice de exposição defensiva.",
        "cons": "Pode se tornar enfadonho ou estéril se o adversário fechar todas as linhas de passe na entrada da área.",
        "counter": "Mantenha linhas muito baixas e compactas (bloco baixo), impedindo infiltrações e apostando em roubadas de bola para contra-atacar.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 38, "y": 42}, {"pos": "CDM", "x": 62, "y": 42},
            {"pos": "LAM", "x": 25, "y": 70}, {"pos": "CAM", "x": 50, "y": 72}, {"pos": "RAM", "x": 75, "y": 70},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-2-3-1 Wide": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Variação do 4-2-3-1 com alas de origem aberta pelas pontas ao invés de meias ofensivos centralizados.",
        "pros": "Melhor cobertura das pontas defensivas e ofensivas mantendo a solidez do duplo pivô.",
        "cons": "Menor densidade central comparado à versão Narrow.",
        "counter": "Controle o centro do campo com um trio de meias e explore a lentidão na transição dos pontas adversários.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 38, "y": 42}, {"pos": "CDM", "x": 62, "y": 42},
            {"pos": "LM", "x": 15, "y": 70}, {"pos": "CAM", "x": 50, "y": 70}, {"pos": "RM", "x": 85, "y": 70},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-2-4": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "O estilo kamikaze do jogo: quatro homens fixos no ataque esperando o bote para acelerar ao máximo rumo ao gol.",
        "pros": "Sufoca a saída de bola do adversário e gera muitas chances claras de gol rapidamente.",
        "cons": "O meio-campo fica totalmente despovoado, facilitando o domínio total do rival no setor.",
        "counter": "Simplesmente controle a posse de bola no meio-campo com uma formação densa (como 4-3-3 Holding ou 3-5-2); o adversário correrá atrás da bola e se desgastará.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CM", "x": 38, "y": 48}, {"pos": "CM", "x": 62, "y": 48},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 40, "y": 90}, {"pos": "ST", "x": 60, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-3-1-2": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Triangulações incessantes por dentro com foco em envolver a zaga rival através de passes curtos e infiltrações do CAM.",
        "pros": "Envolvimento técnico excelente e superioridade no terço final central.",
        "cons": "Totalmente vulnerável a equipes que atacam pelas pontas.",
        "counter": "Explore os corredores laterais com pontas rápidos e cruzamentos para a área.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CM", "x": 30, "y": 48}, {"pos": "CDM", "x": 50, "y": 40}, {"pos": "CM", "x": 70, "y": 48},
            {"pos": "CAM", "x": 50, "y": 68},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-3-2-1": {
        "default_style": "Balanced (Equilibrado)",
        "info": "A formação meta por excelência, combinando os dois CFs e o ST em uma movimentação fluida e equilibrada.",
        "pros": "Quebra qualquer linha defensiva com tabelas rápidas e infiltrações surpresa pelo meio-espaço.",
        "cons": "Exige mecânicas manuais refinadas e posicionamento impecável dos laterais.",
        "counter": "Utilize marcação por zona rigorosa com volantes focados em cortar a linha de passe para os dois meias avançados.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CM", "x": 28, "y": 48}, {"pos": "CM", "x": 50, "y": 42}, {"pos": "CM", "x": 72, "y": 48},
            {"pos": "CF", "x": 35, "y": 75}, {"pos": "CF", "x": 65, "y": 75},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-3-3 Flat": {
        "default_style": "Balanced (Equilibrado)",
        "info": "A base do futebol mundial adaptada ao FC 26, focando em largura com pontas e solidez de trio de meio plano.",
        "pros": "Geometria perfeita de campo, oferecendo opções de passes curtos e compridos em todas as direções.",
        "cons": "Se o estilo for rígido demais, perde flexibilidade contra esquemas superpopulosos no meio.",
        "counter": "Espelhe a formação ou utilize um 4-2-3-1 para neutralizar os criadores de jogadas no setor central.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CM", "x": 30, "y": 48}, {"pos": "CM", "x": 50, "y": 45}, {"pos": "CM", "x": 70, "y": 48},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-3-3 Holding": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Variação defensiva do 4-3-3 com um volante fixo protegendo a zaga e dois meias interiores armando o jogo.",
        "pros": "Excelente equilíbrio na transição defensiva e proteção contra contra-ataques.",
        "cons": "Pode pecar em volume ofensivo caso os meias interiores não avancem com frequência.",
        "counter": "Pressione a saída de bola do volante central e mantenha a linha defensiva concentrada.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "CM", "x": 35, "y": 55}, {"pos": "CM", "x": 65, "y": 55},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-3-3 Defend": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Possui dois volantes na base do meio-campo e um meia central avançado.",
        "pros": "Muro defensivo formidável sem perder o poder de fogo dos pontas.",
        "cons": "Pouca criatividade caso o único meia central seja neutralizado.",
        "counter": "Feche os espaços centrais e deixe o adversário circular a bola sem perigo nas alas.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 38, "y": 42}, {"pos": "CDM", "x": 62, "y": 42},
            {"pos": "CM", "x": 50, "y": 58},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-3-3 Attack": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Possui um volante e dois meias ofensivos (CAMs) logo atrás do trio de ataque.",
        "pros": "Poder ofensivo avassalador com muitos jogadores chegando na área.",
        "cons": "Extremamente vulnerável a contra-ataques rápidos nas costas dos meias.",
        "counter": "Atacar com velocidade pelos espaços deixados pelos meias ofensivos ao subirem.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CDM", "x": 50, "y": 38},
            {"pos": "CAM", "x": 35, "y": 62}, {"pos": "CAM", "x": 65, "y": 62},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-3-3 False 9": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "O centroavante recua para armar o jogo, criando caos na linha defensiva adversária.",
        "pros": "Imprevisibilidade total na movimentação do ataque e superioridade no meio.",
        "cons": "Falta um homem de referência fixa dentro da pequena área.",
        "counter": "Não siga o centroavante quando ele recuar; mantenha a linha de zaga firme e compacta.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "CM", "x": 30, "y": 48}, {"pos": "CM", "x": 50, "y": 42}, {"pos": "CM", "x": 70, "y": 48},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "CF", "x": 50, "y": 72}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "4-4-1-1 Attack": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Duas linhas de 4 sólidas com um segundo atacante (CF) muito ativo logo atrás do centroavante.",
        "pros": "Excelente organização defensiva com ótima ocupação de espaços.",
        "cons": "Pode faltar profundidade caso os pontas/meias laterais não acompanhem.",
        "counter": "Utilize meias criativos que flutuem entre as duas linhas de 4.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CM", "x": 38, "y": 50}, {"pos": "CM", "x": 62, "y": 50}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "CF", "x": 50, "y": 75},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-4-1-1 Midfield": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Variação voltada para a contenção e posse no meio-campo com o segundo atacante mais recuado.",
        "pros": "Controle absoluto do ritmo e consistência defensiva alta.",
        "cons": "Transição ofensiva mais lenta e dependente de lampejos.",
        "counter": "Acelere o ritmo da partida e force erros na saída de bola.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CM", "x": 38, "y": 50}, {"pos": "CM", "x": 62, "y": 50}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "CAM", "x": 50, "y": 70},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-4-2 Flat": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Duas linhas de quatro compactas aliadas a uma dupla de ataque clássica, priorizando transições organizadas e solidez.",
        "pros": "Altamente intuitiva, segura e excelente para manter o bloco defensivo uníssono.",
        "cons": "Pode sofrer contra o toque de bola refinado de equipes com 3 ou mais meias centrais.",
        "counter": "Supere o meio-campo adversário utilizando jogadores que saibam flutuar entre as linhas (como um CAM ágil).",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CM", "x": 38, "y": 52}, {"pos": "CM", "x": 62, "y": 52}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-4-2 Holding": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Variação da linha de 4 com maior foco na proteção defensiva central dos meias centrais.",
        "pros": "Maior contenção de jogadas pelo meio mantendo o esquema clássico de dois atacantes.",
        "cons": "Menor liberdade criativa para os meias centrais.",
        "counter": "Explore as laterais com ultrapassagens rápidas.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CDM", "x": 38, "y": 48}, {"pos": "CDM", "x": 62, "y": 48}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "4-5-1 Attack": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Retenção máxima de bola com 5 homens no meio-campo, sufocando o adversário pela posse prolongada.",
        "pros": "Impossível de roubar a bola facilmente se o jogador souber trocar passes com paciência.",
        "cons": "Lentidão crônica nas transições ofensivas e isolamento do centroavante.",
        "counter": "Mantenha a calma, não dê botes precipitados na intermediária e aguarde o erro de aproximação do adversário.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 58}, {"pos": "CAM", "x": 35, "y": 62}, {"pos": "CDM", "x": 50, "y": 42}, {"pos": "CAM", "x": 65, "y": 62}, {"pos": "RM", "x": 85, "y": 58},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "4-5-1 Flat": {
        "default_style": "Short Passing (Toque Curto)",
        "info": "Linha compacta de 5 meias planos com 1 atacante isolado.",
        "pros": "Densidade defensiva intransponível no setor intermediário.",
        "cons": "Pouquíssima presença na área rival.",
        "counter": "Avance as linhas e force cruzamentos de longa distância.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LB", "x": 15, "y": 25}, {"pos": "CB", "x": 38, "y": 20}, {"pos": "CB", "x": 62, "y": 20}, {"pos": "RB", "x": 85, "y": 25},
            {"pos": "LM", "x": 15, "y": 55}, {"pos": "CM", "x": 32, "y": 52}, {"pos": "CM", "x": 50, "y": 50}, {"pos": "CM", "x": 68, "y": 52}, {"pos": "RM", "x": 85, "y": 55},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "5-1-2-2": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Sistemas defensivos pesados focados em fechar completamente a própria área e disparar em contra-ataques rápidos com os alas e atacantes.",
        "pros": "Linha defensiva praticamente intransponível por bolas enfiadas terrestres; solidez extrema.",
        "cons": "Ofensivamente pobres se jogados estritamente na retranca; podem sofrer com chutes de longa distância.",
        "counter": "Arrisque chutes de fora da área com jogadores que possuem PlayStyles adequados, utilize cruzamentos na medida e mantenha a paciência.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CDM", "x": 50, "y": 42},
            {"pos": "CM", "x": 38, "y": 58}, {"pos": "CM", "x": 62, "y": 58},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "5-2-1-2": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Linha de 5 defensiva com duplo pivô e um CAM articulando o jogo para a dupla de ataque.",
        "pros": "Segurança defensiva impecável com ótima ligação central.",
        "cons": "Exige alas com muita capacidade física para apoiar o ataque e voltar.",
        "counter": "Pressione a saída pelos flancos e obrigue os alas a se defenderem o tempo todo.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CDM", "x": 38, "y": 45}, {"pos": "CDM", "x": 62, "y": 45},
            {"pos": "CAM", "x": 50, "y": 68},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "5-2-2-1": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Linha de 5 com dois alas, dois meias centrais e um trio de ataque rápido.",
        "pros": "Contra-ataques mortais com pontas e ala disparando em velocidade.",
        "cons": "Meio-campo pode sofrer contra equipes que dominam a posse.",
        "counter": "Mantenha posse paciente e não perca a bola no campo de ataque sem cobertura.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CM", "x": 38, "y": 50}, {"pos": "CM", "x": 62, "y": 50},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "5-2-3": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Formação ultra defensiva com trio ofensivo fixo nas pontas.",
        "pros": "Três atacantes sempre prontos para puxar o contra-ataque em velocidade.",
        "cons": "Buraco criativo no meio-campo entre a defesa e o ataque.",
        "counter": "Domine o meio-campo com superioridade numérica absoluta.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CM", "x": 38, "y": 48}, {"pos": "CM", "x": 62, "y": 48},
            {"pos": "LW", "x": 20, "y": 85}, {"pos": "ST", "x": 50, "y": 90}, {"pos": "RW", "x": 80, "y": 85}
        ]
    },
    "5-3-2": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Linha defensiva de 5 encorpada com trio de meio-campo e dupla de ataque.",
        "pros": "Solidez defensiva máxima sem abdicar de ter duas referências na frente.",
        "cons": "Pouca criatividade nas pontas sem alas muito dinâmicos.",
        "counter": "Explore as costas dos alas defensivos com pontas velozes.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CM", "x": 30, "y": 52}, {"pos": "CDM", "x": 50, "y": 45}, {"pos": "CM", "x": 70, "y": 52},
            {"pos": "ST", "x": 40, "y": 88}, {"pos": "ST", "x": 60, "y": 88}
        ]
    },
    "5-4-1 Flat": {
        "default_style": "Counter (Contra-Ataque)",
        "info": "Retranca clássica com duas linhas de 4 e 5 muito compactas e um atacante isolado.",
        "pros": "Quase impossível de ser penetrada pelo centro.",
        "cons": "Nenhum poder ofensivo real sem contra-ataques encaixados.",
        "counter": "Chutes de longa distância, paciência e cruzamentos altos.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "LM", "x": 15, "y": 58}, {"pos": "CM", "x": 38, "y": 55}, {"pos": "CM", "x": 62, "y": 55}, {"pos": "RM", "x": 85, "y": 58},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    },
    "5-4-1 Diamond": {
        "default_style": "Balanced (Equilibrado)",
        "info": "Variação da linha de 5 com meio-campo em formato losango compactado.",
        "pros": "Proteção lateral e central equilibrada com apoio no ataque.",
        "cons": "Exige extremo rigor tático para não abrir espaços.",
        "counter": "Inverta o jogo rapidamente de um lado para o outro para cansar a defesa.",
        "coords": [
            {"pos": "GK", "x": 50, "y": 5},
            {"pos": "LWB", "x": 10, "y": 38}, {"pos": "CB", "x": 28, "y": 22}, {"pos": "CB", "x": 50, "y": 20}, {"pos": "CB", "x": 72, "y": 22}, {"pos": "RWB", "x": 90, "y": 38},
            {"pos": "CDM", "x": 50, "y": 42}, {"pos": "LM", "x": 20, "y": 58}, {"pos": "RM", "x": 80, "y": 58}, {"pos": "CAM", "x": 50, "y": 70},
            {"pos": "ST", "x": 50, "y": 90}
        ]
    }
}

# -----------------------------------------------------------------------------
# 3. LEITURA DOS DADOS E ALGORITMO DE SIMILARIDADE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("EAFC26.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("sofifa_players_2.csv")
        except FileNotFoundError:
            try:
                df = pd.read_csv("sofifa_players.csv")
            except FileNotFoundError:
                st.error("❌ Arquivo EAFC26.csv não encontrado.")
                st.stop()

    df['Name'] = df['Name'].fillna('Jogador Sem Nome').astype(str)
    df['Team'] = df['Team'].fillna('Sem Clube').astype(str)
    df['Position'] = df['Position'].fillna('N/A').astype(str)
    df['League'] = df['League'].fillna('Desconhecida').astype(str)
    df['GENDER'] = df['GENDER'].fillna('M').astype(str)
    df['Preferred foot'] = df['Preferred foot'].fillna('Right').astype(str)
    
    for col in ['OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Age', 'Weak foot', 'Skill moves']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    return df

df_raw = load_data()

def get_val(player_row, col_name, default=50):
    if col_name in player_row.index and pd.notna(player_row[col_name]):
        val = pd.to_numeric(player_row[col_name], errors='coerce')
        if not pd.isna(val):
            return int(val)
    return int(default)

def render_stat_item(label, value):
    val_int = int(value) if str(value).isdigit() else 50
    badge_class = "stat-green" if val_int >= 70 else ("stat-yellow" if val_int >= 60 else "stat-red")
    return f"""
    <div class="stat-box">
        <span class="stat-badge {badge_class}">{val_int}</span>
        <span class="stat-label">{label}</span>
    </div>
    """

def find_similar_players(df, target_player, top_n=3, regens_only=False):
    gender = target_player.get('GENDER', 'M')
    cond = (df['GENDER'] == gender) & (df['Name'] != target_player['Name'])
    
    if regens_only:
        cond = cond & (df['Age'] <= 23)
        
    candidates = df[cond].copy()
    if candidates.empty:
        return candidates

    stat_cols = ['OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Age']
    target_vec = np.array([get_val(target_player, col, 50) for col in stat_cols], dtype=float)
    cand_vecs = candidates[stat_cols].apply(pd.to_numeric, errors='coerce').fillna(50).to_numpy(dtype=float)

    std_vec = np.array(df[stat_cols].apply(pd.to_numeric, errors='coerce').std().values, dtype=float)
    std_vec = np.where((np.isnan(std_vec)) | (std_vec == 0), 1.0, std_vec)

    dist = np.linalg.norm((cand_vecs - target_vec) / std_vec, axis=1)
    target_pos = str(target_player['Position'])
    pos_penalty = np.where(candidates['Position'] == target_pos, 0.0, 1.2)

    try:
        t_styles = set(ast.literal_eval(str(target_player.get('play style', '[]'))))
    except:
        t_styles = set()

    def style_dist(style_str):
        try:
            s_set = set(ast.literal_eval(str(style_str)))
            if not t_styles and not s_set:
                return 0.0
            union = len(t_styles.union(s_set))
            return 1.0 - (len(t_styles.intersection(s_set)) / union) if union > 0 else 1.0
        except:
            return 1.0

    style_penalties = candidates['play style'].apply(style_dist).to_numpy(dtype=float) * 1.0
    candidates['similarity_score'] = dist + pos_penalty + style_penalties
    return candidates.sort_values('similarity_score').head(top_n)

# -----------------------------------------------------------------------------
# 4. BARRA LATERAL E NAVEGAÇÃO ENTRE PÁGINAS
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard FC26")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")

page_selection = st.sidebar.radio("Ir para:", ["Perfil Detalhado", "Formações"])

df = df_raw.copy()

# -----------------------------------------------------------------------------
# 5. PÁGINA 1: PERFIL DETALHADO
# -----------------------------------------------------------------------------
if page_selection == "Perfil Detalhado":
    st.title("👤 Perfil Detalhado")

    col_quem, _ = st.columns([1, 2])
    player_list = sorted(df['Name'].unique().tolist())
    default_index = player_list.index("Bradley Barcola") if "Bradley Barcola" in player_list else 0

    with col_quem:
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list, index=default_index)

    p = df[df['Name'] == target_player_name].iloc[0]

    play_styles_raw = str(p.get('play style', '[]'))
    try:
        play_styles = ast.literal_eval(play_styles_raw)
        if not isinstance(play_styles, list):
            play_styles = []
    except:
        play_styles = []

    perna_boa = "Esq." if p.get('Preferred foot', 'Right') == 'Left' else "Dir."
    fintas = p.get('Skill moves', 2)
    perna_ruim = p.get('Weak foot', 2)
    rep_int = p.get('Rank', 1)

    c_face, c_info, c_details = st.columns([1.2, 2.5, 3.3])

    # Exemplo de verificação segura para a foto/card do jogador:
player_df = df[df["Name"] == selected_player]

    # 2. Garanta que esta linha 'if' tenha exatamente o mesmo recuo da linha acima
    if not player_df.empty:
        player_data = player_df.iloc[0]

        # Busca da imagem do jogador
        card_img = None
        if "card_img" in player_data and pd.notna(player_data["card_img"]):
            card_img = player_data["card_img"]
        elif "Photo" in player_data and pd.notna(player_data["Photo"]):
            card_img = player_data["Photo"]

        if card_img and str(card_img).startswith("http"):
            st.image(card_img)

    with c_info:
        st.markdown(f"<h2>🏃 <span class='var-text'>{p['Name']}</span></h2>", unsafe_allow_html=True)
        st.markdown(f"**Clube:** <span class='var-text'>{p['Team']}</span> ({p['League']})", unsafe_allow_html=True)
        st.markdown(f"**Posição:** <span style='background-color: #262626; color: #10b981; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['Position']}</span> | **Nacionalidade:** <span class='var-text'>{p.get('Nation', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall:** <span style='background-color: #262626; color: #10b981; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['OVR']}</span> | **Idade:** <span class='var-text'>{p['Age']} anos</span>", unsafe_allow_html=True)

    with c_details:
        st.markdown(f"""
        <div class="profile-info-box">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong style="color:#ffffff;">Perfil</strong><br>
                    <span>Perna boa: <b class="var-text">{perna_boa}</b></span><br>
                    <span><b class="var-text">{fintas} ★</b> Fintas</span><br>
                    <span><b class="var-text">{perna_ruim} ★</b> Perna ruim</span><br>
                    <span>Rank: <b class="var-text">#{rep_int}</b></span>
                </div>
                <div>
                    <strong style="color:#ffffff;">Atributos Globais</strong><br>
                    <span>PAC: <b class="var-text">{p.get('PAC', 0)}</b></span> | 
                    <span>SHO: <b class="var-text">{p.get('SHO', 0)}</b></span><br>
                    <span>PAS: <b class="var-text">{p.get('PAS', 0)}</b></span> | 
                    <span>DRI: <b class="var-text">{p.get('DRI', 0)}</b></span><br>
                    <span>DEF: <b class="var-text">{p.get('DEF', 0)}</b></span> | 
                    <span>PHY: <b class="var-text">{p.get('PHY', 0)}</b></span>
                </div>
                <div>
                    <strong style="color:#ffffff;">Clube</strong><br>
                    <span><b class="var-text">{p['Team']}</b></span><br>
                    <span>Posição <b class="var-text">{p['Position']}</b></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_sim_title, col_btn_todos, col_btn_regen = st.columns([1.5, 0.6, 0.6])
    with col_sim_title:
        st.markdown("### 👥 Jogadores Parecidos")

    if "sim_filter_mode" not in st.session_state:
        st.session_state["sim_filter_mode"] = "Todos"

    with col_btn_todos:
        if st.button("Todos", use_container_width=True):
            st.session_state["sim_filter_mode"] = "Todos"
    with col_btn_regen:
        if st.button("Regen", use_container_width=True):
            st.session_state["sim_filter_mode"] = "Regen"

    is_regens = (st.session_state["sim_filter_mode"] == "Regen")
    similar_df = find_similar_players(df, p, top_n=3, regens_only=is_regens)

    sim_cols = st.columns(3)
    if not similar_df.empty:
        for idx, (_, sim_p) in enumerate(similar_df.iterrows()):
            with sim_cols[idx]:
                try:
                    s_list = ast.literal_eval(str(sim_p.get('play style', '[]')))
                    styles_txt = ", ".join(s_list[:2]) if s_list else "Padrão"
                except:
                    styles_txt = "Padrão"

                st.markdown(f"""
                <div class="similar-card">
                    <div class="similar-name">⚽ {sim_p['Name']}</div>
                    <div class="similar-meta">
                        <b>Pos:</b> <span class="var-text">{sim_p['Position']}</span> | <b>Idade:</b> <span class="var-text">{sim_p['Age']} yrs</span><br>
                        <b>OVR:</b> <span class="var-text">{sim_p['OVR']}</span> | <b>Clube:</b> <span class="var-text">{sim_p['Team']}</span><br>
                        <span style="color:#a3a3a3; font-size:0.75rem;">Estilo: <span class="var-text">{styles_txt}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum jogador semelhante encontrado com esses critérios.")

    st.markdown("---")

    all_stat_keys = []
    for g_name, g_stats in STAT_GROUPS.items():
        for stat_label in g_stats.keys():
            all_stat_keys.append(f"chk_{g_name}_{stat_label}")

    def select_all_stats():
        for k in all_stat_keys:
            st.session_state[k] = True

    def deselect_all_stats():
        for k in all_stat_keys:
            st.session_state[k] = False

    POSITION_SUGGESTIONS = {
        'ST': ['Finalização', 'Pos. ataque', 'Aceleração', 'Pique', 'Força chute', 'Compostura'],
        'CF': ['Finalização', 'Dribles', 'Controle bola', 'Visão de jogo', 'Pos. ataque', 'Agilidade'],
        'LW': ['Aceleração', 'Pique', 'Dribles', 'Agilidade', 'Cruzamento', 'Finalização'],
        'RW': ['Aceleração', 'Pique', 'Dribles', 'Agilidade', 'Cruzamento', 'Finalização'],
        'LM': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Passe curto', 'Dribles'],
        'RM': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Passe curto', 'Dribles'],
        'CAM': ['Visão de jogo', 'Passe curto', 'Lançamento', 'Dribles', 'Controle bola', 'Compostura'],
        'CM': ['Passe curto', 'Lançamento', 'Visão de jogo', 'Fôlego', 'Reação', 'Combatividade'],
        'CDM': ['Intercept.', 'Hab. defensiva', 'Dividida pé', 'Combatividade', 'Fôlego', 'Força'],
        'CB': ['Hab. defensiva', 'Dividida pé', 'Prec. Cabeceio', 'Força', 'Combatividade', 'Intercept.'],
        'LB': ['Aceleração', 'Pique', 'Cruzamento', 'Hab. defensiva', 'Dividida pé', 'Fôlego'],
        'RB': ['Aceleração', 'Pique', 'Cruzamento', 'Hab. defensiva', 'Dividida pé', 'Fôlego'],
        'LWB': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Hab. defensiva', 'Dividida pé'],
        'RWB': ['Aceleração', 'Pique', 'Cruzamento', 'Fôlego', 'Hab. defensiva', 'Dividida pé'],
        'GK': ['Elasticidade GL', 'Manejo GL', 'Chute GL', 'Posicion. GL', 'Reflexos GL', 'Reação']
    }

    def suggest_stats():
        for k in all_stat_keys:
            st.session_state[k] = False
        pos = str(p.get('Position', 'CM')).upper()
        suggested_list = POSITION_SUGGESTIONS.get(pos, POSITION_SUGGESTIONS['CM'])
        for g_name, g_stats in STAT_GROUPS.items():
            for stat_label in g_stats.keys():
                if stat_label in suggested_list:
                    st.session_state[f"chk_{g_name}_{stat_label}"] = True

    c_title, c_btn1, c_btn2, c_btn3 = st.columns([2.2, 1.1, 1.1, 1.1])
    with c_title:
        st.markdown("### 2 · Indicadores de Performance")
    with c_btn1:
        st.button("✅ Marcar Todos", on_click=select_all_stats, use_container_width=True)
    with c_btn2:
        st.button("❌ Desmarcar", on_click=deselect_all_stats, use_container_width=True)
    with c_btn3:
        st.button("💡 Sugestão", on_click=suggest_stats, use_container_width=True)

    selected_stats_map = {}

    with st.expander("📌 Clique para expandir e selecionar as Estatísticas por Grupo", expanded=True):
        cols = st.columns(4)
        group_keys = list(STAT_GROUPS.keys())
        for idx, group_name in enumerate(group_keys):
            col_target = cols[idx % 4]
            with col_target:
                st.markdown(f"**{group_name}**")
                for stat_label, csv_col in STAT_GROUPS[group_name].items():
                    chk_key = f"chk_{group_name}_{stat_label}"
                    if chk_key not in st.session_state:
                        st.session_state[chk_key] = stat_label in ['Aceleração', 'Pique', 'Dribles', 'Curva']
                    checked = st.checkbox(stat_label, key=chk_key)
                    if checked:
                        selected_stats_map[stat_label] = csv_col

    col_comp_left, col_chart_right = st.columns([1, 2.5])

    with col_comp_left:
        st.markdown("#### ⚔️ Comparar Jogadores")
        st.caption("Adicione até 3 jogadores para comparar com o selecionado:")

        other_players = ["Nenhum"] + [name for name in player_list if name != target_player_name]
        comp1 = st.selectbox("🔵 Jogador Comparado 1:", options=other_players, index=0, key="comp_slot_1")
        options_p2 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1]] if comp1 != "Nenhum" else ["Nenhum"]
        comp2 = st.selectbox("🟢 Jogador Comparado 2:", options=options_p2, index=0, key="comp_slot_2", disabled=(comp1 == "Nenhum"))
        options_p3 = ["Nenhum"] + [name for name in player_list if name not in [target_player_name, comp1, comp2]] if comp2 != "Nenhum" else ["Nenhum"]
        comp3 = st.selectbox("🟡 Jogador Comparado 3:", options=options_p3, index=0, key="comp_slot_3", disabled=(comp2 == "Nenhum"))

    with col_chart_right:
        if selected_stats_map:
            radar_labels = list(selected_stats_map.keys())
            theta_labs = radar_labels + [radar_labels[0]]

            fig = go.Figure()
            radar_values = [get_val(p, csv_col) for csv_col in selected_stats_map.values()]
            r_vals = radar_values + [radar_values[0]]

            fig.add_trace(go.Scatterpolar(
                r=r_vals, theta=theta_labs, mode='lines+markers', fill='none',
                line=dict(color='#ef4444', width=3), marker=dict(size=8, color='#ef4444'),
                name=f"{p['Name']} (Principal)"
            ))

            slot_colors = {'comp_slot_1': '#3b82f6', 'comp_slot_2': '#10b981', 'comp_slot_3': '#f59e0b'}
            active_slots = [('comp_slot_1', comp1), ('comp_slot_2', comp2), ('comp_slot_3', comp3)]

            for slot_key, comp_name in active_slots:
                if comp_name != "Nenhum":
                    comp_row = df[df['Name'] == comp_name].iloc[0]
                    comp_radar_values = [get_val(comp_row, csv_col) for csv_col in selected_stats_map.values()]
                    comp_r_vals = comp_radar_values + [comp_radar_values[0]]
                    color = slot_colors[slot_key]

                    fig.add_trace(go.Scatterpolar(
                        r=comp_r_vals, theta=theta_labs, mode='lines+markers', fill='none',
                        line=dict(color=color, width=2.5, dash='solid'), marker=dict(size=7, color=color),
                        name=f"{comp_row['Name']} ({comp_row['OVR']})"
                    ))

            fig.update_layout(
                title=dict(text=f"Análise Comparativa Radar: {p['Name']} (OVR: {p['OVR']})", font=dict(color='#ffffff', size=16)),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='#cbd5e1'), gridcolor='#333333'),
                    angularaxis=dict(tickfont=dict(color='#ffffff', size=13), gridcolor='#333333')
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=480,
                margin=dict(l=30, r=30, t=50, b=40),
                legend=dict(font=dict(color='#ffffff'), orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Marque pelo menos uma estatística para exibir o gráfico.")

    st.markdown("---")

    st.markdown("### 📊 Estatísticas Detalhadas do Jogador")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### Ofensivo")
        for lbl, col in STAT_GROUPS['Ofensivo'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Mentalidade")
        for lbl, col in STAT_GROUPS['Mentalidade'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)

    with col2:
        st.markdown("#### Habilidade")
        for lbl, col in STAT_GROUPS['Habilidade'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Defesa")
        for lbl, col in STAT_GROUPS['Defesa'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)

    with col3:
        st.markdown("#### Movimentação")
        for lbl, col in STAT_GROUPS['Movimentação'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Atributos GL")
        for lbl, col in STAT_GROUPS['Atributos GL'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col, 10)), unsafe_allow_html=True)

    with col4:
        st.markdown("#### Força")
        for lbl, col in STAT_GROUPS['Força'].items():
            st.markdown(render_stat_item(lbl, get_val(p, col)), unsafe_allow_html=True)
        st.markdown("#### Estilos de Jogo")
        if play_styles:
            for style in play_styles:
                st.markdown(f"- **<span class='var-text'>{style}</span>**", unsafe_allow_html=True)
        else:
            st.markdown("- *<span class='var-text'>Nenhum estilo de jogo específico</span>*", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. PÁGINA 2: FORMAÇÕES E ANÁLISE TÁTICA (ATUALIZADA)
# -----------------------------------------------------------------------------
elif page_selection == "Formações":
    st.title("📋 Guia de Formações & Tactical Presets (FC26)")
    st.markdown("Analise a disposição tática em campo, os estilos de construção de jogada e as estratégias completas.")
    
    # Declarar o HTML diretamente aqui evita erros de importação entre arquivos
    painel_html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <style>
        body { background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; display: flex; justify-content: center; margin: 0; padding: 10px; }
        .painel-container { display: flex; gap: 20px; background: #1e1e1e; padding: 20px; border-radius: 8px; max-width: 950px; width: 100%; }
        .campo-futebol { width: 100%; max-width: 450px; aspect-ratio: 105 / 68; background-color: #1b4d3e; position: relative; border: 2px solid white; border-radius: 4px; overflow: hidden; flex-shrink: 0; }
        .linha-meio { position: absolute; top: 0; bottom: 0; left: 50%; border-left: 2px dashed rgba(255, 255, 255, 0.7); }
        .circulo-central { position: absolute; top: 50%; left: 50%; width: 20%; aspect-ratio: 1/1; border: 2px solid rgba(255, 255, 255, 0.7); border-radius: 50%; transform: translate(-50%, -50%); }
        .grande-area-esq, .grande-area-dir { position: absolute; top: 20%; bottom: 20%; width: 15%; border: 2px solid rgba(255, 255, 255, 0.7); }
        .grande-area-esq { left: 0; border-left: none; }
        .grande-area-dir { right: 0; border-right: none; }
        .jogador { position: absolute; transform: translate(-50%, -50%); width: 26px; height: 26px; background-color: #ffffff; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 9px; transition: all 0.3s ease-in-out; }
        .informacoes { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .seletor-duplo { display: flex; gap: 10px; }
        .seletor-grupo { flex: 1; background: #2a2a2a; padding: 10px; border-radius: 6px; }
        .seletor-grupo label { display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold; }
        .seletor-grupo select { width: 100%; padding: 6px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; font-size: 12px; }
        .card-info { background: #2a2a2a; padding: 10px 12px; border-radius: 6px; border-left: 4px solid #3b82f6; }
        .card-info h3 { margin: 0 0 4px 0; font-size: 12px; text-transform: uppercase; }
        .card-info p { margin: 0; font-size: 12px; color: #ccc; line-height: 1.3; }
      </style>
    </head>
    <body>
      <div class="painel-container">
        <div class="campo-futebol" id="campo">
          <div class="linha-meio"></div>
          <div class="circulo-central"></div>
          <div class="grande-area-esq"></div>
          <div class="grande-area-dir"></div>
        </div>
        <div class="informacoes">
          <div class="seletor-duplo">
            <div class="seletor-grupo">
              <label for="formacao-select">Formação:</label>
              <select id="formacao-select" onchange="atualizarPainel()">
                <option value="433-holding">4-3-3 Holding</option>
                <option value="442">4-4-2 Tradicional</option>
                <option value="352">3-5-2</option>
              </select>
            </div>
            <div class="seletor-grupo">
              <label for="preset-select">Tactical Preset:</label>
              <select id="preset-select" onchange="atualizarPainel()">
                <option value="padrao">Padrão (Standard)</option>
                <option value="pontas">Jogo pelas Pontas</option>
                <option value="tikitaka">Tiki-Taka / Posse</option>
                <option value="contra-ataque">Contra-Ataque</option>
                <option value="gegenpress">Gegenpressing</option>
                <option value="kick-rush">Chuta e Corre</option>
                <option value="park-bus">Estacionar o Ônibus</option>
              </select>
            </div>
          </div>
          <div class="card-info" style="border-left-color: #3b82f6;"><h3>Explicação Breve</h3><p id="info-descricao">-</p></div>
          <div class="card-info" style="border-left-color: #10b981;"><h3>Vantagens (Prós)</h3><p id="info-pros">-</p></div>
          <div class="card-info" style="border-left-color: #ef4444;"><h3>Desvantagens (Contras)</h3><p id="info-contras">-</p></div>
          <div class="card-info" style="border-left-color: #f59e0b;"><h3>Estratégia de Combate</h3><p id="info-combate">-</p></div>
        </div>
      </div>
      <script>
        const posicoes = {
          "433-holding": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"VOL",t:50,l:38},{p:"MC",t:30,l:55},{p:"MC",t:70,l:55},{p:"PE",t:15,l:78},{p:"CA",t:50,l:82},{p:"PD",t:85,l:78}],
          "442": [{p:"GOL",t:50,l:6},{p:"LD",t:15,l:25},{p:"ZAG",t:38,l:20},{p:"ZAG",t:62,l:20},{p:"LE",t:85,l:25},{p:"MD",t:15,l:50},{p:"MC",t:38,l:45},{p:"MC",t:62,l:45},{p:"ME",t:85,l:50},{p:"ATA",t:38,l:78},{p:"ATA",t:62,l:78}],
          "352": [{p:"GOL",t:50,l:6},{p:"ZAG",t:25,l:20},{p:"ZAG",t:50,l:18},{p:"ZAG",t:75,l:20},{p:"ALA",t:10,l:50},{p:"VOL",t:38,l:40},{p:"MC",t:50,l:55},{p:"VOL",t:62,l:40},{p:"ALA",t:90,l:50},{p:"ATA",t:35,l:80},{p:"ATA",t:65,l:80}]
        };
        const matriz = {
          "433-holding": {
            "padrao": {d:"Estrutura equilibrada com o volante assegurando a proteção defensiva.",p:"Ocupação homogênea de espaço.",c:"Pode faltar agressividade contra blocos baixos.",b:"Pressionar o volante distribuidor."},
            "pontas": {d:"Pontas abertos buscando o fundo com apoio de laterais.",p:"Isolamento 1v1 nos corredores.",c:"Espaço vago nas costas dos laterais.",b:"Dobrar a marcação nos pontas."},
            "tikitaka": {d:"Triangulações curtas e paciência para infiltração.",p:"Controle absoluto da posse.",c:"Risco de perda na saída de bola.",b:"Bloqueio médio-baixo compacto."},
            "contra-ataque": {d:"Bloco recuado com passe rápido em profundidade.",p:"Letal em espaço aberto.",c:"Isolamento do centroavante.",b:"Manter contra-pressão imediata."},
            "gegenpress": {d:"Pressão sufocante no campo de ataque.",p:"Recuperação perto do gol rival.",c:"Desgaste físico alto e linha defensiva exposta.",b:"Usar ligações diretas."},
            "kick-rush": {d:"Bolas longas buscando o CA ou disputa de pontas.",p:"Bypassa a pressão adversária.",c:"Baixo aproveitamento de posse.",b:"Soberania nos duelos aéreos."},
            "park-bus": {d:"Linha de 4 e volante cimentados na área.",p:"Dificuldade nula de ceder gols por dentro.",c:"Incapacidade de sair ao ataque.",b:"Chutes de média e longa distância."}
          },
          "442": {
            "padrao": {d:"Duas linhas de quatro com dupla de ataque.",p:"Fácil entendimento e solidez.",c:"Inferioridade contra trios de meio.",b:"Explorar entrelinhas no meio-campo."},
            "pontas": {d:"Dobradinhas laterais para cruzamento.",p:"Aproveitamento da dupla de área.",c:"Corredor central exposto.",b:"Atacar por dentro no mano a mano."},
            "tikitaka": {d:"Passes curtos entre linhas de meio e ataque.",p:"Apoio constante entre setores.",c:"Falta de amplitude sem pontas natos.",b:"Afunilar a marcação no centro."},
            "contra-ataque": {d:"Duas linhas baixas e saída vertical rápida.",p:"Muralha defensiva eficiente.",c:"Alto desgaste dos meias abertos.",b:"Balanço defensivo constante."},
            "gegenpress": {d:"Ataque e meias abafam a saída rival.",p:"Força erros na área adversária.",c:"Espaço entre a defesa e meio.",b:"Giro rápido com inversão de jogo."},
            "kick-rush": {d:"Lançamentos diretos para a dupla de frente.",p:"Ganha segundas bolas no ataque.",c:"Pouca criação pelo chão.",b:"Recolher sobras com os volantes."},
            "park-bus": {d:"Linhas ultra compactas perto do gol.",p:"Fechamento total dos corredores.",c:"Presença nula no ataque.",b:"Circulação rápida para descompactar."}
          },
          "352": {
            "padrao": {d:"Três zagueiros e alas cobrindo os lados.",p:"Superioridade numérica no meio.",c:"Costas dos alas vulneráveis.",b:"Atacar os espaços dos alas."},
            "pontas": {d:"Alas atuam avançados como pontas.",p:"Amplitude máxima e cruzamentos.",c:"Sobrecarga física nos alas.",b:"Explorar zagueiros de lado no 1v1."},
            "tikitaka": {d:"Saída com 3 defensores e meio povoado.",p:"Fácil saída sob pressão.",c:"Lentidão se a bola não chegar à frente.",b:"Pressionar com 3 atacantes."},
            "contra-ataque": {d:"Linha de 5 sem a bola e transição direta.",p:"Inviolável pelo centro.",c:"Distância grande para os atacantes.",b:"Chutes de fora da área."},
            "gegenpress": {d:"Pressão com 5 meio-campistas no alto.",p:"Domínio físico no meio.",c:"Um passe certo quebra a linha toda.",b:"Passes verticais longos."},
            "kick-rush": {d:"Zagueiros lançam para a dupla de ataque.",p:"Simplicidade e presença física.",c:"Descarte da criação dos volantes.",b:"Dominar a primeira bola aérea."},
            "park-bus": {d:"Linha de 5 zagueiros + 3 volantes recuados.",p:"Bloqueio total na grande área.",c:"Falta de saída de bola.",b:"Movimentação intensa sem bola."}
          }
        };

        function atualizarPainel() {
          const f = document.getElementById("formacao-select").value;
          const p = document.getElementById("preset-select").value;
          const campo = document.getElementById("campo");
          campo.querySelectorAll(".jogador").forEach(j => j.remove());
          
          posicoes[f].forEach(j => {
            const div = document.createElement("div");
            div.className = "jogador";
            div.style.top = j.t + "%";
            div.style.left = j.l + "%";
            div.innerText = j.p;
            campo.appendChild(div);
          });

          const d = matriz[f][p];
          document.getElementById("info-descricao").innerText = d.d;
          document.getElementById("info-pros").innerText = d.p;
          document.getElementById("info-contras").innerText = d.c;
          document.getElementById("info-combate").innerText = d.b;
        }
        window.onload = atualizarPainel;
      </script>
    </body>
    </html>
    """
    
    components.html(painel_html, height=520, scrolling=True)
