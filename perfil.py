# Arquivo: perfil.py
import streamlit as st
import pandas as pd
import ast
import numpy as np

def renderizar_perfil(df, find_similar_players):
    st.title("👤 Perfil Detalhado")

    col_quem, _ = st.columns([1, 2])
    player_list = sorted(df['Name'].unique().tolist())
    default_index = player_list.index("Bradley Barcola") if "Bradley Barcola" in player_list else 0

    with col_quem:
        target_player_name = st.selectbox("Buscar Jogador:", options=player_list, index=default_index)

    p = df[df['Name'] == target_player_name].iloc[0]
    
    perna_boa = "Esq." if p.get('Preferred foot', 'Right') == 'Left' else "Dir."
    fintas = p.get('Skill moves', 2)
    perna_ruim = p.get('Weak foot', 2)
    rep_int = p.get('Rank', 1)

    c_face, c_info, c_details = st.columns([1.2, 2.5, 3.3])

    with c_face:
        card_img = p.get('card', '')
        if pd.notna(card_img) and str(card_img).startswith("http"):
            st.image(card_img, width=140)
        else:
            st.image("https://cdn.sofifa.net/player_0.png", width=130)

    with c_info:
        st.markdown(f"<h2>🏃 <span class='var-text'>{p['Name']}</span></h2>", unsafe_allow_html=True)
        st.markdown(f"**Clube:** <span class='var-text'>{p['Team']}</span> ({p['League']})", unsafe_allow_html=True)
        st.markdown(f"**Posição:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['Position']}</span> | **Nacionalidade:** <span class='var-text'>{p.get('Nation', 'N/A')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Overall:** <span style='background-color: #1a2234; color: #00ffcc; padding: 2px 8px; border-radius: 4px; font-weight: bold;'>{p['OVR']}</span> | **Idade:** <span class='var-text'>{p['Age']} anos</span>", unsafe_allow_html=True)

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
                        <span style="color:#94a3b8; font-size:0.75rem;">Estilo: <span class="var-text">{styles_txt}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum jogador semelhante encontrado com esses critérios.")
