# -----------------------------------------------------------------------------
# 3. BARRA LATERAL E NAVEGAÇÃO MODERNA (st.navigation)
# -----------------------------------------------------------------------------
st.sidebar.image("https://sofifa.com/static/common/logo.svg", width=180)
st.sidebar.title("⚽ Dashboard FC26")
st.sidebar.markdown("---")

df = df_raw.copy()

def wrapper_perfil():
    renderizar_perfil(df, find_similar_players, STAT_GROUPS, get_val)

pagina_perfil = st.Page(wrapper_perfil, title="Perfil Detalhado", icon="👤", default=True)
pagina_formacoes = st.Page(renderizar_painel_tatico, title="Formações", icon="📋")
pagina_playstyles = st.Page(renderizar_playstyles, title="PlayStyles", icon="⚡")
pagina_stats = st.Page(renderizar_explicando_stats, title="Explicando stats", icon="📊")

# Removida a pagina_busca da lista de navegação
pg = st.navigation([pagina_perfil, pagina_formacoes, pagina_playstyles, pagina_stats])
pg.run()
