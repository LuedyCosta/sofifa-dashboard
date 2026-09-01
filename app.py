# Arquivo: app.py
import streamlit as st
import pandas as pd

# 1. Configuração inicial da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Dashboard Sofifa / FC",
    page_icon="⚽",
    layout="wide"
)

# 2. Injeção de Estilos CSS Globais (Tema escuro e classes padrão)
st.markdown("""
<style>
    .var-text {
        color: #00ffcc !important;
        font-weight: bold;
    }
    .similar-card {
        background-color: #131b2e;
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .similar-name {
        font-size: 1.1rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .similar-meta {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    .stat-box {
        background-color: #1a2234;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .stat-badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .stat-green { background-color: #10b981; color: #000; }
    .stat-yellow { background-color: #f59e0b; color: #000; }
    .stat-red { background-color: #ef4444; color: #fff; }
</style>
""", unsafe_allow_html=True)

# 3. Função para carregar os dados (com cache para otimizar a performance)
@st.cache_data
def carregar_dados():
    # Substitua pelo nome correto do seu arquivo CSV ou base de dados
    try:
        df = pd.read_csv('dados_jogadores.csv')
    except:
        # Fallforming caso o arquivo principal tenha outro nome ou caminho
        try:
            df = pd.read_csv('players.csv')
        except:
            # DataFrame de exemplo caso não encontre nenhum arquivo físico no ambiente imediato
            df = pd.DataFrame({
                'id': [1, 2],
                'Name': ['Bradley Barcola', 'Kylian Mbappé'],
                'OVR': [82, 91],
                'Position': ['LW', 'ST'],
                'Age': [21, 25],
                'Team': ['Paris SG', 'Real Madrid'],
                'League': ['Ligue 1', 'La Liga'],
                'PAC': [90, 97], 'SHO': [77, 90], 'PAS': [78, 80],
                'DRI': [84, 92], 'DEF': [39, 36], 'PHY': [66, 78]
            })
    return df

# Carrega o DataFrame principal
df = carregar_dados()

# SALVA O DATAFRAME NO SESSION_STATE PARA ACESSO GLOBAL NAS PÁGINAS
st.session_state['df'] = df

# 4. Configuração das páginas do app usando st.navigation
# Certifique-se de que os arquivos 'busca_jogadores.py' e 'perfil.py' estão na mesma pasta
paginas = [
    st.Page("busca_jogadores.py", title="Busca de Jogadores", icon="🔍"),
    st.Page("perfil.py", title="Perfil do Jogador", icon="👤")
]

pg = st.navigation(paginas)

# 5. Executa a navegação de forma segura
pg.run()
