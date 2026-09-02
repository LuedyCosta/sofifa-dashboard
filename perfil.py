import streamlit as st
import pandas as pd
import ast
import plotly.graph_objects as go

def renderizar_perfil(df, find_similar_players, STAT_GROUPS, get_val):
    st.title("👤 Perfil Detalhado")

    player_list = sorted(df['Name'].unique().tolist())
    default_index = player_list.index("Bradley Barcola") if "Bradley Barcola" in player_list else 0

    target_player_name = st.selectbox("Buscar Jogador:", options=player_list, index=default_index)

    p = df[df['Name'] == target_player_name].iloc[0]
    
    play_styles_raw = str(p.get('play style', '[]'))
    try:
        play_styles = ast.literal_eval(play_styles_raw)
        if not isinstance(play_styles, list): play_styles = []
    except:
        play_styles = []

    perna_boa = "Esq." if p.get('Preferred foot', 'Right') == 'Left' else "Dir."
    fintas = p.get('Skill moves', 2)
    perna_ruim = p.get('Weak foot', 2)
    rep_int = p.get('Rank', 1)

    c_face, c_info = st.columns([1, 2.5])

    with c_face:
        card_img = p.get('card', '')
        if pd.notna(card_img) and str(card_img).startswith("http"):
            st.image(card_img, width=130)
        else:
            st.image("https://cdn.sofifa.net/player_0.png", width=120)

    with c_info:
        st.markdown(f"<h2>🏃 <span class='var-text'>{p['Name']}</span></h2>", unsafe_allow_html=True)
        st.markdown(f"**Clube:** <span class='var-text'>{p['Team']}</span> ({p['League']})", unsafe_allow_html=True)
        st.markdown(f"**Posição:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['Position']}</span> | **Nacionalidade:** <span class='var-text'>{p.get('Nation', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['OVR']}</span> | **Idade:** <span class='var-text'>{p['Age']} anos</span>", unsafe_allow_html=True)

    with st.container(border=True):
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            st.markdown(f"""
            <strong style="color:#ffffff;">Perfil</strong><br>
            <span>Perna boa: <b class="var-text">{perna_boa}</b></span><br>
            <span><b class="var-text">{fintas} ★</b> Fintas</span><br>
            <span><b class="var-text">{perna_ruim} ★</b> Perna ruim</span><br>
            <span>Rank: <b class="var-text">#{rep_int}</b></span>
            """, unsafe_allow_html=True)
        with b_col2:
            st.markdown(f"""
            <strong style="color:#ffffff;">Atributos Globais</strong><br>
            <span>PAC: <b class="var-text">{p.get('PAC', 0)}</b></span> | 
            <span>SHO: <b class="var-text">{p.get('SHO', 0)}</b></span><br>
            <span>PAS: <b class="var-text">{p.get('PAS', 0)}</b></span> | 
            <span>DRI: <b class="var-text">{p.get('DRI', 0)}</b></span><br>
            <span>DEF: <b class="var-text">{p.get('DEF', 0)}</b></span> | 
            <span>PHY: <b class="var-text">{p.get('PHY', 0)}</b></span>
            """, unsafe_allow_html=True)
        with b_col3:
            st.markdown(f"""
            <strong style="color:#ffffff;">Clube</strong><br>
            <span><b class="var-text">{p['Team']}</b></span><br>
            <span>Posição: <b class="var-text">{p['Position']}</b></span>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Detalhamento Completo por Categoria")
    tab_names = list(STAT_GROUPS.keys()) if STAT_GROUPS else ['Playstyles']
    tabs = st.tabs(tab_names)
    
    for tab_idx, tab_name in enumerate(tab_names):
        with tabs[tab_idx]:
            if tab_name == 'Playstyles':
                if not play_styles:
                    st.info("Não tem")
                else:
                    descriptions = {
                        "Power Shot": "Disparos com força significativamente maior e velocidade extrema de chute.",
                        "Technical": "Habilidade para realizar curvas e precisão em passes/chutes rasteiros.",
                        "Speed Dribbler": "Capacidade de correr em velocidade máxima mantendo a bola muito próxima.",
                        "Trickster": "Acesso a animações especiais e fintas mais rápidas e eficientes.",
                        "Rapid": "Aceleração e velocidade explosiva ao conduzir a bola.",
                        "Finesse Shot": "Chutes colocados com curva acentuada e alta precisão.",
                        "Trivela": "Passes e finalizações utilizando a parte externa do pé com maestria.",
                        "Chip Shot": "Finalizações por cobertura com maior precisão e altura adequada."
                    }
                    
                    ps_cols = st.columns(2)
                    for i, ps in enumerate(play_styles):
                        desc = descriptions.get(ps, "Melhora o desempenho do atleta em situações específicas de jogo correspondentes a esta habilidade.")
                        with ps_cols[i % 2]:
                            st.markdown(f"""
                            <div class="similar-card" style="margin-bottom: 12px;">
                                <div class="similar-name">⚡ {ps}</div>
                                <div class="similar-meta" style="color: #94a3b8 !important;">{desc}</div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                group_dict = STAT_GROUPS.get(tab_name, {})
                sub_cols = st.columns(2)
                items = list(group_dict.items())
                half = (len(items) + 1) // 2
                
                def render_stat_item(label, value):
                    val_int = int(value) if str(value).isdigit() else 50
                    badge_class = "stat-green" if val_int >= 70 else ("stat-yellow" if val_int >= 60 else "stat-red")
                    return f"""
                    <div class="stat-box">
                        <span class="stat-badge {badge_class}">{val_int}</span>
                        <span class="stat-label">{label}</span>
                    </div>
                    """

                with sub_cols[0]:
                    for label, col_csv in items[:half]:
                        val = get_val(p, col_csv, 50)
                        st.markdown(render_stat_item(label, val), unsafe_allow_html=True)
                with sub_cols[1]:
                    for label, col_csv in items[half:]:
                        val = get_val(p, col_csv, 50)
                        st.markdown(render_stat_item(label, val), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 2 · Indicadores de Performance")

    all_attributes = {}
    for group_name, attrs in STAT_GROUPS.items():
        if group_name == 'Playstyles':
            continue
        for label_pt, col_en in attrs.items():
            all_attributes[f"{group_name} - {label_pt}"] = col_en

    if "selected_indicators" not in st.session_state:
        st.session_state["selected_indicators"] = [
            "Ofensivo - Finalização", 
            "Habilidade - Dribles", 
            "Movimentação - Agilidade", 
            "Força - Fôlego"
        ]

    position_suggestions = {
        'GOL': ["Goleiro - Reflexos GL", "Goleiro - Manejo GL", "Goleiro - Posicion. GL", "Goleiro - Elasticidade GL", "Goleiro - Chute GL"],
        'GK': ["Goleiro - Reflexos GL", "Goleiro - Manejo GL", "Goleiro - Posicion. GL", "Goleiro - Elasticidade GL", "Goleiro - Chute GL"],
        
        'ZAG': ["Defesa - Dividida pé", "Defesa - Intercept.", "Ofensivo - Prec. Cabeceio", "Força - Força", "Força - Impulsão"],
        'CB': ["Defesa - Dividida pé", "Defesa - Intercept.", "Ofensivo - Prec. Cabeceio", "Força - Força", "Força - Impulsão"],
        
        'LD': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        'RB': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        
        'LE': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        'LB': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        
        'ALA': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        'RWB': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        'LWB': ["Força - Fôlego", "Movimentação - Aceleração", "Ofensivo - Cruzamento", "Defesa - Dividida pé", "Movimentação - Agilidade"],
        
        'VOL': ["Força - Fôlego", "Defesa - Intercept.", "Força - Força", "Defesa - Dividida pé", "Habilidade - Passe curto"],
        'CDM': ["Força - Fôlego", "Defesa - Intercept.", "Força - Força", "Defesa - Dividida pé", "Habilidade - Passe curto"],
        
        'MC': ["Mentalidade - Visão de jogo", "Habilidade - Passe curto", "Habilidade - Controle bola", "Movimentação - Agilidade", "Habilidade - Chutes longe"],
        'CM': ["Mentalidade - Visão de jogo", "Habilidade - Passe curto", "Habilidade - Controle bola", "Movimentação - Agilidade", "Habilidade - Chutes longe"],
        
        'MEI': ["Mentalidade - Visão de jogo", "Habilidade - Passe curto", "Habilidade - Controle bola", "Movimentação - Agilidade", "Habilidade - Chutes longe"],
        'CAM': ["Mentalidade - Visão de jogo", "Habilidade - Passe curto", "Habilidade - Controle bola", "Movimentação - Agilidade", "Habilidade - Chutes longe"],
        
        'PE': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        'LM': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        'LW': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        
        'PD': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        'RM': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        'RW': ["Movimentação - Aceleração", "Movimentação - Pique", "Habilidade - Dribles", "Ofensivo - Cruzamento", "Habilidade - Curva"],
        
        'ATA': ["Ofensivo - Finalização", "Mentalidade - Pos. ataque", "Força - Força chute", "Mentalidade - Compostura", "Força - Força"],
        'CA': ["Ofensivo - Finalização", "Mentalidade - Pos. ataque", "Força - Força chute", "Mentalidade - Compostura", "Força - Força"],
        'ST': ["Ofensivo - Finalização", "Mentalidade - Pos. ataque", "Força - Força chute", "Mentalidade - Compostura", "Força - Força"],
        'CF': ["Ofensivo - Finalização", "Mentalidade - Pos. ataque", "Força - Força chute", "Mentalidade - Compostura", "Força - Força"]
    }

    c_b1, c_b2, c_b3 = st.columns(3)
    
    with c_b1:
        if st.button("✅ Marcar", use_container_width=True, key="btn_marcar_todos"):
            st.session_state["selected_indicators"] = list(all_attributes.keys())
            for k in all_attributes.keys():
                st.session_state[f"chk_{k}"] = True
            st.rerun()
            
    with c_b2:
        if st.button("❌ Limpar", use_container_width=True, key="btn_limpar_todos"):
            st.session_state["selected_indicators"] = []
            for k in all_attributes.keys():
                st.session_state[f"chk_{k}"] = False
            st.rerun()
            
    with c_b3:
        if st.button("💡 Sugestão", use_container_width=True, key="btn_sugestao_pos"):
            pos_atual = str(p.get('Position', 'MC')).strip().upper()
            sugestoes_desejadas = position_suggestions.get(pos_atual, [
                "Ofensivo - Finalização", 
                "Habilidade - Dribles", 
                "Movimentação - Aceleração", 
                "Força - Força chute",
                "Mentalidade - Visão de jogo"
            ])
            
            validas = [s for s in sugestoes_desejadas if s in all_attributes]
            if not validas:
                validas = list(all_attributes.keys())[:5]
            
            st.session_state["selected_indicators"] = validas
            
            for key_name in all_attributes.keys():
                st.session_state[f"chk_{key_name}"] = (key_name in validas)
                
            st.rerun()

    for key_name in all_attributes.keys():
        if f"chk_{key_name}" not in st.session_state:
            st.session_state[f"chk_{key_name}"] = key_name in st.session_state["selected_indicators"]

    with st.expander("📌 Clique para expandir e selecionar as Estatísticas por Grupo", expanded=False):
        selected_stats = []
        for group_name, attrs in STAT_GROUPS.items():
            if group_name == 'Playstyles':
                continue
            st.markdown(f"**{group_name}**")
            cols_check = st.columns(2)
            idx_chk = 0
            for label_pt, col_en in attrs.items():
                key_name = f"{group_name} - {label_pt}"
                
                with cols_check[idx_chk % 2]:
                    is_on = st.checkbox(label_pt, key=f"chk_{key_name}")
                    if is_on and key_name not in selected_stats:
                        selected_stats.append(key_name)
                    elif not is_on and key_name in selected_stats:
                        selected_stats.remove(key_name)
                idx_chk += 1
        
        st.session_state["selected_indicators"] = selected_stats

    st.markdown("---")

    st.markdown("### ⚖️ Comparação com Outros Jogadores")
    
    # Legendas visuais atualizadas com as cores solicitadas
    st.markdown("""
    <div style="display: flex; gap: 20px; margin-bottom: 10px; font-weight: bold;">
        <span style="color: #ef4444;">🔴 Jogador 1</span>
        <span style="color: #a855f7;">🟣 Jogador 2</span>
        <span style="color: #eab308;">🟡 Jogador 3</span>
    </div>
    """, unsafe_allow_html=True)

    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    with col_comp1:
        comp1_name = st.selectbox("Jogador 1", options=["Nenhum"] + player_list, index=0, key="comp1")
    with col_comp2:
        comp2_name = st.selectbox("Jogador 2", options=["Nenhum"] + player_list, index=0, key="comp2")
    with col_comp3:
        comp3_name = st.selectbox("Jogador 3", options=["Nenhum"] + player_list, index=0, key="comp3")

    st.markdown("---")
    st.markdown(f"### Análise Comparativa Radar: <span class='var-text'>{p['Name']}</span>", unsafe_allow_html=True)

    selected_keys = st.session_state.get("selected_indicators", [])
    if not selected_keys:
        st.warning("Selecione pelo menos um indicador de performance acima para exibir o gráfico de radar.")
    else:
        categories = [k.split(" - ")[1] for k in selected_keys]
        col_names = [all_attributes[k] for k in selected_keys if k in all_attributes]

        fig = go.Figure()

        # Jogador 1 -> Vermelho (#ef4444)
        if comp1_name != "Nenhum":
            p1 = df[df['Name'] == comp1_name].iloc[0]
            vals_p1 = [get_val(p1, col_en, 50) for col_en in col_names]
            if vals_p1:
                vals_p1.append(vals_p1[0])
                fig.add_trace(go.Scatterpolar(
                    r=vals_p1,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=p1['Name'],
                    fillcolor='rgba(239, 68, 68, 0.15)',
                    line=dict(color='#ef4444', width=2)
                ))

        # Jogador 2 -> Roxo (#a855f7)
        if comp2_name != "Nenhum":
            p2 = df[df['Name'] == comp2_name].iloc[0]
            vals_p2 = [get_val(p2, col_en, 50) for col_en in col_names]
            if vals_p2:
                vals_p2.append(vals_p2[0])
                fig.add_trace(go.Scatterpolar(
                    r=vals_p2,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=p2['Name'],
                    fillcolor='rgba(168, 85, 247, 0.15)',
                    line=dict(color='#a855f7', width=2)
                ))

        # Jogador 3 -> Amarelo (#eab308)
        if comp3_name != "Nenhum":
            p3 = df[df['Name'] == comp3_name].iloc[0]
            vals_p3 = [get_val(p3, col_en, 50) for col_en in col_names]
            if vals_p3:
                vals_p3.append(vals_p3[0])
                fig.add_trace(go.Scatterpolar(
                    r=vals_p3,
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=p3['Name'],
                    fillcolor='rgba(234, 179, 8, 0.15)',
                    line=dict(color='#eab308', width=2)
                ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8'),
                angularaxis=dict(color='#ffffff')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40),
            height=450,
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col_sim_title, col_btn_todos, col_btn_regen = st.columns([1.5, 0.7, 0.7])
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
                        <span style="color:#94a3b8; font-size:0.75rem;">Estilo: <span class="var-text">{styles_txt}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum jogador semelhante encontrado com esses critérios.")
